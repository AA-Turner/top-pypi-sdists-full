r'''
# `google_kms_crypto_key_version`

Refer to the Terraform Registry for docs: [`google_kms_crypto_key_version`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version).
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


class KmsCryptoKeyVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version google_kms_crypto_key_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        crypto_key: builtins.str,
        external_protection_level_options: typing.Optional[typing.Union["KmsCryptoKeyVersionExternalProtectionLevelOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KmsCryptoKeyVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version google_kms_crypto_key_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param crypto_key: The name of the cryptoKey associated with the CryptoKeyVersions. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyring}}/cryptoKeys/{{cryptoKey}}''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#crypto_key KmsCryptoKeyVersion#crypto_key}
        :param external_protection_level_options: external_protection_level_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#external_protection_level_options KmsCryptoKeyVersion#external_protection_level_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#id KmsCryptoKeyVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param state: The current state of the CryptoKeyVersion. Note: you can only specify this field to manually 'ENABLE' or 'DISABLE' the CryptoKeyVersion, otherwise the value of this field is always retrieved automatically. Possible values: ["PENDING_GENERATION", "ENABLED", "DISABLED", "DESTROYED", "DESTROY_SCHEDULED", "PENDING_IMPORT", "IMPORT_FAILED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#state KmsCryptoKeyVersion#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#timeouts KmsCryptoKeyVersion#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88667e8a0911f0140154a60baeac65cf8c65bb6a824a2077e9c34c3cbe7dbd8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KmsCryptoKeyVersionConfig(
            crypto_key=crypto_key,
            external_protection_level_options=external_protection_level_options,
            id=id,
            state=state,
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
        '''Generates CDKTF code for importing a KmsCryptoKeyVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KmsCryptoKeyVersion to import.
        :param import_from_id: The id of the existing KmsCryptoKeyVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KmsCryptoKeyVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f179fbf10329cf60b3df4992750db71615dec26abfaaa296aad3efb314ab3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExternalProtectionLevelOptions")
    def put_external_protection_level_options(
        self,
        *,
        ekm_connection_key_path: typing.Optional[builtins.str] = None,
        external_key_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ekm_connection_key_path: The path to the external key material on the EKM when using EkmConnection e.g., "v0/my/key". Set this field instead of externalKeyUri when using an EkmConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#ekm_connection_key_path KmsCryptoKeyVersion#ekm_connection_key_path}
        :param external_key_uri: The URI for an external resource that this CryptoKeyVersion represents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#external_key_uri KmsCryptoKeyVersion#external_key_uri}
        '''
        value = KmsCryptoKeyVersionExternalProtectionLevelOptions(
            ekm_connection_key_path=ekm_connection_key_path,
            external_key_uri=external_key_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putExternalProtectionLevelOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#create KmsCryptoKeyVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#delete KmsCryptoKeyVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#update KmsCryptoKeyVersion#update}.
        '''
        value = KmsCryptoKeyVersionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetExternalProtectionLevelOptions")
    def reset_external_protection_level_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalProtectionLevelOptions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

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
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @builtins.property
    @jsii.member(jsii_name="attestation")
    def attestation(self) -> "KmsCryptoKeyVersionAttestationList":
        return typing.cast("KmsCryptoKeyVersionAttestationList", jsii.get(self, "attestation"))

    @builtins.property
    @jsii.member(jsii_name="externalProtectionLevelOptions")
    def external_protection_level_options(
        self,
    ) -> "KmsCryptoKeyVersionExternalProtectionLevelOptionsOutputReference":
        return typing.cast("KmsCryptoKeyVersionExternalProtectionLevelOptionsOutputReference", jsii.get(self, "externalProtectionLevelOptions"))

    @builtins.property
    @jsii.member(jsii_name="generateTime")
    def generate_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="protectionLevel")
    def protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectionLevel"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KmsCryptoKeyVersionTimeoutsOutputReference":
        return typing.cast("KmsCryptoKeyVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyInput")
    def crypto_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cryptoKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="externalProtectionLevelOptionsInput")
    def external_protection_level_options_input(
        self,
    ) -> typing.Optional["KmsCryptoKeyVersionExternalProtectionLevelOptions"]:
        return typing.cast(typing.Optional["KmsCryptoKeyVersionExternalProtectionLevelOptions"], jsii.get(self, "externalProtectionLevelOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KmsCryptoKeyVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KmsCryptoKeyVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKey")
    def crypto_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoKey"))

    @crypto_key.setter
    def crypto_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2657864322ffee6aec1ec9e2b8068d1d3cb72028081bc304990a65d7262211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4feac4f76b7154076887b1e938a105680d455314d7b59e2828f8fe00e3bc4331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd7d4ca9fce26f76b876a43dc7985034047b489a53b11ff35c0c21a6cd67b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestation",
    jsii_struct_bases=[],
    name_mapping={},
)
class KmsCryptoKeyVersionAttestation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionAttestation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationCertChains",
    jsii_struct_bases=[],
    name_mapping={},
)
class KmsCryptoKeyVersionAttestationCertChains:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionAttestationCertChains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsCryptoKeyVersionAttestationCertChainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationCertChainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dc164a84e484c215d8f1d7c317a13ee30b12b2648c4f25f7ac4ff5dcb0e50bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KmsCryptoKeyVersionAttestationCertChainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee71b0fc3975dfef81e00d72a552049d31458573dc587dab7ff2855480742a2e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KmsCryptoKeyVersionAttestationCertChainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b82abc94a439539224bcf034fa69c3c37190b36fe6733a40e5f9373f8054a4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abde10e888ec82308e1256f4c8e55c4cf9f6c8aa76c5df3897fbf90d4e4e8cc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b122c4e11706518d44c430342b44c1cd555810a8524499e4deebfd97772b55bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KmsCryptoKeyVersionAttestationCertChainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationCertChainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5c35213bf320e75c0249292405cc678f62cd6226fc20e969f6538ce435f5f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="caviumCerts")
    def cavium_certs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "caviumCerts"))

    @builtins.property
    @jsii.member(jsii_name="googleCardCerts")
    def google_card_certs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "googleCardCerts"))

    @builtins.property
    @jsii.member(jsii_name="googlePartitionCerts")
    def google_partition_certs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "googlePartitionCerts"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KmsCryptoKeyVersionAttestationCertChains]:
        return typing.cast(typing.Optional[KmsCryptoKeyVersionAttestationCertChains], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KmsCryptoKeyVersionAttestationCertChains],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3417486ce98156d88c7e2dd1cfbd57aab8eba58e191a2a696483ea496567c3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b31d294d0e839cdf608c58cebda0a18c7c266433727cf09fa74ee66553e5d40e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fc38a8c82c9d560927584f3f821ef8cabbe62f5c719bc7b1cdd1fe21db2bf3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d758c3a673b10816c895734d935bdefb3abdc5359d096018c409f79791ee9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ece2d8abf1683b29ea8783ce22368068e72fa15c4e994ed49476bace523f3ec8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a9304473b90ea35ab5639200ee3d70939be89896068944fa17554858b45c954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9478ee2c0794930911eb154ad6fbe56c7c45c257e506aff3c169460caa90fe7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ekmConnectionKeyPath")
    def ekm_connection_key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ekmConnectionKeyPath"))

    @builtins.property
    @jsii.member(jsii_name="externalKeyUri")
    def external_key_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalKeyUri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions]:
        return typing.cast(typing.Optional[KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0167a4e157c1d3fd7348de36466caec872b46babb502435f723a33dddfe1af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KmsCryptoKeyVersionAttestationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7053cb850137de6cdf219a82974e98a4f3b53b06ca8a75b0656f5df1c2e024ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KmsCryptoKeyVersionAttestationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e130cc1c826fac2570f92f23179cfcad6043497002afac2c64d6526674b5e32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KmsCryptoKeyVersionAttestationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac56075a134ca4e37b663f933c128613951b97fdfe90a831d0982a3b616eff3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e97c78d4a464340f39a3f6c295d960dbd00c1afade45d10b3d43e310d6f21dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcf54345e78d8a3a1d89e092b7164c29903effadba738134a7313211c34ee00e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KmsCryptoKeyVersionAttestationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionAttestationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20ddc544e6a10ccc459856aa63689ef1c808910ac6a2c21358d8fbe3846494d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certChains")
    def cert_chains(self) -> KmsCryptoKeyVersionAttestationCertChainsList:
        return typing.cast(KmsCryptoKeyVersionAttestationCertChainsList, jsii.get(self, "certChains"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @builtins.property
    @jsii.member(jsii_name="externalProtectionLevelOptions")
    def external_protection_level_options(
        self,
    ) -> KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsList:
        return typing.cast(KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsList, jsii.get(self, "externalProtectionLevelOptions"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KmsCryptoKeyVersionAttestation]:
        return typing.cast(typing.Optional[KmsCryptoKeyVersionAttestation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KmsCryptoKeyVersionAttestation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b5d3d6a2763d3b0961c261fdfe5880c3bc2cca056dd7685bac18831edc9d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "crypto_key": "cryptoKey",
        "external_protection_level_options": "externalProtectionLevelOptions",
        "id": "id",
        "state": "state",
        "timeouts": "timeouts",
    },
)
class KmsCryptoKeyVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        crypto_key: builtins.str,
        external_protection_level_options: typing.Optional[typing.Union["KmsCryptoKeyVersionExternalProtectionLevelOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KmsCryptoKeyVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param crypto_key: The name of the cryptoKey associated with the CryptoKeyVersions. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyring}}/cryptoKeys/{{cryptoKey}}''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#crypto_key KmsCryptoKeyVersion#crypto_key}
        :param external_protection_level_options: external_protection_level_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#external_protection_level_options KmsCryptoKeyVersion#external_protection_level_options}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#id KmsCryptoKeyVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param state: The current state of the CryptoKeyVersion. Note: you can only specify this field to manually 'ENABLE' or 'DISABLE' the CryptoKeyVersion, otherwise the value of this field is always retrieved automatically. Possible values: ["PENDING_GENERATION", "ENABLED", "DISABLED", "DESTROYED", "DESTROY_SCHEDULED", "PENDING_IMPORT", "IMPORT_FAILED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#state KmsCryptoKeyVersion#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#timeouts KmsCryptoKeyVersion#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(external_protection_level_options, dict):
            external_protection_level_options = KmsCryptoKeyVersionExternalProtectionLevelOptions(**external_protection_level_options)
        if isinstance(timeouts, dict):
            timeouts = KmsCryptoKeyVersionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1242d282edc3128495b051d3f08077089049f111e9d689c49a8715aafa07f363)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument crypto_key", value=crypto_key, expected_type=type_hints["crypto_key"])
            check_type(argname="argument external_protection_level_options", value=external_protection_level_options, expected_type=type_hints["external_protection_level_options"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crypto_key": crypto_key,
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
        if external_protection_level_options is not None:
            self._values["external_protection_level_options"] = external_protection_level_options
        if id is not None:
            self._values["id"] = id
        if state is not None:
            self._values["state"] = state
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
    def crypto_key(self) -> builtins.str:
        '''The name of the cryptoKey associated with the CryptoKeyVersions. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyring}}/cryptoKeys/{{cryptoKey}}''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#crypto_key KmsCryptoKeyVersion#crypto_key}
        '''
        result = self._values.get("crypto_key")
        assert result is not None, "Required property 'crypto_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_protection_level_options(
        self,
    ) -> typing.Optional["KmsCryptoKeyVersionExternalProtectionLevelOptions"]:
        '''external_protection_level_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#external_protection_level_options KmsCryptoKeyVersion#external_protection_level_options}
        '''
        result = self._values.get("external_protection_level_options")
        return typing.cast(typing.Optional["KmsCryptoKeyVersionExternalProtectionLevelOptions"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#id KmsCryptoKeyVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The current state of the CryptoKeyVersion.

        Note: you can only specify this field to manually 'ENABLE' or 'DISABLE' the CryptoKeyVersion,
        otherwise the value of this field is always retrieved automatically. Possible values: ["PENDING_GENERATION", "ENABLED", "DISABLED", "DESTROYED", "DESTROY_SCHEDULED", "PENDING_IMPORT", "IMPORT_FAILED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#state KmsCryptoKeyVersion#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KmsCryptoKeyVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#timeouts KmsCryptoKeyVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KmsCryptoKeyVersionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionExternalProtectionLevelOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ekm_connection_key_path": "ekmConnectionKeyPath",
        "external_key_uri": "externalKeyUri",
    },
)
class KmsCryptoKeyVersionExternalProtectionLevelOptions:
    def __init__(
        self,
        *,
        ekm_connection_key_path: typing.Optional[builtins.str] = None,
        external_key_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ekm_connection_key_path: The path to the external key material on the EKM when using EkmConnection e.g., "v0/my/key". Set this field instead of externalKeyUri when using an EkmConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#ekm_connection_key_path KmsCryptoKeyVersion#ekm_connection_key_path}
        :param external_key_uri: The URI for an external resource that this CryptoKeyVersion represents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#external_key_uri KmsCryptoKeyVersion#external_key_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c35bcfd62e6f66fd98107d89a9f2210ffd3414f034d470f058517db487f6594)
            check_type(argname="argument ekm_connection_key_path", value=ekm_connection_key_path, expected_type=type_hints["ekm_connection_key_path"])
            check_type(argname="argument external_key_uri", value=external_key_uri, expected_type=type_hints["external_key_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ekm_connection_key_path is not None:
            self._values["ekm_connection_key_path"] = ekm_connection_key_path
        if external_key_uri is not None:
            self._values["external_key_uri"] = external_key_uri

    @builtins.property
    def ekm_connection_key_path(self) -> typing.Optional[builtins.str]:
        '''The path to the external key material on the EKM when using EkmConnection e.g., "v0/my/key". Set this field instead of externalKeyUri when using an EkmConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#ekm_connection_key_path KmsCryptoKeyVersion#ekm_connection_key_path}
        '''
        result = self._values.get("ekm_connection_key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_key_uri(self) -> typing.Optional[builtins.str]:
        '''The URI for an external resource that this CryptoKeyVersion represents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#external_key_uri KmsCryptoKeyVersion#external_key_uri}
        '''
        result = self._values.get("external_key_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionExternalProtectionLevelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsCryptoKeyVersionExternalProtectionLevelOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionExternalProtectionLevelOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__152aa05ca5fc3dc48004456fe51d16ce277b76d4896ce59b4aeb58446b4c6447)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEkmConnectionKeyPath")
    def reset_ekm_connection_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEkmConnectionKeyPath", []))

    @jsii.member(jsii_name="resetExternalKeyUri")
    def reset_external_key_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalKeyUri", []))

    @builtins.property
    @jsii.member(jsii_name="ekmConnectionKeyPathInput")
    def ekm_connection_key_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ekmConnectionKeyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="externalKeyUriInput")
    def external_key_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalKeyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="ekmConnectionKeyPath")
    def ekm_connection_key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ekmConnectionKeyPath"))

    @ekm_connection_key_path.setter
    def ekm_connection_key_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2567ed5fb9f85b948e90952515f1d4fa34a9de7d0a11241d3f2028ad6be609b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ekmConnectionKeyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalKeyUri")
    def external_key_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalKeyUri"))

    @external_key_uri.setter
    def external_key_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673c991468c8c594aea4bea9e0656ea191bda2ab6c4818a5a4e7d44724ab7765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalKeyUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KmsCryptoKeyVersionExternalProtectionLevelOptions]:
        return typing.cast(typing.Optional[KmsCryptoKeyVersionExternalProtectionLevelOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KmsCryptoKeyVersionExternalProtectionLevelOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2599e6d87d61d9c4358397fd289263948f19c37010e81a4ae17cff34059ff575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KmsCryptoKeyVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#create KmsCryptoKeyVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#delete KmsCryptoKeyVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#update KmsCryptoKeyVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1d9468b572d2581ca56fe8197af668195d5f398f53976b6232a13ebc475083)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#create KmsCryptoKeyVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#delete KmsCryptoKeyVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_crypto_key_version#update KmsCryptoKeyVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsCryptoKeyVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKeyVersion.KmsCryptoKeyVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc6e74b4dc65b3aad2fd67eecd1e070faa57d2c1c283312150f342b53ef2e4b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8c16e21bc4ce1d8681c0d0f2a610389ad196339547c7d183abd37a30a7f01d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8123a1c151bd377f8bfc9876f7ada13cef631e9e719a5866e088f3e002ee34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9baa78ed3add0c79fbb1273b23f2d1078168036a0451b8b029428c90e170ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsCryptoKeyVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsCryptoKeyVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsCryptoKeyVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497a900e4eed6a9f5431a09d6753c23565902069fe4e8493838d7040d03fbaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KmsCryptoKeyVersion",
    "KmsCryptoKeyVersionAttestation",
    "KmsCryptoKeyVersionAttestationCertChains",
    "KmsCryptoKeyVersionAttestationCertChainsList",
    "KmsCryptoKeyVersionAttestationCertChainsOutputReference",
    "KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions",
    "KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsList",
    "KmsCryptoKeyVersionAttestationExternalProtectionLevelOptionsOutputReference",
    "KmsCryptoKeyVersionAttestationList",
    "KmsCryptoKeyVersionAttestationOutputReference",
    "KmsCryptoKeyVersionConfig",
    "KmsCryptoKeyVersionExternalProtectionLevelOptions",
    "KmsCryptoKeyVersionExternalProtectionLevelOptionsOutputReference",
    "KmsCryptoKeyVersionTimeouts",
    "KmsCryptoKeyVersionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__88667e8a0911f0140154a60baeac65cf8c65bb6a824a2077e9c34c3cbe7dbd8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    crypto_key: builtins.str,
    external_protection_level_options: typing.Optional[typing.Union[KmsCryptoKeyVersionExternalProtectionLevelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KmsCryptoKeyVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b1f179fbf10329cf60b3df4992750db71615dec26abfaaa296aad3efb314ab3f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2657864322ffee6aec1ec9e2b8068d1d3cb72028081bc304990a65d7262211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feac4f76b7154076887b1e938a105680d455314d7b59e2828f8fe00e3bc4331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd7d4ca9fce26f76b876a43dc7985034047b489a53b11ff35c0c21a6cd67b14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc164a84e484c215d8f1d7c317a13ee30b12b2648c4f25f7ac4ff5dcb0e50bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee71b0fc3975dfef81e00d72a552049d31458573dc587dab7ff2855480742a2e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b82abc94a439539224bcf034fa69c3c37190b36fe6733a40e5f9373f8054a4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abde10e888ec82308e1256f4c8e55c4cf9f6c8aa76c5df3897fbf90d4e4e8cc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b122c4e11706518d44c430342b44c1cd555810a8524499e4deebfd97772b55bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5c35213bf320e75c0249292405cc678f62cd6226fc20e969f6538ce435f5f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3417486ce98156d88c7e2dd1cfbd57aab8eba58e191a2a696483ea496567c3ed(
    value: typing.Optional[KmsCryptoKeyVersionAttestationCertChains],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31d294d0e839cdf608c58cebda0a18c7c266433727cf09fa74ee66553e5d40e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fc38a8c82c9d560927584f3f821ef8cabbe62f5c719bc7b1cdd1fe21db2bf3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d758c3a673b10816c895734d935bdefb3abdc5359d096018c409f79791ee9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece2d8abf1683b29ea8783ce22368068e72fa15c4e994ed49476bace523f3ec8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9304473b90ea35ab5639200ee3d70939be89896068944fa17554858b45c954(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9478ee2c0794930911eb154ad6fbe56c7c45c257e506aff3c169460caa90fe7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0167a4e157c1d3fd7348de36466caec872b46babb502435f723a33dddfe1af9(
    value: typing.Optional[KmsCryptoKeyVersionAttestationExternalProtectionLevelOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7053cb850137de6cdf219a82974e98a4f3b53b06ca8a75b0656f5df1c2e024ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e130cc1c826fac2570f92f23179cfcad6043497002afac2c64d6526674b5e32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac56075a134ca4e37b663f933c128613951b97fdfe90a831d0982a3b616eff3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e97c78d4a464340f39a3f6c295d960dbd00c1afade45d10b3d43e310d6f21dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf54345e78d8a3a1d89e092b7164c29903effadba738134a7313211c34ee00e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ddc544e6a10ccc459856aa63689ef1c808910ac6a2c21358d8fbe3846494d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b5d3d6a2763d3b0961c261fdfe5880c3bc2cca056dd7685bac18831edc9d56(
    value: typing.Optional[KmsCryptoKeyVersionAttestation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1242d282edc3128495b051d3f08077089049f111e9d689c49a8715aafa07f363(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    crypto_key: builtins.str,
    external_protection_level_options: typing.Optional[typing.Union[KmsCryptoKeyVersionExternalProtectionLevelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KmsCryptoKeyVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c35bcfd62e6f66fd98107d89a9f2210ffd3414f034d470f058517db487f6594(
    *,
    ekm_connection_key_path: typing.Optional[builtins.str] = None,
    external_key_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152aa05ca5fc3dc48004456fe51d16ce277b76d4896ce59b4aeb58446b4c6447(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2567ed5fb9f85b948e90952515f1d4fa34a9de7d0a11241d3f2028ad6be609b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673c991468c8c594aea4bea9e0656ea191bda2ab6c4818a5a4e7d44724ab7765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2599e6d87d61d9c4358397fd289263948f19c37010e81a4ae17cff34059ff575(
    value: typing.Optional[KmsCryptoKeyVersionExternalProtectionLevelOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1d9468b572d2581ca56fe8197af668195d5f398f53976b6232a13ebc475083(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6e74b4dc65b3aad2fd67eecd1e070faa57d2c1c283312150f342b53ef2e4b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c16e21bc4ce1d8681c0d0f2a610389ad196339547c7d183abd37a30a7f01d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8123a1c151bd377f8bfc9876f7ada13cef631e9e719a5866e088f3e002ee34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9baa78ed3add0c79fbb1273b23f2d1078168036a0451b8b029428c90e170ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497a900e4eed6a9f5431a09d6753c23565902069fe4e8493838d7040d03fbaef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsCryptoKeyVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
