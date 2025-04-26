r'''
# cdk8s-redis

> Redis constructs for cdk8s

Basic implementation of a Redis construct for cdk8s. Contributions are welcome!

## Usage

The following will define a Redis cluster with a primary and 2 replicas:

```python
import { Redis } from 'cdk8s-redis';

// inside your chart:
const redis = new Redis(this, 'my-redis');
```

DNS names can be obtained from `redis.primaryHost` and `redis.replicaHost`.

You can specify how many replicas to define:

```python
new Redis(this, 'my-redis', {
  replicas: 4
});
```

Or, you can specify no replicas:

```python
new Redis(this, 'my-redis', {
  replicas: 0
});
```

## License

Distributed under the [Apache 2.0](./LICENSE) license.
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

from ._jsii import *

import constructs as _constructs_77d1e7e8


class Redis(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-redis.Redis",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param labels: (experimental) Extra labels to associate with resources. Default: - none
        :param replicas: (experimental) Number of replicas. Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3af7b9f76a9ac8d7168553e9fec19d5299b0ea47bac03341447b27e44c3c3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RedisOptions(labels=labels, replicas=replicas)

        jsii.create(self.__class__, self, [scope, id, options])

    @builtins.property
    @jsii.member(jsii_name="primaryHost")
    def primary_host(self) -> builtins.str:
        '''(experimental) The DNS host for the primary service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "primaryHost"))

    @builtins.property
    @jsii.member(jsii_name="replicaHost")
    def replica_host(self) -> builtins.str:
        '''(experimental) The DNS host for the replica service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "replicaHost"))


@jsii.data_type(
    jsii_type="cdk8s-redis.RedisOptions",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "replicas": "replicas"},
)
class RedisOptions:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param labels: (experimental) Extra labels to associate with resources. Default: - none
        :param replicas: (experimental) Number of replicas. Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d35c212ac7ffff620a95bfad5857df9b6d8bb4e089d9aacde83f4854a019863)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Extra labels to associate with resources.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of replicas.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Redis",
    "RedisOptions",
]

publication.publish()

def _typecheckingstub__ef3af7b9f76a9ac8d7168553e9fec19d5299b0ea47bac03341447b27e44c3c3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d35c212ac7ffff620a95bfad5857df9b6d8bb4e089d9aacde83f4854a019863(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
