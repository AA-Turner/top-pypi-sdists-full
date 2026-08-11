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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_wellarchitected.ILensRef")
class ILensRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Lens.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="lensRef")
    def lens_ref(self) -> "LensReference":
        '''(experimental) A reference to a Lens resource.

        :stability: experimental
        '''
        ...


class _ILensRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Lens.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_wellarchitected.ILensRef"

    @builtins.property
    @jsii.member(jsii_name="lensRef")
    def lens_ref(self) -> "LensReference":
        '''(experimental) A reference to a Lens resource.

        :stability: experimental
        '''
        return typing.cast("LensReference", jsii.get(self, "lensRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILensRef).__jsii_proxy_class__ = lambda : _ILensRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_wellarchitected.IProfileRef")
class IProfileRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Profile.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="profileRef")
    def profile_ref(self) -> "ProfileReference":
        '''(experimental) A reference to a Profile resource.

        :stability: experimental
        '''
        ...


class _IProfileRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Profile.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_wellarchitected.IProfileRef"

    @builtins.property
    @jsii.member(jsii_name="profileRef")
    def profile_ref(self) -> "ProfileReference":
        '''(experimental) A reference to a Profile resource.

        :stability: experimental
        '''
        return typing.cast("ProfileReference", jsii.get(self, "profileRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProfileRef).__jsii_proxy_class__ = lambda : _IProfileRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_wellarchitected.IReviewTemplateRef"
)
class IReviewTemplateRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ReviewTemplate.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="reviewTemplateRef")
    def review_template_ref(self) -> "ReviewTemplateReference":
        '''(experimental) A reference to a ReviewTemplate resource.

        :stability: experimental
        '''
        ...


class _IReviewTemplateRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ReviewTemplate.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_wellarchitected.IReviewTemplateRef"

    @builtins.property
    @jsii.member(jsii_name="reviewTemplateRef")
    def review_template_ref(self) -> "ReviewTemplateReference":
        '''(experimental) A reference to a ReviewTemplate resource.

        :stability: experimental
        '''
        return typing.cast("ReviewTemplateReference", jsii.get(self, "reviewTemplateRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReviewTemplateRef).__jsii_proxy_class__ = lambda : _IReviewTemplateRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_wellarchitected.LensReference",
    jsii_struct_bases=[],
    name_mapping={"lens_arn": "lensArn"},
)
class LensReference:
    def __init__(self, *, lens_arn: builtins.str) -> None:
        '''A reference to a Lens resource.

        :param lens_arn: The LensArn of the Lens resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_wellarchitected as interfaces_wellarchitected
            
            lens_reference = interfaces_wellarchitected.LensReference(
                lens_arn="lensArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f32344e8e195ba084ce4fcf47286bb12830dd7f6eb5a3d62943b345edff1b52f)
            check_type(argname="argument lens_arn", value=lens_arn, expected_type=type_hints["lens_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lens_arn": lens_arn,
        }

    @builtins.property
    def lens_arn(self) -> builtins.str:
        '''The LensArn of the Lens resource.'''
        result = self._values.get("lens_arn")
        assert result is not None, "Required property 'lens_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LensReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_wellarchitected.ProfileReference",
    jsii_struct_bases=[],
    name_mapping={"profile_arn": "profileArn"},
)
class ProfileReference:
    def __init__(self, *, profile_arn: builtins.str) -> None:
        '''A reference to a Profile resource.

        :param profile_arn: The ProfileArn of the Profile resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_wellarchitected as interfaces_wellarchitected
            
            profile_reference = interfaces_wellarchitected.ProfileReference(
                profile_arn="profileArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8ae04271fcde99607a1aceb6f7563e89a6fe87895a913e2d8e18fa75b01e68eb)
            check_type(argname="argument profile_arn", value=profile_arn, expected_type=type_hints["profile_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profile_arn": profile_arn,
        }

    @builtins.property
    def profile_arn(self) -> builtins.str:
        '''The ProfileArn of the Profile resource.'''
        result = self._values.get("profile_arn")
        assert result is not None, "Required property 'profile_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfileReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_wellarchitected.ReviewTemplateReference",
    jsii_struct_bases=[],
    name_mapping={"template_arn": "templateArn"},
)
class ReviewTemplateReference:
    def __init__(self, *, template_arn: builtins.str) -> None:
        '''A reference to a ReviewTemplate resource.

        :param template_arn: The TemplateArn of the ReviewTemplate resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_wellarchitected as interfaces_wellarchitected
            
            review_template_reference = interfaces_wellarchitected.ReviewTemplateReference(
                template_arn="templateArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aff0e657e253e8180fdf4b38be6787eb3cfa2166327da2bcb2125bd911df96a6)
            check_type(argname="argument template_arn", value=template_arn, expected_type=type_hints["template_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_arn": template_arn,
        }

    @builtins.property
    def template_arn(self) -> builtins.str:
        '''The TemplateArn of the ReviewTemplate resource.'''
        result = self._values.get("template_arn")
        assert result is not None, "Required property 'template_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReviewTemplateReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ILensRef",
    "IProfileRef",
    "IReviewTemplateRef",
    "LensReference",
    "ProfileReference",
    "ReviewTemplateReference",
]

publication.publish()

def _typecheckingstub__f32344e8e195ba084ce4fcf47286bb12830dd7f6eb5a3d62943b345edff1b52f(
    *,
    lens_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae04271fcde99607a1aceb6f7563e89a6fe87895a913e2d8e18fa75b01e68eb(
    *,
    profile_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff0e657e253e8180fdf4b38be6787eb3cfa2166327da2bcb2125bd911df96a6(
    *,
    template_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ILensRef, IProfileRef, IReviewTemplateRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
