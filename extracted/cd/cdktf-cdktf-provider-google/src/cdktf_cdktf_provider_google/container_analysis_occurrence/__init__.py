r'''
# `google_container_analysis_occurrence`

Refer to the Terraform Registry for docs: [`google_container_analysis_occurrence`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence).
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


class ContainerAnalysisOccurrence(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrence",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence google_container_analysis_occurrence}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        attestation: typing.Union["ContainerAnalysisOccurrenceAttestation", typing.Dict[builtins.str, typing.Any]],
        note_name: builtins.str,
        resource_uri: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remediation: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAnalysisOccurrenceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence google_container_analysis_occurrence} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param attestation: attestation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#attestation ContainerAnalysisOccurrence#attestation}
        :param note_name: The analysis note associated with this occurrence, in the form of projects/[PROJECT]/notes/[NOTE_ID]. This field can be used as a filter in list requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#note_name ContainerAnalysisOccurrence#note_name}
        :param resource_uri: Required. Immutable. A URI that represents the resource for which the occurrence applies. For example, https://gcr.io/project/image@sha256:123abc for a Docker image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#resource_uri ContainerAnalysisOccurrence#resource_uri}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#id ContainerAnalysisOccurrence#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#project ContainerAnalysisOccurrence#project}.
        :param remediation: A description of actions that can be taken to remedy the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#remediation ContainerAnalysisOccurrence#remediation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#timeouts ContainerAnalysisOccurrence#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ae24827bf4ea0778f4201dd67ab25e1e5751dab424f4ac8c474f4954449aa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAnalysisOccurrenceConfig(
            attestation=attestation,
            note_name=note_name,
            resource_uri=resource_uri,
            id=id,
            project=project,
            remediation=remediation,
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
        '''Generates CDKTF code for importing a ContainerAnalysisOccurrence resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAnalysisOccurrence to import.
        :param import_from_id: The id of the existing ContainerAnalysisOccurrence that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAnalysisOccurrence to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925623735809da7bde58a8a2c67d3510b2c619f266e6ed2fa7ba53d7dd2c1a4c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttestation")
    def put_attestation(
        self,
        *,
        serialized_payload: builtins.str,
        signatures: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAnalysisOccurrenceAttestationSignatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param serialized_payload: The serialized payload that is verified by one or more signatures. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#serialized_payload ContainerAnalysisOccurrence#serialized_payload}
        :param signatures: signatures block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#signatures ContainerAnalysisOccurrence#signatures}
        '''
        value = ContainerAnalysisOccurrenceAttestation(
            serialized_payload=serialized_payload, signatures=signatures
        )

        return typing.cast(None, jsii.invoke(self, "putAttestation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#create ContainerAnalysisOccurrence#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#delete ContainerAnalysisOccurrence#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#update ContainerAnalysisOccurrence#update}.
        '''
        value = ContainerAnalysisOccurrenceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRemediation")
    def reset_remediation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemediation", []))

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
    @jsii.member(jsii_name="attestation")
    def attestation(self) -> "ContainerAnalysisOccurrenceAttestationOutputReference":
        return typing.cast("ContainerAnalysisOccurrenceAttestationOutputReference", jsii.get(self, "attestation"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAnalysisOccurrenceTimeoutsOutputReference":
        return typing.cast("ContainerAnalysisOccurrenceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="attestationInput")
    def attestation_input(
        self,
    ) -> typing.Optional["ContainerAnalysisOccurrenceAttestation"]:
        return typing.cast(typing.Optional["ContainerAnalysisOccurrenceAttestation"], jsii.get(self, "attestationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="noteNameInput")
    def note_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noteNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="remediationInput")
    def remediation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remediationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceUriInput")
    def resource_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAnalysisOccurrenceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAnalysisOccurrenceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17e52d4ce0a0f82aed8a62dae5e274d2ef84ae22b95f4f831a9ec4a93074d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noteName")
    def note_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noteName"))

    @note_name.setter
    def note_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f3e1c04fe9c5c3ea08e8ce0810c7c62da656dc3f70a3a2730ad2655dee2e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noteName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa1ff62a207352a89238c00def5274431bb066837f43b8ef919f6940a21d601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remediation")
    def remediation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remediation"))

    @remediation.setter
    def remediation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ece014d8ed4cabd9dbcfe3c4382d43a43143e6952f9c00b7c91db19924de7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remediation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceUri")
    def resource_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceUri"))

    @resource_uri.setter
    def resource_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350cfc641798eca50b7cb9540dde9dfc342d56d6dbe6e7d6284f19b77009a208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceUri", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceAttestation",
    jsii_struct_bases=[],
    name_mapping={
        "serialized_payload": "serializedPayload",
        "signatures": "signatures",
    },
)
class ContainerAnalysisOccurrenceAttestation:
    def __init__(
        self,
        *,
        serialized_payload: builtins.str,
        signatures: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAnalysisOccurrenceAttestationSignatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param serialized_payload: The serialized payload that is verified by one or more signatures. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#serialized_payload ContainerAnalysisOccurrence#serialized_payload}
        :param signatures: signatures block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#signatures ContainerAnalysisOccurrence#signatures}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ad7a54237818156b24b851c29fc5ad0507b98af68002361d1569b624838f4e)
            check_type(argname="argument serialized_payload", value=serialized_payload, expected_type=type_hints["serialized_payload"])
            check_type(argname="argument signatures", value=signatures, expected_type=type_hints["signatures"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "serialized_payload": serialized_payload,
            "signatures": signatures,
        }

    @builtins.property
    def serialized_payload(self) -> builtins.str:
        '''The serialized payload that is verified by one or more signatures. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#serialized_payload ContainerAnalysisOccurrence#serialized_payload}
        '''
        result = self._values.get("serialized_payload")
        assert result is not None, "Required property 'serialized_payload' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signatures(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisOccurrenceAttestationSignatures"]]:
        '''signatures block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#signatures ContainerAnalysisOccurrence#signatures}
        '''
        result = self._values.get("signatures")
        assert result is not None, "Required property 'signatures' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisOccurrenceAttestationSignatures"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisOccurrenceAttestation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAnalysisOccurrenceAttestationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceAttestationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97c2bec96b9205d056a45113fe6d820d99b76f7b7a3031b804f5be708d3df7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSignatures")
    def put_signatures(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAnalysisOccurrenceAttestationSignatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848c7f6c2483b60ce1305bccdbfe7fc71e8c84de2e7979a68965bd42eed99dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSignatures", [value]))

    @builtins.property
    @jsii.member(jsii_name="signatures")
    def signatures(self) -> "ContainerAnalysisOccurrenceAttestationSignaturesList":
        return typing.cast("ContainerAnalysisOccurrenceAttestationSignaturesList", jsii.get(self, "signatures"))

    @builtins.property
    @jsii.member(jsii_name="serializedPayloadInput")
    def serialized_payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serializedPayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="signaturesInput")
    def signatures_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisOccurrenceAttestationSignatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisOccurrenceAttestationSignatures"]]], jsii.get(self, "signaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="serializedPayload")
    def serialized_payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serializedPayload"))

    @serialized_payload.setter
    def serialized_payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3f25b82b8c0fc412526da4304080ff5d4e0ba51442da1dc4edc6499ecd9ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serializedPayload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAnalysisOccurrenceAttestation]:
        return typing.cast(typing.Optional[ContainerAnalysisOccurrenceAttestation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAnalysisOccurrenceAttestation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1dc6b14ec466623003d9f964ae5214c7783a68e9b356e0bee19c0820f6e829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceAttestationSignatures",
    jsii_struct_bases=[],
    name_mapping={"public_key_id": "publicKeyId", "signature": "signature"},
)
class ContainerAnalysisOccurrenceAttestationSignatures:
    def __init__(
        self,
        *,
        public_key_id: builtins.str,
        signature: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_key_id: The identifier for the public key that verifies this signature. MUST be an RFC3986 conformant URI. * When possible, the key id should be an immutable reference, such as a cryptographic digest. Examples of valid values: - OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr for more details on this scheme. - 'openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA' - RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization): - "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#public_key_id ContainerAnalysisOccurrence#public_key_id}
        :param signature: The content of the signature, an opaque bytestring. The payload that this signature verifies MUST be unambiguously provided with the Signature during verification. A wrapper message might provide the payload explicitly. Alternatively, a message might have a canonical serialization that can always be unambiguously computed to derive the payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#signature ContainerAnalysisOccurrence#signature}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fae1ed2ac4517c8e78a35e5fa438efc9c1f4a54a3f7dee58582f3035791ebbd)
            check_type(argname="argument public_key_id", value=public_key_id, expected_type=type_hints["public_key_id"])
            check_type(argname="argument signature", value=signature, expected_type=type_hints["signature"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key_id": public_key_id,
        }
        if signature is not None:
            self._values["signature"] = signature

    @builtins.property
    def public_key_id(self) -> builtins.str:
        '''The identifier for the public key that verifies this signature.

        MUST be an RFC3986 conformant
        URI. * When possible, the key id should be an
        immutable reference, such as a cryptographic digest.
        Examples of valid values:

        - OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
          for more details on this scheme.

          - 'openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA'

        - RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization):

          - "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#public_key_id ContainerAnalysisOccurrence#public_key_id}
        '''
        result = self._values.get("public_key_id")
        assert result is not None, "Required property 'public_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signature(self) -> typing.Optional[builtins.str]:
        '''The content of the signature, an opaque bytestring.

        The payload that this signature verifies MUST be
        unambiguously provided with the Signature during
        verification. A wrapper message might provide the
        payload explicitly. Alternatively, a message might
        have a canonical serialization that can always be
        unambiguously computed to derive the payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#signature ContainerAnalysisOccurrence#signature}
        '''
        result = self._values.get("signature")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisOccurrenceAttestationSignatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAnalysisOccurrenceAttestationSignaturesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceAttestationSignaturesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__142ced14f40eb3012b1b068ed4b7a078862ceb0987f989490927f63325a333b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAnalysisOccurrenceAttestationSignaturesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf11fb53c9134ec7e9de92b83530a890ee38570b09b8f826395bbf0c82d01e8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAnalysisOccurrenceAttestationSignaturesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68ae14b4aac564b11890d14576352441086651db6f28c14e12f4bb23cafb3c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d488873492048c045f68bf78f788494cde274e358ba7657dcec9c08d6024436a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24adc5754b2ece2e959a2d03d710c4b1f7a1a46d82177afcf27139670bdbd192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisOccurrenceAttestationSignatures]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisOccurrenceAttestationSignatures]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisOccurrenceAttestationSignatures]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2d675b39e14e691e3e3e054fdfa6bbc34e20ee396919c8d554cd8af33f6e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAnalysisOccurrenceAttestationSignaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceAttestationSignaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17bf956e6c5932e997ae6cae196178fa27d4fef31e0c5313b75a1ecc79c4f3a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSignature")
    def reset_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignature", []))

    @builtins.property
    @jsii.member(jsii_name="publicKeyIdInput")
    def public_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureInput")
    def signature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyId")
    def public_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKeyId"))

    @public_key_id.setter
    def public_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e275fb2ef6f693dae7d66c2be9cf11ad064cb9f33d38af01415e70a6103321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signature")
    def signature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signature"))

    @signature.setter
    def signature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e17f02b91b5eb91395ea3c3db7990b7f3f4165a80f20b8ec14d770e0d78bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceAttestationSignatures]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceAttestationSignatures]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceAttestationSignatures]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a28bd759b8408e68b11796c78227846238b259c9bad0b1c4896336f5d4d3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "attestation": "attestation",
        "note_name": "noteName",
        "resource_uri": "resourceUri",
        "id": "id",
        "project": "project",
        "remediation": "remediation",
        "timeouts": "timeouts",
    },
)
class ContainerAnalysisOccurrenceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        attestation: typing.Union[ContainerAnalysisOccurrenceAttestation, typing.Dict[builtins.str, typing.Any]],
        note_name: builtins.str,
        resource_uri: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remediation: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAnalysisOccurrenceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param attestation: attestation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#attestation ContainerAnalysisOccurrence#attestation}
        :param note_name: The analysis note associated with this occurrence, in the form of projects/[PROJECT]/notes/[NOTE_ID]. This field can be used as a filter in list requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#note_name ContainerAnalysisOccurrence#note_name}
        :param resource_uri: Required. Immutable. A URI that represents the resource for which the occurrence applies. For example, https://gcr.io/project/image@sha256:123abc for a Docker image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#resource_uri ContainerAnalysisOccurrence#resource_uri}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#id ContainerAnalysisOccurrence#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#project ContainerAnalysisOccurrence#project}.
        :param remediation: A description of actions that can be taken to remedy the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#remediation ContainerAnalysisOccurrence#remediation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#timeouts ContainerAnalysisOccurrence#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(attestation, dict):
            attestation = ContainerAnalysisOccurrenceAttestation(**attestation)
        if isinstance(timeouts, dict):
            timeouts = ContainerAnalysisOccurrenceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00f7c8ef4474335d85c0ac36e092b4caf44e1b46eb4cfda3ac23d5b24dccfe3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument attestation", value=attestation, expected_type=type_hints["attestation"])
            check_type(argname="argument note_name", value=note_name, expected_type=type_hints["note_name"])
            check_type(argname="argument resource_uri", value=resource_uri, expected_type=type_hints["resource_uri"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument remediation", value=remediation, expected_type=type_hints["remediation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attestation": attestation,
            "note_name": note_name,
            "resource_uri": resource_uri,
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
        if project is not None:
            self._values["project"] = project
        if remediation is not None:
            self._values["remediation"] = remediation
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
    def attestation(self) -> ContainerAnalysisOccurrenceAttestation:
        '''attestation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#attestation ContainerAnalysisOccurrence#attestation}
        '''
        result = self._values.get("attestation")
        assert result is not None, "Required property 'attestation' is missing"
        return typing.cast(ContainerAnalysisOccurrenceAttestation, result)

    @builtins.property
    def note_name(self) -> builtins.str:
        '''The analysis note associated with this occurrence, in the form of projects/[PROJECT]/notes/[NOTE_ID].

        This field can be used as a
        filter in list requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#note_name ContainerAnalysisOccurrence#note_name}
        '''
        result = self._values.get("note_name")
        assert result is not None, "Required property 'note_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_uri(self) -> builtins.str:
        '''Required. Immutable. A URI that represents the resource for which the occurrence applies. For example, https://gcr.io/project/image@sha256:123abc for a Docker image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#resource_uri ContainerAnalysisOccurrence#resource_uri}
        '''
        result = self._values.get("resource_uri")
        assert result is not None, "Required property 'resource_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#id ContainerAnalysisOccurrence#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#project ContainerAnalysisOccurrence#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remediation(self) -> typing.Optional[builtins.str]:
        '''A description of actions that can be taken to remedy the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#remediation ContainerAnalysisOccurrence#remediation}
        '''
        result = self._values.get("remediation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAnalysisOccurrenceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#timeouts ContainerAnalysisOccurrence#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAnalysisOccurrenceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisOccurrenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAnalysisOccurrenceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#create ContainerAnalysisOccurrence#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#delete ContainerAnalysisOccurrence#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#update ContainerAnalysisOccurrence#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a9f0b8beadc2acae6893017e32e6965c599ff90406c2d29f77aa0d6c6fd565)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#create ContainerAnalysisOccurrence#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#delete ContainerAnalysisOccurrence#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_occurrence#update ContainerAnalysisOccurrence#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisOccurrenceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAnalysisOccurrenceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisOccurrence.ContainerAnalysisOccurrenceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__131546da67a9593263fb81635a42576e84e00854ca81a290a5f9c33204e9e913)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e64ba90c50018f3ba66298065ba5dc03f62132262427e33b1cbb83636d8e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce579cd788ebd7bc09d43447e89d95198c5f7dc1645fc93fbfcfc5d6397c772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45c2bbfb21eb79ceadd83ad6ec1b4b8f567f49175fa5dbe11b47a079b5a67f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e33d96a91fd33a19a686356fa7fe404100944191ede4cf276e34e948c563ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAnalysisOccurrence",
    "ContainerAnalysisOccurrenceAttestation",
    "ContainerAnalysisOccurrenceAttestationOutputReference",
    "ContainerAnalysisOccurrenceAttestationSignatures",
    "ContainerAnalysisOccurrenceAttestationSignaturesList",
    "ContainerAnalysisOccurrenceAttestationSignaturesOutputReference",
    "ContainerAnalysisOccurrenceConfig",
    "ContainerAnalysisOccurrenceTimeouts",
    "ContainerAnalysisOccurrenceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__89ae24827bf4ea0778f4201dd67ab25e1e5751dab424f4ac8c474f4954449aa1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    attestation: typing.Union[ContainerAnalysisOccurrenceAttestation, typing.Dict[builtins.str, typing.Any]],
    note_name: builtins.str,
    resource_uri: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remediation: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAnalysisOccurrenceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__925623735809da7bde58a8a2c67d3510b2c619f266e6ed2fa7ba53d7dd2c1a4c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17e52d4ce0a0f82aed8a62dae5e274d2ef84ae22b95f4f831a9ec4a93074d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f3e1c04fe9c5c3ea08e8ce0810c7c62da656dc3f70a3a2730ad2655dee2e16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa1ff62a207352a89238c00def5274431bb066837f43b8ef919f6940a21d601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ece014d8ed4cabd9dbcfe3c4382d43a43143e6952f9c00b7c91db19924de7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350cfc641798eca50b7cb9540dde9dfc342d56d6dbe6e7d6284f19b77009a208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ad7a54237818156b24b851c29fc5ad0507b98af68002361d1569b624838f4e(
    *,
    serialized_payload: builtins.str,
    signatures: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAnalysisOccurrenceAttestationSignatures, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97c2bec96b9205d056a45113fe6d820d99b76f7b7a3031b804f5be708d3df7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848c7f6c2483b60ce1305bccdbfe7fc71e8c84de2e7979a68965bd42eed99dfd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAnalysisOccurrenceAttestationSignatures, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3f25b82b8c0fc412526da4304080ff5d4e0ba51442da1dc4edc6499ecd9ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1dc6b14ec466623003d9f964ae5214c7783a68e9b356e0bee19c0820f6e829(
    value: typing.Optional[ContainerAnalysisOccurrenceAttestation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fae1ed2ac4517c8e78a35e5fa438efc9c1f4a54a3f7dee58582f3035791ebbd(
    *,
    public_key_id: builtins.str,
    signature: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142ced14f40eb3012b1b068ed4b7a078862ceb0987f989490927f63325a333b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf11fb53c9134ec7e9de92b83530a890ee38570b09b8f826395bbf0c82d01e8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68ae14b4aac564b11890d14576352441086651db6f28c14e12f4bb23cafb3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d488873492048c045f68bf78f788494cde274e358ba7657dcec9c08d6024436a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24adc5754b2ece2e959a2d03d710c4b1f7a1a46d82177afcf27139670bdbd192(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2d675b39e14e691e3e3e054fdfa6bbc34e20ee396919c8d554cd8af33f6e13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisOccurrenceAttestationSignatures]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bf956e6c5932e997ae6cae196178fa27d4fef31e0c5313b75a1ecc79c4f3a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e275fb2ef6f693dae7d66c2be9cf11ad064cb9f33d38af01415e70a6103321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e17f02b91b5eb91395ea3c3db7990b7f3f4165a80f20b8ec14d770e0d78bbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a28bd759b8408e68b11796c78227846238b259c9bad0b1c4896336f5d4d3a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceAttestationSignatures]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00f7c8ef4474335d85c0ac36e092b4caf44e1b46eb4cfda3ac23d5b24dccfe3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    attestation: typing.Union[ContainerAnalysisOccurrenceAttestation, typing.Dict[builtins.str, typing.Any]],
    note_name: builtins.str,
    resource_uri: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remediation: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAnalysisOccurrenceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a9f0b8beadc2acae6893017e32e6965c599ff90406c2d29f77aa0d6c6fd565(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131546da67a9593263fb81635a42576e84e00854ca81a290a5f9c33204e9e913(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e64ba90c50018f3ba66298065ba5dc03f62132262427e33b1cbb83636d8e11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce579cd788ebd7bc09d43447e89d95198c5f7dc1645fc93fbfcfc5d6397c772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45c2bbfb21eb79ceadd83ad6ec1b4b8f567f49175fa5dbe11b47a079b5a67f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e33d96a91fd33a19a686356fa7fe404100944191ede4cf276e34e948c563ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisOccurrenceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
