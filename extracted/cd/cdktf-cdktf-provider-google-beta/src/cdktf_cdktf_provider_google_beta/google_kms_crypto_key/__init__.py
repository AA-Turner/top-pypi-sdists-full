r'''
# `google_kms_crypto_key`

Refer to the Terraform Registry for docs: [`google_kms_crypto_key`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key).
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


class GoogleKmsCryptoKey(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKey",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key google_kms_crypto_key}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key_ring: builtins.str,
        name: builtins.str,
        crypto_key_backend: typing.Optional[builtins.str] = None,
        destroy_scheduled_duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_access_justifications_policy: typing.Optional[typing.Union["GoogleKmsCryptoKeyKeyAccessJustificationsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        purpose: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
        skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleKmsCryptoKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_template: typing.Optional[typing.Union["GoogleKmsCryptoKeyVersionTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key google_kms_crypto_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key_ring: The KeyRing that this key belongs to. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyRing}}''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#key_ring GoogleKmsCryptoKey#key_ring}
        :param name: The resource name for the CryptoKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#name GoogleKmsCryptoKey#name}
        :param crypto_key_backend: The resource name of the backend environment associated with all CryptoKeyVersions within this CryptoKey. The resource name is in the format "projects/* /locations/* /ekmConnections/*" and only applies to "EXTERNAL_VPC" keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#crypto_key_backend GoogleKmsCryptoKey#crypto_key_backend} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param destroy_scheduled_duration: The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED. If not specified at creation time, the default duration is 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#destroy_scheduled_duration GoogleKmsCryptoKey#destroy_scheduled_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#id GoogleKmsCryptoKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_only: Whether this key may contain imported versions only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#import_only GoogleKmsCryptoKey#import_only}
        :param key_access_justifications_policy: key_access_justifications_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#key_access_justifications_policy GoogleKmsCryptoKey#key_access_justifications_policy}
        :param labels: Labels with user-defined metadata to apply to this resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#labels GoogleKmsCryptoKey#labels}
        :param purpose: The immutable purpose of this CryptoKey. See the `purpose reference <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyPurpose>`_ for possible inputs. Default value is "ENCRYPT_DECRYPT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#purpose GoogleKmsCryptoKey#purpose}
        :param rotation_period: Every time this period passes, generate a new CryptoKeyVersion and set it as the primary. The first rotation will take place after the specified period. The rotation period has the format of a decimal number with up to 9 fractional digits, followed by the letter 's' (seconds). It must be greater than a day (ie, 86400). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#rotation_period GoogleKmsCryptoKey#rotation_period}
        :param skip_initial_version_creation: If set to true, the request will create a CryptoKey without any CryptoKeyVersions. You must use the 'google_kms_crypto_key_version' resource to create a new CryptoKeyVersion or 'google_kms_key_ring_import_job' resource to import the CryptoKeyVersion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#skip_initial_version_creation GoogleKmsCryptoKey#skip_initial_version_creation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#timeouts GoogleKmsCryptoKey#timeouts}
        :param version_template: version_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#version_template GoogleKmsCryptoKey#version_template}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71293baedbcdf4e5e15bd41d6d230b947890fa753b31d9d934001a103587bccb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleKmsCryptoKeyConfig(
            key_ring=key_ring,
            name=name,
            crypto_key_backend=crypto_key_backend,
            destroy_scheduled_duration=destroy_scheduled_duration,
            id=id,
            import_only=import_only,
            key_access_justifications_policy=key_access_justifications_policy,
            labels=labels,
            purpose=purpose,
            rotation_period=rotation_period,
            skip_initial_version_creation=skip_initial_version_creation,
            timeouts=timeouts,
            version_template=version_template,
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
        '''Generates CDKTF code for importing a GoogleKmsCryptoKey resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleKmsCryptoKey to import.
        :param import_from_id: The id of the existing GoogleKmsCryptoKey that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleKmsCryptoKey to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9000975014e7a5d9f8fd243b9a4578a615a25a2a3fb7fee88bc1d074d606b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKeyAccessJustificationsPolicy")
    def put_key_access_justifications_policy(
        self,
        *,
        allowed_access_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_access_reasons: The list of allowed reasons for access to this CryptoKey. Zero allowed access reasons means all encrypt, decrypt, and sign operations for this CryptoKey will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#allowed_access_reasons GoogleKmsCryptoKey#allowed_access_reasons}
        '''
        value = GoogleKmsCryptoKeyKeyAccessJustificationsPolicy(
            allowed_access_reasons=allowed_access_reasons
        )

        return typing.cast(None, jsii.invoke(self, "putKeyAccessJustificationsPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#create GoogleKmsCryptoKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#delete GoogleKmsCryptoKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#update GoogleKmsCryptoKey#update}.
        '''
        value = GoogleKmsCryptoKeyTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVersionTemplate")
    def put_version_template(
        self,
        *,
        algorithm: builtins.str,
        protection_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm to use when creating a version based on this template. See the `algorithm reference <https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm>`_ for possible inputs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#algorithm GoogleKmsCryptoKey#algorithm}
        :param protection_level: The protection level to use when creating a version based on this template. Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#protection_level GoogleKmsCryptoKey#protection_level}
        '''
        value = GoogleKmsCryptoKeyVersionTemplate(
            algorithm=algorithm, protection_level=protection_level
        )

        return typing.cast(None, jsii.invoke(self, "putVersionTemplate", [value]))

    @jsii.member(jsii_name="resetCryptoKeyBackend")
    def reset_crypto_key_backend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoKeyBackend", []))

    @jsii.member(jsii_name="resetDestroyScheduledDuration")
    def reset_destroy_scheduled_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestroyScheduledDuration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportOnly")
    def reset_import_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportOnly", []))

    @jsii.member(jsii_name="resetKeyAccessJustificationsPolicy")
    def reset_key_access_justifications_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAccessJustificationsPolicy", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPurpose")
    def reset_purpose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurpose", []))

    @jsii.member(jsii_name="resetRotationPeriod")
    def reset_rotation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationPeriod", []))

    @jsii.member(jsii_name="resetSkipInitialVersionCreation")
    def reset_skip_initial_version_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipInitialVersionCreation", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersionTemplate")
    def reset_version_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionTemplate", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="keyAccessJustificationsPolicy")
    def key_access_justifications_policy(
        self,
    ) -> "GoogleKmsCryptoKeyKeyAccessJustificationsPolicyOutputReference":
        return typing.cast("GoogleKmsCryptoKeyKeyAccessJustificationsPolicyOutputReference", jsii.get(self, "keyAccessJustificationsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> "GoogleKmsCryptoKeyPrimaryList":
        return typing.cast("GoogleKmsCryptoKeyPrimaryList", jsii.get(self, "primary"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleKmsCryptoKeyTimeoutsOutputReference":
        return typing.cast("GoogleKmsCryptoKeyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionTemplate")
    def version_template(self) -> "GoogleKmsCryptoKeyVersionTemplateOutputReference":
        return typing.cast("GoogleKmsCryptoKeyVersionTemplateOutputReference", jsii.get(self, "versionTemplate"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyBackendInput")
    def crypto_key_backend_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cryptoKeyBackendInput"))

    @builtins.property
    @jsii.member(jsii_name="destroyScheduledDurationInput")
    def destroy_scheduled_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destroyScheduledDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importOnlyInput")
    def import_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "importOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAccessJustificationsPolicyInput")
    def key_access_justifications_policy_input(
        self,
    ) -> typing.Optional["GoogleKmsCryptoKeyKeyAccessJustificationsPolicy"]:
        return typing.cast(typing.Optional["GoogleKmsCryptoKeyKeyAccessJustificationsPolicy"], jsii.get(self, "keyAccessJustificationsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRingInput")
    def key_ring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyRingInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="purposeInput")
    def purpose_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "purposeInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationPeriodInput")
    def rotation_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="skipInitialVersionCreationInput")
    def skip_initial_version_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipInitialVersionCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleKmsCryptoKeyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleKmsCryptoKeyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionTemplateInput")
    def version_template_input(
        self,
    ) -> typing.Optional["GoogleKmsCryptoKeyVersionTemplate"]:
        return typing.cast(typing.Optional["GoogleKmsCryptoKeyVersionTemplate"], jsii.get(self, "versionTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyBackend")
    def crypto_key_backend(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoKeyBackend"))

    @crypto_key_backend.setter
    def crypto_key_backend(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb898b24bc04d49783c892c5540ceec5b6ee8735c38b2b0163c7a7909ca7745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoKeyBackend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destroyScheduledDuration")
    def destroy_scheduled_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destroyScheduledDuration"))

    @destroy_scheduled_duration.setter
    def destroy_scheduled_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7434f791c070a33b04c10d05d6be6fd53ba2bf68e27007cc71bf6d5f9982b464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destroyScheduledDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917b34cd4362a5ec6f5a52e29c8924a87e9b19e05d43c516fd9a6b4d1ccd5b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importOnly")
    def import_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "importOnly"))

    @import_only.setter
    def import_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06addf4319c0a2c88197eaeb7b28736f874db698a04daa66f0e3d2b051b5b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyRing")
    def key_ring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRing"))

    @key_ring.setter
    def key_ring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0dd172e00d38f90f4ffdb8b5f7a186a98efb715be73b4deafd3c8904d11222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abb00004a919b67843b5bffb27ccab0fa13af5499735cd3aee03fd3ed1d812f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99df6f766a2b3a0639d428498f0cbf11afbd6771a723482d36e81c3ed95efe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purpose")
    def purpose(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purpose"))

    @purpose.setter
    def purpose(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d7f9388c41f89f351ca796d25549c01477278d69f9509437be00df8eec938a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purpose", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dafe148d6bd748902bc2ff268f095cc9a9f591d7debfdf0c8f0fd366c432128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipInitialVersionCreation")
    def skip_initial_version_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipInitialVersionCreation"))

    @skip_initial_version_creation.setter
    def skip_initial_version_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbae328991e47cdb99f8c99ed16a9cd6f65412d1305c55167de440219c11ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipInitialVersionCreation", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key_ring": "keyRing",
        "name": "name",
        "crypto_key_backend": "cryptoKeyBackend",
        "destroy_scheduled_duration": "destroyScheduledDuration",
        "id": "id",
        "import_only": "importOnly",
        "key_access_justifications_policy": "keyAccessJustificationsPolicy",
        "labels": "labels",
        "purpose": "purpose",
        "rotation_period": "rotationPeriod",
        "skip_initial_version_creation": "skipInitialVersionCreation",
        "timeouts": "timeouts",
        "version_template": "versionTemplate",
    },
)
class GoogleKmsCryptoKeyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key_ring: builtins.str,
        name: builtins.str,
        crypto_key_backend: typing.Optional[builtins.str] = None,
        destroy_scheduled_duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_access_justifications_policy: typing.Optional[typing.Union["GoogleKmsCryptoKeyKeyAccessJustificationsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        purpose: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
        skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleKmsCryptoKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_template: typing.Optional[typing.Union["GoogleKmsCryptoKeyVersionTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key_ring: The KeyRing that this key belongs to. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyRing}}''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#key_ring GoogleKmsCryptoKey#key_ring}
        :param name: The resource name for the CryptoKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#name GoogleKmsCryptoKey#name}
        :param crypto_key_backend: The resource name of the backend environment associated with all CryptoKeyVersions within this CryptoKey. The resource name is in the format "projects/* /locations/* /ekmConnections/*" and only applies to "EXTERNAL_VPC" keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#crypto_key_backend GoogleKmsCryptoKey#crypto_key_backend} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param destroy_scheduled_duration: The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED. If not specified at creation time, the default duration is 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#destroy_scheduled_duration GoogleKmsCryptoKey#destroy_scheduled_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#id GoogleKmsCryptoKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_only: Whether this key may contain imported versions only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#import_only GoogleKmsCryptoKey#import_only}
        :param key_access_justifications_policy: key_access_justifications_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#key_access_justifications_policy GoogleKmsCryptoKey#key_access_justifications_policy}
        :param labels: Labels with user-defined metadata to apply to this resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#labels GoogleKmsCryptoKey#labels}
        :param purpose: The immutable purpose of this CryptoKey. See the `purpose reference <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyPurpose>`_ for possible inputs. Default value is "ENCRYPT_DECRYPT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#purpose GoogleKmsCryptoKey#purpose}
        :param rotation_period: Every time this period passes, generate a new CryptoKeyVersion and set it as the primary. The first rotation will take place after the specified period. The rotation period has the format of a decimal number with up to 9 fractional digits, followed by the letter 's' (seconds). It must be greater than a day (ie, 86400). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#rotation_period GoogleKmsCryptoKey#rotation_period}
        :param skip_initial_version_creation: If set to true, the request will create a CryptoKey without any CryptoKeyVersions. You must use the 'google_kms_crypto_key_version' resource to create a new CryptoKeyVersion or 'google_kms_key_ring_import_job' resource to import the CryptoKeyVersion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#skip_initial_version_creation GoogleKmsCryptoKey#skip_initial_version_creation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#timeouts GoogleKmsCryptoKey#timeouts}
        :param version_template: version_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#version_template GoogleKmsCryptoKey#version_template}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(key_access_justifications_policy, dict):
            key_access_justifications_policy = GoogleKmsCryptoKeyKeyAccessJustificationsPolicy(**key_access_justifications_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleKmsCryptoKeyTimeouts(**timeouts)
        if isinstance(version_template, dict):
            version_template = GoogleKmsCryptoKeyVersionTemplate(**version_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaa35b264143150b895c4022296aa8e839aa7981576548516ba24d0943a0d82)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key_ring", value=key_ring, expected_type=type_hints["key_ring"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument crypto_key_backend", value=crypto_key_backend, expected_type=type_hints["crypto_key_backend"])
            check_type(argname="argument destroy_scheduled_duration", value=destroy_scheduled_duration, expected_type=type_hints["destroy_scheduled_duration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_only", value=import_only, expected_type=type_hints["import_only"])
            check_type(argname="argument key_access_justifications_policy", value=key_access_justifications_policy, expected_type=type_hints["key_access_justifications_policy"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument purpose", value=purpose, expected_type=type_hints["purpose"])
            check_type(argname="argument rotation_period", value=rotation_period, expected_type=type_hints["rotation_period"])
            check_type(argname="argument skip_initial_version_creation", value=skip_initial_version_creation, expected_type=type_hints["skip_initial_version_creation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_template", value=version_template, expected_type=type_hints["version_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_ring": key_ring,
            "name": name,
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
        if crypto_key_backend is not None:
            self._values["crypto_key_backend"] = crypto_key_backend
        if destroy_scheduled_duration is not None:
            self._values["destroy_scheduled_duration"] = destroy_scheduled_duration
        if id is not None:
            self._values["id"] = id
        if import_only is not None:
            self._values["import_only"] = import_only
        if key_access_justifications_policy is not None:
            self._values["key_access_justifications_policy"] = key_access_justifications_policy
        if labels is not None:
            self._values["labels"] = labels
        if purpose is not None:
            self._values["purpose"] = purpose
        if rotation_period is not None:
            self._values["rotation_period"] = rotation_period
        if skip_initial_version_creation is not None:
            self._values["skip_initial_version_creation"] = skip_initial_version_creation
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_template is not None:
            self._values["version_template"] = version_template

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
    def key_ring(self) -> builtins.str:
        '''The KeyRing that this key belongs to. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyRing}}''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#key_ring GoogleKmsCryptoKey#key_ring}
        '''
        result = self._values.get("key_ring")
        assert result is not None, "Required property 'key_ring' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for the CryptoKey.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#name GoogleKmsCryptoKey#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def crypto_key_backend(self) -> typing.Optional[builtins.str]:
        '''The resource name of the backend environment associated with all CryptoKeyVersions within this CryptoKey.

        The resource name is in the format "projects/* /locations/* /ekmConnections/*" and only applies to "EXTERNAL_VPC" keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#crypto_key_backend GoogleKmsCryptoKey#crypto_key_backend}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("crypto_key_backend")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destroy_scheduled_duration(self) -> typing.Optional[builtins.str]:
        '''The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED.

        If not specified at creation time, the default duration is 30 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#destroy_scheduled_duration GoogleKmsCryptoKey#destroy_scheduled_duration}
        '''
        result = self._values.get("destroy_scheduled_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#id GoogleKmsCryptoKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this key may contain imported versions only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#import_only GoogleKmsCryptoKey#import_only}
        '''
        result = self._values.get("import_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_access_justifications_policy(
        self,
    ) -> typing.Optional["GoogleKmsCryptoKeyKeyAccessJustificationsPolicy"]:
        '''key_access_justifications_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#key_access_justifications_policy GoogleKmsCryptoKey#key_access_justifications_policy}
        '''
        result = self._values.get("key_access_justifications_policy")
        return typing.cast(typing.Optional["GoogleKmsCryptoKeyKeyAccessJustificationsPolicy"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata to apply to this resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#labels GoogleKmsCryptoKey#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def purpose(self) -> typing.Optional[builtins.str]:
        '''The immutable purpose of this CryptoKey. See the `purpose reference <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyPurpose>`_ for possible inputs. Default value is "ENCRYPT_DECRYPT".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#purpose GoogleKmsCryptoKey#purpose}
        '''
        result = self._values.get("purpose")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_period(self) -> typing.Optional[builtins.str]:
        '''Every time this period passes, generate a new CryptoKeyVersion and set it as the primary.

        The first rotation will take place after the specified period. The rotation period has
        the format of a decimal number with up to 9 fractional digits, followed by the
        letter 's' (seconds). It must be greater than a day (ie, 86400).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#rotation_period GoogleKmsCryptoKey#rotation_period}
        '''
        result = self._values.get("rotation_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_initial_version_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the request will create a CryptoKey without any CryptoKeyVersions.

        You must use the 'google_kms_crypto_key_version' resource to create a new CryptoKeyVersion
        or 'google_kms_key_ring_import_job' resource to import the CryptoKeyVersion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#skip_initial_version_creation GoogleKmsCryptoKey#skip_initial_version_creation}
        '''
        result = self._values.get("skip_initial_version_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleKmsCryptoKeyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#timeouts GoogleKmsCryptoKey#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleKmsCryptoKeyTimeouts"], result)

    @builtins.property
    def version_template(self) -> typing.Optional["GoogleKmsCryptoKeyVersionTemplate"]:
        '''version_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#version_template GoogleKmsCryptoKey#version_template}
        '''
        result = self._values.get("version_template")
        return typing.cast(typing.Optional["GoogleKmsCryptoKeyVersionTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleKmsCryptoKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyKeyAccessJustificationsPolicy",
    jsii_struct_bases=[],
    name_mapping={"allowed_access_reasons": "allowedAccessReasons"},
)
class GoogleKmsCryptoKeyKeyAccessJustificationsPolicy:
    def __init__(
        self,
        *,
        allowed_access_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_access_reasons: The list of allowed reasons for access to this CryptoKey. Zero allowed access reasons means all encrypt, decrypt, and sign operations for this CryptoKey will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#allowed_access_reasons GoogleKmsCryptoKey#allowed_access_reasons}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2eb4dcc15d06713041548ea4f3c75e23a6b546d0538f51f2420d373e9abe86)
            check_type(argname="argument allowed_access_reasons", value=allowed_access_reasons, expected_type=type_hints["allowed_access_reasons"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_access_reasons is not None:
            self._values["allowed_access_reasons"] = allowed_access_reasons

    @builtins.property
    def allowed_access_reasons(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed reasons for access to this CryptoKey.

        Zero allowed
        access reasons means all encrypt, decrypt, and sign operations for
        this CryptoKey will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#allowed_access_reasons GoogleKmsCryptoKey#allowed_access_reasons}
        '''
        result = self._values.get("allowed_access_reasons")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleKmsCryptoKeyKeyAccessJustificationsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleKmsCryptoKeyKeyAccessJustificationsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyKeyAccessJustificationsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9b4f0c229b7af30472f0aaa186589483b6264db261b6019c7b015c5861d690d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAccessReasons")
    def reset_allowed_access_reasons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAccessReasons", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAccessReasonsInput")
    def allowed_access_reasons_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAccessReasonsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAccessReasons")
    def allowed_access_reasons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAccessReasons"))

    @allowed_access_reasons.setter
    def allowed_access_reasons(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9894c4334eb2f4b7fdb5c65e2e367bc48ee9d060f601e44522f8877fa1c0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAccessReasons", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleKmsCryptoKeyKeyAccessJustificationsPolicy]:
        return typing.cast(typing.Optional[GoogleKmsCryptoKeyKeyAccessJustificationsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleKmsCryptoKeyKeyAccessJustificationsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054a17da2ac75ff4354419d791ca9de83a70341afd22dd12976548543e97e34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyPrimary",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleKmsCryptoKeyPrimary:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleKmsCryptoKeyPrimary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleKmsCryptoKeyPrimaryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyPrimaryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__776797b49c6fb4099ae467ea86efa80c17be4d8ff189a93244025178cbca8b7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleKmsCryptoKeyPrimaryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bde89fe2f817058717ee4c4355ffc4601b81d327346082bf7008ba1008a0f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleKmsCryptoKeyPrimaryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c745559a885498f1b66ecd127d483c7d9487f02afa7d291406dbf326e4576772)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd3c4a327775e3905162f4ad661c15ff717f3b915bd46835c8d3fe836ec8bf52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8da65e1399c8a61d161a6dd962d9c2ad1f80bd2142238ecf8a84bf093596728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleKmsCryptoKeyPrimaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyPrimaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e125ce1f78de2e6898d4e9822a7e938782fb49273d50c5ebf0e0e53bce2b863d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleKmsCryptoKeyPrimary]:
        return typing.cast(typing.Optional[GoogleKmsCryptoKeyPrimary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleKmsCryptoKeyPrimary]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94185b5d8a1faccdd7c0594f27ea1d45207d7531dd09cec31d0acd69cb49e034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleKmsCryptoKeyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#create GoogleKmsCryptoKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#delete GoogleKmsCryptoKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#update GoogleKmsCryptoKey#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3db9319d6fbc46477b78b4a43ef0bbb789c1fed7b0515d6cce48941fd048bae)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#create GoogleKmsCryptoKey#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#delete GoogleKmsCryptoKey#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#update GoogleKmsCryptoKey#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleKmsCryptoKeyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleKmsCryptoKeyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39281685c1f9e4a18b192b477b7534b1edc5931c39109e33a868f0fd1bb9a93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__648abfd6681ab24b61452ad60bd1027a3d7b69d6783600e9b2d1d20ab3b37052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0266e62fbdabadf1dac5d6506a79063113260820b68ac096066e807a3e048c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d6d981610f6265287a81de597812cfde9cac1fd005a1f2c686ce6001fbdb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleKmsCryptoKeyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleKmsCryptoKeyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleKmsCryptoKeyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3652ecfb96863789e65800cc911d0681a80189a3d64d43e53059133507993f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyVersionTemplate",
    jsii_struct_bases=[],
    name_mapping={"algorithm": "algorithm", "protection_level": "protectionLevel"},
)
class GoogleKmsCryptoKeyVersionTemplate:
    def __init__(
        self,
        *,
        algorithm: builtins.str,
        protection_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm to use when creating a version based on this template. See the `algorithm reference <https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm>`_ for possible inputs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#algorithm GoogleKmsCryptoKey#algorithm}
        :param protection_level: The protection level to use when creating a version based on this template. Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#protection_level GoogleKmsCryptoKey#protection_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce114baf752c074a994aba4d77016c38cbb20959c35bbb52198b39d1630e74b)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument protection_level", value=protection_level, expected_type=type_hints["protection_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "algorithm": algorithm,
        }
        if protection_level is not None:
            self._values["protection_level"] = protection_level

    @builtins.property
    def algorithm(self) -> builtins.str:
        '''The algorithm to use when creating a version based on this template. See the `algorithm reference <https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm>`_ for possible inputs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#algorithm GoogleKmsCryptoKey#algorithm}
        '''
        result = self._values.get("algorithm")
        assert result is not None, "Required property 'algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protection_level(self) -> typing.Optional[builtins.str]:
        '''The protection level to use when creating a version based on this template.

        Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_kms_crypto_key#protection_level GoogleKmsCryptoKey#protection_level}
        '''
        result = self._values.get("protection_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleKmsCryptoKeyVersionTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleKmsCryptoKeyVersionTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleKmsCryptoKey.GoogleKmsCryptoKeyVersionTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e66da02880aa5b8f9d53492fa7b8336694c8029bab8e3a828749b7a418709bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProtectionLevel")
    def reset_protection_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectionLevel", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="protectionLevelInput")
    def protection_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectionLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3976aabc399e8d18be14fac46f3dd58a5769977d19fb9080c8368edda4c43947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectionLevel")
    def protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectionLevel"))

    @protection_level.setter
    def protection_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160c4af31ff665095af312752e4ecdf262809525b4cc58a34c90cc23606c9635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectionLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleKmsCryptoKeyVersionTemplate]:
        return typing.cast(typing.Optional[GoogleKmsCryptoKeyVersionTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleKmsCryptoKeyVersionTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f19eacc6ff6ebfa664a8fae02282308afeafc472bca9edbfbe8a1e12b1f776a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleKmsCryptoKey",
    "GoogleKmsCryptoKeyConfig",
    "GoogleKmsCryptoKeyKeyAccessJustificationsPolicy",
    "GoogleKmsCryptoKeyKeyAccessJustificationsPolicyOutputReference",
    "GoogleKmsCryptoKeyPrimary",
    "GoogleKmsCryptoKeyPrimaryList",
    "GoogleKmsCryptoKeyPrimaryOutputReference",
    "GoogleKmsCryptoKeyTimeouts",
    "GoogleKmsCryptoKeyTimeoutsOutputReference",
    "GoogleKmsCryptoKeyVersionTemplate",
    "GoogleKmsCryptoKeyVersionTemplateOutputReference",
]

publication.publish()

def _typecheckingstub__71293baedbcdf4e5e15bd41d6d230b947890fa753b31d9d934001a103587bccb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key_ring: builtins.str,
    name: builtins.str,
    crypto_key_backend: typing.Optional[builtins.str] = None,
    destroy_scheduled_duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_access_justifications_policy: typing.Optional[typing.Union[GoogleKmsCryptoKeyKeyAccessJustificationsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    purpose: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[builtins.str] = None,
    skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleKmsCryptoKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_template: typing.Optional[typing.Union[GoogleKmsCryptoKeyVersionTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aa9000975014e7a5d9f8fd243b9a4578a615a25a2a3fb7fee88bc1d074d606b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb898b24bc04d49783c892c5540ceec5b6ee8735c38b2b0163c7a7909ca7745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7434f791c070a33b04c10d05d6be6fd53ba2bf68e27007cc71bf6d5f9982b464(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917b34cd4362a5ec6f5a52e29c8924a87e9b19e05d43c516fd9a6b4d1ccd5b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06addf4319c0a2c88197eaeb7b28736f874db698a04daa66f0e3d2b051b5b00(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0dd172e00d38f90f4ffdb8b5f7a186a98efb715be73b4deafd3c8904d11222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abb00004a919b67843b5bffb27ccab0fa13af5499735cd3aee03fd3ed1d812f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99df6f766a2b3a0639d428498f0cbf11afbd6771a723482d36e81c3ed95efe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d7f9388c41f89f351ca796d25549c01477278d69f9509437be00df8eec938a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dafe148d6bd748902bc2ff268f095cc9a9f591d7debfdf0c8f0fd366c432128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbae328991e47cdb99f8c99ed16a9cd6f65412d1305c55167de440219c11ca0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaa35b264143150b895c4022296aa8e839aa7981576548516ba24d0943a0d82(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_ring: builtins.str,
    name: builtins.str,
    crypto_key_backend: typing.Optional[builtins.str] = None,
    destroy_scheduled_duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_access_justifications_policy: typing.Optional[typing.Union[GoogleKmsCryptoKeyKeyAccessJustificationsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    purpose: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[builtins.str] = None,
    skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleKmsCryptoKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_template: typing.Optional[typing.Union[GoogleKmsCryptoKeyVersionTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2eb4dcc15d06713041548ea4f3c75e23a6b546d0538f51f2420d373e9abe86(
    *,
    allowed_access_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b4f0c229b7af30472f0aaa186589483b6264db261b6019c7b015c5861d690d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9894c4334eb2f4b7fdb5c65e2e367bc48ee9d060f601e44522f8877fa1c0c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054a17da2ac75ff4354419d791ca9de83a70341afd22dd12976548543e97e34e(
    value: typing.Optional[GoogleKmsCryptoKeyKeyAccessJustificationsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776797b49c6fb4099ae467ea86efa80c17be4d8ff189a93244025178cbca8b7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bde89fe2f817058717ee4c4355ffc4601b81d327346082bf7008ba1008a0f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c745559a885498f1b66ecd127d483c7d9487f02afa7d291406dbf326e4576772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3c4a327775e3905162f4ad661c15ff717f3b915bd46835c8d3fe836ec8bf52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8da65e1399c8a61d161a6dd962d9c2ad1f80bd2142238ecf8a84bf093596728(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e125ce1f78de2e6898d4e9822a7e938782fb49273d50c5ebf0e0e53bce2b863d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94185b5d8a1faccdd7c0594f27ea1d45207d7531dd09cec31d0acd69cb49e034(
    value: typing.Optional[GoogleKmsCryptoKeyPrimary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3db9319d6fbc46477b78b4a43ef0bbb789c1fed7b0515d6cce48941fd048bae(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39281685c1f9e4a18b192b477b7534b1edc5931c39109e33a868f0fd1bb9a93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648abfd6681ab24b61452ad60bd1027a3d7b69d6783600e9b2d1d20ab3b37052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0266e62fbdabadf1dac5d6506a79063113260820b68ac096066e807a3e048c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d6d981610f6265287a81de597812cfde9cac1fd005a1f2c686ce6001fbdb6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3652ecfb96863789e65800cc911d0681a80189a3d64d43e53059133507993f67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleKmsCryptoKeyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce114baf752c074a994aba4d77016c38cbb20959c35bbb52198b39d1630e74b(
    *,
    algorithm: builtins.str,
    protection_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e66da02880aa5b8f9d53492fa7b8336694c8029bab8e3a828749b7a418709bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3976aabc399e8d18be14fac46f3dd58a5769977d19fb9080c8368edda4c43947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160c4af31ff665095af312752e4ecdf262809525b4cc58a34c90cc23606c9635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f19eacc6ff6ebfa664a8fae02282308afeafc472bca9edbfbe8a1e12b1f776a(
    value: typing.Optional[GoogleKmsCryptoKeyVersionTemplate],
) -> None:
    """Type checking stubs"""
    pass
