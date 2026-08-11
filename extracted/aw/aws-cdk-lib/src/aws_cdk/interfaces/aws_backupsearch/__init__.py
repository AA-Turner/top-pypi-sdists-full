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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_backupsearch.ISearchJobRef")
class ISearchJobRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a SearchJob.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="searchJobRef")
    def search_job_ref(self) -> "SearchJobReference":
        '''(experimental) A reference to a SearchJob resource.

        :stability: experimental
        '''
        ...


class _ISearchJobRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a SearchJob.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_backupsearch.ISearchJobRef"

    @builtins.property
    @jsii.member(jsii_name="searchJobRef")
    def search_job_ref(self) -> "SearchJobReference":
        '''(experimental) A reference to a SearchJob resource.

        :stability: experimental
        '''
        return typing.cast("SearchJobReference", jsii.get(self, "searchJobRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISearchJobRef).__jsii_proxy_class__ = lambda : _ISearchJobRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_backupsearch.SearchJobReference",
    jsii_struct_bases=[],
    name_mapping={"search_job_arn": "searchJobArn"},
)
class SearchJobReference:
    def __init__(self, *, search_job_arn: builtins.str) -> None:
        '''A reference to a SearchJob resource.

        :param search_job_arn: The SearchJobArn of the SearchJob resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_backupsearch as interfaces_backupsearch
            
            search_job_reference = interfaces_backupsearch.SearchJobReference(
                search_job_arn="searchJobArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__319569b7173aa6227e7b3d846c082c835590528b49a1e946edde766c6d0e91e4)
            check_type(argname="argument search_job_arn", value=search_job_arn, expected_type=type_hints["search_job_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "search_job_arn": search_job_arn,
        }

    @builtins.property
    def search_job_arn(self) -> builtins.str:
        '''The SearchJobArn of the SearchJob resource.'''
        result = self._values.get("search_job_arn")
        assert result is not None, "Required property 'search_job_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SearchJobReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ISearchJobRef",
    "SearchJobReference",
]

publication.publish()

def _typecheckingstub__319569b7173aa6227e7b3d846c082c835590528b49a1e946edde766c6d0e91e4(
    *,
    search_job_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ISearchJobRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
