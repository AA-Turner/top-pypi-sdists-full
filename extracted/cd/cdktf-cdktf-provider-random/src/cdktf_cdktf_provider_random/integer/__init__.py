r'''
# `random_integer`

Refer to the Terraform Registry for docs: [`random_integer`](https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer).
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


class Integer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-random.integer.Integer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer random_integer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        max: jsii.Number,
        min: jsii.Number,
        keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        seed: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer random_integer} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param max: The maximum inclusive value of the range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#max Integer#max}
        :param min: The minimum inclusive value of the range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#min Integer#min}
        :param keepers: Arbitrary map of values that, when changed, will trigger recreation of resource. See `the main provider documentation <../index.html>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#keepers Integer#keepers}
        :param seed: A custom seed to always produce the same value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#seed Integer#seed}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4513d793dfc4b1aba508ca5c737b31b28b994e474031e4d0fc62b702eafa233d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = IntegerConfig(
            max=max,
            min=min,
            keepers=keepers,
            seed=seed,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Integer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Integer to import.
        :param import_from_id: The id of the existing Integer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Integer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c078996ee8278b776471ca21a90a5217326d1f2476e21f9d820e7ebb207db3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetKeepers")
    def reset_keepers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepers", []))

    @jsii.member(jsii_name="resetSeed")
    def reset_seed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeed", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="keepersInput")
    def keepers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "keepersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="seedInput")
    def seed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "seedInput"))

    @builtins.property
    @jsii.member(jsii_name="keepers")
    def keepers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "keepers"))

    @keepers.setter
    def keepers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb9f9b8b8b42e57d06a5f1cc14d099f747c18193743671e0a8549c65430a960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ecf5197acb7a6b20a9f06ea877e3b2d1a370d85e0d520710ac73738e7893b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e413953769692f5b76f30c9b99d2a9d29e69dae61aa0a23e06271df4dc349ad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seed")
    def seed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seed"))

    @seed.setter
    def seed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034b74ab91f487177c9a602c1b2caca265fe4cf6dcbd4b0a092898eb5aaa27f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seed", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-random.integer.IntegerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "max": "max",
        "min": "min",
        "keepers": "keepers",
        "seed": "seed",
    },
)
class IntegerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        max: jsii.Number,
        min: jsii.Number,
        keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        seed: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param max: The maximum inclusive value of the range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#max Integer#max}
        :param min: The minimum inclusive value of the range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#min Integer#min}
        :param keepers: Arbitrary map of values that, when changed, will trigger recreation of resource. See `the main provider documentation <../index.html>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#keepers Integer#keepers}
        :param seed: A custom seed to always produce the same value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#seed Integer#seed}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04175ec3d89c278ab4a4bc44ebb2dcc46a7b50760dac507c790c3c1e17f479c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument keepers", value=keepers, expected_type=type_hints["keepers"])
            check_type(argname="argument seed", value=seed, expected_type=type_hints["seed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "min": min,
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
        if keepers is not None:
            self._values["keepers"] = keepers
        if seed is not None:
            self._values["seed"] = seed

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
    def max(self) -> jsii.Number:
        '''The maximum inclusive value of the range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#max Integer#max}
        '''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min(self) -> jsii.Number:
        '''The minimum inclusive value of the range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#min Integer#min}
        '''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def keepers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Arbitrary map of values that, when changed, will trigger recreation of resource.

        See `the main provider documentation <../index.html>`_ for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#keepers Integer#keepers}
        '''
        result = self._values.get("keepers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def seed(self) -> typing.Optional[builtins.str]:
        '''A custom seed to always produce the same value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/integer#seed Integer#seed}
        '''
        result = self._values.get("seed")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Integer",
    "IntegerConfig",
]

publication.publish()

def _typecheckingstub__4513d793dfc4b1aba508ca5c737b31b28b994e474031e4d0fc62b702eafa233d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    max: jsii.Number,
    min: jsii.Number,
    keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    seed: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__56c078996ee8278b776471ca21a90a5217326d1f2476e21f9d820e7ebb207db3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb9f9b8b8b42e57d06a5f1cc14d099f747c18193743671e0a8549c65430a960(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ecf5197acb7a6b20a9f06ea877e3b2d1a370d85e0d520710ac73738e7893b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e413953769692f5b76f30c9b99d2a9d29e69dae61aa0a23e06271df4dc349ad6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034b74ab91f487177c9a602c1b2caca265fe4cf6dcbd4b0a092898eb5aaa27f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04175ec3d89c278ab4a4bc44ebb2dcc46a7b50760dac507c790c3c1e17f479c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max: jsii.Number,
    min: jsii.Number,
    keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    seed: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
