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


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_codebuild.BuildBatchReference",
    jsii_struct_bases=[],
    name_mapping={
        "build_batch_arn": "buildBatchArn",
        "build_batch_id": "buildBatchId",
    },
)
class BuildBatchReference:
    def __init__(
        self,
        *,
        build_batch_arn: builtins.str,
        build_batch_id: builtins.str,
    ) -> None:
        '''A reference to a BuildBatch resource.

        :param build_batch_arn: The ARN of the BuildBatch resource.
        :param build_batch_id: The Id of the BuildBatch resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_codebuild as interfaces_codebuild
            
            build_batch_reference = interfaces_codebuild.BuildBatchReference(
                build_batch_arn="buildBatchArn",
                build_batch_id="buildBatchId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c0f8f89b7bee3b8d8a65337ed27bfce7cb2481adb9bccbd4944ee93a49b341cb)
            check_type(argname="argument build_batch_arn", value=build_batch_arn, expected_type=type_hints["build_batch_arn"])
            check_type(argname="argument build_batch_id", value=build_batch_id, expected_type=type_hints["build_batch_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "build_batch_arn": build_batch_arn,
            "build_batch_id": build_batch_id,
        }

    @builtins.property
    def build_batch_arn(self) -> builtins.str:
        '''The ARN of the BuildBatch resource.'''
        result = self._values.get("build_batch_arn")
        assert result is not None, "Required property 'build_batch_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_batch_id(self) -> builtins.str:
        '''The Id of the BuildBatch resource.'''
        result = self._values.get("build_batch_id")
        assert result is not None, "Required property 'build_batch_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildBatchReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_codebuild.BuildReference",
    jsii_struct_bases=[],
    name_mapping={"build_arn": "buildArn", "build_id": "buildId"},
)
class BuildReference:
    def __init__(self, *, build_arn: builtins.str, build_id: builtins.str) -> None:
        '''A reference to a Build resource.

        :param build_arn: The ARN of the Build resource.
        :param build_id: The Id of the Build resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_codebuild as interfaces_codebuild
            
            build_reference = interfaces_codebuild.BuildReference(
                build_arn="buildArn",
                build_id="buildId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9ff0146471318239ef232ee6efb3ff810eea25751a723f2b5dbd267efa920750)
            check_type(argname="argument build_arn", value=build_arn, expected_type=type_hints["build_arn"])
            check_type(argname="argument build_id", value=build_id, expected_type=type_hints["build_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "build_arn": build_arn,
            "build_id": build_id,
        }

    @builtins.property
    def build_arn(self) -> builtins.str:
        '''The ARN of the Build resource.'''
        result = self._values.get("build_arn")
        assert result is not None, "Required property 'build_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_id(self) -> builtins.str:
        '''The Id of the Build resource.'''
        result = self._values.get("build_id")
        assert result is not None, "Required property 'build_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_codebuild.FleetReference",
    jsii_struct_bases=[],
    name_mapping={"fleet_arn": "fleetArn"},
)
class FleetReference:
    def __init__(self, *, fleet_arn: builtins.str) -> None:
        '''A reference to a Fleet resource.

        :param fleet_arn: The Arn of the Fleet resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_codebuild as interfaces_codebuild
            
            fleet_reference = interfaces_codebuild.FleetReference(
                fleet_arn="fleetArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b252b09ea2d7a037ef7eb8c132fdc4bf9af5d216a313e3c3b3a3847f4e0d380c)
            check_type(argname="argument fleet_arn", value=fleet_arn, expected_type=type_hints["fleet_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fleet_arn": fleet_arn,
        }

    @builtins.property
    def fleet_arn(self) -> builtins.str:
        '''The Arn of the Fleet resource.'''
        result = self._values.get("fleet_arn")
        assert result is not None, "Required property 'fleet_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FleetReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_codebuild.IBuildBatchRef")
class IBuildBatchRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a BuildBatch.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="buildBatchRef")
    def build_batch_ref(self) -> "BuildBatchReference":
        '''(experimental) A reference to a BuildBatch resource.

        :stability: experimental
        '''
        ...


class _IBuildBatchRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a BuildBatch.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_codebuild.IBuildBatchRef"

    @builtins.property
    @jsii.member(jsii_name="buildBatchRef")
    def build_batch_ref(self) -> "BuildBatchReference":
        '''(experimental) A reference to a BuildBatch resource.

        :stability: experimental
        '''
        return typing.cast("BuildBatchReference", jsii.get(self, "buildBatchRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBuildBatchRef).__jsii_proxy_class__ = lambda : _IBuildBatchRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_codebuild.IBuildRef")
class IBuildRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Build.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="buildRef")
    def build_ref(self) -> "BuildReference":
        '''(experimental) A reference to a Build resource.

        :stability: experimental
        '''
        ...


class _IBuildRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Build.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_codebuild.IBuildRef"

    @builtins.property
    @jsii.member(jsii_name="buildRef")
    def build_ref(self) -> "BuildReference":
        '''(experimental) A reference to a Build resource.

        :stability: experimental
        '''
        return typing.cast("BuildReference", jsii.get(self, "buildRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBuildRef).__jsii_proxy_class__ = lambda : _IBuildRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_codebuild.IFleetRef")
class IFleetRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Fleet.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fleetRef")
    def fleet_ref(self) -> "FleetReference":
        '''(experimental) A reference to a Fleet resource.

        :stability: experimental
        '''
        ...


class _IFleetRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Fleet.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_codebuild.IFleetRef"

    @builtins.property
    @jsii.member(jsii_name="fleetRef")
    def fleet_ref(self) -> "FleetReference":
        '''(experimental) A reference to a Fleet resource.

        :stability: experimental
        '''
        return typing.cast("FleetReference", jsii.get(self, "fleetRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFleetRef).__jsii_proxy_class__ = lambda : _IFleetRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_codebuild.IProjectRef")
class IProjectRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Project.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="projectRef")
    def project_ref(self) -> "ProjectReference":
        '''(experimental) A reference to a Project resource.

        :stability: experimental
        '''
        ...


class _IProjectRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Project.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_codebuild.IProjectRef"

    @builtins.property
    @jsii.member(jsii_name="projectRef")
    def project_ref(self) -> "ProjectReference":
        '''(experimental) A reference to a Project resource.

        :stability: experimental
        '''
        return typing.cast("ProjectReference", jsii.get(self, "projectRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProjectRef).__jsii_proxy_class__ = lambda : _IProjectRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_codebuild.IReportGroupRef")
class IReportGroupRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ReportGroup.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="reportGroupRef")
    def report_group_ref(self) -> "ReportGroupReference":
        '''(experimental) A reference to a ReportGroup resource.

        :stability: experimental
        '''
        ...


class _IReportGroupRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ReportGroup.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_codebuild.IReportGroupRef"

    @builtins.property
    @jsii.member(jsii_name="reportGroupRef")
    def report_group_ref(self) -> "ReportGroupReference":
        '''(experimental) A reference to a ReportGroup resource.

        :stability: experimental
        '''
        return typing.cast("ReportGroupReference", jsii.get(self, "reportGroupRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReportGroupRef).__jsii_proxy_class__ = lambda : _IReportGroupRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_codebuild.ISourceCredentialRef")
class ISourceCredentialRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a SourceCredential.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="sourceCredentialRef")
    def source_credential_ref(self) -> "SourceCredentialReference":
        '''(experimental) A reference to a SourceCredential resource.

        :stability: experimental
        '''
        ...


class _ISourceCredentialRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a SourceCredential.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_codebuild.ISourceCredentialRef"

    @builtins.property
    @jsii.member(jsii_name="sourceCredentialRef")
    def source_credential_ref(self) -> "SourceCredentialReference":
        '''(experimental) A reference to a SourceCredential resource.

        :stability: experimental
        '''
        return typing.cast("SourceCredentialReference", jsii.get(self, "sourceCredentialRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceCredentialRef).__jsii_proxy_class__ = lambda : _ISourceCredentialRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_codebuild.ProjectReference",
    jsii_struct_bases=[],
    name_mapping={"project_arn": "projectArn", "project_name": "projectName"},
)
class ProjectReference:
    def __init__(
        self,
        *,
        project_arn: builtins.str,
        project_name: builtins.str,
    ) -> None:
        '''A reference to a Project resource.

        :param project_arn: The ARN of the Project resource.
        :param project_name: The Name of the Project resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_codebuild as interfaces_codebuild
            
            project_reference = interfaces_codebuild.ProjectReference(
                project_arn="projectArn",
                project_name="projectName"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__938517d640cf480acbfa73e5d436dfdb8249909865744af5fcd6ced48675a435)
            check_type(argname="argument project_arn", value=project_arn, expected_type=type_hints["project_arn"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_arn": project_arn,
            "project_name": project_name,
        }

    @builtins.property
    def project_arn(self) -> builtins.str:
        '''The ARN of the Project resource.'''
        result = self._values.get("project_arn")
        assert result is not None, "Required property 'project_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''The Name of the Project resource.'''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_codebuild.ReportGroupReference",
    jsii_struct_bases=[],
    name_mapping={"report_group_arn": "reportGroupArn"},
)
class ReportGroupReference:
    def __init__(self, *, report_group_arn: builtins.str) -> None:
        '''A reference to a ReportGroup resource.

        :param report_group_arn: The Arn of the ReportGroup resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_codebuild as interfaces_codebuild
            
            report_group_reference = interfaces_codebuild.ReportGroupReference(
                report_group_arn="reportGroupArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7cd46ecb1a45984facc4fba5861d8c76e61cb467c28f418886f84499d8ece72c)
            check_type(argname="argument report_group_arn", value=report_group_arn, expected_type=type_hints["report_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "report_group_arn": report_group_arn,
        }

    @builtins.property
    def report_group_arn(self) -> builtins.str:
        '''The Arn of the ReportGroup resource.'''
        result = self._values.get("report_group_arn")
        assert result is not None, "Required property 'report_group_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReportGroupReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_codebuild.SourceCredentialReference",
    jsii_struct_bases=[],
    name_mapping={"source_credential_id": "sourceCredentialId"},
)
class SourceCredentialReference:
    def __init__(self, *, source_credential_id: builtins.str) -> None:
        '''A reference to a SourceCredential resource.

        :param source_credential_id: The Id of the SourceCredential resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_codebuild as interfaces_codebuild
            
            source_credential_reference = interfaces_codebuild.SourceCredentialReference(
                source_credential_id="sourceCredentialId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1401c6ca94e02a490ee8ba6e38db6ee0841aa4f2e47c6995257d49aa5711a95c)
            check_type(argname="argument source_credential_id", value=source_credential_id, expected_type=type_hints["source_credential_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_credential_id": source_credential_id,
        }

    @builtins.property
    def source_credential_id(self) -> builtins.str:
        '''The Id of the SourceCredential resource.'''
        result = self._values.get("source_credential_id")
        assert result is not None, "Required property 'source_credential_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCredentialReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BuildBatchReference",
    "BuildReference",
    "FleetReference",
    "IBuildBatchRef",
    "IBuildRef",
    "IFleetRef",
    "IProjectRef",
    "IReportGroupRef",
    "ISourceCredentialRef",
    "ProjectReference",
    "ReportGroupReference",
    "SourceCredentialReference",
]

publication.publish()

def _typecheckingstub__c0f8f89b7bee3b8d8a65337ed27bfce7cb2481adb9bccbd4944ee93a49b341cb(
    *,
    build_batch_arn: builtins.str,
    build_batch_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff0146471318239ef232ee6efb3ff810eea25751a723f2b5dbd267efa920750(
    *,
    build_arn: builtins.str,
    build_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b252b09ea2d7a037ef7eb8c132fdc4bf9af5d216a313e3c3b3a3847f4e0d380c(
    *,
    fleet_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938517d640cf480acbfa73e5d436dfdb8249909865744af5fcd6ced48675a435(
    *,
    project_arn: builtins.str,
    project_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd46ecb1a45984facc4fba5861d8c76e61cb467c28f418886f84499d8ece72c(
    *,
    report_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1401c6ca94e02a490ee8ba6e38db6ee0841aa4f2e47c6995257d49aa5711a95c(
    *,
    source_credential_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IBuildBatchRef, IBuildRef, IFleetRef, IProjectRef, IReportGroupRef, ISourceCredentialRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
