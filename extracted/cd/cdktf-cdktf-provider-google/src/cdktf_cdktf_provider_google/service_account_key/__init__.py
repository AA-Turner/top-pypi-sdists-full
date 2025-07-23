r'''
# `google_service_account_key`

Refer to the Terraform Registry for docs: [`google_service_account_key`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key).
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


class ServiceAccountKey(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.serviceAccountKey.ServiceAccountKey",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key google_service_account_key}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service_account_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_algorithm: typing.Optional[builtins.str] = None,
        private_key_type: typing.Optional[builtins.str] = None,
        public_key_data: typing.Optional[builtins.str] = None,
        public_key_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key google_service_account_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service_account_id: The ID of the parent service account of the key. This can be a string in the format {ACCOUNT} or projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}, where {ACCOUNT} is the email address or unique id of the service account. If the {ACCOUNT} syntax is used, the project will be inferred from the provider's configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#service_account_id ServiceAccountKey#service_account_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#id ServiceAccountKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keepers: Arbitrary map of values that, when changed, will trigger recreation of resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#keepers ServiceAccountKey#keepers}
        :param key_algorithm: The algorithm used to generate the key, used only on create. KEY_ALG_RSA_2048 is the default algorithm. Valid values are: "KEY_ALG_RSA_1024", "KEY_ALG_RSA_2048". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#key_algorithm ServiceAccountKey#key_algorithm}
        :param private_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#private_key_type ServiceAccountKey#private_key_type}.
        :param public_key_data: A field that allows clients to upload their own public key. If set, use this public key data to create a service account key for given service account. Please note, the expected format for this field is a base64 encoded X509_PEM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#public_key_data ServiceAccountKey#public_key_data}
        :param public_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#public_key_type ServiceAccountKey#public_key_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95e7d726a44a5789b4ce4b3f584febc38778edd4123f86d94fdb25710d3df13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceAccountKeyConfig(
            service_account_id=service_account_id,
            id=id,
            keepers=keepers,
            key_algorithm=key_algorithm,
            private_key_type=private_key_type,
            public_key_data=public_key_data,
            public_key_type=public_key_type,
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
        '''Generates CDKTF code for importing a ServiceAccountKey resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceAccountKey to import.
        :param import_from_id: The id of the existing ServiceAccountKey that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceAccountKey to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ea26e33183f12dff4226d4bb33bc8ecdb12557ec66e8c06184334498a0c605)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeepers")
    def reset_keepers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepers", []))

    @jsii.member(jsii_name="resetKeyAlgorithm")
    def reset_key_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAlgorithm", []))

    @jsii.member(jsii_name="resetPrivateKeyType")
    def reset_private_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyType", []))

    @jsii.member(jsii_name="resetPublicKeyData")
    def reset_public_key_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKeyData", []))

    @jsii.member(jsii_name="resetPublicKeyType")
    def reset_public_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKeyType", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="validAfter")
    def valid_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validAfter"))

    @builtins.property
    @jsii.member(jsii_name="validBefore")
    def valid_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validBefore"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keepersInput")
    def keepers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "keepersInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithmInput")
    def key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyTypeInput")
    def private_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyDataInput")
    def public_key_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyDataInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyTypeInput")
    def public_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountIdInput")
    def service_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98c401b3a755a42c3276538113c6b38c794916a35a7453d19fbfd279709a100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepers")
    def keepers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "keepers"))

    @keepers.setter
    def keepers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90ee2f0694e9f8af2ca8ff2fa45df10fe0c132a271370061e4a50b8a2dc457d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlgorithm"))

    @key_algorithm.setter
    def key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b13dc80345850d846a2001f3fa50d1103ccfff9fa4289801fd746dde6e292d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyType")
    def private_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyType"))

    @private_key_type.setter
    def private_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8273dbbf65ef0b70915c3724f116fd84a85bce7fe396299c1b55f38834d073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicKeyData")
    def public_key_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKeyData"))

    @public_key_data.setter
    def public_key_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67659efc747564eed81d1432b64146065ab86fdb07544bb1ac403c89e631a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicKeyType")
    def public_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKeyType"))

    @public_key_type.setter
    def public_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee38128e91cc8e6e99ae4eb4e5dbd45034abbb63a1586ed4911267b0c9a0a693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountId")
    def service_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountId"))

    @service_account_id.setter
    def service_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289d3ac24eb062c5e02fba978f55acda9b82a20cc30fb30691e092d3756d3c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.serviceAccountKey.ServiceAccountKeyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "service_account_id": "serviceAccountId",
        "id": "id",
        "keepers": "keepers",
        "key_algorithm": "keyAlgorithm",
        "private_key_type": "privateKeyType",
        "public_key_data": "publicKeyData",
        "public_key_type": "publicKeyType",
    },
)
class ServiceAccountKeyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service_account_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_algorithm: typing.Optional[builtins.str] = None,
        private_key_type: typing.Optional[builtins.str] = None,
        public_key_data: typing.Optional[builtins.str] = None,
        public_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param service_account_id: The ID of the parent service account of the key. This can be a string in the format {ACCOUNT} or projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}, where {ACCOUNT} is the email address or unique id of the service account. If the {ACCOUNT} syntax is used, the project will be inferred from the provider's configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#service_account_id ServiceAccountKey#service_account_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#id ServiceAccountKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keepers: Arbitrary map of values that, when changed, will trigger recreation of resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#keepers ServiceAccountKey#keepers}
        :param key_algorithm: The algorithm used to generate the key, used only on create. KEY_ALG_RSA_2048 is the default algorithm. Valid values are: "KEY_ALG_RSA_1024", "KEY_ALG_RSA_2048". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#key_algorithm ServiceAccountKey#key_algorithm}
        :param private_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#private_key_type ServiceAccountKey#private_key_type}.
        :param public_key_data: A field that allows clients to upload their own public key. If set, use this public key data to create a service account key for given service account. Please note, the expected format for this field is a base64 encoded X509_PEM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#public_key_data ServiceAccountKey#public_key_data}
        :param public_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#public_key_type ServiceAccountKey#public_key_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876eb097883413b1602378c3fc5defb263b7a3474bd19b5f05e685cf59852e2b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument service_account_id", value=service_account_id, expected_type=type_hints["service_account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument keepers", value=keepers, expected_type=type_hints["keepers"])
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument private_key_type", value=private_key_type, expected_type=type_hints["private_key_type"])
            check_type(argname="argument public_key_data", value=public_key_data, expected_type=type_hints["public_key_data"])
            check_type(argname="argument public_key_type", value=public_key_type, expected_type=type_hints["public_key_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_id": service_account_id,
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
        if id is not None:
            self._values["id"] = id
        if keepers is not None:
            self._values["keepers"] = keepers
        if key_algorithm is not None:
            self._values["key_algorithm"] = key_algorithm
        if private_key_type is not None:
            self._values["private_key_type"] = private_key_type
        if public_key_data is not None:
            self._values["public_key_data"] = public_key_data
        if public_key_type is not None:
            self._values["public_key_type"] = public_key_type

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
    def service_account_id(self) -> builtins.str:
        '''The ID of the parent service account of the key.

        This can be a string in the format {ACCOUNT} or projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}, where {ACCOUNT} is the email address or unique id of the service account. If the {ACCOUNT} syntax is used, the project will be inferred from the provider's configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#service_account_id ServiceAccountKey#service_account_id}
        '''
        result = self._values.get("service_account_id")
        assert result is not None, "Required property 'service_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#id ServiceAccountKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keepers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Arbitrary map of values that, when changed, will trigger recreation of resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#keepers ServiceAccountKey#keepers}
        '''
        result = self._values.get("keepers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def key_algorithm(self) -> typing.Optional[builtins.str]:
        '''The algorithm used to generate the key, used only on create.

        KEY_ALG_RSA_2048 is the default algorithm. Valid values are: "KEY_ALG_RSA_1024", "KEY_ALG_RSA_2048".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#key_algorithm ServiceAccountKey#key_algorithm}
        '''
        result = self._values.get("key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#private_key_type ServiceAccountKey#private_key_type}.'''
        result = self._values.get("private_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key_data(self) -> typing.Optional[builtins.str]:
        '''A field that allows clients to upload their own public key.

        If set, use this public key data to create a service account key for given service account. Please note, the expected format for this field is a base64 encoded X509_PEM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#public_key_data ServiceAccountKey#public_key_data}
        '''
        result = self._values.get("public_key_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/service_account_key#public_key_type ServiceAccountKey#public_key_type}.'''
        result = self._values.get("public_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAccountKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ServiceAccountKey",
    "ServiceAccountKeyConfig",
]

publication.publish()

def _typecheckingstub__b95e7d726a44a5789b4ce4b3f584febc38778edd4123f86d94fdb25710d3df13(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service_account_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_algorithm: typing.Optional[builtins.str] = None,
    private_key_type: typing.Optional[builtins.str] = None,
    public_key_data: typing.Optional[builtins.str] = None,
    public_key_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__19ea26e33183f12dff4226d4bb33bc8ecdb12557ec66e8c06184334498a0c605(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98c401b3a755a42c3276538113c6b38c794916a35a7453d19fbfd279709a100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90ee2f0694e9f8af2ca8ff2fa45df10fe0c132a271370061e4a50b8a2dc457d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b13dc80345850d846a2001f3fa50d1103ccfff9fa4289801fd746dde6e292d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8273dbbf65ef0b70915c3724f116fd84a85bce7fe396299c1b55f38834d073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67659efc747564eed81d1432b64146065ab86fdb07544bb1ac403c89e631a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee38128e91cc8e6e99ae4eb4e5dbd45034abbb63a1586ed4911267b0c9a0a693(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289d3ac24eb062c5e02fba978f55acda9b82a20cc30fb30691e092d3756d3c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876eb097883413b1602378c3fc5defb263b7a3474bd19b5f05e685cf59852e2b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_algorithm: typing.Optional[builtins.str] = None,
    private_key_type: typing.Optional[builtins.str] = None,
    public_key_data: typing.Optional[builtins.str] = None,
    public_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
