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
    "IVocabularyFilterRef",
    "VocabularyFilterReference",
]

publication.publish()

def _typecheckingstub__582efec5c1b8cc6f8fc29d3a057121fb149398b5d6c637b114509b7b274c6ae9(
    *,
    vocabulary_filter_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IVocabularyFilterRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
