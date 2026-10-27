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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_polly.ILexiconRef")
class ILexiconRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Lexicon.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="lexiconRef")
    def lexicon_ref(self) -> "LexiconReference":
        '''(experimental) A reference to a Lexicon resource.

        :stability: experimental
        '''
        ...


class _ILexiconRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Lexicon.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_polly.ILexiconRef"

    @builtins.property
    @jsii.member(jsii_name="lexiconRef")
    def lexicon_ref(self) -> "LexiconReference":
        '''(experimental) A reference to a Lexicon resource.

        :stability: experimental
        '''
        return typing.cast("LexiconReference", jsii.get(self, "lexiconRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILexiconRef).__jsii_proxy_class__ = lambda : _ILexiconRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_polly.LexiconReference",
    jsii_struct_bases=[],
    name_mapping={"lexicon_arn": "lexiconArn"},
)
class LexiconReference:
    def __init__(self, *, lexicon_arn: builtins.str) -> None:
        '''A reference to a Lexicon resource.

        :param lexicon_arn: The Arn of the Lexicon resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_polly as interfaces_polly
            
            lexicon_reference = interfaces_polly.LexiconReference(
                lexicon_arn="lexiconArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7824e8adaa6cce9de08e8a488af9b7ecc23a335a03ffaa5b7ee1f1079ab4903)
            check_type(argname="argument lexicon_arn", value=lexicon_arn, expected_type=type_hints["lexicon_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lexicon_arn": lexicon_arn,
        }

    @builtins.property
    def lexicon_arn(self) -> builtins.str:
        '''The Arn of the Lexicon resource.'''
        result = self._values.get("lexicon_arn")
        assert result is not None, "Required property 'lexicon_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LexiconReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ILexiconRef",
    "LexiconReference",
]

publication.publish()

def _typecheckingstub__a7824e8adaa6cce9de08e8a488af9b7ecc23a335a03ffaa5b7ee1f1079ab4903(
    *,
    lexicon_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ILexiconRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
