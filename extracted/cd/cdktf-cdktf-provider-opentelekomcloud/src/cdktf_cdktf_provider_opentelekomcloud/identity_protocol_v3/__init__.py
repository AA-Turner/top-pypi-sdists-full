r'''
# `opentelekomcloud_identity_protocol_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_identity_protocol_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3).
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


class IdentityProtocolV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtocolV3.IdentityProtocolV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3 opentelekomcloud_identity_protocol_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        mapping_id: builtins.str,
        protocol: builtins.str,
        provider_id: builtins.str,
        access_config: typing.Optional[typing.Union["IdentityProtocolV3AccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["IdentityProtocolV3Metadata", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3 opentelekomcloud_identity_protocol_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mapping_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#mapping_id IdentityProtocolV3#mapping_id}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#protocol IdentityProtocolV3#protocol}.
        :param provider_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#provider_id IdentityProtocolV3#provider_id}.
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#access_config IdentityProtocolV3#access_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#id IdentityProtocolV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#metadata IdentityProtocolV3#metadata}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64bb8be3f8726e41f4947d9ab43cc61a3791635fc7307dff8d3521823a6e3796)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityProtocolV3Config(
            mapping_id=mapping_id,
            protocol=protocol,
            provider_id=provider_id,
            access_config=access_config,
            id=id,
            metadata=metadata,
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
        '''Generates CDKTF code for importing a IdentityProtocolV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityProtocolV3 to import.
        :param import_from_id: The id of the existing IdentityProtocolV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityProtocolV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ff8e252e686d53925c7d2c9cf015df346c95f870458651bb659b7d77538e50)
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
        :param access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#access_type IdentityProtocolV3#access_type}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#client_id IdentityProtocolV3#client_id}.
        :param provider_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#provider_url IdentityProtocolV3#provider_url}.
        :param signing_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#signing_key IdentityProtocolV3#signing_key}.
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#authorization_endpoint IdentityProtocolV3#authorization_endpoint}.
        :param response_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#response_mode IdentityProtocolV3#response_mode}.
        :param response_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#response_type IdentityProtocolV3#response_type}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#scopes IdentityProtocolV3#scopes}.
        '''
        value = IdentityProtocolV3AccessConfig(
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

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        domain_id: builtins.str,
        metadata: builtins.str,
        xaccount_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#domain_id IdentityProtocolV3#domain_id}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#metadata IdentityProtocolV3#metadata}.
        :param xaccount_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#xaccount_type IdentityProtocolV3#xaccount_type}.
        '''
        value = IdentityProtocolV3Metadata(
            domain_id=domain_id, metadata=metadata, xaccount_type=xaccount_type
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

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
    def access_config(self) -> "IdentityProtocolV3AccessConfigOutputReference":
        return typing.cast("IdentityProtocolV3AccessConfigOutputReference", jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "IdentityProtocolV3MetadataOutputReference":
        return typing.cast("IdentityProtocolV3MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(self) -> typing.Optional["IdentityProtocolV3AccessConfig"]:
        return typing.cast(typing.Optional["IdentityProtocolV3AccessConfig"], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingIdInput")
    def mapping_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["IdentityProtocolV3Metadata"]:
        return typing.cast(typing.Optional["IdentityProtocolV3Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb4e987d2990f18fc1ecf0e7c07bc7f2b1593e5db8cbc90ef23a21b9c5bc5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mappingId")
    def mapping_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappingId"))

    @mapping_id.setter
    def mapping_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8364ed1155d542c26adabe07227fef5f4a30874a4fdd0a263bb37aa2d408fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffd3c27f9692ac1882efa38ffdab484942acef3353f247c0b8de5a85bf78d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4a96280f3796cf3611f379a0569de40788edacecc604b1d81aa69e74e985aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtocolV3.IdentityProtocolV3AccessConfig",
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
class IdentityProtocolV3AccessConfig:
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
        :param access_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#access_type IdentityProtocolV3#access_type}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#client_id IdentityProtocolV3#client_id}.
        :param provider_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#provider_url IdentityProtocolV3#provider_url}.
        :param signing_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#signing_key IdentityProtocolV3#signing_key}.
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#authorization_endpoint IdentityProtocolV3#authorization_endpoint}.
        :param response_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#response_mode IdentityProtocolV3#response_mode}.
        :param response_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#response_type IdentityProtocolV3#response_type}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#scopes IdentityProtocolV3#scopes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c060c2aee236b4c8555735a23b3ddcc8d6bf7c16216e64b83287311e73e1164b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#access_type IdentityProtocolV3#access_type}.'''
        result = self._values.get("access_type")
        assert result is not None, "Required property 'access_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#client_id IdentityProtocolV3#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#provider_url IdentityProtocolV3#provider_url}.'''
        result = self._values.get("provider_url")
        assert result is not None, "Required property 'provider_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#signing_key IdentityProtocolV3#signing_key}.'''
        result = self._values.get("signing_key")
        assert result is not None, "Required property 'signing_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#authorization_endpoint IdentityProtocolV3#authorization_endpoint}.'''
        result = self._values.get("authorization_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#response_mode IdentityProtocolV3#response_mode}.'''
        result = self._values.get("response_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#response_type IdentityProtocolV3#response_type}.'''
        result = self._values.get("response_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#scopes IdentityProtocolV3#scopes}.'''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProtocolV3AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProtocolV3AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtocolV3.IdentityProtocolV3AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffe3e5df8dea5533d9ef0118c4078102c076106b9167e38a3a29c15cf385ec1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e18a9ab68be4dc5243a225f48674714ecb5132dc77c6ca072d07225e6c1a188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpoint")
    def authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationEndpoint"))

    @authorization_endpoint.setter
    def authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15bf4c7012a7342f6da6bf15f3ebb0ca86250c044b98992e82ba1bb2cc1c1923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed29044b2277f9353a5b716e09821a0dbab6d5b11a779c156cbb442bcfa450ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerUrl")
    def provider_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerUrl"))

    @provider_url.setter
    def provider_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3cb74793cc4df6b072e54ce7dc6c09052fb8477922b52ec201dc60e24c6a467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseMode")
    def response_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseMode"))

    @response_mode.setter
    def response_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2400777cde9f76ea29cb39c4a5153226c3e8ac70364cb3f4394f4bdf6f5a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseType")
    def response_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseType"))

    @response_type.setter
    def response_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202a4ccf6591c965a00d76ee727b211ee5f20c6b9cce43319a86e66d481a6966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646f5fd4b94689291debda1449a13d8ac0d5110b1f43727dd6878a30d59e399b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signingKey")
    def signing_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingKey"))

    @signing_key.setter
    def signing_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a892f4896ab8f19a970c7c9049f3663fb6f4ca0480cfda0c809d8ba7f1f7a569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IdentityProtocolV3AccessConfig]:
        return typing.cast(typing.Optional[IdentityProtocolV3AccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProtocolV3AccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af075b24618f2f025dad2e30793664bf864769377942ae4328edef2d56c146d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtocolV3.IdentityProtocolV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "mapping_id": "mappingId",
        "protocol": "protocol",
        "provider_id": "providerId",
        "access_config": "accessConfig",
        "id": "id",
        "metadata": "metadata",
    },
)
class IdentityProtocolV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        mapping_id: builtins.str,
        protocol: builtins.str,
        provider_id: builtins.str,
        access_config: typing.Optional[typing.Union[IdentityProtocolV3AccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["IdentityProtocolV3Metadata", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param mapping_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#mapping_id IdentityProtocolV3#mapping_id}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#protocol IdentityProtocolV3#protocol}.
        :param provider_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#provider_id IdentityProtocolV3#provider_id}.
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#access_config IdentityProtocolV3#access_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#id IdentityProtocolV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#metadata IdentityProtocolV3#metadata}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_config, dict):
            access_config = IdentityProtocolV3AccessConfig(**access_config)
        if isinstance(metadata, dict):
            metadata = IdentityProtocolV3Metadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7b2dac2a689e943e2d449546c80e45c5b3a3ce0f782dd0c16407d30e70b6b4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument mapping_id", value=mapping_id, expected_type=type_hints["mapping_id"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument provider_id", value=provider_id, expected_type=type_hints["provider_id"])
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mapping_id": mapping_id,
            "protocol": protocol,
            "provider_id": provider_id,
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
        if id is not None:
            self._values["id"] = id
        if metadata is not None:
            self._values["metadata"] = metadata

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
    def mapping_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#mapping_id IdentityProtocolV3#mapping_id}.'''
        result = self._values.get("mapping_id")
        assert result is not None, "Required property 'mapping_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#protocol IdentityProtocolV3#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#provider_id IdentityProtocolV3#provider_id}.'''
        result = self._values.get("provider_id")
        assert result is not None, "Required property 'provider_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_config(self) -> typing.Optional[IdentityProtocolV3AccessConfig]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#access_config IdentityProtocolV3#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[IdentityProtocolV3AccessConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#id IdentityProtocolV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional["IdentityProtocolV3Metadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#metadata IdentityProtocolV3#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["IdentityProtocolV3Metadata"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProtocolV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtocolV3.IdentityProtocolV3Metadata",
    jsii_struct_bases=[],
    name_mapping={
        "domain_id": "domainId",
        "metadata": "metadata",
        "xaccount_type": "xaccountType",
    },
)
class IdentityProtocolV3Metadata:
    def __init__(
        self,
        *,
        domain_id: builtins.str,
        metadata: builtins.str,
        xaccount_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#domain_id IdentityProtocolV3#domain_id}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#metadata IdentityProtocolV3#metadata}.
        :param xaccount_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#xaccount_type IdentityProtocolV3#xaccount_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e27a8aafec6da09e43d8562adfb6c752c388529c50b218c82a070b31c94a045)
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument xaccount_type", value=xaccount_type, expected_type=type_hints["xaccount_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_id": domain_id,
            "metadata": metadata,
        }
        if xaccount_type is not None:
            self._values["xaccount_type"] = xaccount_type

    @builtins.property
    def domain_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#domain_id IdentityProtocolV3#domain_id}.'''
        result = self._values.get("domain_id")
        assert result is not None, "Required property 'domain_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#metadata IdentityProtocolV3#metadata}.'''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def xaccount_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protocol_v3#xaccount_type IdentityProtocolV3#xaccount_type}.'''
        result = self._values.get("xaccount_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProtocolV3Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProtocolV3MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtocolV3.IdentityProtocolV3MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47bd25b7a227f5d3786d7ad4b66a92303b4b3f1db4603d2da77336d6ff7ffe09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetXaccountType")
    def reset_xaccount_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXaccountType", []))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="xaccountTypeInput")
    def xaccount_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "xaccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdf773430bf56e4f71d38bc8b06bb8cec1b6a15fbd2d8a081bff6cf55f75588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0653b7da5409fd87430fee00dfbc6545f104089a474bc9aa9f3155414fb9e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xaccountType")
    def xaccount_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "xaccountType"))

    @xaccount_type.setter
    def xaccount_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93be25f4cd8f841ef6feec9740d3e2280abb16e544902069107aecdc95166789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xaccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IdentityProtocolV3Metadata]:
        return typing.cast(typing.Optional[IdentityProtocolV3Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProtocolV3Metadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c956b46aee67df2770de9f04a5de12f103fc2f761d81ee08b133af45d09240e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IdentityProtocolV3",
    "IdentityProtocolV3AccessConfig",
    "IdentityProtocolV3AccessConfigOutputReference",
    "IdentityProtocolV3Config",
    "IdentityProtocolV3Metadata",
    "IdentityProtocolV3MetadataOutputReference",
]

publication.publish()

def _typecheckingstub__64bb8be3f8726e41f4947d9ab43cc61a3791635fc7307dff8d3521823a6e3796(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    mapping_id: builtins.str,
    protocol: builtins.str,
    provider_id: builtins.str,
    access_config: typing.Optional[typing.Union[IdentityProtocolV3AccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[IdentityProtocolV3Metadata, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__79ff8e252e686d53925c7d2c9cf015df346c95f870458651bb659b7d77538e50(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb4e987d2990f18fc1ecf0e7c07bc7f2b1593e5db8cbc90ef23a21b9c5bc5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8364ed1155d542c26adabe07227fef5f4a30874a4fdd0a263bb37aa2d408fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffd3c27f9692ac1882efa38ffdab484942acef3353f247c0b8de5a85bf78d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4a96280f3796cf3611f379a0569de40788edacecc604b1d81aa69e74e985aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c060c2aee236b4c8555735a23b3ddcc8d6bf7c16216e64b83287311e73e1164b(
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

def _typecheckingstub__ffe3e5df8dea5533d9ef0118c4078102c076106b9167e38a3a29c15cf385ec1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e18a9ab68be4dc5243a225f48674714ecb5132dc77c6ca072d07225e6c1a188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bf4c7012a7342f6da6bf15f3ebb0ca86250c044b98992e82ba1bb2cc1c1923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed29044b2277f9353a5b716e09821a0dbab6d5b11a779c156cbb442bcfa450ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cb74793cc4df6b072e54ce7dc6c09052fb8477922b52ec201dc60e24c6a467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2400777cde9f76ea29cb39c4a5153226c3e8ac70364cb3f4394f4bdf6f5a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202a4ccf6591c965a00d76ee727b211ee5f20c6b9cce43319a86e66d481a6966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646f5fd4b94689291debda1449a13d8ac0d5110b1f43727dd6878a30d59e399b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a892f4896ab8f19a970c7c9049f3663fb6f4ca0480cfda0c809d8ba7f1f7a569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af075b24618f2f025dad2e30793664bf864769377942ae4328edef2d56c146d(
    value: typing.Optional[IdentityProtocolV3AccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7b2dac2a689e943e2d449546c80e45c5b3a3ce0f782dd0c16407d30e70b6b4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mapping_id: builtins.str,
    protocol: builtins.str,
    provider_id: builtins.str,
    access_config: typing.Optional[typing.Union[IdentityProtocolV3AccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[IdentityProtocolV3Metadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e27a8aafec6da09e43d8562adfb6c752c388529c50b218c82a070b31c94a045(
    *,
    domain_id: builtins.str,
    metadata: builtins.str,
    xaccount_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bd25b7a227f5d3786d7ad4b66a92303b4b3f1db4603d2da77336d6ff7ffe09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdf773430bf56e4f71d38bc8b06bb8cec1b6a15fbd2d8a081bff6cf55f75588(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0653b7da5409fd87430fee00dfbc6545f104089a474bc9aa9f3155414fb9e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93be25f4cd8f841ef6feec9740d3e2280abb16e544902069107aecdc95166789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c956b46aee67df2770de9f04a5de12f103fc2f761d81ee08b133af45d09240e(
    value: typing.Optional[IdentityProtocolV3Metadata],
) -> None:
    """Type checking stubs"""
    pass
