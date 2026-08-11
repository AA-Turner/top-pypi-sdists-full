from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from ..._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk.interfaces as _interfaces_8ca7e747
    import constructs as _constructs_77d1e7e8
else:

    _constructs_77d1e7e8 = _LazyImport("constructs")
    _interfaces_8ca7e747 = _LazyImport("aws_cdk.interfaces")


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_transcribe.IMedicalTranscriptionJobRef"
)
class IMedicalTranscriptionJobRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a MedicalTranscriptionJob.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="medicalTranscriptionJobRef")
    def medical_transcription_job_ref(self) -> "MedicalTranscriptionJobReference":
        '''(experimental) A reference to a MedicalTranscriptionJob resource.

        :stability: experimental
        '''
        ...


class _IMedicalTranscriptionJobRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a MedicalTranscriptionJob.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_transcribe.IMedicalTranscriptionJobRef"

    @builtins.property
    @jsii.member(jsii_name="medicalTranscriptionJobRef")
    def medical_transcription_job_ref(self) -> "MedicalTranscriptionJobReference":
        '''(experimental) A reference to a MedicalTranscriptionJob resource.

        :stability: experimental
        '''
        return typing.cast("MedicalTranscriptionJobReference", jsii.get(self, "medicalTranscriptionJobRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMedicalTranscriptionJobRef).__jsii_proxy_class__ = lambda : _IMedicalTranscriptionJobRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_transcribe.IVocabularyFilterRef")
class IVocabularyFilterRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a VocabularyFilter.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterRef")
    def vocabulary_filter_ref(self) -> "VocabularyFilterReference":
        '''(experimental) A reference to a VocabularyFilter resource.

        :stability: experimental
        '''
        ...


class _IVocabularyFilterRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a VocabularyFilter.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_transcribe.IVocabularyFilterRef"

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterRef")
    def vocabulary_filter_ref(self) -> "VocabularyFilterReference":
        '''(experimental) A reference to a VocabularyFilter resource.

        :stability: experimental
        '''
        return typing.cast("VocabularyFilterReference", jsii.get(self, "vocabularyFilterRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVocabularyFilterRef).__jsii_proxy_class__ = lambda : _IVocabularyFilterRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_transcribe.MedicalTranscriptionJobReference",
    jsii_struct_bases=[],
    name_mapping={"medical_transcription_job_arn": "medicalTranscriptionJobArn"},
)
class MedicalTranscriptionJobReference:
    def __init__(self, *, medical_transcription_job_arn: builtins.str) -> None:
        '''A reference to a MedicalTranscriptionJob resource.

        :param medical_transcription_job_arn: The Arn of the MedicalTranscriptionJob resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_transcribe as interfaces_transcribe
            
            medical_transcription_job_reference = interfaces_transcribe.MedicalTranscriptionJobReference(
                medical_transcription_job_arn="medicalTranscriptionJobArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7359cd72e7d7deba00da2a34076f98861c44809c455c938b43585099515bd209)
            check_type(argname="argument medical_transcription_job_arn", value=medical_transcription_job_arn, expected_type=type_hints["medical_transcription_job_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "medical_transcription_job_arn": medical_transcription_job_arn,
        }

    @builtins.property
    def medical_transcription_job_arn(self) -> builtins.str:
        '''The Arn of the MedicalTranscriptionJob resource.'''
        result = self._values.get("medical_transcription_job_arn")
        assert result is not None, "Required property 'medical_transcription_job_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MedicalTranscriptionJobReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_transcribe.VocabularyFilterReference",
    jsii_struct_bases=[],
    name_mapping={"vocabulary_filter_arn": "vocabularyFilterArn"},
)
class VocabularyFilterReference:
    def __init__(self, *, vocabulary_filter_arn: builtins.str) -> None:
        '''A reference to a VocabularyFilter resource.

        :param vocabulary_filter_arn: The Arn of the VocabularyFilter resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_transcribe as interfaces_transcribe
            
            vocabulary_filter_reference = interfaces_transcribe.VocabularyFilterReference(
                vocabulary_filter_arn="vocabularyFilterArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__582efec5c1b8cc6f8fc29d3a057121fb149398b5d6c637b114509b7b274c6ae9)
            check_type(argname="argument vocabulary_filter_arn", value=vocabulary_filter_arn, expected_type=type_hints["vocabulary_filter_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vocabulary_filter_arn": vocabulary_filter_arn,
        }

    @builtins.property
    def vocabulary_filter_arn(self) -> builtins.str:
        '''The Arn of the VocabularyFilter resource.'''
        result = self._values.get("vocabulary_filter_arn")
        assert result is not None, "Required property 'vocabulary_filter_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VocabularyFilterReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IMedicalTranscriptionJobRef",
    "IVocabularyFilterRef",
    "MedicalTranscriptionJobReference",
    "VocabularyFilterReference",
]

publication.publish()

def _typecheckingstub__7359cd72e7d7deba00da2a34076f98861c44809c455c938b43585099515bd209(
    *,
    medical_transcription_job_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582efec5c1b8cc6f8fc29d3a057121fb149398b5d6c637b114509b7b274c6ae9(
    *,
    vocabulary_filter_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IMedicalTranscriptionJobRef, IVocabularyFilterRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
