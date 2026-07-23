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
    jsii_type="aws-cdk-lib.interfaces.aws_healthlake.FHIRDatastoreReference",
    jsii_struct_bases=[],
    name_mapping={"datastore_arn": "datastoreArn", "datastore_id": "datastoreId"},
)
class FHIRDatastoreReference:
    def __init__(
        self,
        *,
        datastore_arn: builtins.str,
        datastore_id: builtins.str,
    ) -> None:
        '''A reference to a FHIRDatastore resource.

        :param datastore_arn: The ARN of the FHIRDatastore resource.
        :param datastore_id: The DatastoreId of the FHIRDatastore resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_healthlake as interfaces_healthlake
            
            f_hir_datastore_reference = interfaces_healthlake.FHIRDatastoreReference(
                datastore_arn="datastoreArn",
                datastore_id="datastoreId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e093434b57404ddeaf19d5c2ba8655e6c19975de0e9c28bc95ddf450dd413528)
            check_type(argname="argument datastore_arn", value=datastore_arn, expected_type=type_hints["datastore_arn"])
            check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "datastore_arn": datastore_arn,
            "datastore_id": datastore_id,
        }

    @builtins.property
    def datastore_arn(self) -> builtins.str:
        '''The ARN of the FHIRDatastore resource.'''
        result = self._values.get("datastore_arn")
        assert result is not None, "Required property 'datastore_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore_id(self) -> builtins.str:
        '''The DatastoreId of the FHIRDatastore resource.'''
        result = self._values.get("datastore_id")
        assert result is not None, "Required property 'datastore_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FHIRDatastoreReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_healthlake.IFHIRDatastoreRef")
class IFHIRDatastoreRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a FHIRDatastore.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fhirDatastoreRef")
    def fhir_datastore_ref(self) -> "FHIRDatastoreReference":
        '''(experimental) A reference to a FHIRDatastore resource.

        :stability: experimental
        '''
        ...


class _IFHIRDatastoreRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a FHIRDatastore.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_healthlake.IFHIRDatastoreRef"

    @builtins.property
    @jsii.member(jsii_name="fhirDatastoreRef")
    def fhir_datastore_ref(self) -> "FHIRDatastoreReference":
        '''(experimental) A reference to a FHIRDatastore resource.

        :stability: experimental
        '''
        return typing.cast("FHIRDatastoreReference", jsii.get(self, "fhirDatastoreRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFHIRDatastoreRef).__jsii_proxy_class__ = lambda : _IFHIRDatastoreRefProxy


__all__ = [
    "FHIRDatastoreReference",
    "IFHIRDatastoreRef",
]

publication.publish()

def _typecheckingstub__e093434b57404ddeaf19d5c2ba8655e6c19975de0e9c28bc95ddf450dd413528(
    *,
    datastore_arn: builtins.str,
    datastore_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IFHIRDatastoreRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
