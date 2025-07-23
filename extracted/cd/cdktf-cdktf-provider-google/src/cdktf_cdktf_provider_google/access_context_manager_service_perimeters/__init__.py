r'''
# `google_access_context_manager_service_perimeters`

Refer to the Terraform Registry for docs: [`google_access_context_manager_service_perimeters`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters).
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


class AccessContextManagerServicePerimeters(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimeters",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters google_access_context_manager_service_perimeters}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        id: typing.Optional[builtins.str] = None,
        service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimeters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimetersTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters google_access_context_manager_service_perimeters} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#parent AccessContextManagerServicePerimeters#parent}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#id AccessContextManagerServicePerimeters#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_perimeters: service_perimeters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_perimeters AccessContextManagerServicePerimeters#service_perimeters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#timeouts AccessContextManagerServicePerimeters#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20511537904f8d642d8951bb064f6628a9c5a512759ebde77eeba1e736057443)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerServicePerimetersConfig(
            parent=parent,
            id=id,
            service_perimeters=service_perimeters,
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
        '''Generates CDKTF code for importing a AccessContextManagerServicePerimeters resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerServicePerimeters to import.
        :param import_from_id: The id of the existing AccessContextManagerServicePerimeters that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerServicePerimeters to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692bfd9e948c83e7946f5bd4715d7e7371a351c9c0578680deb5692ab10fb0a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServicePerimeters")
    def put_service_perimeters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimeters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9155ed35bb8c12ec27eba53f876da50943ce2010586c76a1b2c5dc1b6a79d278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServicePerimeters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#create AccessContextManagerServicePerimeters#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#delete AccessContextManagerServicePerimeters#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#update AccessContextManagerServicePerimeters#update}.
        '''
        value = AccessContextManagerServicePerimetersTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetServicePerimeters")
    def reset_service_perimeters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePerimeters", []))

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
    @jsii.member(jsii_name="servicePerimeters")
    def service_perimeters(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersList":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersList", jsii.get(self, "servicePerimeters"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AccessContextManagerServicePerimetersTimeoutsOutputReference":
        return typing.cast("AccessContextManagerServicePerimetersTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePerimetersInput")
    def service_perimeters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimeters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimeters"]]], jsii.get(self, "servicePerimetersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimetersTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimetersTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631ed769051cf24fa8bf3a50555fc1bc24084f5ca3ce8926ae474bb14820f8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ac3049fb0b06674e186a93c4f0340961eb62288bab7193213ab4319cbd280a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "parent": "parent",
        "id": "id",
        "service_perimeters": "servicePerimeters",
        "timeouts": "timeouts",
    },
)
class AccessContextManagerServicePerimetersConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        parent: builtins.str,
        id: typing.Optional[builtins.str] = None,
        service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimeters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimetersTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#parent AccessContextManagerServicePerimeters#parent}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#id AccessContextManagerServicePerimeters#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_perimeters: service_perimeters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_perimeters AccessContextManagerServicePerimeters#service_perimeters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#timeouts AccessContextManagerServicePerimeters#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerServicePerimetersTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd838d90a72b55f4d9d4bdf91501eef94468f1de3ad6262aa03a7510c4e89e13)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_perimeters", value=service_perimeters, expected_type=type_hints["service_perimeters"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent": parent,
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
        if service_perimeters is not None:
            self._values["service_perimeters"] = service_perimeters
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
    def parent(self) -> builtins.str:
        '''The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#parent AccessContextManagerServicePerimeters#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#id AccessContextManagerServicePerimeters#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_perimeters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimeters"]]]:
        '''service_perimeters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_perimeters AccessContextManagerServicePerimeters#service_perimeters}
        '''
        result = self._values.get("service_perimeters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimeters"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#timeouts AccessContextManagerServicePerimeters#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimeters",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "title": "title",
        "description": "description",
        "perimeter_type": "perimeterType",
        "spec": "spec",
        "status": "status",
        "use_explicit_dry_run_spec": "useExplicitDryRunSpec",
    },
)
class AccessContextManagerServicePerimetersServicePerimeters:
    def __init__(
        self,
        *,
        name: builtins.str,
        title: builtins.str,
        description: typing.Optional[builtins.str] = None,
        perimeter_type: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Resource name for the ServicePerimeter. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/servicePerimeters/{short_name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#name AccessContextManagerServicePerimeters#name}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        :param description: Description of the ServicePerimeter and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#description AccessContextManagerServicePerimeters#description}
        :param perimeter_type: Specifies the type of the Perimeter. There are two types: regular and bridge. Regular Service Perimeter contains resources, access levels, and restricted services. Every resource can be in at most ONE regular Service Perimeter. In addition to being in a regular service perimeter, a resource can also be in zero or more perimeter bridges. A perimeter bridge only contains resources. Cross project operations are permitted if all effected resources share some perimeter (whether bridge or regular). Perimeter Bridge does not contain access levels or services: those are governed entirely by the regular perimeter that resource is in. Perimeter Bridges are typically useful when building more complex topologies with many independent perimeters that need to share some data with a common perimeter, but should not be able to share data among themselves. Default value: "PERIMETER_TYPE_REGULAR" Possible values: ["PERIMETER_TYPE_REGULAR", "PERIMETER_TYPE_BRIDGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#perimeter_type AccessContextManagerServicePerimeters#perimeter_type}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#spec AccessContextManagerServicePerimeters#spec}
        :param status: status block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#status AccessContextManagerServicePerimeters#status}
        :param use_explicit_dry_run_spec: Use explicit dry run spec flag. Ordinarily, a dry-run spec implicitly exists for all Service Perimeters, and that spec is identical to the status for those Service Perimeters. When this flag is set, it inhibits the generation of the implicit spec, thereby allowing the user to explicitly provide a configuration ("spec") to use in a dry-run version of the Service Perimeter. This allows the user to test changes to the enforced config ("status") without actually enforcing them. This testing is done through analyzing the differences between currently enforced and suggested restrictions. useExplicitDryRunSpec must bet set to True if any of the fields in the spec are set to non-default values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#use_explicit_dry_run_spec AccessContextManagerServicePerimeters#use_explicit_dry_run_spec}
        '''
        if isinstance(spec, dict):
            spec = AccessContextManagerServicePerimetersServicePerimetersSpec(**spec)
        if isinstance(status, dict):
            status = AccessContextManagerServicePerimetersServicePerimetersStatus(**status)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad80091b91c130052f3d00c5ac4be25b3f18aced723460939542ba1902f47938)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument perimeter_type", value=perimeter_type, expected_type=type_hints["perimeter_type"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument use_explicit_dry_run_spec", value=use_explicit_dry_run_spec, expected_type=type_hints["use_explicit_dry_run_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "title": title,
        }
        if description is not None:
            self._values["description"] = description
        if perimeter_type is not None:
            self._values["perimeter_type"] = perimeter_type
        if spec is not None:
            self._values["spec"] = spec
        if status is not None:
            self._values["status"] = status
        if use_explicit_dry_run_spec is not None:
            self._values["use_explicit_dry_run_spec"] = use_explicit_dry_run_spec

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name for the ServicePerimeter. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/servicePerimeters/{short_name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#name AccessContextManagerServicePerimeters#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Human readable title. Must be unique within the Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the ServicePerimeter and its use. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#description AccessContextManagerServicePerimeters#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def perimeter_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of the Perimeter.

        There are two types: regular and
        bridge. Regular Service Perimeter contains resources, access levels,
        and restricted services. Every resource can be in at most
        ONE regular Service Perimeter.

        In addition to being in a regular service perimeter, a resource can also
        be in zero or more perimeter bridges. A perimeter bridge only contains
        resources. Cross project operations are permitted if all effected
        resources share some perimeter (whether bridge or regular). Perimeter
        Bridge does not contain access levels or services: those are governed
        entirely by the regular perimeter that resource is in.

        Perimeter Bridges are typically useful when building more complex
        topologies with many independent perimeters that need to share some data
        with a common perimeter, but should not be able to share data among
        themselves. Default value: "PERIMETER_TYPE_REGULAR" Possible values: ["PERIMETER_TYPE_REGULAR", "PERIMETER_TYPE_BRIDGE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#perimeter_type AccessContextManagerServicePerimeters#perimeter_type}
        '''
        result = self._values.get("perimeter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#spec AccessContextManagerServicePerimeters#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpec"], result)

    @builtins.property
    def status(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatus"]:
        '''status block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#status AccessContextManagerServicePerimeters#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatus"], result)

    @builtins.property
    def use_explicit_dry_run_spec(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use explicit dry run spec flag.

        Ordinarily, a dry-run spec implicitly exists
        for all Service Perimeters, and that spec is identical to the status for those
        Service Perimeters. When this flag is set, it inhibits the generation of the
        implicit spec, thereby allowing the user to explicitly provide a
        configuration ("spec") to use in a dry-run version of the Service Perimeter.
        This allows the user to test changes to the enforced config ("status") without
        actually enforcing them. This testing is done through analyzing the differences
        between currently enforced and suggested restrictions. useExplicitDryRunSpec must
        bet set to True if any of the fields in the spec are set to non-default values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#use_explicit_dry_run_spec AccessContextManagerServicePerimeters#use_explicit_dry_run_spec}
        '''
        result = self._values.get("use_explicit_dry_run_spec")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimeters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c6d00e0d00675bf19a4b39459c895fb55d61d494cea0c8ef5349aa904b7f55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7883de5adcd195a69b5377dd4006d3b26f65de0d57ada4c5ac9658fd87278331)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2821cdf32a4249d160a6e4decc3d51066808fbd09142fac20c58085376e9d7a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6d0887b90c17e87ac7558834d2f0e18167ca9bd12a78814564b2cd90e77fe0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00601aa992c4bb27148d8f5cb14fdc1fd8ce332cb8e476d5b09751219591969c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimeters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimeters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimeters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c38a810195501dfd11c5fc07a4c124ab1edc6c08faa732183ee184a7d5910b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0fca80ac926fdf2e8e1b8403d0e55df3d35e1c1e7d0090f91269f4b453ebc90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_levels AccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_policies AccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_policies AccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#restricted_services AccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#vpc_accessible_services AccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersSpec(
            access_levels=access_levels,
            egress_policies=egress_policies,
            ingress_policies=ingress_policies,
            resources=resources,
            restricted_services=restricted_services,
            vpc_accessible_services=vpc_accessible_services,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putStatus")
    def put_status(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_levels AccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_policies AccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_policies AccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#restricted_services AccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#vpc_accessible_services AccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersStatus(
            access_levels=access_levels,
            egress_policies=egress_policies,
            ingress_policies=ingress_policies,
            resources=resources,
            restricted_services=restricted_services,
            vpc_accessible_services=vpc_accessible_services,
        )

        return typing.cast(None, jsii.invoke(self, "putStatus", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetPerimeterType")
    def reset_perimeter_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerimeterType", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetUseExplicitDryRunSpec")
    def reset_use_explicit_dry_run_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseExplicitDryRunSpec", []))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecOutputReference":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusOutputReference":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusOutputReference", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="perimeterTypeInput")
    def perimeter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perimeterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpec"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatus"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatus"], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="useExplicitDryRunSpecInput")
    def use_explicit_dry_run_spec_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useExplicitDryRunSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac1fb2d34dd1dd39a207e493a29089d7792525d7f7fdf104caacff01320bd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c58909c279674995a38ddc30eb28d414f806ec2cafba5a89c79749a7819d6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perimeterType")
    def perimeter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perimeterType"))

    @perimeter_type.setter
    def perimeter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec34e5c347634b2e453103b14b8c21655a22bf9acb9f05fbb379348cfa7d34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perimeterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecba00de86f43c0b478071ae7aa5309b2b9322beb0c3c7358d7de47e3c9bb8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExplicitDryRunSpec")
    def use_explicit_dry_run_spec(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useExplicitDryRunSpec"))

    @use_explicit_dry_run_spec.setter
    def use_explicit_dry_run_spec(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0218df3f77f5a244b7c63832ab64bbe9539b1f94c5d8c8a5a2d7e706708d1b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExplicitDryRunSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimeters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimeters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimeters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2d470f61a8ba43d21759f4f313278cef86ef8feeaf28a4a3f7c7ac9c50bc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpec",
    jsii_struct_bases=[],
    name_mapping={
        "access_levels": "accessLevels",
        "egress_policies": "egressPolicies",
        "ingress_policies": "ingressPolicies",
        "resources": "resources",
        "restricted_services": "restrictedServices",
        "vpc_accessible_services": "vpcAccessibleServices",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpec:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_levels AccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_policies AccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_policies AccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#restricted_services AccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#vpc_accessible_services AccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        if isinstance(vpc_accessible_services, dict):
            vpc_accessible_services = AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices(**vpc_accessible_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f687bc982fc859ec56680688b6193187525de8c5a0e9632366da52f1ebfbb5ea)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument egress_policies", value=egress_policies, expected_type=type_hints["egress_policies"])
            check_type(argname="argument ingress_policies", value=ingress_policies, expected_type=type_hints["ingress_policies"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument restricted_services", value=restricted_services, expected_type=type_hints["restricted_services"])
            check_type(argname="argument vpc_accessible_services", value=vpc_accessible_services, expected_type=type_hints["vpc_accessible_services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels
        if egress_policies is not None:
            self._values["egress_policies"] = egress_policies
        if ingress_policies is not None:
            self._values["ingress_policies"] = ingress_policies
        if resources is not None:
            self._values["resources"] = resources
        if restricted_services is not None:
            self._values["restricted_services"] = restricted_services
        if vpc_accessible_services is not None:
            self._values["vpc_accessible_services"] = vpc_accessible_services

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet.

        AccessLevels listed must be in the same policy as this
        ServicePerimeter. Referencing a nonexistent AccessLevel is a
        syntax error. If no AccessLevel names are listed, resources within
        the perimeter can only be accessed via GCP calls with request
        origins within the perimeter. For Service Perimeter Bridge, must
        be empty.

        Format: accessPolicies/{policy_id}/accessLevels/{access_level_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_levels AccessContextManagerServicePerimeters#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def egress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies"]]]:
        '''egress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_policies AccessContextManagerServicePerimeters#egress_policies}
        '''
        result = self._values.get("egress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies"]]], result)

    @builtins.property
    def ingress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies"]]]:
        '''ingress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_policies AccessContextManagerServicePerimeters#ingress_policies}
        '''
        result = self._values.get("ingress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def restricted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''GCP services that are subject to the Service Perimeter restrictions.

        Must contain a list of services. For example, if
        'storage.googleapis.com' is specified, access to the storage
        buckets inside the perimeter must meet the perimeter's access
        restrictions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#restricted_services AccessContextManagerServicePerimeters#restricted_services}
        '''
        result = self._values.get("restricted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_accessible_services(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"]:
        '''vpc_accessible_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#vpc_accessible_services AccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        result = self._values.get("vpc_accessible_services")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies:
    def __init__(
        self,
        *,
        egress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_from AccessContextManagerServicePerimeters#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_to AccessContextManagerServicePerimeters#egress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        if isinstance(egress_from, dict):
            egress_from = AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo(**egress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304162195f6de9798f7333074ecc7a9f01dffcecf3a8a6f421f6c295db32fcaf)
            check_type(argname="argument egress_from", value=egress_from, expected_type=type_hints["egress_from"])
            check_type(argname="argument egress_to", value=egress_to, expected_type=type_hints["egress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_from is not None:
            self._values["egress_from"] = egress_from
        if egress_to is not None:
            self._values["egress_to"] = egress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def egress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_from AccessContextManagerServicePerimeters#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_to AccessContextManagerServicePerimeters#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#source_restriction AccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de63a26e640eee4e5e43f9bc117f905357bf16fce521ab522858e1a8e5b727e)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument source_restriction", value=source_restriction, expected_type=type_hints["source_restriction"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if source_restriction is not None:
            self._values["source_restriction"] = source_restriction
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identities can be an individual user, service account, Google group, or third-party identity.

        For third-party identity, only single identities
        are supported and other identity types are not supported.The v1 identities
        that have the prefix user, group and serviceAccount in
        https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#source_restriction AccessContextManagerServicePerimeters#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__273220e67f028a9f18475eba8beef9302f66fffb3d14d7e3b3de0f7e2a058830)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff7e724a73322e174610387a6ee96aba2f07c9e52da2333b35ec61d82c42f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSourceRestriction")
    def reset_source_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRestriction", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRestrictionInput")
    def source_restriction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c691bd9fa2194c863dc81412b054a548ac64060cc459d5dbbe02a23fe7eed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b995c91dd7b8d533182e3a60b5e1a4f15512cacd0a23ea142fc0fdfe52aebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a44da70b358048311d94201c9755b7198923ede60bb926ebb2819421fa10aef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cc5f1d7ec85ae8a23e53b01d34ece9b5e4c69e19b731c6da6c5a4dd353cdd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a736b1e2a5b4c143528db17cf0e10854e188137795a9cb7ea7e6e34fd4455bc9)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to egress the perimeter.

        Requests from these resources are allowed to access data outside the perimeter.
        Currently only projects are allowed. Project format: 'projects/{project_number}'.
        The resource may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the
        case of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9f3e09c4edb32214d4f671cb583be4ce20cd085208afd9d83ba321960123e3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93147fd2545c48a06f527587351d7b4ff72679d7189d7b55e6af44b71aeaad2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38360c37c09ecb93ad25e1f4ad9ea6fd64e05d78d8b98132731ee9ec08ba2e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__378ee99b7dfc142cbb8b51dbbf3236ff8bb3d99802cd1690f7a3fe104c5be63b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d0624794076f5cf73e169d5a4b6150f749fb73b6ec9a96604c3f9e426ddc54d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf386c3b17e230ba98c97b9105a3081858e43dc8cb00f908cd77c3bff518ca88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb26fc899866c35836bb60aa56b4a643fb333365ad353263c398152d0a93741e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6d12c43c67bdd12d61a933b5a82519ad23720dfb56fe22bcc26cc315648a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cb37bcc40ada38d0ffc20bfac8768dbc98b9eacea9f2f1f76d1425fe19f84b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e6dc07b79dafb5ccf7bc8884d9a36ee80d0473cfc71955432814a6f9ef24a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#external_resources AccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ad5f4fd4e05942a594a97f876703894f98f6193dc0e53ecd25958cafc1baf8)
            check_type(argname="argument external_resources", value=external_resources, expected_type=type_hints["external_resources"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_resources is not None:
            self._values["external_resources"] = external_resources
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def external_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of external resources that are allowed to be accessed.

        A request
        matches if it contains an external resource in this list (Example:
        s3://bucket/path). Currently '*' is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#external_resources AccessContextManagerServicePerimeters#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8c0914a2e1c62859d6db6c9ceed359dcddad21896b5f23d25ffe0e0d1c4d9b)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cca87b850114d23162c77025b7884c4503849c213e2da06cb0331b519a7298b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07918e5b342ea3a0786e27a1ffa812d3f6010f3e8e4ba319d656d8516e4262b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762f159b24a9517167d52a7f04e8e3887d6e5dd22d47ebe8bd34372a23e98e9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__301563821486c244eb4cbff184dd4f2d54dac705ebd8b335341efccebeef7295)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82e2fa79a51edcdbef591d095d04c51f24adb612af83e1aebba6d735e80892bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60908b2e39cc56aa74d9af33d78ac1b9f3a9d58c8acbf50322d4afb2309e58ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe527a2096a44d7560612cfc69257da8b67579719a94358578a46b3f8d6301c)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'.

        If '*' used as value for method,
        then ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6770e6523eab18616aa5232837d90a7895dd818cdb3939a106367f5482c034d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9d07529133b40c7695e40c373fb3c8f2425b527e13616383f56c60a502e1b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ba4fc37c8a740e7f50c3288605761a988f7991885d656ad00a916966be4550)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e77baa97fbd787a2a2bcad039b747ffeb2717c92be4f78d16b253151c08b6fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b6eb4a556ba79d595eef13e06e1bea60ac31cc610cde664ac49b294d075b4bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c522f786be3e64c182f1b82732551f61560478b37df0a7807a2cb09c281eea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0938fa434a4d2034d0215f253df512c68d70b468f8080f89e3a9abf0cb4a8c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5710c0c0273d081995c95c3d441e8eca5b5c76a407a39d23aa9a6ef5288b662c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cc3b033c0afeaaf4e206c42bd5a8e69345d4140231fb86ac778c397c05f4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c1e4d99fbd002f9dbcf9669becb214cdea84f47daa71aa5c5785671106a3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__681acb625fb7d6f81fabb6eb13429c27a6a18b7e7ea09fd9dbfa5513be123e57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd7182940eaf5a34f3cdade98d8d77b50294332ae72ccdd1273ebd6cabd65bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cb301ee98819a421d165c9b5344edb9042e180001c4963883f4589573fd7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1568e5b678a696bf35d6d9c2dfbb47df595a05780ac71bad7c95d33d2e499c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32140d1966ea6a367acb63adac16e0c6e150490d2ecc1c12fa490cd2b52269e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242825bf74a9a410c56bc5d578439bcb18c9197b386e3ce7bf7aeb9a1729f896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetExternalResources")
    def reset_external_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalResources", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="externalResources")
    def external_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalResources"))

    @external_resources.setter
    def external_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ca2e918882c501d89ef14fa1a036025cbb6ac8b657fc9882c28c1cabbe2347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4477eca30891d0e60ccaa3efbe3280006c6b72fb50144d6bd2725094b523e0ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a0b0ef22bb5b737cd6b4a335ad4afac60a0a425a5eacce4b11985fa0d3f1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b04bb3444e046cf223b37af6f8aa51489b8c3460d5090099c0bbf4fbdeeaca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcf20dcd46917dff50d572cff2d39bbcf38ca698dda6d22c4083f0e5ba07d91a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0d6c1faaf9b7b6a5331f9f6fb92c9a8eaa28565d6a8afe3f04be5410432ebb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cba011cd40c8384c8dd3a29f9959e9e4e5670e0d2ba021cfd324a8c2fd77775)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b0dd4d586d77406a271a434708e9db5d3982fcfc9dedd9fa2c5bf97c85ca9e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ee4b801e14103d28ef3499238a5dcbb06917cd596d2323b1c39b0d8bcedb60e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c58b0a26e3d5f7a367ea19f30b6fa0b73a0da550273ff0af1a01390a62123e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5145e4e566e2f12a283b4ecddd6508eb18321d27abe56fa81cbd65d849ee871)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEgressFrom")
    def put_egress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#source_restriction AccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom(
            identities=identities,
            identity_type=identity_type,
            source_restriction=source_restriction,
            sources=sources,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressFrom", [value]))

    @jsii.member(jsii_name="putEgressTo")
    def put_egress_to(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#external_resources AccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo(
            external_resources=external_resources,
            operations=operations,
            resources=resources,
            roles=roles,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressTo", [value]))

    @jsii.member(jsii_name="resetEgressFrom")
    def reset_egress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressFrom", []))

    @jsii.member(jsii_name="resetEgressTo")
    def reset_egress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="egressFrom")
    def egress_from(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference, jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference, jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo], jsii.get(self, "egressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3085df03cbe0b090c7bcd3694225183b71254b97df293bcc4c2d0edf0a0cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eef1a45656c3855c0a5488aaba45c80db0ce4b3710814336e777690dc34635b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies:
    def __init__(
        self,
        *,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_from AccessContextManagerServicePerimeters#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_to AccessContextManagerServicePerimeters#ingress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        if isinstance(ingress_from, dict):
            ingress_from = AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo(**ingress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebce31978098e2da81b907dedf8686d94675331f55521a5323fa560fc0566cf)
            check_type(argname="argument ingress_from", value=ingress_from, expected_type=type_hints["ingress_from"])
            check_type(argname="argument ingress_to", value=ingress_to, expected_type=type_hints["ingress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress_from is not None:
            self._values["ingress_from"] = ingress_from
        if ingress_to is not None:
            self._values["ingress_to"] = ingress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def ingress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_from AccessContextManagerServicePerimeters#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_to AccessContextManagerServicePerimeters#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9072fc81a07ad50e42326e0247395116f86381f72fbc35ac6ea3f3ec183d8bc2)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identities that are allowed access through this ingress policy.

        Should be in the format of email address. The email address should represent
        individual user or service account only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc39d3689ecf3c690b26ab2c482c244568206f6d035ae9b621fe2a70734cb9dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a18a0aa5738f17b30abde2986cc322d553ba4a9a2c4f58f1449b0e17399267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eefc416fc5715bfd86afce72ee0fe32f32becca6371546829c4a7d2c2dc75ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ee802fc063934b0a4a0203cbff7ca495547474e7ee09852728bc56e24a686f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe4e7149a72bf9a0db93a3679051e156faa223cccd8eb4f257014abbe407ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects are allowed. Format 'projects/{project_number}' The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80832a016d9e694055603be26099c462bb9448379c80dd227b390a5bb2b16f4)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet.

        'AccessLevels' listed
        must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent
        'AccessLevel' will cause an error. If no 'AccessLevel' names are listed,
        resources within the perimeter can only be accessed via Google Cloud calls
        with request origins within the perimeter.
        Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.'
        If * is specified, then all IngressSources will be allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to ingress the perimeter.

        Requests from these resources will be allowed to access perimeter data.
        Currently only projects are allowed. Format 'projects/{project_number}'
        The project may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the case
        of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__085292a17de3c32ce83070b68e5b650041ce5cb46a646f5fe95c379944da2440)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1c18681703ace32bf6b923a8745a37eda7fede47a1a5345f44e859252ca9e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162764321515e7e87cb15a940f44214c9969d11eddb1ee12d6eafab092c5f99b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58afbee2478952737951a75bf69101007e7ef6816026ef0c8ec963f0a9a2505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff51a3565ce7da07a3facbd283fbd184e829d2e19eda26d2b878f0adfcf815c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c467706a308e7bb663cfc73cff3f4b582979a384c1ba58f135dc4fb915cf1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__603322aace6dcb24e76f2b265b3b92f028bee740030beabe5cdb45354975531b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bbc5d7f3f380f3b0b59db022793ef06723b0b65dd6980bcb73096609e56765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0dea92c66e3d0e696fdca7c5b3779f2540ac728660d86ee5c956fa55cadb98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a483071c0e05dd2e494270a4c5e1f85e1aa6f43de87dd55265aa935afa2071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cea687ebc16ed5e2ee9b09b302df21dbeac65b13ea3bb7a443d934bf9fec3c)
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff427f0631f5708c73b09e92edad04f4deb559062ef366d7c4f4f271b8cd042)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76e298471d3de8ed6350fbcbb11322dd5bccba287a2b36d8d0a7a7c23855f1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd4f58d9ef012293423db2d42bc623407e2ac66de4efe5880f1bacdc6aea96a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d53ac2eb0300ee4ff6119f877de2ae7b071767c28caa138013180d844c1529)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19b9e1624efe7290c0d3b2deb6575c3ea5c8215f41236c75caefa74a8f7101d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5da62ca6042bf1bf7421c1e981cba8339e01d6436cb12fdce636d9685e09369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a261b4d6531c0bb503520192af5d800320a8483ed0c281ab62e6fefbdd971c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f0f85128f856a3d14f16e35c1d9a05b04cd76b692a5aed4f8cf498adf224be)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'.

        If '*' used as value for 'method', then
        ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37b406475d6feef9fa77911f0fbb3bb33d462d17012b88135c0b8940f3c0ed4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1121b76b7166f2627509a4095e19b54d0ce2899c15bf5b936afd0bda98a4885b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f15923242bdc2970ab894eab58da6a551398293b5f579956ad4eb16f7c6271)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f97706262acce9f2bde0c13ca832ec76c3cfd5a437cae0787a5aa087477324cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abdd6099f12891c25f3c74b49248e7a9d44921f5dbbe16742baa69b1efea18bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4b063e751611589a220823014fd838b08506b8ae5d367b0eebd9f66f5ffb1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4305c7cecbf4084723f976541ba58878165bb14bde5cb14c2742570fc5a5be4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158888f0df93395044c1bd6ff2190b2c3a998cfb0b219e7975b51ee91f85f932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bc509e65b16164dcdf4341b689289f90ad01831ad3ac873ec03c864f0a61e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62d1be43c75cf606a622d83c64c17b3af9c80b2032f635b4b1dfaefbe880e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f16a40a2b0e533371470b3943885f55f30d2be31bbf73dc84cda1c8d02eaa71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b167dc0266088e4fdebf748c755a0eabd7717b6dfd6d214cc63b3e8073e8c82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138ff1a3405fd2c5ad8c34800ac749a6cb79bc03bb147192ea2773b28adc63e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63aa96806df39daae271fe0e070d65df2b1725ebe2c6c362d6a2dce74598c112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c37bfe81178576f254c00aca2f719a837f92ad02bcafb6851be0968b61faeb80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8dd7852ab3fe4ef06eaee648f48e7406dbbc8701f74a94ec8b6993809cbf42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb89c61142a04ebb9a8492bfb64b35757aa2463dfe214e8e702e08aaed8e7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856d89264a1f9084c8ae1bb766907258b299b1bfb3789057e29e1c15e49fdbea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b267c0e9e7f640f69580e8dd10ce6eaaa32b0b7ac7526db55e182035f8b447ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc4736a3a9507e68819e6e0b086fbd05f484a63bc86fb02b27f8513adff45fc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc718116f218e2a98937e15579b99773e97ddba6c70612d5cddffb5928ab80d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ea4dfffe9f6b95ddf775a7daa632d35cf689c5800cdc0c1d02e5909cbea6b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82f256fdc4a992a64c79f9bd46ee657ca68f6464f9ca5c4fd2cfb0e9255195d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef57d67b71b683429565f15c5819e80d5e28cf9a9941ee6bbe830062ba0be26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5a41c54f2c24d12dcae11da485a86f485359cf116c8563989238a93959c268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d19af31a819781ac97203dc63a1296157608fd80601994ead7cbd511e781977)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIngressFrom")
    def put_ingress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo(
            operations=operations, resources=resources, roles=roles
        )

        return typing.cast(None, jsii.invoke(self, "putIngressTo", [value]))

    @jsii.member(jsii_name="resetIngressFrom")
    def reset_ingress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressFrom", []))

    @jsii.member(jsii_name="resetIngressTo")
    def reset_ingress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="ingressFrom")
    def ingress_from(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference, jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference, jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo], jsii.get(self, "ingressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ede4a960fc7a97c89c07cf0a3af2f289db4315b5ab5db54d269e2120283d00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710000f81d129f2a6feb6e8cbf12edfb5bfb90bf04cec15788fd8265b44cf6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d78b15d316d06280c3ddb65eaaa5954a44306af2f3279be5973fc0fe5a1e5b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressPolicies")
    def put_egress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2f7f0b0e261f685250c3c56db1056b3896aa5679dafad58d892ca8d1e3e697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEgressPolicies", [value]))

    @jsii.member(jsii_name="putIngressPolicies")
    def put_ingress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362e125d922d7c6f7c095c838cd568153ae57d539664d3730f4f50d227680dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngressPolicies", [value]))

    @jsii.member(jsii_name="putVpcAccessibleServices")
    def put_vpc_accessible_services(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#allowed_services AccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#enable_restriction AccessContextManagerServicePerimeters#enable_restriction}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices(
            allowed_services=allowed_services, enable_restriction=enable_restriction
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccessibleServices", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @jsii.member(jsii_name="resetEgressPolicies")
    def reset_egress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressPolicies", []))

    @jsii.member(jsii_name="resetIngressPolicies")
    def reset_ingress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressPolicies", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRestrictedServices")
    def reset_restricted_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedServices", []))

    @jsii.member(jsii_name="resetVpcAccessibleServices")
    def reset_vpc_accessible_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccessibleServices", []))

    @builtins.property
    @jsii.member(jsii_name="egressPolicies")
    def egress_policies(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList, jsii.get(self, "egressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="ingressPolicies")
    def ingress_policies(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList, jsii.get(self, "ingressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServices")
    def vpc_accessible_services(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference", jsii.get(self, "vpcAccessibleServices"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="egressPoliciesInput")
    def egress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]], jsii.get(self, "egressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressPoliciesInput")
    def ingress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]], jsii.get(self, "ingressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedServicesInput")
    def restricted_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServicesInput")
    def vpc_accessible_services_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"], jsii.get(self, "vpcAccessibleServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27668b27ec99e9d38991a9364c07cef250604ad27412f0d1c2032ed27fe669dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1731d42addcc4abf32626875e593cc96f4e80329c532026e6e60502b117c73d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedServices")
    def restricted_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedServices"))

    @restricted_services.setter
    def restricted_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e44864b3d577c3906015d3c9548fa206f0ceb9b9f28b7d6f0d4ed621d0904bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpec]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a4629e2483d1578da01a23b2fbec851f60c3a184189284348e843f0c24c814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services": "allowedServices",
        "enable_restriction": "enableRestriction",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices:
    def __init__(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#allowed_services AccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#enable_restriction AccessContextManagerServicePerimeters#enable_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08518110bc6021d0a6f511117793194d2850a2f66dbd5730eeaa96fcebf7c8e2)
            check_type(argname="argument allowed_services", value=allowed_services, expected_type=type_hints["allowed_services"])
            check_type(argname="argument enable_restriction", value=enable_restriction, expected_type=type_hints["enable_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_services is not None:
            self._values["allowed_services"] = allowed_services
        if enable_restriction is not None:
            self._values["enable_restriction"] = enable_restriction

    @builtins.property
    def allowed_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#allowed_services AccessContextManagerServicePerimeters#allowed_services}
        '''
        result = self._values.get("allowed_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#enable_restriction AccessContextManagerServicePerimeters#enable_restriction}
        '''
        result = self._values.get("enable_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8bf2068bb696bfbedb309dbd5312541671fc316d7d473a94e61f7334e06f9bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedServices")
    def reset_allowed_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedServices", []))

    @jsii.member(jsii_name="resetEnableRestriction")
    def reset_enable_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="allowedServicesInput")
    def allowed_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRestrictionInput")
    def enable_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedServices")
    def allowed_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedServices"))

    @allowed_services.setter
    def allowed_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf25f3100a12ee69d02d915004e7c67872e503c7d56390ab5ba1c0b0f14b0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRestriction")
    def enable_restriction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRestriction"))

    @enable_restriction.setter
    def enable_restriction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bed6f9ba706ba0c85c7624c193b97e0be9752d867ef6decd412305013bdf5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b937b30337a20ed623adb0f3cff84f4802b091cfdb9660fec7b55e90caca2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatus",
    jsii_struct_bases=[],
    name_mapping={
        "access_levels": "accessLevels",
        "egress_policies": "egressPolicies",
        "ingress_policies": "ingressPolicies",
        "resources": "resources",
        "restricted_services": "restrictedServices",
        "vpc_accessible_services": "vpcAccessibleServices",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatus:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_levels AccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_policies AccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_policies AccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#restricted_services AccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#vpc_accessible_services AccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        if isinstance(vpc_accessible_services, dict):
            vpc_accessible_services = AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices(**vpc_accessible_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3bd3f0f6aef338a7b6935a30f7b328d8211e59fe573a1314eeefa8bc0b77d7)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument egress_policies", value=egress_policies, expected_type=type_hints["egress_policies"])
            check_type(argname="argument ingress_policies", value=ingress_policies, expected_type=type_hints["ingress_policies"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument restricted_services", value=restricted_services, expected_type=type_hints["restricted_services"])
            check_type(argname="argument vpc_accessible_services", value=vpc_accessible_services, expected_type=type_hints["vpc_accessible_services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels
        if egress_policies is not None:
            self._values["egress_policies"] = egress_policies
        if ingress_policies is not None:
            self._values["ingress_policies"] = ingress_policies
        if resources is not None:
            self._values["resources"] = resources
        if restricted_services is not None:
            self._values["restricted_services"] = restricted_services
        if vpc_accessible_services is not None:
            self._values["vpc_accessible_services"] = vpc_accessible_services

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet.

        AccessLevels listed must be in the same policy as this
        ServicePerimeter. Referencing a nonexistent AccessLevel is a
        syntax error. If no AccessLevel names are listed, resources within
        the perimeter can only be accessed via GCP calls with request
        origins within the perimeter. For Service Perimeter Bridge, must
        be empty.

        Format: accessPolicies/{policy_id}/accessLevels/{access_level_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_levels AccessContextManagerServicePerimeters#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def egress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies"]]]:
        '''egress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_policies AccessContextManagerServicePerimeters#egress_policies}
        '''
        result = self._values.get("egress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies"]]], result)

    @builtins.property
    def ingress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies"]]]:
        '''ingress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_policies AccessContextManagerServicePerimeters#ingress_policies}
        '''
        result = self._values.get("ingress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def restricted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''GCP services that are subject to the Service Perimeter restrictions.

        Must contain a list of services. For example, if
        'storage.googleapis.com' is specified, access to the storage
        buckets inside the perimeter must meet the perimeter's access
        restrictions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#restricted_services AccessContextManagerServicePerimeters#restricted_services}
        '''
        result = self._values.get("restricted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_accessible_services(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"]:
        '''vpc_accessible_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#vpc_accessible_services AccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        result = self._values.get("vpc_accessible_services")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies:
    def __init__(
        self,
        *,
        egress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_from AccessContextManagerServicePerimeters#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_to AccessContextManagerServicePerimeters#egress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        if isinstance(egress_from, dict):
            egress_from = AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo(**egress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7695f3d877318d12c7174cf877cf79789a8c8978d11230a1f87a30d71b858bfd)
            check_type(argname="argument egress_from", value=egress_from, expected_type=type_hints["egress_from"])
            check_type(argname="argument egress_to", value=egress_to, expected_type=type_hints["egress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_from is not None:
            self._values["egress_from"] = egress_from
        if egress_to is not None:
            self._values["egress_to"] = egress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def egress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_from AccessContextManagerServicePerimeters#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#egress_to AccessContextManagerServicePerimeters#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this 'EgressPolicy'. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#source_restriction AccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fa0d2bf000d4165b6097ef5549cfe21e95ae57f7318253f73f9238dc72afbb)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument source_restriction", value=source_restriction, expected_type=type_hints["source_restriction"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if source_restriction is not None:
            self._values["source_restriction"] = source_restriction
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identities that are allowed access through this 'EgressPolicy'.

        Should be in the format of email address. The email address should
        represent individual user or service account only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#source_restriction AccessContextManagerServicePerimeters#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c720fe7368db2c834d936e0e1cab72d7b55bc506440ee7494a432870aa8cbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f860fe125746540e6c5d36f28bf837d123c0a465f457e71099ae367669bc420c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSourceRestriction")
    def reset_source_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRestriction", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRestrictionInput")
    def source_restriction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac1d89cc64bf4178c9be64af0d8f2674cf6414a299e65fd4827356bcae4cd37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f300bd1a49bb976f3b783b62d41416d21396319a50c9c676052b2b256778b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86bfb256d67fcc051728465b9f813b30e37b8df9f72918e9ff07d19ef2d9abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ad0e4d75f78271b55a33ba3d380907822a3d2677b03eadea4673d8fb4b1dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b611f37d468b3eb70d6ceb851537bf4055c9c6b1596cce741d5a6cdb720a64)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to egress the perimeter.

        Requests from these resources are allowed to access data outside the perimeter.
        Currently only projects are allowed. Project format: 'projects/{project_number}'.
        The resource may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the
        case of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1902c5fba2618bceb58e6ae603fb63d26f0bccdbb24d193a17e20ba92ad5a08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab8c844db69f6bc1be9d4038ad28bd8e9b7134de3b8ef5ee87d750ad48cd21c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9274e4490c5a0c022974d1c26c4278f8382ac565a781af286b3e82b7a8f274ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__343698fc33c2244ccbae4747aa47c205f5436094ac4cacab7b5bbd257cdbec45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba9bdb233fc52083abb81e27e6fce17de7cbc723761a4a7118383b6ee7e7f4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d66ce9970826418012404fb36274a9e180f5e4a46ccfede7d7c77110412dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b87b4502984a207ff7646ace120174fd453648a2ec8d2811d92df25c7ae2db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ff356a2ddde7fc2084d6585ae24bde6eddc4801b4e47da76ab8448d46f8e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f149d24a25a8bbdd60c1a4d57c87d753dd207c5895995d53b7f1b2cde62633ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7990e202be937fee0fa41a23a133840fafb905ea10f7dbe32fb4601e3c34c731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#external_resources AccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6101f857cf4cf5d696721317c0ca84f368b3d3720c7a1bff24b16edec59c6fb)
            check_type(argname="argument external_resources", value=external_resources, expected_type=type_hints["external_resources"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_resources is not None:
            self._values["external_resources"] = external_resources
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def external_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of external resources that are allowed to be accessed.

        A request
        matches if it contains an external resource in this list (Example:
        s3://bucket/path). Currently '*' is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#external_resources AccessContextManagerServicePerimeters#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a9cbf286093d343dad42ccb8df6425891760a71ba411bf956cb48ea1c292b6)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c97718d184a6639c93d6ddadf12d40ac0d10fa9b3f456576f52775edb26080c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1077beaa3827059153ef19dbe9d333c47b7817dd3385300f47bd80e1741e2272)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f0b5f7ea4a61029f5ecdacfdc54d4e8275bd7fe98ca4aa0b1342c1cf6ed7bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5660a3db9f90c893b3f4e8dfc5a10c03369f62f80b4f72a255808f02547983bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04a8d620b95b0bfbe5c53b598fd12ce4c4de05606e564d91266e4ed01044d521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d02b1af372b8eb54e418880259dcd894ad25d4dc0c9f4abcfefab4915b10dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1479bab99e44463526516d1ddbe2c69fc0a45bed51b1e3d4465f1b9482e8c4)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'.

        If '*' used as value for method,
        then ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d3c46850119a0555102dd1dfb7ea035b92f52726b91217bd5977ae983081c17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6225370144a5e668a63b9b909a42d96b049b80306b0c7763858d2b75792271)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e56df1efe6a55f3e9319348727f06d8e05e70107b3dcc6dd6ea5ecbccaceee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c1a8efdfa010cb3ecfcd4e0dabcce85cb4ae85ce32b7fcb1cc66681014062f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5752ad6dfb951e8f0b10c7f98635669b61f7d058b1565e664bf3afd7b49fde81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3466f28b0478a04a6afebe7a4e1a45d935aa3f53985b3989be2a1b910ad81f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__502d6d44839f6e847cf6e363c7b98cc150b6ada911dae78eb9d6537817241094)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a31fa6d5658891968446e6f5054080cf90aef430f4b42ffb069e45c484bd1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b85606691cf86259ac1a189ea063494f1e79ded16a66e8d1f49fb360b5e158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b023e8d609e2c887b90d990c4471b048b1f8a442f400d49bb4637e952607158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52308fdebb0f3c99088c89e1fa5a299814c532e9584e7f717e5a4f69a211384d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2d83be92ec47bcd12055b16f93d76ece8c827403c7ed6aadfc7a9e9006718e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a49baaf899793ebb0736eadd5bde9ee787c48a32f3be3f1cbfd32849b38e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44c248e9f3dcb3e8c24fa9388dd200d3c84fb07896aff9a8e7eca8139dfee74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d95ce91f950d66abfd9587b7c60e9ca51bd487e3cbe77cdcfce6bf973e815f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1bcf482cfdc106666b1c1f494f1ccfb9453d576940084092048897b88e7718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetExternalResources")
    def reset_external_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalResources", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="externalResources")
    def external_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalResources"))

    @external_resources.setter
    def external_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d03a3b57dca9a6a3511f664adf03214dcf04cc97d0a2196e297fc66f54888c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43dd8b5af2a74cbe736f0f2cdd15bf40e5f08dc8037f92a33affa9f04437222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec1a4895b89b5952797106575c184e6d601b7fede4e78cdc43be16f9d985a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e1206a8127c6e8fcbf0a0592f838d3538e37c84e0ed1f37c9d40c9af4e70ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f74dc0813e80f49fc1d05c72060325ed8dab3d93a68fa94ad143686f3da50198)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe8cd20fb9496cb1d10bb3f9b8cf767014346340d95aadb8ef527659155207a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1b9f297f552be5e2b8e39711f844af2da83e6363714427456dfee5db70faf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5fc251bcddb6cf9ffc9d0503c50f3ccdcde48bc39342d9ae02dd0a600695939)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86f463316341a2d4a692c7a53d19857e19d0edbc13ae7b21570b9710fd0e29da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78dba7df66649f4462ef6b6959c18368546c006c1e888599cb03db6f5c30842d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc809bad3770179274d4353edc4bad0341c1283089523e7819bdc8081e4852e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEgressFrom")
    def put_egress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this 'EgressPolicy'. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#source_restriction AccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom(
            identities=identities,
            identity_type=identity_type,
            source_restriction=source_restriction,
            sources=sources,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressFrom", [value]))

    @jsii.member(jsii_name="putEgressTo")
    def put_egress_to(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#external_resources AccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo(
            external_resources=external_resources,
            operations=operations,
            resources=resources,
            roles=roles,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressTo", [value]))

    @jsii.member(jsii_name="resetEgressFrom")
    def reset_egress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressFrom", []))

    @jsii.member(jsii_name="resetEgressTo")
    def reset_egress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="egressFrom")
    def egress_from(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference, jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference, jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo], jsii.get(self, "egressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094634721a657f7d9b19eed5543a8556feb002f0872e55f52b7a1a8f8ab36d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3c86d755d35003fa8f7c1bcd86f960b1fd28498beaf63b5df22f107024f68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies:
    def __init__(
        self,
        *,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_from AccessContextManagerServicePerimeters#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_to AccessContextManagerServicePerimeters#ingress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        if isinstance(ingress_from, dict):
            ingress_from = AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo(**ingress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec146dd6d0bc59a1910e31f4253979ff34adb3fafcc963a79d5003a218d254d5)
            check_type(argname="argument ingress_from", value=ingress_from, expected_type=type_hints["ingress_from"])
            check_type(argname="argument ingress_to", value=ingress_to, expected_type=type_hints["ingress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress_from is not None:
            self._values["ingress_from"] = ingress_from
        if ingress_to is not None:
            self._values["ingress_to"] = ingress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def ingress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_from AccessContextManagerServicePerimeters#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#ingress_to AccessContextManagerServicePerimeters#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#title AccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b479cda59a4b25f948bf8bd9c4d1d563cafc84976d45766128afb883ceaf0568)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identities that are allowed access through this ingress policy.

        Should be in the format of email address. The email address should represent
        individual user or service account only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29495f3bdb50030b86bc32d8d12396f83b60de289a60b1312f59febed189ba12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500e44ff62e70e0600553d034a1db4b8af7b08657c705f5abda0ae745d9dc693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6422f4d8c2169b8156c4cfc802b69fa0cf7d91e62ad247e89d6776650dc17476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673f179dbee43872ad464f3fb539047fb124b7c6ad0c9dd4490ecbc87b154fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09927459399d191f3d50c28e8e7f8bf34b9377dcb4ffced97f4057af5429eb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects are allowed. Format 'projects/{project_number}' The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07882a668f479875f36ca6a72e917e46a6f9bb7955facdb2cdfd058b8025b575)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet.

        'AccessLevels' listed
        must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent
        'AccessLevel' will cause an error. If no 'AccessLevel' names are listed,
        resources within the perimeter can only be accessed via Google Cloud calls
        with request origins within the perimeter.
        Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.'
        If * is specified, then all IngressSources will be allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#access_level AccessContextManagerServicePerimeters#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to ingress the perimeter.

        Requests from these resources will be allowed to access perimeter data.
        Currently only projects are allowed. Format 'projects/{project_number}'
        The project may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the case
        of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resource AccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3fa9432fe25649bcf44041011af7f4afeb8358db0f71c90dbe278a55aa69a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9633144a56f4645238d49b6cf6c1751cefa79dddcf1e498527db913973525ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f0c4abb3b1221bc2ea993eb11a4167ed5b3bf5c2d79ebbdd901991aacb5cc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d26a6384acfc51867c24b7203b45f6aa00db51f1c494a874fa1b9b4675fcb863)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccb1f4f0fa72c07d06c9d8102b040068e784851eb717d05c369d53303f8e0033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0760c92025b8538eafcfbf42bf684db8e2a30be8f2b68a7b8a4a0deb90928d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__710367f153ceeaad8c1529ec1cdd93a3f143674161407dafe205206e9635a312)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815423983d1fdc7edf2928821e17b8dbbe9d6b45dd19d17015b34d7d88321fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f483b78389bfb1f0c8741cc4754a0b54c11a9387663add455303a320902736a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6036c671c334cc509670f38f93111ee4908b2bfb1f0ec89e20ad4fb9f87bebf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf1f4ddf80925e50d62402980ea5db0c1329f60f74d0196925fb3aa649ed1a0)
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51127e251c8dfad0e4f11d03228089969f949cd3bf6762634189967118c82658)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method_selectors AccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#service_name AccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdcfe982fae71db3c66dcc786ef7f73a8989aa78d13321221efabfecf6d73219)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709b51fc982baaad196df0fe74766d3162eeb5a0f418c8d5bd831d674063e62e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7857d336962a03303fab130e75873715671d0af7c839b2b99543b87627db0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12d21fddb21699597cdd0351f63b9fcde52d8900dd653a2f0baf8b672a27cad6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53a81540398ea10eda474bdd2f7839c20c50c3cd8e2ba463607299631d394a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10bd9e5fd610a39193dd7d7656dd24805da6e2c918e0f57033275803c0c34d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0167aa9d7a1710f42e373d340608fd7665d91f45b3ee53bc84950ab38137b5d)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'.

        If '*' used as value for 'method', then
        ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#method AccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#permission AccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bc89b040eabebb74e73c99e0e3770e8cb83db4c9a0f3b67bcdc25f9ee195664)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3334fdf7305f4e8103e081fdd6d4461998941f30e13af8089e72616139cddbc8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633bce7033346dc1a0239a2a375a59c4b8afb631ea1ecc6ef191e52ef8bd704c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de9a3b2df7c0f7847e291e165d8f5ca180f796e07f288ab1aef5f565d8b0b712)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eba6464104f630e2f5334014d45e3d2b7962f4895e08cd85905e633393cf718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccdf860a271058e6fea59d0857aaeffc26b90c50bc046574fd1b22b8e670674e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0dfd6eb1456385a596c139dcc3961379050afa0124ced9b80884ea8fd39bd90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6692788d9bec09d7ee5e41d552c055cb7c76b275abe52294fcfd5780103b379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a802d7688e622c5629564a47864b5841a61ef26f54d5f3dbeaf219e7cc068e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2837c4ec46d580897d7943c887eab8a155ed856acbc0df609eb5d59de9d2d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5907eec738c3adb1fa84f7ab6eeeb83f86c4d265afa294306cdbe43d8519af71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93ecebf25e7ec0bb7b578a5cf466928a1b4d74a9eb371dbadd30d68d500754a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d24e24516fcdf2d04e0c2cc6eb0eec195fa1b2aa16f8ba12ce460b9a19c9f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8281611da730b661f9dce8d041fb52add4a6bd0721fb18592462958ec91ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7554f94039b241cf61803e914db40dc4cd06970794b4b270fe207c16e9a2f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31471fb9c03d66c27199f9dc474ee0eb3f8b895c1092846c10cf52786bab9d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2411e67db2f9442595c51376883f3cdb90d43290177029dc48fd46d2012f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085a7b6d6da81867cc08587bb60952b4833da5bea145db6857e8478e417a1c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6f95c3d6f4c9b462506e4b76a3b611045092d9a859b3ca7e6c2681c3c3210e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe692dfcec9be1c4e98ec7cfa1e7cdfb60769e5fb15f1fe47dcaa52d6875faf3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cdfbb0a0cd7e1a6a062b9488bbe81fd4ce4a798ecbd3ab044fdc6f9b84bcf3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482b3ac09c0846351cb6e2e7cca20abf188437360d72b5fb371906a30a5ed992)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6108aa5d956c9e7533482f5c89c4d663033edf0546887280c05c85e07865f43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0646fb45b683012b7ff69e5f07e13bb6e8cf7aab5c845c8be78ea1e1f66fb94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e33f0ecfccf630820592a8fd089f76d438cab5ef3b773d2199e133691a4cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e91bc0c69ac1695698a7ea1a8c4e772b9ff32931dbf7bef582b2ad0215eee411)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIngressFrom")
    def put_ingress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identities AccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#identity_type AccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#sources AccessContextManagerServicePerimeters#sources}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#operations AccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#resources AccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#roles AccessContextManagerServicePerimeters#roles}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo(
            operations=operations, resources=resources, roles=roles
        )

        return typing.cast(None, jsii.invoke(self, "putIngressTo", [value]))

    @jsii.member(jsii_name="resetIngressFrom")
    def reset_ingress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressFrom", []))

    @jsii.member(jsii_name="resetIngressTo")
    def reset_ingress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="ingressFrom")
    def ingress_from(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference, jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference, jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo], jsii.get(self, "ingressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2defc57ac4a66f1fb7f9c9bf2184618b4cf696568a319ff6645acd76343d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809ff00968cd45684d07d547c29438f63c91b596c95fad859001ef1c9521bde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimetersServicePerimetersStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a026f936b7edb8410d6be14aae73b34732041f680c0a4ed9df687368aca810c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressPolicies")
    def put_egress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b9053b4e0da01f366e5a94bf9265fd3792e4b7730f956325dbcb505dfeb96c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEgressPolicies", [value]))

    @jsii.member(jsii_name="putIngressPolicies")
    def put_ingress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d5bd61315eed87ca8dd4d08053ef6c4d3242448112adcd97167c921dfc51d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngressPolicies", [value]))

    @jsii.member(jsii_name="putVpcAccessibleServices")
    def put_vpc_accessible_services(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#allowed_services AccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#enable_restriction AccessContextManagerServicePerimeters#enable_restriction}
        '''
        value = AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices(
            allowed_services=allowed_services, enable_restriction=enable_restriction
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccessibleServices", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @jsii.member(jsii_name="resetEgressPolicies")
    def reset_egress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressPolicies", []))

    @jsii.member(jsii_name="resetIngressPolicies")
    def reset_ingress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressPolicies", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRestrictedServices")
    def reset_restricted_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedServices", []))

    @jsii.member(jsii_name="resetVpcAccessibleServices")
    def reset_vpc_accessible_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccessibleServices", []))

    @builtins.property
    @jsii.member(jsii_name="egressPolicies")
    def egress_policies(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList, jsii.get(self, "egressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="ingressPolicies")
    def ingress_policies(
        self,
    ) -> AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList, jsii.get(self, "ingressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServices")
    def vpc_accessible_services(
        self,
    ) -> "AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference":
        return typing.cast("AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference", jsii.get(self, "vpcAccessibleServices"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="egressPoliciesInput")
    def egress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]], jsii.get(self, "egressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressPoliciesInput")
    def ingress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]], jsii.get(self, "ingressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedServicesInput")
    def restricted_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServicesInput")
    def vpc_accessible_services_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"], jsii.get(self, "vpcAccessibleServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c178fe6165fb097d4971768e2dacd9130fac4c0b753bfecf0e3160d5edfd7a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf61223ff8428a6d1805272c77bec53265740bde08db64e4b40da47a39e8befd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedServices")
    def restricted_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedServices"))

    @restricted_services.setter
    def restricted_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31f63008a4b00beffb18e89571a81bb38342f5bc2035879f666c89c6f8d6986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatus]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf00e38b2fa97cbf863e21de6a9dbcba49c78b71638b84cb1e51c5d0829b7baf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services": "allowedServices",
        "enable_restriction": "enableRestriction",
    },
)
class AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices:
    def __init__(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#allowed_services AccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#enable_restriction AccessContextManagerServicePerimeters#enable_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1724c0cdd499cdb17097bf5d052a8c1f9db09ef7c976ddee30f52c3d1f3efe)
            check_type(argname="argument allowed_services", value=allowed_services, expected_type=type_hints["allowed_services"])
            check_type(argname="argument enable_restriction", value=enable_restriction, expected_type=type_hints["enable_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_services is not None:
            self._values["allowed_services"] = allowed_services
        if enable_restriction is not None:
            self._values["enable_restriction"] = enable_restriction

    @builtins.property
    def allowed_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#allowed_services AccessContextManagerServicePerimeters#allowed_services}
        '''
        result = self._values.get("allowed_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#enable_restriction AccessContextManagerServicePerimeters#enable_restriction}
        '''
        result = self._values.get("enable_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d5b5dc89ab12f9cdf12aa0de80a2e4cf7ef4288982cc4e4efdd083d784095f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedServices")
    def reset_allowed_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedServices", []))

    @jsii.member(jsii_name="resetEnableRestriction")
    def reset_enable_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="allowedServicesInput")
    def allowed_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRestrictionInput")
    def enable_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedServices")
    def allowed_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedServices"))

    @allowed_services.setter
    def allowed_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a8be223d08ac8a2c04102cb2545191a3f5cc3c046ef3bf33ff024dc9758436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRestriction")
    def enable_restriction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRestriction"))

    @enable_restriction.setter
    def enable_restriction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ea70c9c699cd4b3b10df8d9a19b120ab6363530e70c197c5aa10aec0dc33fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe15143a577b96fda6e3547e01cc184ec6d02b2047e16a65e95a885c0832f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessContextManagerServicePerimetersTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#create AccessContextManagerServicePerimeters#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#delete AccessContextManagerServicePerimeters#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#update AccessContextManagerServicePerimeters#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5963dfa1fa1a92203f3b86a3ed83f230ee5be9905760dd52142e5969289f9d05)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#create AccessContextManagerServicePerimeters#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#delete AccessContextManagerServicePerimeters#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeters#update AccessContextManagerServicePerimeters#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimetersTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimetersTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeters.AccessContextManagerServicePerimetersTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83745032a13ebe3ddb50c702054ab3c03ff3a6ac0e6ac4568816bc882d2cbbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f491fbcd4a996e2f2d32c30a435a4c4d72e1cd467de00b96f128e62ce3db9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd976e4c07f71d50ea89eb1e4e6e12388e2782203390bc822bece8d2e99e591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eeb9488eda5a35edef3b3c30d8495574b8247b6ffd29c1cbec228b995aee14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1eb74ef95f56705442b27b8b5a85cf2ce10350bdfefae6223cd8fee9c67173b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerServicePerimeters",
    "AccessContextManagerServicePerimetersConfig",
    "AccessContextManagerServicePerimetersServicePerimeters",
    "AccessContextManagerServicePerimetersServicePerimetersList",
    "AccessContextManagerServicePerimetersServicePerimetersOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpec",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList",
    "AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices",
    "AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatus",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList",
    "AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusOutputReference",
    "AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices",
    "AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference",
    "AccessContextManagerServicePerimetersTimeouts",
    "AccessContextManagerServicePerimetersTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__20511537904f8d642d8951bb064f6628a9c5a512759ebde77eeba1e736057443(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    id: typing.Optional[builtins.str] = None,
    service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimeters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimetersTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__692bfd9e948c83e7946f5bd4715d7e7371a351c9c0578680deb5692ab10fb0a6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9155ed35bb8c12ec27eba53f876da50943ce2010586c76a1b2c5dc1b6a79d278(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimeters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631ed769051cf24fa8bf3a50555fc1bc24084f5ca3ce8926ae474bb14820f8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ac3049fb0b06674e186a93c4f0340961eb62288bab7193213ab4319cbd280a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd838d90a72b55f4d9d4bdf91501eef94468f1de3ad6262aa03a7510c4e89e13(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    id: typing.Optional[builtins.str] = None,
    service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimeters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimetersTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad80091b91c130052f3d00c5ac4be25b3f18aced723460939542ba1902f47938(
    *,
    name: builtins.str,
    title: builtins.str,
    description: typing.Optional[builtins.str] = None,
    perimeter_type: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c6d00e0d00675bf19a4b39459c895fb55d61d494cea0c8ef5349aa904b7f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7883de5adcd195a69b5377dd4006d3b26f65de0d57ada4c5ac9658fd87278331(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2821cdf32a4249d160a6e4decc3d51066808fbd09142fac20c58085376e9d7a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6d0887b90c17e87ac7558834d2f0e18167ca9bd12a78814564b2cd90e77fe0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00601aa992c4bb27148d8f5cb14fdc1fd8ce332cb8e476d5b09751219591969c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c38a810195501dfd11c5fc07a4c124ab1edc6c08faa732183ee184a7d5910b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimeters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fca80ac926fdf2e8e1b8403d0e55df3d35e1c1e7d0090f91269f4b453ebc90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac1fb2d34dd1dd39a207e493a29089d7792525d7f7fdf104caacff01320bd84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c58909c279674995a38ddc30eb28d414f806ec2cafba5a89c79749a7819d6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec34e5c347634b2e453103b14b8c21655a22bf9acb9f05fbb379348cfa7d34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecba00de86f43c0b478071ae7aa5309b2b9322beb0c3c7358d7de47e3c9bb8bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0218df3f77f5a244b7c63832ab64bbe9539b1f94c5d8c8a5a2d7e706708d1b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2d470f61a8ba43d21759f4f313278cef86ef8feeaf28a4a3f7c7ac9c50bc46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimeters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f687bc982fc859ec56680688b6193187525de8c5a0e9632366da52f1ebfbb5ea(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_accessible_services: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304162195f6de9798f7333074ecc7a9f01dffcecf3a8a6f421f6c295db32fcaf(
    *,
    egress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de63a26e640eee4e5e43f9bc117f905357bf16fce521ab522858e1a8e5b727e(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273220e67f028a9f18475eba8beef9302f66fffb3d14d7e3b3de0f7e2a058830(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff7e724a73322e174610387a6ee96aba2f07c9e52da2333b35ec61d82c42f81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c691bd9fa2194c863dc81412b054a548ac64060cc459d5dbbe02a23fe7eed8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b995c91dd7b8d533182e3a60b5e1a4f15512cacd0a23ea142fc0fdfe52aebb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a44da70b358048311d94201c9755b7198923ede60bb926ebb2819421fa10aef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cc5f1d7ec85ae8a23e53b01d34ece9b5e4c69e19b731c6da6c5a4dd353cdd0(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a736b1e2a5b4c143528db17cf0e10854e188137795a9cb7ea7e6e34fd4455bc9(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f3e09c4edb32214d4f671cb583be4ce20cd085208afd9d83ba321960123e3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93147fd2545c48a06f527587351d7b4ff72679d7189d7b55e6af44b71aeaad2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38360c37c09ecb93ad25e1f4ad9ea6fd64e05d78d8b98132731ee9ec08ba2e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378ee99b7dfc142cbb8b51dbbf3236ff8bb3d99802cd1690f7a3fe104c5be63b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0624794076f5cf73e169d5a4b6150f749fb73b6ec9a96604c3f9e426ddc54d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf386c3b17e230ba98c97b9105a3081858e43dc8cb00f908cd77c3bff518ca88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb26fc899866c35836bb60aa56b4a643fb333365ad353263c398152d0a93741e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6d12c43c67bdd12d61a933b5a82519ad23720dfb56fe22bcc26cc315648a95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cb37bcc40ada38d0ffc20bfac8768dbc98b9eacea9f2f1f76d1425fe19f84b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e6dc07b79dafb5ccf7bc8884d9a36ee80d0473cfc71955432814a6f9ef24a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ad5f4fd4e05942a594a97f876703894f98f6193dc0e53ecd25958cafc1baf8(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8c0914a2e1c62859d6db6c9ceed359dcddad21896b5f23d25ffe0e0d1c4d9b(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cca87b850114d23162c77025b7884c4503849c213e2da06cb0331b519a7298b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07918e5b342ea3a0786e27a1ffa812d3f6010f3e8e4ba319d656d8516e4262b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762f159b24a9517167d52a7f04e8e3887d6e5dd22d47ebe8bd34372a23e98e9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301563821486c244eb4cbff184dd4f2d54dac705ebd8b335341efccebeef7295(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e2fa79a51edcdbef591d095d04c51f24adb612af83e1aebba6d735e80892bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60908b2e39cc56aa74d9af33d78ac1b9f3a9d58c8acbf50322d4afb2309e58ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe527a2096a44d7560612cfc69257da8b67579719a94358578a46b3f8d6301c(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6770e6523eab18616aa5232837d90a7895dd818cdb3939a106367f5482c034d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9d07529133b40c7695e40c373fb3c8f2425b527e13616383f56c60a502e1b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ba4fc37c8a740e7f50c3288605761a988f7991885d656ad00a916966be4550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e77baa97fbd787a2a2bcad039b747ffeb2717c92be4f78d16b253151c08b6fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6eb4a556ba79d595eef13e06e1bea60ac31cc610cde664ac49b294d075b4bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c522f786be3e64c182f1b82732551f61560478b37df0a7807a2cb09c281eea7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0938fa434a4d2034d0215f253df512c68d70b468f8080f89e3a9abf0cb4a8c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5710c0c0273d081995c95c3d441e8eca5b5c76a407a39d23aa9a6ef5288b662c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cc3b033c0afeaaf4e206c42bd5a8e69345d4140231fb86ac778c397c05f4cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c1e4d99fbd002f9dbcf9669becb214cdea84f47daa71aa5c5785671106a3f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681acb625fb7d6f81fabb6eb13429c27a6a18b7e7ea09fd9dbfa5513be123e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd7182940eaf5a34f3cdade98d8d77b50294332ae72ccdd1273ebd6cabd65bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cb301ee98819a421d165c9b5344edb9042e180001c4963883f4589573fd7a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1568e5b678a696bf35d6d9c2dfbb47df595a05780ac71bad7c95d33d2e499c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32140d1966ea6a367acb63adac16e0c6e150490d2ecc1c12fa490cd2b52269e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242825bf74a9a410c56bc5d578439bcb18c9197b386e3ce7bf7aeb9a1729f896(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ca2e918882c501d89ef14fa1a036025cbb6ac8b657fc9882c28c1cabbe2347(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4477eca30891d0e60ccaa3efbe3280006c6b72fb50144d6bd2725094b523e0ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a0b0ef22bb5b737cd6b4a335ad4afac60a0a425a5eacce4b11985fa0d3f1e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b04bb3444e046cf223b37af6f8aa51489b8c3460d5090099c0bbf4fbdeeaca3(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf20dcd46917dff50d572cff2d39bbcf38ca698dda6d22c4083f0e5ba07d91a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0d6c1faaf9b7b6a5331f9f6fb92c9a8eaa28565d6a8afe3f04be5410432ebb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cba011cd40c8384c8dd3a29f9959e9e4e5670e0d2ba021cfd324a8c2fd77775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0dd4d586d77406a271a434708e9db5d3982fcfc9dedd9fa2c5bf97c85ca9e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee4b801e14103d28ef3499238a5dcbb06917cd596d2323b1c39b0d8bcedb60e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c58b0a26e3d5f7a367ea19f30b6fa0b73a0da550273ff0af1a01390a62123e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5145e4e566e2f12a283b4ecddd6508eb18321d27abe56fa81cbd65d849ee871(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3085df03cbe0b090c7bcd3694225183b71254b97df293bcc4c2d0edf0a0cce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eef1a45656c3855c0a5488aaba45c80db0ce4b3710814336e777690dc34635b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebce31978098e2da81b907dedf8686d94675331f55521a5323fa560fc0566cf(
    *,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9072fc81a07ad50e42326e0247395116f86381f72fbc35ac6ea3f3ec183d8bc2(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc39d3689ecf3c690b26ab2c482c244568206f6d035ae9b621fe2a70734cb9dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a18a0aa5738f17b30abde2986cc322d553ba4a9a2c4f58f1449b0e17399267(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eefc416fc5715bfd86afce72ee0fe32f32becca6371546829c4a7d2c2dc75ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ee802fc063934b0a4a0203cbff7ca495547474e7ee09852728bc56e24a686f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe4e7149a72bf9a0db93a3679051e156faa223cccd8eb4f257014abbe407ae6(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80832a016d9e694055603be26099c462bb9448379c80dd227b390a5bb2b16f4(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085292a17de3c32ce83070b68e5b650041ce5cb46a646f5fe95c379944da2440(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1c18681703ace32bf6b923a8745a37eda7fede47a1a5345f44e859252ca9e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162764321515e7e87cb15a940f44214c9969d11eddb1ee12d6eafab092c5f99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58afbee2478952737951a75bf69101007e7ef6816026ef0c8ec963f0a9a2505(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff51a3565ce7da07a3facbd283fbd184e829d2e19eda26d2b878f0adfcf815c9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c467706a308e7bb663cfc73cff3f4b582979a384c1ba58f135dc4fb915cf1b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603322aace6dcb24e76f2b265b3b92f028bee740030beabe5cdb45354975531b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bbc5d7f3f380f3b0b59db022793ef06723b0b65dd6980bcb73096609e56765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dea92c66e3d0e696fdca7c5b3779f2540ac728660d86ee5c956fa55cadb98e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a483071c0e05dd2e494270a4c5e1f85e1aa6f43de87dd55265aa935afa2071(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cea687ebc16ed5e2ee9b09b302df21dbeac65b13ea3bb7a443d934bf9fec3c(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff427f0631f5708c73b09e92edad04f4deb559062ef366d7c4f4f271b8cd042(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76e298471d3de8ed6350fbcbb11322dd5bccba287a2b36d8d0a7a7c23855f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd4f58d9ef012293423db2d42bc623407e2ac66de4efe5880f1bacdc6aea96a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d53ac2eb0300ee4ff6119f877de2ae7b071767c28caa138013180d844c1529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19b9e1624efe7290c0d3b2deb6575c3ea5c8215f41236c75caefa74a8f7101d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5da62ca6042bf1bf7421c1e981cba8339e01d6436cb12fdce636d9685e09369(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a261b4d6531c0bb503520192af5d800320a8483ed0c281ab62e6fefbdd971c5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f0f85128f856a3d14f16e35c1d9a05b04cd76b692a5aed4f8cf498adf224be(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37b406475d6feef9fa77911f0fbb3bb33d462d17012b88135c0b8940f3c0ed4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1121b76b7166f2627509a4095e19b54d0ce2899c15bf5b936afd0bda98a4885b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f15923242bdc2970ab894eab58da6a551398293b5f579956ad4eb16f7c6271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97706262acce9f2bde0c13ca832ec76c3cfd5a437cae0787a5aa087477324cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdd6099f12891c25f3c74b49248e7a9d44921f5dbbe16742baa69b1efea18bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4b063e751611589a220823014fd838b08506b8ae5d367b0eebd9f66f5ffb1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4305c7cecbf4084723f976541ba58878165bb14bde5cb14c2742570fc5a5be4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158888f0df93395044c1bd6ff2190b2c3a998cfb0b219e7975b51ee91f85f932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bc509e65b16164dcdf4341b689289f90ad01831ad3ac873ec03c864f0a61e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62d1be43c75cf606a622d83c64c17b3af9c80b2032f635b4b1dfaefbe880e00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f16a40a2b0e533371470b3943885f55f30d2be31bbf73dc84cda1c8d02eaa71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b167dc0266088e4fdebf748c755a0eabd7717b6dfd6d214cc63b3e8073e8c82(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138ff1a3405fd2c5ad8c34800ac749a6cb79bc03bb147192ea2773b28adc63e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63aa96806df39daae271fe0e070d65df2b1725ebe2c6c362d6a2dce74598c112(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37bfe81178576f254c00aca2f719a837f92ad02bcafb6851be0968b61faeb80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8dd7852ab3fe4ef06eaee648f48e7406dbbc8701f74a94ec8b6993809cbf42(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb89c61142a04ebb9a8492bfb64b35757aa2463dfe214e8e702e08aaed8e7de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856d89264a1f9084c8ae1bb766907258b299b1bfb3789057e29e1c15e49fdbea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b267c0e9e7f640f69580e8dd10ce6eaaa32b0b7ac7526db55e182035f8b447ca(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4736a3a9507e68819e6e0b086fbd05f484a63bc86fb02b27f8513adff45fc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc718116f218e2a98937e15579b99773e97ddba6c70612d5cddffb5928ab80d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ea4dfffe9f6b95ddf775a7daa632d35cf689c5800cdc0c1d02e5909cbea6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f256fdc4a992a64c79f9bd46ee657ca68f6464f9ca5c4fd2cfb0e9255195d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef57d67b71b683429565f15c5819e80d5e28cf9a9941ee6bbe830062ba0be26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5a41c54f2c24d12dcae11da485a86f485359cf116c8563989238a93959c268(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d19af31a819781ac97203dc63a1296157608fd80601994ead7cbd511e781977(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ede4a960fc7a97c89c07cf0a3af2f289db4315b5ab5db54d269e2120283d00a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710000f81d129f2a6feb6e8cbf12edfb5bfb90bf04cec15788fd8265b44cf6fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d78b15d316d06280c3ddb65eaaa5954a44306af2f3279be5973fc0fe5a1e5b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2f7f0b0e261f685250c3c56db1056b3896aa5679dafad58d892ca8d1e3e697(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362e125d922d7c6f7c095c838cd568153ae57d539664d3730f4f50d227680dfd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27668b27ec99e9d38991a9364c07cef250604ad27412f0d1c2032ed27fe669dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1731d42addcc4abf32626875e593cc96f4e80329c532026e6e60502b117c73d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e44864b3d577c3906015d3c9548fa206f0ceb9b9f28b7d6f0d4ed621d0904bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a4629e2483d1578da01a23b2fbec851f60c3a184189284348e843f0c24c814(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08518110bc6021d0a6f511117793194d2850a2f66dbd5730eeaa96fcebf7c8e2(
    *,
    allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bf2068bb696bfbedb309dbd5312541671fc316d7d473a94e61f7334e06f9bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf25f3100a12ee69d02d915004e7c67872e503c7d56390ab5ba1c0b0f14b0ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bed6f9ba706ba0c85c7624c193b97e0be9752d867ef6decd412305013bdf5bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b937b30337a20ed623adb0f3cff84f4802b091cfdb9660fec7b55e90caca2b5(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3bd3f0f6aef338a7b6935a30f7b328d8211e59fe573a1314eeefa8bc0b77d7(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_accessible_services: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7695f3d877318d12c7174cf877cf79789a8c8978d11230a1f87a30d71b858bfd(
    *,
    egress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fa0d2bf000d4165b6097ef5549cfe21e95ae57f7318253f73f9238dc72afbb(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c720fe7368db2c834d936e0e1cab72d7b55bc506440ee7494a432870aa8cbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f860fe125746540e6c5d36f28bf837d123c0a465f457e71099ae367669bc420c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac1d89cc64bf4178c9be64af0d8f2674cf6414a299e65fd4827356bcae4cd37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f300bd1a49bb976f3b783b62d41416d21396319a50c9c676052b2b256778b45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86bfb256d67fcc051728465b9f813b30e37b8df9f72918e9ff07d19ef2d9abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ad0e4d75f78271b55a33ba3d380907822a3d2677b03eadea4673d8fb4b1dbe(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b611f37d468b3eb70d6ceb851537bf4055c9c6b1596cce741d5a6cdb720a64(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1902c5fba2618bceb58e6ae603fb63d26f0bccdbb24d193a17e20ba92ad5a08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab8c844db69f6bc1be9d4038ad28bd8e9b7134de3b8ef5ee87d750ad48cd21c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9274e4490c5a0c022974d1c26c4278f8382ac565a781af286b3e82b7a8f274ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343698fc33c2244ccbae4747aa47c205f5436094ac4cacab7b5bbd257cdbec45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9bdb233fc52083abb81e27e6fce17de7cbc723761a4a7118383b6ee7e7f4bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d66ce9970826418012404fb36274a9e180f5e4a46ccfede7d7c77110412dfc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b87b4502984a207ff7646ace120174fd453648a2ec8d2811d92df25c7ae2db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ff356a2ddde7fc2084d6585ae24bde6eddc4801b4e47da76ab8448d46f8e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f149d24a25a8bbdd60c1a4d57c87d753dd207c5895995d53b7f1b2cde62633ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7990e202be937fee0fa41a23a133840fafb905ea10f7dbe32fb4601e3c34c731(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6101f857cf4cf5d696721317c0ca84f368b3d3720c7a1bff24b16edec59c6fb(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a9cbf286093d343dad42ccb8df6425891760a71ba411bf956cb48ea1c292b6(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c97718d184a6639c93d6ddadf12d40ac0d10fa9b3f456576f52775edb26080c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1077beaa3827059153ef19dbe9d333c47b7817dd3385300f47bd80e1741e2272(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f0b5f7ea4a61029f5ecdacfdc54d4e8275bd7fe98ca4aa0b1342c1cf6ed7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5660a3db9f90c893b3f4e8dfc5a10c03369f62f80b4f72a255808f02547983bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a8d620b95b0bfbe5c53b598fd12ce4c4de05606e564d91266e4ed01044d521(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d02b1af372b8eb54e418880259dcd894ad25d4dc0c9f4abcfefab4915b10dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1479bab99e44463526516d1ddbe2c69fc0a45bed51b1e3d4465f1b9482e8c4(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3c46850119a0555102dd1dfb7ea035b92f52726b91217bd5977ae983081c17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6225370144a5e668a63b9b909a42d96b049b80306b0c7763858d2b75792271(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e56df1efe6a55f3e9319348727f06d8e05e70107b3dcc6dd6ea5ecbccaceee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c1a8efdfa010cb3ecfcd4e0dabcce85cb4ae85ce32b7fcb1cc66681014062f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5752ad6dfb951e8f0b10c7f98635669b61f7d058b1565e664bf3afd7b49fde81(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3466f28b0478a04a6afebe7a4e1a45d935aa3f53985b3989be2a1b910ad81f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502d6d44839f6e847cf6e363c7b98cc150b6ada911dae78eb9d6537817241094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a31fa6d5658891968446e6f5054080cf90aef430f4b42ffb069e45c484bd1b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b85606691cf86259ac1a189ea063494f1e79ded16a66e8d1f49fb360b5e158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b023e8d609e2c887b90d990c4471b048b1f8a442f400d49bb4637e952607158(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52308fdebb0f3c99088c89e1fa5a299814c532e9584e7f717e5a4f69a211384d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2d83be92ec47bcd12055b16f93d76ece8c827403c7ed6aadfc7a9e9006718e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a49baaf899793ebb0736eadd5bde9ee787c48a32f3be3f1cbfd32849b38e97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44c248e9f3dcb3e8c24fa9388dd200d3c84fb07896aff9a8e7eca8139dfee74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d95ce91f950d66abfd9587b7c60e9ca51bd487e3cbe77cdcfce6bf973e815f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1bcf482cfdc106666b1c1f494f1ccfb9453d576940084092048897b88e7718(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d03a3b57dca9a6a3511f664adf03214dcf04cc97d0a2196e297fc66f54888c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43dd8b5af2a74cbe736f0f2cdd15bf40e5f08dc8037f92a33affa9f04437222(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec1a4895b89b5952797106575c184e6d601b7fede4e78cdc43be16f9d985a27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e1206a8127c6e8fcbf0a0592f838d3538e37c84e0ed1f37c9d40c9af4e70ea(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74dc0813e80f49fc1d05c72060325ed8dab3d93a68fa94ad143686f3da50198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe8cd20fb9496cb1d10bb3f9b8cf767014346340d95aadb8ef527659155207a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1b9f297f552be5e2b8e39711f844af2da83e6363714427456dfee5db70faf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fc251bcddb6cf9ffc9d0503c50f3ccdcde48bc39342d9ae02dd0a600695939(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f463316341a2d4a692c7a53d19857e19d0edbc13ae7b21570b9710fd0e29da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78dba7df66649f4462ef6b6959c18368546c006c1e888599cb03db6f5c30842d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc809bad3770179274d4353edc4bad0341c1283089523e7819bdc8081e4852e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094634721a657f7d9b19eed5543a8556feb002f0872e55f52b7a1a8f8ab36d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3c86d755d35003fa8f7c1bcd86f960b1fd28498beaf63b5df22f107024f68c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec146dd6d0bc59a1910e31f4253979ff34adb3fafcc963a79d5003a218d254d5(
    *,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b479cda59a4b25f948bf8bd9c4d1d563cafc84976d45766128afb883ceaf0568(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29495f3bdb50030b86bc32d8d12396f83b60de289a60b1312f59febed189ba12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500e44ff62e70e0600553d034a1db4b8af7b08657c705f5abda0ae745d9dc693(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6422f4d8c2169b8156c4cfc802b69fa0cf7d91e62ad247e89d6776650dc17476(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673f179dbee43872ad464f3fb539047fb124b7c6ad0c9dd4490ecbc87b154fe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09927459399d191f3d50c28e8e7f8bf34b9377dcb4ffced97f4057af5429eb2f(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07882a668f479875f36ca6a72e917e46a6f9bb7955facdb2cdfd058b8025b575(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3fa9432fe25649bcf44041011af7f4afeb8358db0f71c90dbe278a55aa69a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9633144a56f4645238d49b6cf6c1751cefa79dddcf1e498527db913973525ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f0c4abb3b1221bc2ea993eb11a4167ed5b3bf5c2d79ebbdd901991aacb5cc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26a6384acfc51867c24b7203b45f6aa00db51f1c494a874fa1b9b4675fcb863(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb1f4f0fa72c07d06c9d8102b040068e784851eb717d05c369d53303f8e0033(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0760c92025b8538eafcfbf42bf684db8e2a30be8f2b68a7b8a4a0deb90928d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710367f153ceeaad8c1529ec1cdd93a3f143674161407dafe205206e9635a312(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815423983d1fdc7edf2928821e17b8dbbe9d6b45dd19d17015b34d7d88321fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f483b78389bfb1f0c8741cc4754a0b54c11a9387663add455303a320902736a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6036c671c334cc509670f38f93111ee4908b2bfb1f0ec89e20ad4fb9f87bebf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf1f4ddf80925e50d62402980ea5db0c1329f60f74d0196925fb3aa649ed1a0(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51127e251c8dfad0e4f11d03228089969f949cd3bf6762634189967118c82658(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcfe982fae71db3c66dcc786ef7f73a8989aa78d13321221efabfecf6d73219(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709b51fc982baaad196df0fe74766d3162eeb5a0f418c8d5bd831d674063e62e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7857d336962a03303fab130e75873715671d0af7c839b2b99543b87627db0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d21fddb21699597cdd0351f63b9fcde52d8900dd653a2f0baf8b672a27cad6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a81540398ea10eda474bdd2f7839c20c50c3cd8e2ba463607299631d394a5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10bd9e5fd610a39193dd7d7656dd24805da6e2c918e0f57033275803c0c34d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0167aa9d7a1710f42e373d340608fd7665d91f45b3ee53bc84950ab38137b5d(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc89b040eabebb74e73c99e0e3770e8cb83db4c9a0f3b67bcdc25f9ee195664(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3334fdf7305f4e8103e081fdd6d4461998941f30e13af8089e72616139cddbc8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633bce7033346dc1a0239a2a375a59c4b8afb631ea1ecc6ef191e52ef8bd704c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9a3b2df7c0f7847e291e165d8f5ca180f796e07f288ab1aef5f565d8b0b712(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eba6464104f630e2f5334014d45e3d2b7962f4895e08cd85905e633393cf718(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdf860a271058e6fea59d0857aaeffc26b90c50bc046574fd1b22b8e670674e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dfd6eb1456385a596c139dcc3961379050afa0124ced9b80884ea8fd39bd90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6692788d9bec09d7ee5e41d552c055cb7c76b275abe52294fcfd5780103b379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a802d7688e622c5629564a47864b5841a61ef26f54d5f3dbeaf219e7cc068e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2837c4ec46d580897d7943c887eab8a155ed856acbc0df609eb5d59de9d2d8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5907eec738c3adb1fa84f7ab6eeeb83f86c4d265afa294306cdbe43d8519af71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93ecebf25e7ec0bb7b578a5cf466928a1b4d74a9eb371dbadd30d68d500754a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d24e24516fcdf2d04e0c2cc6eb0eec195fa1b2aa16f8ba12ce460b9a19c9f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8281611da730b661f9dce8d041fb52add4a6bd0721fb18592462958ec91ead(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7554f94039b241cf61803e914db40dc4cd06970794b4b270fe207c16e9a2f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31471fb9c03d66c27199f9dc474ee0eb3f8b895c1092846c10cf52786bab9d5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2411e67db2f9442595c51376883f3cdb90d43290177029dc48fd46d2012f14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085a7b6d6da81867cc08587bb60952b4833da5bea145db6857e8478e417a1c09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6f95c3d6f4c9b462506e4b76a3b611045092d9a859b3ca7e6c2681c3c3210e(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe692dfcec9be1c4e98ec7cfa1e7cdfb60769e5fb15f1fe47dcaa52d6875faf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cdfbb0a0cd7e1a6a062b9488bbe81fd4ce4a798ecbd3ab044fdc6f9b84bcf3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482b3ac09c0846351cb6e2e7cca20abf188437360d72b5fb371906a30a5ed992(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6108aa5d956c9e7533482f5c89c4d663033edf0546887280c05c85e07865f43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0646fb45b683012b7ff69e5f07e13bb6e8cf7aab5c845c8be78ea1e1f66fb94d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e33f0ecfccf630820592a8fd089f76d438cab5ef3b773d2199e133691a4cbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91bc0c69ac1695698a7ea1a8c4e772b9ff32931dbf7bef582b2ad0215eee411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2defc57ac4a66f1fb7f9c9bf2184618b4cf696568a319ff6645acd76343d64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809ff00968cd45684d07d547c29438f63c91b596c95fad859001ef1c9521bde0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a026f936b7edb8410d6be14aae73b34732041f680c0a4ed9df687368aca810c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b9053b4e0da01f366e5a94bf9265fd3792e4b7730f956325dbcb505dfeb96c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d5bd61315eed87ca8dd4d08053ef6c4d3242448112adcd97167c921dfc51d4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c178fe6165fb097d4971768e2dacd9130fac4c0b753bfecf0e3160d5edfd7a68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf61223ff8428a6d1805272c77bec53265740bde08db64e4b40da47a39e8befd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31f63008a4b00beffb18e89571a81bb38342f5bc2035879f666c89c6f8d6986(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf00e38b2fa97cbf863e21de6a9dbcba49c78b71638b84cb1e51c5d0829b7baf(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1724c0cdd499cdb17097bf5d052a8c1f9db09ef7c976ddee30f52c3d1f3efe(
    *,
    allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d5b5dc89ab12f9cdf12aa0de80a2e4cf7ef4288982cc4e4efdd083d784095f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a8be223d08ac8a2c04102cb2545191a3f5cc3c046ef3bf33ff024dc9758436(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ea70c9c699cd4b3b10df8d9a19b120ab6363530e70c197c5aa10aec0dc33fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe15143a577b96fda6e3547e01cc184ec6d02b2047e16a65e95a885c0832f11(
    value: typing.Optional[AccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5963dfa1fa1a92203f3b86a3ed83f230ee5be9905760dd52142e5969289f9d05(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83745032a13ebe3ddb50c702054ab3c03ff3a6ac0e6ac4568816bc882d2cbbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f491fbcd4a996e2f2d32c30a435a4c4d72e1cd467de00b96f128e62ce3db9d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd976e4c07f71d50ea89eb1e4e6e12388e2782203390bc822bece8d2e99e591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eeb9488eda5a35edef3b3c30d8495574b8247b6ffd29c1cbec228b995aee14b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1eb74ef95f56705442b27b8b5a85cf2ce10350bdfefae6223cd8fee9c67173b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimetersTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
