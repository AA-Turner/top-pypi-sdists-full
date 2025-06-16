r'''
# `google_access_context_manager_service_perimeters`

Refer to the Terraform Registry for docs: [`google_access_context_manager_service_perimeters`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters).
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


class GoogleAccessContextManagerServicePerimeters(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimeters",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters google_access_context_manager_service_perimeters}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        id: typing.Optional[builtins.str] = None,
        service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimeters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters google_access_context_manager_service_perimeters} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#parent GoogleAccessContextManagerServicePerimeters#parent}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#id GoogleAccessContextManagerServicePerimeters#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_perimeters: service_perimeters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_perimeters GoogleAccessContextManagerServicePerimeters#service_perimeters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#timeouts GoogleAccessContextManagerServicePerimeters#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23560c1d2a29ff4d0f657dae94bd29192fc86a8b49fe2d942b658e623ae1ca71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAccessContextManagerServicePerimetersConfig(
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
        '''Generates CDKTF code for importing a GoogleAccessContextManagerServicePerimeters resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAccessContextManagerServicePerimeters to import.
        :param import_from_id: The id of the existing GoogleAccessContextManagerServicePerimeters that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAccessContextManagerServicePerimeters to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8c492fa4b7c462fef595ea55b2085b845298e44d69269a1cd87a341ca2dcb1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServicePerimeters")
    def put_service_perimeters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimeters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf492ec5ee57c7e2c3d6e706eb86b8c73b03e743b27e8118765674743fcd815)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#create GoogleAccessContextManagerServicePerimeters#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#delete GoogleAccessContextManagerServicePerimeters#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#update GoogleAccessContextManagerServicePerimeters#update}.
        '''
        value = GoogleAccessContextManagerServicePerimetersTimeouts(
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
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersList":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersList", jsii.get(self, "servicePerimeters"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleAccessContextManagerServicePerimetersTimeoutsOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimetersTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimeters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimeters"]]], jsii.get(self, "servicePerimetersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAccessContextManagerServicePerimetersTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAccessContextManagerServicePerimetersTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e4eeb5b70a5ab525a9b5e94276b37224ca129b4a78477e14527194ff71f429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af59dc20b949e5a8c85ee99b59263acd2438584d9446d1f1828b058c46888dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersConfig",
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
class GoogleAccessContextManagerServicePerimetersConfig(
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
        service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimeters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#parent GoogleAccessContextManagerServicePerimeters#parent}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#id GoogleAccessContextManagerServicePerimeters#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_perimeters: service_perimeters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_perimeters GoogleAccessContextManagerServicePerimeters#service_perimeters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#timeouts GoogleAccessContextManagerServicePerimeters#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleAccessContextManagerServicePerimetersTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fbeefe925919db09adbd43a1db886070eb2756bb6603020962493b84c371b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#parent GoogleAccessContextManagerServicePerimeters#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#id GoogleAccessContextManagerServicePerimeters#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_perimeters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimeters"]]]:
        '''service_perimeters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_perimeters GoogleAccessContextManagerServicePerimeters#service_perimeters}
        '''
        result = self._values.get("service_perimeters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimeters"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#timeouts GoogleAccessContextManagerServicePerimeters#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimeters",
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
class GoogleAccessContextManagerServicePerimetersServicePerimeters:
    def __init__(
        self,
        *,
        name: builtins.str,
        title: builtins.str,
        description: typing.Optional[builtins.str] = None,
        perimeter_type: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Resource name for the ServicePerimeter. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/servicePerimeters/{short_name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#name GoogleAccessContextManagerServicePerimeters#name}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        :param description: Description of the ServicePerimeter and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#description GoogleAccessContextManagerServicePerimeters#description}
        :param perimeter_type: Specifies the type of the Perimeter. There are two types: regular and bridge. Regular Service Perimeter contains resources, access levels, and restricted services. Every resource can be in at most ONE regular Service Perimeter. In addition to being in a regular service perimeter, a resource can also be in zero or more perimeter bridges. A perimeter bridge only contains resources. Cross project operations are permitted if all effected resources share some perimeter (whether bridge or regular). Perimeter Bridge does not contain access levels or services: those are governed entirely by the regular perimeter that resource is in. Perimeter Bridges are typically useful when building more complex topologies with many independent perimeters that need to share some data with a common perimeter, but should not be able to share data among themselves. Default value: "PERIMETER_TYPE_REGULAR" Possible values: ["PERIMETER_TYPE_REGULAR", "PERIMETER_TYPE_BRIDGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#perimeter_type GoogleAccessContextManagerServicePerimeters#perimeter_type}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#spec GoogleAccessContextManagerServicePerimeters#spec}
        :param status: status block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#status GoogleAccessContextManagerServicePerimeters#status}
        :param use_explicit_dry_run_spec: Use explicit dry run spec flag. Ordinarily, a dry-run spec implicitly exists for all Service Perimeters, and that spec is identical to the status for those Service Perimeters. When this flag is set, it inhibits the generation of the implicit spec, thereby allowing the user to explicitly provide a configuration ("spec") to use in a dry-run version of the Service Perimeter. This allows the user to test changes to the enforced config ("status") without actually enforcing them. This testing is done through analyzing the differences between currently enforced and suggested restrictions. useExplicitDryRunSpec must bet set to True if any of the fields in the spec are set to non-default values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#use_explicit_dry_run_spec GoogleAccessContextManagerServicePerimeters#use_explicit_dry_run_spec}
        '''
        if isinstance(spec, dict):
            spec = GoogleAccessContextManagerServicePerimetersServicePerimetersSpec(**spec)
        if isinstance(status, dict):
            status = GoogleAccessContextManagerServicePerimetersServicePerimetersStatus(**status)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a00c96006a5da3e2d3537ca9be4727f31d43a8ac1997925bc303da6ad21f4e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#name GoogleAccessContextManagerServicePerimeters#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Human readable title. Must be unique within the Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the ServicePerimeter and its use. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#description GoogleAccessContextManagerServicePerimeters#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#perimeter_type GoogleAccessContextManagerServicePerimeters#perimeter_type}
        '''
        result = self._values.get("perimeter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#spec GoogleAccessContextManagerServicePerimeters#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpec"], result)

    @builtins.property
    def status(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatus"]:
        '''status block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#status GoogleAccessContextManagerServicePerimeters#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatus"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#use_explicit_dry_run_spec GoogleAccessContextManagerServicePerimeters#use_explicit_dry_run_spec}
        '''
        result = self._values.get("use_explicit_dry_run_spec")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimeters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbf94993a8cd14dff85565577cba446a2e19b3054478aacc844dce3e61bb2e6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45eeb216b326a72caa00567ada4f3a6c29f7966fbc245e4032b517b4d6cd4ab2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfeb4c59c96e388a020438dac62ee08c1110bfa2aea821ca9cdf81c3cbc8ef49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f643af0fa3050d2f3b67487b61ddb4030db0fb2c8c1395c4a8a82d3a0889c50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf24ac1cfdb329c7b82141b17346868caa2709ac57eec3832b6eff17eb36607a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimeters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimeters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimeters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896dbc08c86c5cfa2d2c2b58283f9e238537d68faa7b600dc66e5fd58feafc22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b359c6049e007a1294ffb93e0397b290a1d3ac07979e7f3abe3ebcb4ac1cc1)
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
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_levels GoogleAccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_policies GoogleAccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_policies GoogleAccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#restricted_services GoogleAccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#vpc_accessible_services GoogleAccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersSpec(
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
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_levels GoogleAccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_policies GoogleAccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_policies GoogleAccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#restricted_services GoogleAccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#vpc_accessible_services GoogleAccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersStatus(
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
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(
        self,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusOutputReference", jsii.get(self, "status"))

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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpec"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatus"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatus"], jsii.get(self, "statusInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__aaed55fe8f7b59c29ab70c07bb3b199713bfa35d2bd17a69f7d42ad67aac2f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137258a116c6ace29297a5056e6ed881aba9726174ce179475e55c0d4506cbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perimeterType")
    def perimeter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perimeterType"))

    @perimeter_type.setter
    def perimeter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7143120d19c35b2e2f710369c3f0e0c6ccccb607577e1f3f778772fdaba0fcd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perimeterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032a53425dacf7471233ba0bdd03443492f821a7e909f0d7b3b3715dec1f7530)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da3048b1e727a1cc3f9736be0a770ba731a73094ddcd2adb573504658e7c43ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExplicitDryRunSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimeters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimeters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimeters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d3fa43fbdac0ae8bfc5c3202fc55bfc8e3743390ec24eec404c6b288d48157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpec",
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
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpec:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_levels GoogleAccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_policies GoogleAccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_policies GoogleAccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#restricted_services GoogleAccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#vpc_accessible_services GoogleAccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        if isinstance(vpc_accessible_services, dict):
            vpc_accessible_services = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices(**vpc_accessible_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12be117eb931eef77c919787dd0d1a11c1358e9e17cbdee274307c86e1ec4ee5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_levels GoogleAccessContextManagerServicePerimeters#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def egress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies"]]]:
        '''egress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_policies GoogleAccessContextManagerServicePerimeters#egress_policies}
        '''
        result = self._values.get("egress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies"]]], result)

    @builtins.property
    def ingress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies"]]]:
        '''ingress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_policies GoogleAccessContextManagerServicePerimeters#ingress_policies}
        '''
        result = self._values.get("ingress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#restricted_services GoogleAccessContextManagerServicePerimeters#restricted_services}
        '''
        result = self._values.get("restricted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_accessible_services(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"]:
        '''vpc_accessible_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#vpc_accessible_services GoogleAccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        result = self._values.get("vpc_accessible_services")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "title": "title",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies:
    def __init__(
        self,
        *,
        egress_from: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_from GoogleAccessContextManagerServicePerimeters#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_to GoogleAccessContextManagerServicePerimeters#egress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        if isinstance(egress_from, dict):
            egress_from = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo(**egress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a529de98004b42124355fb7c7fcac5e4e5f1729e4d1b5e79dfd743cc7c940c8)
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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_from GoogleAccessContextManagerServicePerimeters#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_to GoogleAccessContextManagerServicePerimeters#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#source_restriction GoogleAccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9a89c1767b2e616a99ad702a9778fd3e2616479f3df9aacb307f5f37429359)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#source_restriction GoogleAccessContextManagerServicePerimeters#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a7cf355cbc2ab6a2624e3bab73dc654bca8f9fcabbada9ec971e190c11d46dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c991030f76ac40cf4d5dd394a9eb414fa720f2460fc6ee6d8f6a03bf08b3f2c7)
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
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList", jsii.get(self, "sources"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d553fdb96119db514fe875def2413f035f500934911a463d3ddd06c15548135f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2091025ca7fa9c0977f8f879e8303d2e61a5ef08c5877b9fe95f047534c4d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8e8da90b51d42599a29039d57da3fea7221a8ee9ca4ce8c566fdba54713177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca876cacd5dd54ca20eda5c59661a33eb5a3032257689a9a492a4c97284775d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d217c91b775f98dc0cc76b86888ac0c1005f562a58b7e7762086ecec7c44fd1a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__680dbaa9d32afac613d145a0b587ac433b1a659224517b3f1a08478c4c16c919)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9643d658ac1997cdefcd5b3a7be1e9ece141d14780ad5a09ae51eded4d281c42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bbedace6cc630ff97fcfe9530026ad43fdaeb9f1abb618c90c06055f316841)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f0aa2b6688d3527893e6dcfcc620cc884be3c4f9cbb26028ce166424fb01b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__175157fde0832726368e4d5482ad1b9d2f1c2b49637ab1e35d17979657e7010a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c48e72b339257e3ac3328d2f8b788b595de06222c435da4d52fc8d2ae67088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc30bb0ae7b0c0f512a3481203656d16067f1e1c509e9ae877a742fc883cc22c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8778f127f58293d02743178afa0a5c62233d0935eb9f40624d9e7437ab486b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4059957e06b7ebe93edd077ccbbc6baabb4453b4e08e91b4aaa2e8b3a340e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6941b85734dd12a452ac2a1500e62130ae15b4eae9024aeebe059d69fda68f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#external_resources GoogleAccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e354ab7dc4144158b85541bb95d5d5a80ed109c60d8dc4b6c534c61f8bac93)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#external_resources GoogleAccessContextManagerServicePerimeters#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cccdf02dc206fb38137e458147dc1eacddec94d8d7d7979dd13a1087e58570)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dff78fc4c4f9774e5965482a39514fa72d47f96ab1ae4d83495ab0af81baa5e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f778ec791767a8ad131e72f05c2b8311c5d736eb3f73de8b8d6e739d36046e7c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9608123dc3104717fce9e9407a5c496b2ee71aa07d307e1bd76ffc598a46e05d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__619c144230da1dabe5110efab59d0c6ee47f05699374ed1c4dcf64f8b925a86c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0511259b799bc73f18db5baab8d358129c04361d490fbae59465634c8c5dea7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4a9f9f1ec4035b23557a316796b304212375398418ed55a548225e9b748d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151df337f0d3200c7d0b94bf424f8cd258de48f910a1ab436f3a148ff522d242)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3950c029844194cb2286d38c335f5f2e72aa8f84d18e954bda87f74cb627ba98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b2c408bbdd58cca78e2e1759eea73a3fbb9148676f988206a64c8624c963f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fa340900704d3cbd0f4c5b811b39af4996e4ea167bace7105bf69965599249)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c365fa44a8d787f47adb30811ed249ed6466ce2db4a3c7f848538cd0e35206)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a87d5e42d7b78002acb32f861e3952a4ecca4ab8af78e4a612f4685a79a8cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0d45db84ca83542699bb821086868cae0e12266ed761886a9050750f25acf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__358743150131f9ea7456b12ba95f830107e7d7d85e511e79999cbb594ba75d32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe445238ce7af8b519f78116b72ead5d71b194e0d6bdade16c20777cf956b041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915c143b4ca9cf322dca2c815f0d88a06f9a5a517ecbdba8218271ff4eb9dc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5158433e8e1eade16049da444aa72720740bf88a746ce964f31a6d20bdf950a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23e1dd3e9d51031242b8148f7ac58c47eabd728aa9166017baab3161a79d68e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b7c7200be42e11298aa0f404fba043f3ee7b62d7e9d221b6cbf9ca865d71f6)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__55131afc069a3670512d541c1a0b9df858c453cb39282d702a2b0c8dae23eb20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64acb45764e454353af6906ee087db66752dba9d3df6a7fd1cea0420c35742ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__404eb83e0194c954f3efa626382ee55b46b100ca6ef2b970caacafca896e1ac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b106e26d3ec9c5152c513e8872124d953bd421863106c396890313f7809afe9)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]], jsii.get(self, "operationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e0d08025e4ecdda766f1c2d4750f5dfe689ee5cd8dd6f0b6c1b313bece914b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cf6c795f36b66bf92ad9c49f094c1acbf1aa5b08ac78ca55553c6ebdc612c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff92cb0872adb1d3b0539d8f4a97651bb19dadfc8186763a14961f82bf54305c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752189c591387c163b5b05da18aff7f00afcb9163e048b9c7530fa9e236a2a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__677cd0c787ce064f0eef9cbba02db7b9cd8b194df96957be6635d52af9f4e9ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4361c1bacf15b768731b7982c639410394582fb94bed82fb397a0f344788087c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb9cf44079e87e07077286c66f80cb9b3fc88153129573d5bfde89ede3c2a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4318c5e091d7fceed3b81157729e4e4e2c8a47fdef1206a71c297fb2246bca0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5818ecdad73e8dfde0a6a5057b0b4ef42f2ed008c3bc41e7cb46ff4fb97a0c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5af523d1982f23b0c4b992dc59c986707eb839c23ee82960599577f9489bb13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f662170781f2cb7ff1d0f709bb4ff35b314d3b67ddc482afed7e62d61a3ddfa)
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
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#source_restriction GoogleAccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom(
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
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#external_resources GoogleAccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo(
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference, jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference, jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo], jsii.get(self, "egressToInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2996a09beb1d8a092d8ff626f40de30724f6150e0b3189728d662674c547cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151b19b19a09e02f5552cf187af461443eeeed55e6a04f6a3db0505eebef80cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "title": "title",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies:
    def __init__(
        self,
        *,
        ingress_from: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_from GoogleAccessContextManagerServicePerimeters#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_to GoogleAccessContextManagerServicePerimeters#ingress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        if isinstance(ingress_from, dict):
            ingress_from = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo(**ingress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75070ccedc888f8aca4ae5b2becd32dc6cd77c519c8ab98e21c1bae4f3a3bb4)
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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_from GoogleAccessContextManagerServicePerimeters#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_to GoogleAccessContextManagerServicePerimeters#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce45c5887476c7adea2801bb23a95c87ee75d30a665680aa2fe9d857ca5ade4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__513811d048204f0e1f5ead57ab8142a3f1400872f49876dcbe90f7c16e8a62f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1762416ffe21bbc554d77134c06978ce2c3151dbe9654852149845c9257c6e5)
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
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList", jsii.get(self, "sources"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203a496767bd81367674f4dc9fa6e27a3d37baff42e87afca877591b1f16353a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d43b6237d0b4b4da2b96899a5b8599f7b5d55c49289f11e140b233521bf9b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f101a4abcc7aa35213791fd5aa040e503837336e524ce4b4bfa53771551612f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects are allowed. Format 'projects/{project_number}' The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65daf89cbbbac9b85cb38649cfd5b7d46e5e28053dac9827013a9e61777f98c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__164cc718c3a29c7b77f50f9bb61e961f97cd31916d91ab9935de36974acd0bfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0ce27376e9d43c9fd6025347e846ca26470a458c65e2ce29e5c07754db5da6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262396f8d86174bf36bccb499163d57d3e3d086e86ff73adf314950352790ee8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b928c0426d951672e2785f0b58e1a82f5d6af67fbbdaa7b137157734e94a41fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8bbddb017ed7cee8eae89517145f264457b1eff30501c4cb9e9ddcf020de8d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d354a36b1ae2dd091e3d78958ee3a7e4ecbda004d2c0e40183bb76d6c68a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58c84f3e4ead031cfab72d6a27651ff10431dcff0e8192d89907349c6f59afa6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__339084c438aa7da1089158bf09f7d738102cf78777cb35fc6e7639996944d9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6214a3a4bdf78052d815e16fb3f38d8608f90b5383a1c675ddef4180242253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a831813538be55a5772a54718892d0d298e77bb8c63f538a6f2dd0bd7b75612a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589730695e84238777574600bbfad13cd160ed8fccd803f1bf0c9d004bc69863)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f81a6de92c072c4800b33fc630d2abc7071ad71d9021b9a1b6bc1f12963e7f)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dda0e6cff5624e911ac6fb24989948a5f2d5a4469f0cd95a5f7ac2b80133ae5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0244f07ceb1a66af9cfed17966985209aec755920efb7fe149cf936b64995c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9894ae4b9ab4c90a1ff440795b42d589415b02fec207363998964f57b850ce58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06d6887319fd4966373d3acc606d5f0974a1461ab2dc30c72cfe0cc791e1cc9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8d68f382d27a530c1aa63f14b6cdc6fd0e2ea6cb084bcf564921192331e6878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfde0b37ed1940d42922c35f1d372dddf6e4383531f04202c79c33243552cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943524f765bf88ff69b015ea8ada19130e09e91926320a77148551bce6fa8b75)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__024aabcc8cffe4f95ba1731b42897765af1cbe2bbc1c95f14c4413601e5167f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb728f26c0cda6aeadfc3e7438f9fa463316fcfe853f244d8a5321e56457ffd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6963dcb7ec9e775a4cc88b5f771a91259cdbcad53a88d727b50807fb36f5dec8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e9e4c58d7f38bb97dce5e2c4809a1df79cd8d5e627626efcda7714fefbce7aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e12d383090b958db904d4b97a13cadacae658e13691a88b6244f9fa516949ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faeaba8bb86c63460b3adf2f7bfc6e6c0833c156b8f577cb1e231edf5f7e2377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb1fe30694687d8ba498f4e6b896b41108c1f378ba10b01df1626b0e00aa948)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ffc11ce904c208f7285001ab49d672591c1cdd0ba79c51b9e97c108dadd083f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9030c0d11babb590c3b7fa29b1088cbc1e1a0756639ee3fce0c272d758e35eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0484bc9cb21b9eedff164db698d82f522899eebb66de99b04096f9b3665e8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f42a162dec83303d27a37767d18c62af32d79c3e3f440a3cfec08241e35e4f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9856565a1f91ccf8d49cad264e4662157e5b630d3ab616de0392fa701532351)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e7308321b8a1f7255082126a042f4d40048017bef0537b92f0ac94de1bdf72b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b116c7ec4cb604ddf4515fc510d83d9de5c7690afc802a69046885d4de81dfc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ace9d13971871ec13cd3bdabcbe532933ecb3aa1cc5bd00db389bca4c470c6e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8980e4d86ad840ea170ad6280b94c612901eed35ade1fc7cdbf274122968d229)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]], jsii.get(self, "operationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__744227b767e3922979729649f3631594313155f85f7ff57d5f2f52b41f71de8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ee9c420103c5baf014f716bf4ec0f9e0543c677399f12961835422c8619ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8840bcf5fae9696b726ce289eb512d4540a6eb4380a9255015dcbc4d9c79f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a12e136c868e04cd40dbf71301ab348e2d9d8e1d7340b34781cc6bad76e6f0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35986f442e5e9019047774509e1ae93b82d82922278003e6600e826e02bf6375)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939d3a8f2d2448f48695bdb0b82c38760b95863106917738eecd995411dbe5e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a8bc1a7ef23e0bde103c04863ade0cff30a8b4e03f0728278020e8d2d52ddb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac60a5cd198105a647d667913552a245ecbe56f88f7d4ca41f67a43bbc804652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1888f8d831ef859a40de52b437e674f524fb769ae68e7f3ebf5a8a882f2285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c0644c80766a22f3f77dd973d76d8a4af93e39cae2415426a8600c66578ae1)
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
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo(
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference, jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference, jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo], jsii.get(self, "ingressToInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4e7747aad9fa8f6aeb697d4fc35acf7e7bf7d7881017fc0d9a84fd5e5a2db3e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38233d194822a00ef0e6a22a8790e2d9ba0cb52da24591ecfa4e25693fd5565b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22c414d4145c6dff2251dac8486f26435db8447dc8aceaa491c3ed3447917822)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressPolicies")
    def put_egress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56748a4e9b7335af9beed6c20bbb6dcb524604520bc37ceeeddf50fa1b51678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEgressPolicies", [value]))

    @jsii.member(jsii_name="putIngressPolicies")
    def put_ingress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ee89c42a0721fd3682ae8a6345ce2b9a029a75a402afc5c552abd9e794a34a)
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
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#allowed_services GoogleAccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#enable_restriction GoogleAccessContextManagerServicePerimeters#enable_restriction}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices(
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList, jsii.get(self, "egressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="ingressPolicies")
    def ingress_policies(
        self,
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList, jsii.get(self, "ingressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServices")
    def vpc_accessible_services(
        self,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference", jsii.get(self, "vpcAccessibleServices"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="egressPoliciesInput")
    def egress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]], jsii.get(self, "egressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressPoliciesInput")
    def ingress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]], jsii.get(self, "ingressPoliciesInput"))

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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices"], jsii.get(self, "vpcAccessibleServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea8c8663a58fddee6f9f8207dd45d3bc0f974f493cfd63901d943a51774686c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7503277c3a9d1bfb788ebdcafdce8a26a183e8af17824521cba07bf247ab4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedServices")
    def restricted_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedServices"))

    @restricted_services.setter
    def restricted_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e51dcf976006a48c157538c482a31dff92a2ed1108a02c8beeb8d4647ed862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpec]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f437fb5c6437541f4314194cd19171f35a93a8138d34e267953fea56d6c2c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services": "allowedServices",
        "enable_restriction": "enableRestriction",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices:
    def __init__(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#allowed_services GoogleAccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#enable_restriction GoogleAccessContextManagerServicePerimeters#enable_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9486400287ce29f63d87ae47ba2fe25bad6491f1d0d1fc7baeda36f81150afaf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#allowed_services GoogleAccessContextManagerServicePerimeters#allowed_services}
        '''
        result = self._values.get("allowed_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#enable_restriction GoogleAccessContextManagerServicePerimeters#enable_restriction}
        '''
        result = self._values.get("enable_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93cd3d94bd587e930b84cca3a90a081ba0f91fb428cfb7d5a30d5ffca631c3ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca191099a15521139ec4eac22d1333715b78c9d8f54b1e7238907b9f3fcf2105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17a4e42ef2c75c54e850d62dd74cbed9cacfa1b35b15cdda07d26b491d64b114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcadc21d724ae061341cce27810e76df3675771a329ffd640af2c93ddc87faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatus",
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
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatus:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_levels GoogleAccessContextManagerServicePerimeters#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_policies GoogleAccessContextManagerServicePerimeters#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_policies GoogleAccessContextManagerServicePerimeters#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#restricted_services GoogleAccessContextManagerServicePerimeters#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#vpc_accessible_services GoogleAccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        if isinstance(vpc_accessible_services, dict):
            vpc_accessible_services = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices(**vpc_accessible_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9410635c96f6c77ed0d0ad26c4a904cfdc0ec76926fe551fbb34583905f503ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_levels GoogleAccessContextManagerServicePerimeters#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def egress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies"]]]:
        '''egress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_policies GoogleAccessContextManagerServicePerimeters#egress_policies}
        '''
        result = self._values.get("egress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies"]]], result)

    @builtins.property
    def ingress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies"]]]:
        '''ingress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_policies GoogleAccessContextManagerServicePerimeters#ingress_policies}
        '''
        result = self._values.get("ingress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#restricted_services GoogleAccessContextManagerServicePerimeters#restricted_services}
        '''
        result = self._values.get("restricted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_accessible_services(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"]:
        '''vpc_accessible_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#vpc_accessible_services GoogleAccessContextManagerServicePerimeters#vpc_accessible_services}
        '''
        result = self._values.get("vpc_accessible_services")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "title": "title",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies:
    def __init__(
        self,
        *,
        egress_from: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_from GoogleAccessContextManagerServicePerimeters#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_to GoogleAccessContextManagerServicePerimeters#egress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        if isinstance(egress_from, dict):
            egress_from = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo(**egress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2efec560495ec63993e702fd89d1c39a48f44927240c2fd25353e7f45a3ce1f7)
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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_from GoogleAccessContextManagerServicePerimeters#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#egress_to GoogleAccessContextManagerServicePerimeters#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this 'EgressPolicy'. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#source_restriction GoogleAccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e35c6b92f0a457e3ab2a8036ad531ab1e5b6193b5171b98ffa1afd524d0535)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#source_restriction GoogleAccessContextManagerServicePerimeters#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a74e2b3317bb2401af2bd97436c3a8ab6c1133ae547f924d46d353ea324b9e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb095440c28e2cb632064523a7efc4affb51284785e1769ac2763e571d69e77)
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
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList", jsii.get(self, "sources"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501731c52dc216acae37c1fefef48f97f69e404c52fc5f4dc9e3edc81494d5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9b19126062105d48da67a28fbd0b9042da0cd21527aa06019ae678a7b89204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7984b29ecf4e2dde429f1c2831cbede6243a052f116a017604f9980c9ff9b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75035971cb67a3fa377c477fa6da3a6e14f932e1bf6516bac1b775382c1ed3da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6e065a058e1e82fb6d5042d505fb3efa3f0f2c4aef57743221efa4ab1d15b6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e5bc4cccd769e7202a3a4c76366e61408c680739899847daec1b210080e22c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2796c9321aa7ee65d43f260f76dc92012e9ab6cbe5fb15d1701b6c4fc869f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f84071379092ff99b9bc18d675ebb7e99fe8c60aa3e8fa57414fa35b8921e88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a8d9851af7fb7be3aaa83921cb0f7eadce68c43e64de1d6f3ca7de1ef3354f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85a8a004645f3e735dab02d4fd32040ccfefb9ed9d44f2cd5a62d727c365d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f43f3478b6ea8d40d97feaf5a731f51257179491269e113f9be9c47779fa70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9465edfdcfa3f2059ae2868619c1133e5bc9ad5b4239711089e464a5a7cd9c87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eca2b16ab409ba15fbb8539cde7e5cf411629a93754cb8f5e400846c9f0492e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1372feb72bb659308415db369f067fd0bcf254568ff2dbd50821a414d2c6ea50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d088d4bafa78d5bc6fa482596bc27b3b3ab907da0682e5d3d9b1bf72fd7473d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#external_resources GoogleAccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fcddb8c860209262c5c89c166a95add2269617d0d3a6f0d6a8ebf50c23c8f2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#external_resources GoogleAccessContextManagerServicePerimeters#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a07af8cc6fca17b41ddf380b1cce59ec70d9deff59681901dc980a88e500802)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f695379d06719123f97d61518f2f5369ffee71488651996f15abd301155a9902)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9915e1d3724f31b2596879519731cd79014ec08a39f14231cad9af17c812a659)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15fe96dd7f144ea12461184cbbec5966c22933eff67a867e15251d60a83b97c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a7379bbed5cc109fb07bdeb2e128b8211231853288c404416c3887874fb1839)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a408c6ffebf077d8e28050d4df8339de94f99fe3c3b90e41a081333996932e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb89c497955f9cfe07362b516944bbad4e50c6de132bfcf441e1fa3bac0be10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afe7bc7357452dfb993e78f9029d6815ec7571e255053e0a9daf176cedb9cd1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6359397eab1cc4b26e48ab66c1aec1425c05b9344100627092055142065d446b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e998a528618f7076728edad42b4ee04c758824011a65abb05e92bc58ae51e27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79699d8fbfd117013e5a79fae113402dd3560238df6dfc5baac0f697806f589)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2346ca8533210781c225733be4899b7b861a5083ad1e051c6c85241af0b968b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__953fd761c2b037488079c7d8f38eeb76b256160db4e62403b07a41cf3211c268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603f25d4f1a5aa374c45063487cacb435428d5a5238c560a4a95f443c7ccac48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f4272fdfb6db46f4dcbf5593eef008e915ea0656ad5673d1055a2f0a9a8609)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f91d45040707a2797da58b6eb26654006dcb3fc39a0c953e4da5bc6ed8f08f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a797e8304fba2bbc05234803b9ae35adecc5cb3d168d09e0de4ff585378bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01bcc29c0190dbff572815a5e3d6c3ea57e0c13ecc3e7d76a15959f4c8be070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08a74f03d07c150c945bd7e1fb2df576300328f0105f2e36590ada8bef468b64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01170567185bb3057c06509745225fb4f8347a0becdfca6caba61e8b1cf448a5)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8272509c50026c2be0e29a1ac37c3f8bad27ddd41fc981198447754c31bd1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5d1e3885b316cd1be25e687efef27da2aa0b4541a4ab6e2f5a7579c745b346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19b0b82b2797847eda9cba90b35177f5cf86719fc8e319b9fedeb441a717a507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4c161e3283287b7521375a4d0612c427e220a01a61b68c088d688450b28f43)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]], jsii.get(self, "operationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__38a1090e6f160115631be6024d7e3f60c36633cbeb9c439ff3b2bd938d1df9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947646cb6da4f401a7d76953a0c132acf5ed827cdf6d5e04527f5d89ae4a8bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fee75e9ef24b8bca8942c7f0e3bef4ea0367fb0f85113d31c35432bb349c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436d0da928862019d3915ddc9281b16682c43381fa92cded9c4ec1cd4edfab70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69dff1e0fecf56acd7aae4288344d5ef2113e75ec4fc41028da629603c73b85a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e991c79bfb60183328bb4377aa6699ca3d1aec9ef6b05096c1da5b18f9f522b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ec82be8352f787e92295a9912f4f919bd2161d56b2f4a24859e702ef3d147f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e25de9ebf7556f29cefd4501d004bc495134e4715b8df09ce277e3b87f306fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48318f4194e208c98550aee511796566a6b5b3557018cde002ebfe4bdb069b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc829795b130cbe84c063e9c2970bb0dd3bd9fe085dbc4f69f1b9af401c98dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b0aba8f8b0f6ac2456100458f3a5a87d5f191e1023f32205ee2dd3590f7a6f)
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
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this 'EgressPolicy'. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#source_restriction GoogleAccessContextManagerServicePerimeters#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom(
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
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#external_resources GoogleAccessContextManagerServicePerimeters#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo(
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference, jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference, jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo], jsii.get(self, "egressToInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__62e91c730ee4d503c0792a3fad38b9691b9fd14e026246eb2911ff72c49caaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8292a00fe604110ba26661a0cfcc21797cd44c4ac1e94cc101b466be31fe93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "title": "title",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies:
    def __init__(
        self,
        *,
        ingress_from: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_from GoogleAccessContextManagerServicePerimeters#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_to GoogleAccessContextManagerServicePerimeters#ingress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        if isinstance(ingress_from, dict):
            ingress_from = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo(**ingress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512ad852d274550a6b4b26325862f061653bcc7ed75aa05467a34728d48a9e83)
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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_from GoogleAccessContextManagerServicePerimeters#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#ingress_to GoogleAccessContextManagerServicePerimeters#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#title GoogleAccessContextManagerServicePerimeters#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc3e0362506b7057f55003cd0d33b3663a9a78bb9fd4f2e8175b5c9fbdee641)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56eeec589e3ca7368be62ee22cf46df948a17770fef5df3be6b38daba41a3071)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296bbaa640fb1f2cd2606d09c19416073145afcb8f3cc0059b00fecbc6bf4e73)
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
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList", jsii.get(self, "sources"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c108114a75b8a6df6fed9f59da177fef27c7819c6abeae11c49a19c98fa2fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b0d8c508b8e0e4c232e61ca38d6fc6addbd8116fd38a95d9b140eb0a6803c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b529ad6e68568ca5316a5f0039d7a12793d4f00897ef085f1c2997e910785c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects are allowed. Format 'projects/{project_number}' The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eca63a2cd243da1336db697516ee903beea56012a0f45a5283f34155bb99d23)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#access_level GoogleAccessContextManagerServicePerimeters#access_level}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resource GoogleAccessContextManagerServicePerimeters#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a418d2a53d0adf5a199ab29a1550ceba87588b78efb56f7926e0572bc3f173a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f806eeedc8983ce74e75802437ecd91050ed499c652f07a462d10665b917b78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d573dcb8029783da1efa96490f77cef700791bb6f5031281b22ac8e0763b8977)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f5f66cba71d7371d3b56617f63be125ea63d16cc1a8b288450ef3eff85714a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b782fb11f37ef0b7487689ccf0c354f700c0f305da55e2b317244b574e5110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e62451ed3c7ab532757f57684ba9ea0344b469016210ee4694c53ce34c55524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__638834a1e3a1dac054eb544afb28c0dce59d4a66586c3a71c2b56982e32e7dc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdd53d5934be3de76bccc266c5ade4ee7d924252574e86643f48860eb45926cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b6d5992104de1d30b7c4d4f486dbd7bb5c2bb5ca7863672cc23316dbc4e153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9885250fd23186411b29121b28c3c04e97ec0dcb97ff099b70c4556c20586f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88a9356bb0bde09e7093ce52158ce53bb362b909f158d3f965ebd38efb2380a)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c772f134fd4bda05f5ebb37ce679a5d575f1be14996969135da8dc49b5fc1e16)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method_selectors GoogleAccessContextManagerServicePerimeters#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#service_name GoogleAccessContextManagerServicePerimeters#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16ced4d1c7f774599f5a98e639ec06336efb01c2e094a735385ca69ce050c278)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38992d278b125d7e74366f3744e7cb31960014c296dfc57a9d731d659863fa6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f4975d16c7cc5026c4ffa0fcde150e7842b519fe9ed6d4cdd1190b49146728)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1bb12c2b757d07122958219941cadfa8ea530d659ff95011d6b0913b920273f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6035baa98813ec45a5545ec7b1c8b9cf27a144475fb008965dd67af44f185f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe03a61eb7994f2bd01b00bfc061f99eee71424854fe39cfbfba6cb59db44f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724e8e9f3dc02e0ef500cfc23ae7b2f5657788704bf28f2ced1fe17aea27db30)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#method GoogleAccessContextManagerServicePerimeters#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#permission GoogleAccessContextManagerServicePerimeters#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15537c8dd5c2b7e268f6abafd565607867d2d4478fbffec91c08890812a0cd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14675d992785bcf2e6b9f92a58d0c143cc51516f0bb62170479ced1f1360b185)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b906b5c3f3af80797f6874c499670bc334d6ae012bb4e9e7b47244a5a3377d40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d36b98b0ee5cf558a36dc955020e03d5dea40da3780fce0c73a0212bf1ef00e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ee33603491a5af570f9de11d369f50c92211ed38a07347e2f0d6cda43ed880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9e6d0312eda03da626d8ee5c4dd000ebc2f0b172947fe3f9b5af6b1d96014d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79bc5a08c7708aa4870899ce820754d6d7ff720e7af4bce3e95294354a23cb81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b78ca97ccbb03ec14c54d1af4d656be8b82ad253c6b6b673deabfb1beaf986dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6d2e61d10c8187fa642903f291ef50d8983dd8943ff567c0a6bc3efddcbb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002352e9bd8575d69e86487d7937b4198c5f16a7ae194616aa241d7ae048f471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec4b4586c68d6f8acd00ff0df12fc2b5c7894e2c0fc156a48ab0263adff57b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66498eb9afeabfded7bfebfebf13ad271030ddf4cf3e014fbc5f10bc39d3c6a5)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e84007a2ddae60c0fbce97ea6d77780aa2b6681baa60fc52f687ada47606b855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a546c84cc455bb6a024a3a2fd2184d0ddb289154d3439367814805c171e30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__216b0c02e952d1e033450859c433787dd2ec44c90cf8b3df06288dd49f815b1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1f1f850a5d7052e8384595750d4e86e7c054599232f47c18e0d6616febd8dc)
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]], jsii.get(self, "operationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__08dff4592b70bd788dbf871a42e736fdc6a4444265a9b53fbc494d6845cae38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f395c3fb6d2c0fe8a97fe3d45bcc69ea1d61b4467756caceb5cdf3f9717d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16899bc656aaff0e2869e617da034d991f5503be2ba84b35ddb5db6cd248d6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__921317b5e6c49ee264fe0dd8b3993a4411f4ecdcad890fb51abf4f9fb28f0699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796703354b6291d3384eed205ccaafaa9842b783f3e908734c35a40285053a0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d19eac2f6f53624ea05bd85a7220b3e5f6ce1d89f535123aeed26896514139f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__759849f2672d6c374ae60cbce14bf36354209d416de02ef7a47879f6ccc1ae76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10d97c3ea18781ca008bec450d15899556ae5adc0c32611bcc822f261c39cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e3010573ede4cbc2151af6297fc077bccde46433bb38f7f720428d2a5d33a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e855e524a7a76ad02bb83e1de101fc870310e33693fd09d51dde06d5ab2f175)
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
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identities GoogleAccessContextManagerServicePerimeters#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#identity_type GoogleAccessContextManagerServicePerimeters#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#sources GoogleAccessContextManagerServicePerimeters#sources}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#operations GoogleAccessContextManagerServicePerimeters#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#resources GoogleAccessContextManagerServicePerimeters#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#roles GoogleAccessContextManagerServicePerimeters#roles}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo(
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference, jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference, jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo], jsii.get(self, "ingressToInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__45b9091cf3738bd161f1413034a3b4f94449d572b86d6fc9e62f9668f3eb7bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24544705359998dbfd02f6e4182d074ae0bffa45aa9133a41ab1d9b9b9784a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__576b4244e122101b192bab47436ac0c2ae541e83a2006461dc33f1eb4b8b1551)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressPolicies")
    def put_egress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327dd42cb29badc3ec6d3c24ca8fc1c4af76cda5e4a248b51faa7b59a44a61d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEgressPolicies", [value]))

    @jsii.member(jsii_name="putIngressPolicies")
    def put_ingress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0620d3114dce3c91793d6785ad7d6c4434939348eeb58102514e7f648be3223)
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
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#allowed_services GoogleAccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#enable_restriction GoogleAccessContextManagerServicePerimeters#enable_restriction}
        '''
        value = GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices(
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
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList, jsii.get(self, "egressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="ingressPolicies")
    def ingress_policies(
        self,
    ) -> GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList:
        return typing.cast(GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList, jsii.get(self, "ingressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServices")
    def vpc_accessible_services(
        self,
    ) -> "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference":
        return typing.cast("GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference", jsii.get(self, "vpcAccessibleServices"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="egressPoliciesInput")
    def egress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]], jsii.get(self, "egressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressPoliciesInput")
    def ingress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]], jsii.get(self, "ingressPoliciesInput"))

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
    ) -> typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices"], jsii.get(self, "vpcAccessibleServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43ef5871caad3a8d4e3516c8390e09f12261b5c59915b1dfa77e77e75c8bc85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c671bad98be7de1295d248fdf198c31b57e136f1357061f8ee2309547031f9d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedServices")
    def restricted_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedServices"))

    @restricted_services.setter
    def restricted_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e122cfaff614163ed6d734ec0c8698b696892712743d3975630d2f71a997e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatus]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d086f3fe3b5e44f46c2da509fd75f825aa89bae5d229ba1b99b5939710bcb233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services": "allowedServices",
        "enable_restriction": "enableRestriction",
    },
)
class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices:
    def __init__(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#allowed_services GoogleAccessContextManagerServicePerimeters#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#enable_restriction GoogleAccessContextManagerServicePerimeters#enable_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d71e91fa2245b95a103bd85da84097bb40ce5d97f4c6d6665aec3b30bba223c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#allowed_services GoogleAccessContextManagerServicePerimeters#allowed_services}
        '''
        result = self._values.get("allowed_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#enable_restriction GoogleAccessContextManagerServicePerimeters#enable_restriction}
        '''
        result = self._values.get("enable_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ed0e4126a752ea6db2109aa206f4bfce6bc0d85b25509665919d04f6a332d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__244e4485d03fb0d7615537ecb79653e5ed110d7493c5bf97b5410fca09d64be7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__293b0351df8782285c3044e205769a5de1943331f660690db4161b53bbef1b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3eb950feda534e49d9ab927822d4c66338780df2ebe13bb9e62039272be8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleAccessContextManagerServicePerimetersTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#create GoogleAccessContextManagerServicePerimeters#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#delete GoogleAccessContextManagerServicePerimeters#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#update GoogleAccessContextManagerServicePerimeters#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41d21872506b32f67fb55361946a51ab32d8e1c73e9de5735b7b8103e144957)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#create GoogleAccessContextManagerServicePerimeters#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#delete GoogleAccessContextManagerServicePerimeters#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_service_perimeters#update GoogleAccessContextManagerServicePerimeters#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerServicePerimetersTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerServicePerimetersTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerServicePerimeters.GoogleAccessContextManagerServicePerimetersTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__315a7a97322097239eb6891dbb774490ad2ff1f2997c65b02b1c8307ec660750)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f153779c40d9a18cf0200e8a088f80e44aac5f2e28cc4ebc50a6f2afa4b07ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84258222110cbcd0a3c2774d50a792e08e9170f5b738aa85774e2cff678418b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1547ac10e52135b2bdba3f489b918dd499d60856579dc1d9693858107fae546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89858fd48913f92cf006308fed3e98f67e093ece60e129194b146ba01cc2a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAccessContextManagerServicePerimeters",
    "GoogleAccessContextManagerServicePerimetersConfig",
    "GoogleAccessContextManagerServicePerimetersServicePerimeters",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpec",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSourcesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSourcesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServicesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatus",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSourcesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSourcesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesList",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusOutputReference",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices",
    "GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServicesOutputReference",
    "GoogleAccessContextManagerServicePerimetersTimeouts",
    "GoogleAccessContextManagerServicePerimetersTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__23560c1d2a29ff4d0f657dae94bd29192fc86a8b49fe2d942b658e623ae1ca71(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    id: typing.Optional[builtins.str] = None,
    service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimeters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2e8c492fa4b7c462fef595ea55b2085b845298e44d69269a1cd87a341ca2dcb1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf492ec5ee57c7e2c3d6e706eb86b8c73b03e743b27e8118765674743fcd815(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimeters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e4eeb5b70a5ab525a9b5e94276b37224ca129b4a78477e14527194ff71f429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af59dc20b949e5a8c85ee99b59263acd2438584d9446d1f1828b058c46888dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fbeefe925919db09adbd43a1db886070eb2756bb6603020962493b84c371b1(
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
    service_perimeters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimeters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a00c96006a5da3e2d3537ca9be4727f31d43a8ac1997925bc303da6ad21f4e7(
    *,
    name: builtins.str,
    title: builtins.str,
    description: typing.Optional[builtins.str] = None,
    perimeter_type: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf94993a8cd14dff85565577cba446a2e19b3054478aacc844dce3e61bb2e6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45eeb216b326a72caa00567ada4f3a6c29f7966fbc245e4032b517b4d6cd4ab2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfeb4c59c96e388a020438dac62ee08c1110bfa2aea821ca9cdf81c3cbc8ef49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f643af0fa3050d2f3b67487b61ddb4030db0fb2c8c1395c4a8a82d3a0889c50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf24ac1cfdb329c7b82141b17346868caa2709ac57eec3832b6eff17eb36607a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896dbc08c86c5cfa2d2c2b58283f9e238537d68faa7b600dc66e5fd58feafc22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimeters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b359c6049e007a1294ffb93e0397b290a1d3ac07979e7f3abe3ebcb4ac1cc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaed55fe8f7b59c29ab70c07bb3b199713bfa35d2bd17a69f7d42ad67aac2f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137258a116c6ace29297a5056e6ed881aba9726174ce179475e55c0d4506cbbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7143120d19c35b2e2f710369c3f0e0c6ccccb607577e1f3f778772fdaba0fcd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032a53425dacf7471233ba0bdd03443492f821a7e909f0d7b3b3715dec1f7530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3048b1e727a1cc3f9736be0a770ba731a73094ddcd2adb573504658e7c43ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d3fa43fbdac0ae8bfc5c3202fc55bfc8e3743390ec24eec404c6b288d48157(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimeters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12be117eb931eef77c919787dd0d1a11c1358e9e17cbdee274307c86e1ec4ee5(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_accessible_services: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a529de98004b42124355fb7c7fcac5e4e5f1729e4d1b5e79dfd743cc7c940c8(
    *,
    egress_from: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9a89c1767b2e616a99ad702a9778fd3e2616479f3df9aacb307f5f37429359(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7cf355cbc2ab6a2624e3bab73dc654bca8f9fcabbada9ec971e190c11d46dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c991030f76ac40cf4d5dd394a9eb414fa720f2460fc6ee6d8f6a03bf08b3f2c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d553fdb96119db514fe875def2413f035f500934911a463d3ddd06c15548135f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2091025ca7fa9c0977f8f879e8303d2e61a5ef08c5877b9fe95f047534c4d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8e8da90b51d42599a29039d57da3fea7221a8ee9ca4ce8c566fdba54713177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca876cacd5dd54ca20eda5c59661a33eb5a3032257689a9a492a4c97284775d(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d217c91b775f98dc0cc76b86888ac0c1005f562a58b7e7762086ecec7c44fd1a(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680dbaa9d32afac613d145a0b587ac433b1a659224517b3f1a08478c4c16c919(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9643d658ac1997cdefcd5b3a7be1e9ece141d14780ad5a09ae51eded4d281c42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bbedace6cc630ff97fcfe9530026ad43fdaeb9f1abb618c90c06055f316841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f0aa2b6688d3527893e6dcfcc620cc884be3c4f9cbb26028ce166424fb01b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175157fde0832726368e4d5482ad1b9d2f1c2b49637ab1e35d17979657e7010a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c48e72b339257e3ac3328d2f8b788b595de06222c435da4d52fc8d2ae67088(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc30bb0ae7b0c0f512a3481203656d16067f1e1c509e9ae877a742fc883cc22c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8778f127f58293d02743178afa0a5c62233d0935eb9f40624d9e7437ab486b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4059957e06b7ebe93edd077ccbbc6baabb4453b4e08e91b4aaa2e8b3a340e7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6941b85734dd12a452ac2a1500e62130ae15b4eae9024aeebe059d69fda68f1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e354ab7dc4144158b85541bb95d5d5a80ed109c60d8dc4b6c534c61f8bac93(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cccdf02dc206fb38137e458147dc1eacddec94d8d7d7979dd13a1087e58570(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff78fc4c4f9774e5965482a39514fa72d47f96ab1ae4d83495ab0af81baa5e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f778ec791767a8ad131e72f05c2b8311c5d736eb3f73de8b8d6e739d36046e7c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9608123dc3104717fce9e9407a5c496b2ee71aa07d307e1bd76ffc598a46e05d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619c144230da1dabe5110efab59d0c6ee47f05699374ed1c4dcf64f8b925a86c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0511259b799bc73f18db5baab8d358129c04361d490fbae59465634c8c5dea7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4a9f9f1ec4035b23557a316796b304212375398418ed55a548225e9b748d20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151df337f0d3200c7d0b94bf424f8cd258de48f910a1ab436f3a148ff522d242(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3950c029844194cb2286d38c335f5f2e72aa8f84d18e954bda87f74cb627ba98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b2c408bbdd58cca78e2e1759eea73a3fbb9148676f988206a64c8624c963f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fa340900704d3cbd0f4c5b811b39af4996e4ea167bace7105bf69965599249(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c365fa44a8d787f47adb30811ed249ed6466ce2db4a3c7f848538cd0e35206(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a87d5e42d7b78002acb32f861e3952a4ecca4ab8af78e4a612f4685a79a8cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0d45db84ca83542699bb821086868cae0e12266ed761886a9050750f25acf8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358743150131f9ea7456b12ba95f830107e7d7d85e511e79999cbb594ba75d32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe445238ce7af8b519f78116b72ead5d71b194e0d6bdade16c20777cf956b041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915c143b4ca9cf322dca2c815f0d88a06f9a5a517ecbdba8218271ff4eb9dc5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5158433e8e1eade16049da444aa72720740bf88a746ce964f31a6d20bdf950a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e1dd3e9d51031242b8148f7ac58c47eabd728aa9166017baab3161a79d68e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b7c7200be42e11298aa0f404fba043f3ee7b62d7e9d221b6cbf9ca865d71f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55131afc069a3670512d541c1a0b9df858c453cb39282d702a2b0c8dae23eb20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64acb45764e454353af6906ee087db66752dba9d3df6a7fd1cea0420c35742ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404eb83e0194c954f3efa626382ee55b46b100ca6ef2b970caacafca896e1ac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b106e26d3ec9c5152c513e8872124d953bd421863106c396890313f7809afe9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d08025e4ecdda766f1c2d4750f5dfe689ee5cd8dd6f0b6c1b313bece914b2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cf6c795f36b66bf92ad9c49f094c1acbf1aa5b08ac78ca55553c6ebdc612c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff92cb0872adb1d3b0539d8f4a97651bb19dadfc8186763a14961f82bf54305c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752189c591387c163b5b05da18aff7f00afcb9163e048b9c7530fa9e236a2a63(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPoliciesEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677cd0c787ce064f0eef9cbba02db7b9cd8b194df96957be6635d52af9f4e9ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4361c1bacf15b768731b7982c639410394582fb94bed82fb397a0f344788087c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb9cf44079e87e07077286c66f80cb9b3fc88153129573d5bfde89ede3c2a20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4318c5e091d7fceed3b81157729e4e4e2c8a47fdef1206a71c297fb2246bca0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5818ecdad73e8dfde0a6a5057b0b4ef42f2ed008c3bc41e7cb46ff4fb97a0c1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5af523d1982f23b0c4b992dc59c986707eb839c23ee82960599577f9489bb13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f662170781f2cb7ff1d0f709bb4ff35b314d3b67ddc482afed7e62d61a3ddfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2996a09beb1d8a092d8ff626f40de30724f6150e0b3189728d662674c547cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151b19b19a09e02f5552cf187af461443eeeed55e6a04f6a3db0505eebef80cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75070ccedc888f8aca4ae5b2becd32dc6cd77c519c8ab98e21c1bae4f3a3bb4(
    *,
    ingress_from: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce45c5887476c7adea2801bb23a95c87ee75d30a665680aa2fe9d857ca5ade4(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513811d048204f0e1f5ead57ab8142a3f1400872f49876dcbe90f7c16e8a62f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1762416ffe21bbc554d77134c06978ce2c3151dbe9654852149845c9257c6e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203a496767bd81367674f4dc9fa6e27a3d37baff42e87afca877591b1f16353a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d43b6237d0b4b4da2b96899a5b8599f7b5d55c49289f11e140b233521bf9b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f101a4abcc7aa35213791fd5aa040e503837336e524ce4b4bfa53771551612f(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65daf89cbbbac9b85cb38649cfd5b7d46e5e28053dac9827013a9e61777f98c(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164cc718c3a29c7b77f50f9bb61e961f97cd31916d91ab9935de36974acd0bfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0ce27376e9d43c9fd6025347e846ca26470a458c65e2ce29e5c07754db5da6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262396f8d86174bf36bccb499163d57d3e3d086e86ff73adf314950352790ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b928c0426d951672e2785f0b58e1a82f5d6af67fbbdaa7b137157734e94a41fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bbddb017ed7cee8eae89517145f264457b1eff30501c4cb9e9ddcf020de8d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d354a36b1ae2dd091e3d78958ee3a7e4ecbda004d2c0e40183bb76d6c68a0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c84f3e4ead031cfab72d6a27651ff10431dcff0e8192d89907349c6f59afa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339084c438aa7da1089158bf09f7d738102cf78777cb35fc6e7639996944d9a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6214a3a4bdf78052d815e16fb3f38d8608f90b5383a1c675ddef4180242253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a831813538be55a5772a54718892d0d298e77bb8c63f538a6f2dd0bd7b75612a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589730695e84238777574600bbfad13cd160ed8fccd803f1bf0c9d004bc69863(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f81a6de92c072c4800b33fc630d2abc7071ad71d9021b9a1b6bc1f12963e7f(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda0e6cff5624e911ac6fb24989948a5f2d5a4469f0cd95a5f7ac2b80133ae5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0244f07ceb1a66af9cfed17966985209aec755920efb7fe149cf936b64995c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9894ae4b9ab4c90a1ff440795b42d589415b02fec207363998964f57b850ce58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d6887319fd4966373d3acc606d5f0974a1461ab2dc30c72cfe0cc791e1cc9d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d68f382d27a530c1aa63f14b6cdc6fd0e2ea6cb084bcf564921192331e6878(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfde0b37ed1940d42922c35f1d372dddf6e4383531f04202c79c33243552cfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943524f765bf88ff69b015ea8ada19130e09e91926320a77148551bce6fa8b75(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024aabcc8cffe4f95ba1731b42897765af1cbe2bbc1c95f14c4413601e5167f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb728f26c0cda6aeadfc3e7438f9fa463316fcfe853f244d8a5321e56457ffd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6963dcb7ec9e775a4cc88b5f771a91259cdbcad53a88d727b50807fb36f5dec8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9e4c58d7f38bb97dce5e2c4809a1df79cd8d5e627626efcda7714fefbce7aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e12d383090b958db904d4b97a13cadacae658e13691a88b6244f9fa516949ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faeaba8bb86c63460b3adf2f7bfc6e6c0833c156b8f577cb1e231edf5f7e2377(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb1fe30694687d8ba498f4e6b896b41108c1f378ba10b01df1626b0e00aa948(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffc11ce904c208f7285001ab49d672591c1cdd0ba79c51b9e97c108dadd083f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9030c0d11babb590c3b7fa29b1088cbc1e1a0756639ee3fce0c272d758e35eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0484bc9cb21b9eedff164db698d82f522899eebb66de99b04096f9b3665e8a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f42a162dec83303d27a37767d18c62af32d79c3e3f440a3cfec08241e35e4f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9856565a1f91ccf8d49cad264e4662157e5b630d3ab616de0392fa701532351(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7308321b8a1f7255082126a042f4d40048017bef0537b92f0ac94de1bdf72b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b116c7ec4cb604ddf4515fc510d83d9de5c7690afc802a69046885d4de81dfc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace9d13971871ec13cd3bdabcbe532933ecb3aa1cc5bd00db389bca4c470c6e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8980e4d86ad840ea170ad6280b94c612901eed35ade1fc7cdbf274122968d229(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744227b767e3922979729649f3631594313155f85f7ff57d5f2f52b41f71de8f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ee9c420103c5baf014f716bf4ec0f9e0543c677399f12961835422c8619ee1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8840bcf5fae9696b726ce289eb512d4540a6eb4380a9255015dcbc4d9c79f1(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPoliciesIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a12e136c868e04cd40dbf71301ab348e2d9d8e1d7340b34781cc6bad76e6f0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35986f442e5e9019047774509e1ae93b82d82922278003e6600e826e02bf6375(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939d3a8f2d2448f48695bdb0b82c38760b95863106917738eecd995411dbe5e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8bc1a7ef23e0bde103c04863ade0cff30a8b4e03f0728278020e8d2d52ddb0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac60a5cd198105a647d667913552a245ecbe56f88f7d4ca41f67a43bbc804652(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1888f8d831ef859a40de52b437e674f524fb769ae68e7f3ebf5a8a882f2285(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c0644c80766a22f3f77dd973d76d8a4af93e39cae2415426a8600c66578ae1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7747aad9fa8f6aeb697d4fc35acf7e7bf7d7881017fc0d9a84fd5e5a2db3e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38233d194822a00ef0e6a22a8790e2d9ba0cb52da24591ecfa4e25693fd5565b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c414d4145c6dff2251dac8486f26435db8447dc8aceaa491c3ed3447917822(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56748a4e9b7335af9beed6c20bbb6dcb524604520bc37ceeeddf50fa1b51678(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ee89c42a0721fd3682ae8a6345ce2b9a029a75a402afc5c552abd9e794a34a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea8c8663a58fddee6f9f8207dd45d3bc0f974f493cfd63901d943a51774686c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7503277c3a9d1bfb788ebdcafdce8a26a183e8af17824521cba07bf247ab4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e51dcf976006a48c157538c482a31dff92a2ed1108a02c8beeb8d4647ed862(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f437fb5c6437541f4314194cd19171f35a93a8138d34e267953fea56d6c2c49(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9486400287ce29f63d87ae47ba2fe25bad6491f1d0d1fc7baeda36f81150afaf(
    *,
    allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cd3d94bd587e930b84cca3a90a081ba0f91fb428cfb7d5a30d5ffca631c3ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca191099a15521139ec4eac22d1333715b78c9d8f54b1e7238907b9f3fcf2105(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a4e42ef2c75c54e850d62dd74cbed9cacfa1b35b15cdda07d26b491d64b114(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcadc21d724ae061341cce27810e76df3675771a329ffd640af2c93ddc87faf(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersSpecVpcAccessibleServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9410635c96f6c77ed0d0ad26c4a904cfdc0ec76926fe551fbb34583905f503ee(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_accessible_services: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efec560495ec63993e702fd89d1c39a48f44927240c2fd25353e7f45a3ce1f7(
    *,
    egress_from: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e35c6b92f0a457e3ab2a8036ad531ab1e5b6193b5171b98ffa1afd524d0535(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a74e2b3317bb2401af2bd97436c3a8ab6c1133ae547f924d46d353ea324b9e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb095440c28e2cb632064523a7efc4affb51284785e1769ac2763e571d69e77(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501731c52dc216acae37c1fefef48f97f69e404c52fc5f4dc9e3edc81494d5e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9b19126062105d48da67a28fbd0b9042da0cd21527aa06019ae678a7b89204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7984b29ecf4e2dde429f1c2831cbede6243a052f116a017604f9980c9ff9b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75035971cb67a3fa377c477fa6da3a6e14f932e1bf6516bac1b775382c1ed3da(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6e065a058e1e82fb6d5042d505fb3efa3f0f2c4aef57743221efa4ab1d15b6(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5bc4cccd769e7202a3a4c76366e61408c680739899847daec1b210080e22c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2796c9321aa7ee65d43f260f76dc92012e9ab6cbe5fb15d1701b6c4fc869f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f84071379092ff99b9bc18d675ebb7e99fe8c60aa3e8fa57414fa35b8921e88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8d9851af7fb7be3aaa83921cb0f7eadce68c43e64de1d6f3ca7de1ef3354f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85a8a004645f3e735dab02d4fd32040ccfefb9ed9d44f2cd5a62d727c365d81(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f43f3478b6ea8d40d97feaf5a731f51257179491269e113f9be9c47779fa70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9465edfdcfa3f2059ae2868619c1133e5bc9ad5b4239711089e464a5a7cd9c87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca2b16ab409ba15fbb8539cde7e5cf411629a93754cb8f5e400846c9f0492e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1372feb72bb659308415db369f067fd0bcf254568ff2dbd50821a414d2c6ea50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d088d4bafa78d5bc6fa482596bc27b3b3ab907da0682e5d3d9b1bf72fd7473d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fcddb8c860209262c5c89c166a95add2269617d0d3a6f0d6a8ebf50c23c8f2(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a07af8cc6fca17b41ddf380b1cce59ec70d9deff59681901dc980a88e500802(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f695379d06719123f97d61518f2f5369ffee71488651996f15abd301155a9902(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9915e1d3724f31b2596879519731cd79014ec08a39f14231cad9af17c812a659(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15fe96dd7f144ea12461184cbbec5966c22933eff67a867e15251d60a83b97c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7379bbed5cc109fb07bdeb2e128b8211231853288c404416c3887874fb1839(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a408c6ffebf077d8e28050d4df8339de94f99fe3c3b90e41a081333996932e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb89c497955f9cfe07362b516944bbad4e50c6de132bfcf441e1fa3bac0be10e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afe7bc7357452dfb993e78f9029d6815ec7571e255053e0a9daf176cedb9cd1(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6359397eab1cc4b26e48ab66c1aec1425c05b9344100627092055142065d446b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e998a528618f7076728edad42b4ee04c758824011a65abb05e92bc58ae51e27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79699d8fbfd117013e5a79fae113402dd3560238df6dfc5baac0f697806f589(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2346ca8533210781c225733be4899b7b861a5083ad1e051c6c85241af0b968b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953fd761c2b037488079c7d8f38eeb76b256160db4e62403b07a41cf3211c268(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603f25d4f1a5aa374c45063487cacb435428d5a5238c560a4a95f443c7ccac48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f4272fdfb6db46f4dcbf5593eef008e915ea0656ad5673d1055a2f0a9a8609(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f91d45040707a2797da58b6eb26654006dcb3fc39a0c953e4da5bc6ed8f08f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a797e8304fba2bbc05234803b9ae35adecc5cb3d168d09e0de4ff585378bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01bcc29c0190dbff572815a5e3d6c3ea57e0c13ecc3e7d76a15959f4c8be070(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a74f03d07c150c945bd7e1fb2df576300328f0105f2e36590ada8bef468b64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01170567185bb3057c06509745225fb4f8347a0becdfca6caba61e8b1cf448a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8272509c50026c2be0e29a1ac37c3f8bad27ddd41fc981198447754c31bd1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5d1e3885b316cd1be25e687efef27da2aa0b4541a4ab6e2f5a7579c745b346(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b0b82b2797847eda9cba90b35177f5cf86719fc8e319b9fedeb441a717a507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4c161e3283287b7521375a4d0612c427e220a01a61b68c088d688450b28f43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a1090e6f160115631be6024d7e3f60c36633cbeb9c439ff3b2bd938d1df9d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947646cb6da4f401a7d76953a0c132acf5ed827cdf6d5e04527f5d89ae4a8bab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fee75e9ef24b8bca8942c7f0e3bef4ea0367fb0f85113d31c35432bb349c05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436d0da928862019d3915ddc9281b16682c43381fa92cded9c4ec1cd4edfab70(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPoliciesEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69dff1e0fecf56acd7aae4288344d5ef2113e75ec4fc41028da629603c73b85a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e991c79bfb60183328bb4377aa6699ca3d1aec9ef6b05096c1da5b18f9f522b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ec82be8352f787e92295a9912f4f919bd2161d56b2f4a24859e702ef3d147f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e25de9ebf7556f29cefd4501d004bc495134e4715b8df09ce277e3b87f306fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48318f4194e208c98550aee511796566a6b5b3557018cde002ebfe4bdb069b89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc829795b130cbe84c063e9c2970bb0dd3bd9fe085dbc4f69f1b9af401c98dbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b0aba8f8b0f6ac2456100458f3a5a87d5f191e1023f32205ee2dd3590f7a6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e91c730ee4d503c0792a3fad38b9691b9fd14e026246eb2911ff72c49caaef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8292a00fe604110ba26661a0cfcc21797cd44c4ac1e94cc101b466be31fe93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512ad852d274550a6b4b26325862f061653bcc7ed75aa05467a34728d48a9e83(
    *,
    ingress_from: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc3e0362506b7057f55003cd0d33b3663a9a78bb9fd4f2e8175b5c9fbdee641(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56eeec589e3ca7368be62ee22cf46df948a17770fef5df3be6b38daba41a3071(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296bbaa640fb1f2cd2606d09c19416073145afcb8f3cc0059b00fecbc6bf4e73(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c108114a75b8a6df6fed9f59da177fef27c7819c6abeae11c49a19c98fa2fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b0d8c508b8e0e4c232e61ca38d6fc6addbd8116fd38a95d9b140eb0a6803c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b529ad6e68568ca5316a5f0039d7a12793d4f00897ef085f1c2997e910785c(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eca63a2cd243da1336db697516ee903beea56012a0f45a5283f34155bb99d23(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a418d2a53d0adf5a199ab29a1550ceba87588b78efb56f7926e0572bc3f173a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f806eeedc8983ce74e75802437ecd91050ed499c652f07a462d10665b917b78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d573dcb8029783da1efa96490f77cef700791bb6f5031281b22ac8e0763b8977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5f66cba71d7371d3b56617f63be125ea63d16cc1a8b288450ef3eff85714a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b782fb11f37ef0b7487689ccf0c354f700c0f305da55e2b317244b574e5110(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e62451ed3c7ab532757f57684ba9ea0344b469016210ee4694c53ce34c55524(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638834a1e3a1dac054eb544afb28c0dce59d4a66586c3a71c2b56982e32e7dc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd53d5934be3de76bccc266c5ade4ee7d924252574e86643f48860eb45926cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b6d5992104de1d30b7c4d4f486dbd7bb5c2bb5ca7863672cc23316dbc4e153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9885250fd23186411b29121b28c3c04e97ec0dcb97ff099b70c4556c20586f00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88a9356bb0bde09e7093ce52158ce53bb362b909f158d3f965ebd38efb2380a(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c772f134fd4bda05f5ebb37ce679a5d575f1be14996969135da8dc49b5fc1e16(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ced4d1c7f774599f5a98e639ec06336efb01c2e094a735385ca69ce050c278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38992d278b125d7e74366f3744e7cb31960014c296dfc57a9d731d659863fa6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f4975d16c7cc5026c4ffa0fcde150e7842b519fe9ed6d4cdd1190b49146728(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bb12c2b757d07122958219941cadfa8ea530d659ff95011d6b0913b920273f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6035baa98813ec45a5545ec7b1c8b9cf27a144475fb008965dd67af44f185f25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe03a61eb7994f2bd01b00bfc061f99eee71424854fe39cfbfba6cb59db44f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724e8e9f3dc02e0ef500cfc23ae7b2f5657788704bf28f2ced1fe17aea27db30(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15537c8dd5c2b7e268f6abafd565607867d2d4478fbffec91c08890812a0cd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14675d992785bcf2e6b9f92a58d0c143cc51516f0bb62170479ced1f1360b185(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b906b5c3f3af80797f6874c499670bc334d6ae012bb4e9e7b47244a5a3377d40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d36b98b0ee5cf558a36dc955020e03d5dea40da3780fce0c73a0212bf1ef00e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ee33603491a5af570f9de11d369f50c92211ed38a07347e2f0d6cda43ed880(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9e6d0312eda03da626d8ee5c4dd000ebc2f0b172947fe3f9b5af6b1d96014d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bc5a08c7708aa4870899ce820754d6d7ff720e7af4bce3e95294354a23cb81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78ca97ccbb03ec14c54d1af4d656be8b82ad253c6b6b673deabfb1beaf986dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6d2e61d10c8187fa642903f291ef50d8983dd8943ff567c0a6bc3efddcbb26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002352e9bd8575d69e86487d7937b4198c5f16a7ae194616aa241d7ae048f471(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec4b4586c68d6f8acd00ff0df12fc2b5c7894e2c0fc156a48ab0263adff57b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66498eb9afeabfded7bfebfebf13ad271030ddf4cf3e014fbc5f10bc39d3c6a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84007a2ddae60c0fbce97ea6d77780aa2b6681baa60fc52f687ada47606b855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a546c84cc455bb6a024a3a2fd2184d0ddb289154d3439367814805c171e30c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216b0c02e952d1e033450859c433787dd2ec44c90cf8b3df06288dd49f815b1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1f1f850a5d7052e8384595750d4e86e7c054599232f47c18e0d6616febd8dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dff4592b70bd788dbf871a42e736fdc6a4444265a9b53fbc494d6845cae38f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f395c3fb6d2c0fe8a97fe3d45bcc69ea1d61b4467756caceb5cdf3f9717d6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16899bc656aaff0e2869e617da034d991f5503be2ba84b35ddb5db6cd248d6fa(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPoliciesIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921317b5e6c49ee264fe0dd8b3993a4411f4ecdcad890fb51abf4f9fb28f0699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796703354b6291d3384eed205ccaafaa9842b783f3e908734c35a40285053a0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d19eac2f6f53624ea05bd85a7220b3e5f6ce1d89f535123aeed26896514139f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759849f2672d6c374ae60cbce14bf36354209d416de02ef7a47879f6ccc1ae76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10d97c3ea18781ca008bec450d15899556ae5adc0c32611bcc822f261c39cd2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e3010573ede4cbc2151af6297fc077bccde46433bb38f7f720428d2a5d33a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e855e524a7a76ad02bb83e1de101fc870310e33693fd09d51dde06d5ab2f175(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b9091cf3738bd161f1413034a3b4f94449d572b86d6fc9e62f9668f3eb7bd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24544705359998dbfd02f6e4182d074ae0bffa45aa9133a41ab1d9b9b9784a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576b4244e122101b192bab47436ac0c2ae541e83a2006461dc33f1eb4b8b1551(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327dd42cb29badc3ec6d3c24ca8fc1c4af76cda5e4a248b51faa7b59a44a61d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0620d3114dce3c91793d6785ad7d6c4434939348eeb58102514e7f648be3223(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43ef5871caad3a8d4e3516c8390e09f12261b5c59915b1dfa77e77e75c8bc85(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c671bad98be7de1295d248fdf198c31b57e136f1357061f8ee2309547031f9d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e122cfaff614163ed6d734ec0c8698b696892712743d3975630d2f71a997e2f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d086f3fe3b5e44f46c2da509fd75f825aa89bae5d229ba1b99b5939710bcb233(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d71e91fa2245b95a103bd85da84097bb40ce5d97f4c6d6665aec3b30bba223c(
    *,
    allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ed0e4126a752ea6db2109aa206f4bfce6bc0d85b25509665919d04f6a332d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244e4485d03fb0d7615537ecb79653e5ed110d7493c5bf97b5410fca09d64be7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293b0351df8782285c3044e205769a5de1943331f660690db4161b53bbef1b10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3eb950feda534e49d9ab927822d4c66338780df2ebe13bb9e62039272be8c2(
    value: typing.Optional[GoogleAccessContextManagerServicePerimetersServicePerimetersStatusVpcAccessibleServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41d21872506b32f67fb55361946a51ab32d8e1c73e9de5735b7b8103e144957(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315a7a97322097239eb6891dbb774490ad2ff1f2997c65b02b1c8307ec660750(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f153779c40d9a18cf0200e8a088f80e44aac5f2e28cc4ebc50a6f2afa4b07ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84258222110cbcd0a3c2774d50a792e08e9170f5b738aa85774e2cff678418b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1547ac10e52135b2bdba3f489b918dd499d60856579dc1d9693858107fae546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89858fd48913f92cf006308fed3e98f67e093ece60e129194b146ba01cc2a23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerServicePerimetersTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
