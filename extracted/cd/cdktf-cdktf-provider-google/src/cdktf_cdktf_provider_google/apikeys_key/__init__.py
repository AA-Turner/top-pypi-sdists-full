r'''
# `google_apikeys_key`

Refer to the Terraform Registry for docs: [`google_apikeys_key`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key).
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


class ApikeysKey(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKey",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key google_apikeys_key}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApikeysKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key google_apikeys_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the key. The name must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. In another word, the name must match the regular expression: ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#name ApikeysKey#name}
        :param display_name: Human-readable display name of this API key. Modifiable by user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#display_name ApikeysKey#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#id ApikeysKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#project ApikeysKey#project}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#restrictions ApikeysKey#restrictions}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#timeouts ApikeysKey#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae4a8afd0e07d7eb325545f7c42fddb686e038ee1a78c37fa837dc7807d6d16)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApikeysKeyConfig(
            name=name,
            display_name=display_name,
            id=id,
            project=project,
            restrictions=restrictions,
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
        '''Generates CDKTF code for importing a ApikeysKey resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApikeysKey to import.
        :param import_from_id: The id of the existing ApikeysKey that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApikeysKey to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd32c3a9fbf82a9cbc124661804c78f9244fcc5322951f716e113b6acbecff2c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRestrictions")
    def put_restrictions(
        self,
        *,
        android_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsAndroidKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        api_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApikeysKeyRestrictionsApiTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        browser_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsBrowserKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        ios_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsIosKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        server_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsServerKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param android_key_restrictions: android_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#android_key_restrictions ApikeysKey#android_key_restrictions}
        :param api_targets: api_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#api_targets ApikeysKey#api_targets}
        :param browser_key_restrictions: browser_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#browser_key_restrictions ApikeysKey#browser_key_restrictions}
        :param ios_key_restrictions: ios_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#ios_key_restrictions ApikeysKey#ios_key_restrictions}
        :param server_key_restrictions: server_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#server_key_restrictions ApikeysKey#server_key_restrictions}
        '''
        value = ApikeysKeyRestrictions(
            android_key_restrictions=android_key_restrictions,
            api_targets=api_targets,
            browser_key_restrictions=browser_key_restrictions,
            ios_key_restrictions=ios_key_restrictions,
            server_key_restrictions=server_key_restrictions,
        )

        return typing.cast(None, jsii.invoke(self, "putRestrictions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#create ApikeysKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#delete ApikeysKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#update ApikeysKey#update}.
        '''
        value = ApikeysKeyTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRestrictions")
    def reset_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictions", []))

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
    @jsii.member(jsii_name="keyString")
    def key_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyString"))

    @builtins.property
    @jsii.member(jsii_name="restrictions")
    def restrictions(self) -> "ApikeysKeyRestrictionsOutputReference":
        return typing.cast("ApikeysKeyRestrictionsOutputReference", jsii.get(self, "restrictions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApikeysKeyTimeoutsOutputReference":
        return typing.cast("ApikeysKeyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionsInput")
    def restrictions_input(self) -> typing.Optional["ApikeysKeyRestrictions"]:
        return typing.cast(typing.Optional["ApikeysKeyRestrictions"], jsii.get(self, "restrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApikeysKeyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApikeysKeyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e44538a83a67996b152b17ba043cee9e90563cf0c442212c4d9834c503ffcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3e697a1fe6ff68771aa4e98ddfe3d438d9f8bca899139e34eb43cf33f4c81b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8f4dc0839a7b081cc071326dc193738574477a898ca235cfed21e6becb1c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3255aea4cb67ac4fa6d538efd14de52e9b0e5b91549f13ea69d1cb32189d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "restrictions": "restrictions",
        "timeouts": "timeouts",
    },
)
class ApikeysKeyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApikeysKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the key. The name must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. In another word, the name must match the regular expression: ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#name ApikeysKey#name}
        :param display_name: Human-readable display name of this API key. Modifiable by user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#display_name ApikeysKey#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#id ApikeysKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#project ApikeysKey#project}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#restrictions ApikeysKey#restrictions}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#timeouts ApikeysKey#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(restrictions, dict):
            restrictions = ApikeysKeyRestrictions(**restrictions)
        if isinstance(timeouts, dict):
            timeouts = ApikeysKeyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b262dadd92109a838856d13c8962318659b99869846b732bd8704d45cb9818b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if restrictions is not None:
            self._values["restrictions"] = restrictions
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
    def name(self) -> builtins.str:
        '''The resource name of the key.

        The name must be unique within the project, must conform with RFC-1034, is restricted to lower-cased letters, and has a maximum length of 63 characters. In another word, the name must match the regular expression: ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#name ApikeysKey#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Human-readable display name of this API key. Modifiable by user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#display_name ApikeysKey#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#id ApikeysKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#project ApikeysKey#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restrictions(self) -> typing.Optional["ApikeysKeyRestrictions"]:
        '''restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#restrictions ApikeysKey#restrictions}
        '''
        result = self._values.get("restrictions")
        return typing.cast(typing.Optional["ApikeysKeyRestrictions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApikeysKeyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#timeouts ApikeysKey#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApikeysKeyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictions",
    jsii_struct_bases=[],
    name_mapping={
        "android_key_restrictions": "androidKeyRestrictions",
        "api_targets": "apiTargets",
        "browser_key_restrictions": "browserKeyRestrictions",
        "ios_key_restrictions": "iosKeyRestrictions",
        "server_key_restrictions": "serverKeyRestrictions",
    },
)
class ApikeysKeyRestrictions:
    def __init__(
        self,
        *,
        android_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsAndroidKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        api_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApikeysKeyRestrictionsApiTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        browser_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsBrowserKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        ios_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsIosKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        server_key_restrictions: typing.Optional[typing.Union["ApikeysKeyRestrictionsServerKeyRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param android_key_restrictions: android_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#android_key_restrictions ApikeysKey#android_key_restrictions}
        :param api_targets: api_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#api_targets ApikeysKey#api_targets}
        :param browser_key_restrictions: browser_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#browser_key_restrictions ApikeysKey#browser_key_restrictions}
        :param ios_key_restrictions: ios_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#ios_key_restrictions ApikeysKey#ios_key_restrictions}
        :param server_key_restrictions: server_key_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#server_key_restrictions ApikeysKey#server_key_restrictions}
        '''
        if isinstance(android_key_restrictions, dict):
            android_key_restrictions = ApikeysKeyRestrictionsAndroidKeyRestrictions(**android_key_restrictions)
        if isinstance(browser_key_restrictions, dict):
            browser_key_restrictions = ApikeysKeyRestrictionsBrowserKeyRestrictions(**browser_key_restrictions)
        if isinstance(ios_key_restrictions, dict):
            ios_key_restrictions = ApikeysKeyRestrictionsIosKeyRestrictions(**ios_key_restrictions)
        if isinstance(server_key_restrictions, dict):
            server_key_restrictions = ApikeysKeyRestrictionsServerKeyRestrictions(**server_key_restrictions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0472af26dccd4e25ad2b33ed54ddbd3b8cc7e17026294ac76499d05e3911022)
            check_type(argname="argument android_key_restrictions", value=android_key_restrictions, expected_type=type_hints["android_key_restrictions"])
            check_type(argname="argument api_targets", value=api_targets, expected_type=type_hints["api_targets"])
            check_type(argname="argument browser_key_restrictions", value=browser_key_restrictions, expected_type=type_hints["browser_key_restrictions"])
            check_type(argname="argument ios_key_restrictions", value=ios_key_restrictions, expected_type=type_hints["ios_key_restrictions"])
            check_type(argname="argument server_key_restrictions", value=server_key_restrictions, expected_type=type_hints["server_key_restrictions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if android_key_restrictions is not None:
            self._values["android_key_restrictions"] = android_key_restrictions
        if api_targets is not None:
            self._values["api_targets"] = api_targets
        if browser_key_restrictions is not None:
            self._values["browser_key_restrictions"] = browser_key_restrictions
        if ios_key_restrictions is not None:
            self._values["ios_key_restrictions"] = ios_key_restrictions
        if server_key_restrictions is not None:
            self._values["server_key_restrictions"] = server_key_restrictions

    @builtins.property
    def android_key_restrictions(
        self,
    ) -> typing.Optional["ApikeysKeyRestrictionsAndroidKeyRestrictions"]:
        '''android_key_restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#android_key_restrictions ApikeysKey#android_key_restrictions}
        '''
        result = self._values.get("android_key_restrictions")
        return typing.cast(typing.Optional["ApikeysKeyRestrictionsAndroidKeyRestrictions"], result)

    @builtins.property
    def api_targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApikeysKeyRestrictionsApiTargets"]]]:
        '''api_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#api_targets ApikeysKey#api_targets}
        '''
        result = self._values.get("api_targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApikeysKeyRestrictionsApiTargets"]]], result)

    @builtins.property
    def browser_key_restrictions(
        self,
    ) -> typing.Optional["ApikeysKeyRestrictionsBrowserKeyRestrictions"]:
        '''browser_key_restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#browser_key_restrictions ApikeysKey#browser_key_restrictions}
        '''
        result = self._values.get("browser_key_restrictions")
        return typing.cast(typing.Optional["ApikeysKeyRestrictionsBrowserKeyRestrictions"], result)

    @builtins.property
    def ios_key_restrictions(
        self,
    ) -> typing.Optional["ApikeysKeyRestrictionsIosKeyRestrictions"]:
        '''ios_key_restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#ios_key_restrictions ApikeysKey#ios_key_restrictions}
        '''
        result = self._values.get("ios_key_restrictions")
        return typing.cast(typing.Optional["ApikeysKeyRestrictionsIosKeyRestrictions"], result)

    @builtins.property
    def server_key_restrictions(
        self,
    ) -> typing.Optional["ApikeysKeyRestrictionsServerKeyRestrictions"]:
        '''server_key_restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#server_key_restrictions ApikeysKey#server_key_restrictions}
        '''
        result = self._values.get("server_key_restrictions")
        return typing.cast(typing.Optional["ApikeysKeyRestrictionsServerKeyRestrictions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsAndroidKeyRestrictions",
    jsii_struct_bases=[],
    name_mapping={"allowed_applications": "allowedApplications"},
)
class ApikeysKeyRestrictionsAndroidKeyRestrictions:
    def __init__(
        self,
        *,
        allowed_applications: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param allowed_applications: allowed_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_applications ApikeysKey#allowed_applications}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13cbd24ad08bd2323ff5cc7a0d62ca286c0eaa860b661e0e7ff65e0e13e89e9)
            check_type(argname="argument allowed_applications", value=allowed_applications, expected_type=type_hints["allowed_applications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_applications": allowed_applications,
        }

    @builtins.property
    def allowed_applications(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications"]]:
        '''allowed_applications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_applications ApikeysKey#allowed_applications}
        '''
        result = self._values.get("allowed_applications")
        assert result is not None, "Required property 'allowed_applications' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictionsAndroidKeyRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications",
    jsii_struct_bases=[],
    name_mapping={
        "package_name": "packageName",
        "sha1_fingerprint": "sha1Fingerprint",
    },
)
class ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications:
    def __init__(
        self,
        *,
        package_name: builtins.str,
        sha1_fingerprint: builtins.str,
    ) -> None:
        '''
        :param package_name: The package name of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#package_name ApikeysKey#package_name}
        :param sha1_fingerprint: The SHA1 fingerprint of the application. For example, both sha1 formats are acceptable : DA:39:A3:EE:5E:6B:4B:0D:32:55:BF:EF:95:60:18:90:AF:D8:07:09 or DA39A3EE5E6B4B0D3255BFEF95601890AFD80709. Output format is the latter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#sha1_fingerprint ApikeysKey#sha1_fingerprint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689261839cc9f86060f3781c21d3b4bd23e4cb8712accabf83e111751ca92570)
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument sha1_fingerprint", value=sha1_fingerprint, expected_type=type_hints["sha1_fingerprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_name": package_name,
            "sha1_fingerprint": sha1_fingerprint,
        }

    @builtins.property
    def package_name(self) -> builtins.str:
        '''The package name of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#package_name ApikeysKey#package_name}
        '''
        result = self._values.get("package_name")
        assert result is not None, "Required property 'package_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha1_fingerprint(self) -> builtins.str:
        '''The SHA1 fingerprint of the application.

        For example, both sha1 formats are acceptable : DA:39:A3:EE:5E:6B:4B:0D:32:55:BF:EF:95:60:18:90:AF:D8:07:09 or DA39A3EE5E6B4B0D3255BFEF95601890AFD80709. Output format is the latter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#sha1_fingerprint ApikeysKey#sha1_fingerprint}
        '''
        result = self._values.get("sha1_fingerprint")
        assert result is not None, "Required property 'sha1_fingerprint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fc392186ff6d49e835ff885848bf8a6d40634894b1dec881c545ee35656be54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94540cd42b9a5c2d08f5b1112d4fec312ece176b5484982c929e42c360b662c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60055000f68f3d553df90e8f5ed59862028fa1819eb98e4c8d02426cb654c65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e138a6726f0051c0a1d62a0f724dbbc200fef8b8fce5e021d15cba1f0ffa7a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__390a6d5edacb92584257574ebaaa7d479f6f3f0292745438a77f06e81ea77a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2122603e92367507c53bf18738eca98cf107c207a79428d4b1ad8adc6aaa49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1610c41220d8d0f75bcdc50b9f4c7d29ef9e785bd293f2e55413b22384bc2121)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="packageNameInput")
    def package_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sha1FingerprintInput")
    def sha1_fingerprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha1FingerprintInput"))

    @builtins.property
    @jsii.member(jsii_name="packageName")
    def package_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packageName"))

    @package_name.setter
    def package_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64eeea05b0585f6b17cf8d6475eecd6907ef496b8509b42e9f4f4708779fef27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha1Fingerprint")
    def sha1_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Fingerprint"))

    @sha1_fingerprint.setter
    def sha1_fingerprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5328f350989ea5fb10d2172b423e7407e322a3e333060e180690c28bb5609205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha1Fingerprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc29b914a5047c0922fcf083afc2602d7a5a66ad4200f19b6c927a0bb5894bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApikeysKeyRestrictionsAndroidKeyRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsAndroidKeyRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c5dae8042c3899340d8ab067282ee49a8403cf1df3b6979a9a7e6f028d47615)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedApplications")
    def put_allowed_applications(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09786c94aaad3ac8fb7be6794b4c93001dd96c3ec452f1573b5fd2cc3931a679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedApplications", [value]))

    @builtins.property
    @jsii.member(jsii_name="allowedApplications")
    def allowed_applications(
        self,
    ) -> ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsList:
        return typing.cast(ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsList, jsii.get(self, "allowedApplications"))

    @builtins.property
    @jsii.member(jsii_name="allowedApplicationsInput")
    def allowed_applications_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]], jsii.get(self, "allowedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsAndroidKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsAndroidKeyRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApikeysKeyRestrictionsAndroidKeyRestrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d727c66bbb5ca66a492799d11addb3d9dd8787cb01cdef8d9a1c437e4c3dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsApiTargets",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "methods": "methods"},
)
class ApikeysKeyRestrictionsApiTargets:
    def __init__(
        self,
        *,
        service: builtins.str,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param service: The service for this restriction. It should be the canonical service name, for example: ``translate.googleapis.com``. You can use ``gcloud services list`` to get a list of services that are enabled in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#service ApikeysKey#service}
        :param methods: Optional. List of one or more methods that can be called. If empty, all methods for the service are allowed. A wildcard (*) can be used as the last symbol. Valid examples: ``google.cloud.translate.v2.TranslateService.GetSupportedLanguage`` ``TranslateText`` ``Get*`` ``translate.googleapis.com.Get*`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#methods ApikeysKey#methods}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4c8d5c48ebf56143ae3d852cd5f2d4b5f7f7fcbeae4f8a82cda757a56e8e71)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if methods is not None:
            self._values["methods"] = methods

    @builtins.property
    def service(self) -> builtins.str:
        '''The service for this restriction.

        It should be the canonical service name, for example: ``translate.googleapis.com``. You can use ``gcloud services list`` to get a list of services that are enabled in the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#service ApikeysKey#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        List of one or more methods that can be called. If empty, all methods for the service are allowed. A wildcard (*) can be used as the last symbol. Valid examples: ``google.cloud.translate.v2.TranslateService.GetSupportedLanguage`` ``TranslateText`` ``Get*`` ``translate.googleapis.com.Get*``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#methods ApikeysKey#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictionsApiTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApikeysKeyRestrictionsApiTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsApiTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4bc9733a35e6430a659252ef56719375d2438363225563ba8aeac3c8dc02245)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApikeysKeyRestrictionsApiTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688546bb4d86de8e1555ce56cda4b35757246fd35f7592d4b55974e9813bc4da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApikeysKeyRestrictionsApiTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddfda6e3d0c8f477fc2d8c33c0a4807f3b9302329221d81dbc6f66a930e80ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4650bbb61f9f47419bd3e39f63ea82efb907060908eaaed1fa944e420e5d97a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__301387b4c8716689e610284d2a522bd4646b1c5bc726e92c2a1cd560c87ff3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsApiTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsApiTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsApiTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3107c49d47bb9e8a75740b586988f425cddb6235d6086898ed77f443d35a0907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApikeysKeyRestrictionsApiTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsApiTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__793df06eab5a13f35ff41a8aa8a10df2a63371db58fca7dcc738d50638a9e15a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethods")
    def reset_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethods", []))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebdf9a3f291dd819eed6de29fa65f81903bc3d9bce021f49dd91ce8b3f86430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a488277bce65e4e1e6b5fada01b28abecb224a4881a768602fcf25c8cab232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsApiTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsApiTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsApiTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9e5bdb326ce4ad23f6491b270829f96e724d3f8c3a9056d9dc52fe85a15b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsBrowserKeyRestrictions",
    jsii_struct_bases=[],
    name_mapping={"allowed_referrers": "allowedReferrers"},
)
class ApikeysKeyRestrictionsBrowserKeyRestrictions:
    def __init__(self, *, allowed_referrers: typing.Sequence[builtins.str]) -> None:
        '''
        :param allowed_referrers: A list of regular expressions for the referrer URLs that are allowed to make API calls with this key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_referrers ApikeysKey#allowed_referrers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ffaa4ef11a0c664d33e4f135e2a57124772f9ff8e2c1534799a721b638b07d)
            check_type(argname="argument allowed_referrers", value=allowed_referrers, expected_type=type_hints["allowed_referrers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_referrers": allowed_referrers,
        }

    @builtins.property
    def allowed_referrers(self) -> typing.List[builtins.str]:
        '''A list of regular expressions for the referrer URLs that are allowed to make API calls with this key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_referrers ApikeysKey#allowed_referrers}
        '''
        result = self._values.get("allowed_referrers")
        assert result is not None, "Required property 'allowed_referrers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictionsBrowserKeyRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApikeysKeyRestrictionsBrowserKeyRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsBrowserKeyRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7934e49f59b58d7a4046a653d2f93038c0da60b89ba4738ecea2136f5da7cf51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedReferrersInput")
    def allowed_referrers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedReferrersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedReferrers")
    def allowed_referrers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedReferrers"))

    @allowed_referrers.setter
    def allowed_referrers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec2ca471d59211ed02d27a6bf717a373a9424c126d8ee1dcee5e7fb2285e719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedReferrers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsBrowserKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsBrowserKeyRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApikeysKeyRestrictionsBrowserKeyRestrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75900fde199d553ed1190e0c04888f951fbfb0f3a7337640d4cbc8a27c92c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsIosKeyRestrictions",
    jsii_struct_bases=[],
    name_mapping={"allowed_bundle_ids": "allowedBundleIds"},
)
class ApikeysKeyRestrictionsIosKeyRestrictions:
    def __init__(self, *, allowed_bundle_ids: typing.Sequence[builtins.str]) -> None:
        '''
        :param allowed_bundle_ids: A list of bundle IDs that are allowed when making API calls with this key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_bundle_ids ApikeysKey#allowed_bundle_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e950e0ee910878c5f0705a8c087265587392a74f0fcc26625950f501ccfb3a0)
            check_type(argname="argument allowed_bundle_ids", value=allowed_bundle_ids, expected_type=type_hints["allowed_bundle_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_bundle_ids": allowed_bundle_ids,
        }

    @builtins.property
    def allowed_bundle_ids(self) -> typing.List[builtins.str]:
        '''A list of bundle IDs that are allowed when making API calls with this key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_bundle_ids ApikeysKey#allowed_bundle_ids}
        '''
        result = self._values.get("allowed_bundle_ids")
        assert result is not None, "Required property 'allowed_bundle_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictionsIosKeyRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApikeysKeyRestrictionsIosKeyRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsIosKeyRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8643c040b19c915405baf6f8128480fd73d801067a94b8e8da3b18e0f9df1d31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedBundleIdsInput")
    def allowed_bundle_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedBundleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedBundleIds")
    def allowed_bundle_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedBundleIds"))

    @allowed_bundle_ids.setter
    def allowed_bundle_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35a38abcab69c17dddd1cd3bbbc8138986a689515cd9c201b52087885abeefe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedBundleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsIosKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsIosKeyRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApikeysKeyRestrictionsIosKeyRestrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8eaf589457f0fb51062a1c986bc66ee3bc02343d902b01b9bf66dc1edd93b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApikeysKeyRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb9a2039dc803303ecd116aba099c2bc4c6a4cd8958fc2fd3a81c3fc900d9098)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAndroidKeyRestrictions")
    def put_android_key_restrictions(
        self,
        *,
        allowed_applications: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param allowed_applications: allowed_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_applications ApikeysKey#allowed_applications}
        '''
        value = ApikeysKeyRestrictionsAndroidKeyRestrictions(
            allowed_applications=allowed_applications
        )

        return typing.cast(None, jsii.invoke(self, "putAndroidKeyRestrictions", [value]))

    @jsii.member(jsii_name="putApiTargets")
    def put_api_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsApiTargets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c93085272d0f38f54ad9ad6dd2246964903fbe516f644ccb90e3c8d3dc7c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiTargets", [value]))

    @jsii.member(jsii_name="putBrowserKeyRestrictions")
    def put_browser_key_restrictions(
        self,
        *,
        allowed_referrers: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_referrers: A list of regular expressions for the referrer URLs that are allowed to make API calls with this key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_referrers ApikeysKey#allowed_referrers}
        '''
        value = ApikeysKeyRestrictionsBrowserKeyRestrictions(
            allowed_referrers=allowed_referrers
        )

        return typing.cast(None, jsii.invoke(self, "putBrowserKeyRestrictions", [value]))

    @jsii.member(jsii_name="putIosKeyRestrictions")
    def put_ios_key_restrictions(
        self,
        *,
        allowed_bundle_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_bundle_ids: A list of bundle IDs that are allowed when making API calls with this key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_bundle_ids ApikeysKey#allowed_bundle_ids}
        '''
        value = ApikeysKeyRestrictionsIosKeyRestrictions(
            allowed_bundle_ids=allowed_bundle_ids
        )

        return typing.cast(None, jsii.invoke(self, "putIosKeyRestrictions", [value]))

    @jsii.member(jsii_name="putServerKeyRestrictions")
    def put_server_key_restrictions(
        self,
        *,
        allowed_ips: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_ips: A list of the caller IP addresses that are allowed to make API calls with this key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_ips ApikeysKey#allowed_ips}
        '''
        value = ApikeysKeyRestrictionsServerKeyRestrictions(allowed_ips=allowed_ips)

        return typing.cast(None, jsii.invoke(self, "putServerKeyRestrictions", [value]))

    @jsii.member(jsii_name="resetAndroidKeyRestrictions")
    def reset_android_key_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAndroidKeyRestrictions", []))

    @jsii.member(jsii_name="resetApiTargets")
    def reset_api_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiTargets", []))

    @jsii.member(jsii_name="resetBrowserKeyRestrictions")
    def reset_browser_key_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowserKeyRestrictions", []))

    @jsii.member(jsii_name="resetIosKeyRestrictions")
    def reset_ios_key_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIosKeyRestrictions", []))

    @jsii.member(jsii_name="resetServerKeyRestrictions")
    def reset_server_key_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerKeyRestrictions", []))

    @builtins.property
    @jsii.member(jsii_name="androidKeyRestrictions")
    def android_key_restrictions(
        self,
    ) -> ApikeysKeyRestrictionsAndroidKeyRestrictionsOutputReference:
        return typing.cast(ApikeysKeyRestrictionsAndroidKeyRestrictionsOutputReference, jsii.get(self, "androidKeyRestrictions"))

    @builtins.property
    @jsii.member(jsii_name="apiTargets")
    def api_targets(self) -> ApikeysKeyRestrictionsApiTargetsList:
        return typing.cast(ApikeysKeyRestrictionsApiTargetsList, jsii.get(self, "apiTargets"))

    @builtins.property
    @jsii.member(jsii_name="browserKeyRestrictions")
    def browser_key_restrictions(
        self,
    ) -> ApikeysKeyRestrictionsBrowserKeyRestrictionsOutputReference:
        return typing.cast(ApikeysKeyRestrictionsBrowserKeyRestrictionsOutputReference, jsii.get(self, "browserKeyRestrictions"))

    @builtins.property
    @jsii.member(jsii_name="iosKeyRestrictions")
    def ios_key_restrictions(
        self,
    ) -> ApikeysKeyRestrictionsIosKeyRestrictionsOutputReference:
        return typing.cast(ApikeysKeyRestrictionsIosKeyRestrictionsOutputReference, jsii.get(self, "iosKeyRestrictions"))

    @builtins.property
    @jsii.member(jsii_name="serverKeyRestrictions")
    def server_key_restrictions(
        self,
    ) -> "ApikeysKeyRestrictionsServerKeyRestrictionsOutputReference":
        return typing.cast("ApikeysKeyRestrictionsServerKeyRestrictionsOutputReference", jsii.get(self, "serverKeyRestrictions"))

    @builtins.property
    @jsii.member(jsii_name="androidKeyRestrictionsInput")
    def android_key_restrictions_input(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsAndroidKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsAndroidKeyRestrictions], jsii.get(self, "androidKeyRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTargetsInput")
    def api_targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsApiTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsApiTargets]]], jsii.get(self, "apiTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="browserKeyRestrictionsInput")
    def browser_key_restrictions_input(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsBrowserKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsBrowserKeyRestrictions], jsii.get(self, "browserKeyRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="iosKeyRestrictionsInput")
    def ios_key_restrictions_input(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsIosKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsIosKeyRestrictions], jsii.get(self, "iosKeyRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverKeyRestrictionsInput")
    def server_key_restrictions_input(
        self,
    ) -> typing.Optional["ApikeysKeyRestrictionsServerKeyRestrictions"]:
        return typing.cast(typing.Optional["ApikeysKeyRestrictionsServerKeyRestrictions"], jsii.get(self, "serverKeyRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApikeysKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApikeysKeyRestrictions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993f8db9fcd1d4ff30ee30345dd86569b629b422099c93d78b11a01d8e67b112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsServerKeyRestrictions",
    jsii_struct_bases=[],
    name_mapping={"allowed_ips": "allowedIps"},
)
class ApikeysKeyRestrictionsServerKeyRestrictions:
    def __init__(self, *, allowed_ips: typing.Sequence[builtins.str]) -> None:
        '''
        :param allowed_ips: A list of the caller IP addresses that are allowed to make API calls with this key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_ips ApikeysKey#allowed_ips}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e2c7ed7a53e1f714d20c1bf5adcb366d2952b42d815a3e77bd858dc36cf991)
            check_type(argname="argument allowed_ips", value=allowed_ips, expected_type=type_hints["allowed_ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_ips": allowed_ips,
        }

    @builtins.property
    def allowed_ips(self) -> typing.List[builtins.str]:
        '''A list of the caller IP addresses that are allowed to make API calls with this key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#allowed_ips ApikeysKey#allowed_ips}
        '''
        result = self._values.get("allowed_ips")
        assert result is not None, "Required property 'allowed_ips' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyRestrictionsServerKeyRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApikeysKeyRestrictionsServerKeyRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyRestrictionsServerKeyRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd599208265bcb8149118bbdd00b5af1549d39e96744db1820cb09e5ee5f90ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedIpsInput")
    def allowed_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIps")
    def allowed_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIps"))

    @allowed_ips.setter
    def allowed_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba103f483b01c50e21271e689b98416007d93c9602e7fc10f1fad5636448edb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApikeysKeyRestrictionsServerKeyRestrictions]:
        return typing.cast(typing.Optional[ApikeysKeyRestrictionsServerKeyRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApikeysKeyRestrictionsServerKeyRestrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf9a477fd401ad35eb136fb0a6347e6f4d6e0bed71c53a5ffca33878e46fff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApikeysKeyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#create ApikeysKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#delete ApikeysKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#update ApikeysKey#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8bd51e6e5bb3c78de2ba49d6c99cb150583c571bfed38c9439eac2251ef00f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#create ApikeysKey#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#delete ApikeysKey#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apikeys_key#update ApikeysKey#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApikeysKeyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApikeysKeyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apikeysKey.ApikeysKeyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e0b061c7d91c1110ecba0060e6bb4cc6909792be200efe42b04d69c40780a90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef5571940520677069ee27ab9c07e57c06472358c073437d7f4e55c161f06aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6e995a63a0fa922c24bcae498781c9780503567eeab24090a2807f009049a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75f2711f37332c822f9917b86078e4dbb2ce57bd95436c2afd87e1c1a14f148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935659fc373323bb9129edf710c773bca4a337b7cf7cdae8beb51c7bd5e710ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApikeysKey",
    "ApikeysKeyConfig",
    "ApikeysKeyRestrictions",
    "ApikeysKeyRestrictionsAndroidKeyRestrictions",
    "ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications",
    "ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsList",
    "ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplicationsOutputReference",
    "ApikeysKeyRestrictionsAndroidKeyRestrictionsOutputReference",
    "ApikeysKeyRestrictionsApiTargets",
    "ApikeysKeyRestrictionsApiTargetsList",
    "ApikeysKeyRestrictionsApiTargetsOutputReference",
    "ApikeysKeyRestrictionsBrowserKeyRestrictions",
    "ApikeysKeyRestrictionsBrowserKeyRestrictionsOutputReference",
    "ApikeysKeyRestrictionsIosKeyRestrictions",
    "ApikeysKeyRestrictionsIosKeyRestrictionsOutputReference",
    "ApikeysKeyRestrictionsOutputReference",
    "ApikeysKeyRestrictionsServerKeyRestrictions",
    "ApikeysKeyRestrictionsServerKeyRestrictionsOutputReference",
    "ApikeysKeyTimeouts",
    "ApikeysKeyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6ae4a8afd0e07d7eb325545f7c42fddb686e038ee1a78c37fa837dc7807d6d16(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    restrictions: typing.Optional[typing.Union[ApikeysKeyRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApikeysKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dd32c3a9fbf82a9cbc124661804c78f9244fcc5322951f716e113b6acbecff2c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e44538a83a67996b152b17ba043cee9e90563cf0c442212c4d9834c503ffcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3e697a1fe6ff68771aa4e98ddfe3d438d9f8bca899139e34eb43cf33f4c81b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8f4dc0839a7b081cc071326dc193738574477a898ca235cfed21e6becb1c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3255aea4cb67ac4fa6d538efd14de52e9b0e5b91549f13ea69d1cb32189d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b262dadd92109a838856d13c8962318659b99869846b732bd8704d45cb9818b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    restrictions: typing.Optional[typing.Union[ApikeysKeyRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApikeysKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0472af26dccd4e25ad2b33ed54ddbd3b8cc7e17026294ac76499d05e3911022(
    *,
    android_key_restrictions: typing.Optional[typing.Union[ApikeysKeyRestrictionsAndroidKeyRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    api_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsApiTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    browser_key_restrictions: typing.Optional[typing.Union[ApikeysKeyRestrictionsBrowserKeyRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    ios_key_restrictions: typing.Optional[typing.Union[ApikeysKeyRestrictionsIosKeyRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    server_key_restrictions: typing.Optional[typing.Union[ApikeysKeyRestrictionsServerKeyRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13cbd24ad08bd2323ff5cc7a0d62ca286c0eaa860b661e0e7ff65e0e13e89e9(
    *,
    allowed_applications: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689261839cc9f86060f3781c21d3b4bd23e4cb8712accabf83e111751ca92570(
    *,
    package_name: builtins.str,
    sha1_fingerprint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc392186ff6d49e835ff885848bf8a6d40634894b1dec881c545ee35656be54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94540cd42b9a5c2d08f5b1112d4fec312ece176b5484982c929e42c360b662c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60055000f68f3d553df90e8f5ed59862028fa1819eb98e4c8d02426cb654c65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e138a6726f0051c0a1d62a0f724dbbc200fef8b8fce5e021d15cba1f0ffa7a20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390a6d5edacb92584257574ebaaa7d479f6f3f0292745438a77f06e81ea77a93(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2122603e92367507c53bf18738eca98cf107c207a79428d4b1ad8adc6aaa49a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1610c41220d8d0f75bcdc50b9f4c7d29ef9e785bd293f2e55413b22384bc2121(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64eeea05b0585f6b17cf8d6475eecd6907ef496b8509b42e9f4f4708779fef27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5328f350989ea5fb10d2172b423e7407e322a3e333060e180690c28bb5609205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc29b914a5047c0922fcf083afc2602d7a5a66ad4200f19b6c927a0bb5894bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5dae8042c3899340d8ab067282ee49a8403cf1df3b6979a9a7e6f028d47615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09786c94aaad3ac8fb7be6794b4c93001dd96c3ec452f1573b5fd2cc3931a679(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsAndroidKeyRestrictionsAllowedApplications, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d727c66bbb5ca66a492799d11addb3d9dd8787cb01cdef8d9a1c437e4c3dd5(
    value: typing.Optional[ApikeysKeyRestrictionsAndroidKeyRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4c8d5c48ebf56143ae3d852cd5f2d4b5f7f7fcbeae4f8a82cda757a56e8e71(
    *,
    service: builtins.str,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bc9733a35e6430a659252ef56719375d2438363225563ba8aeac3c8dc02245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688546bb4d86de8e1555ce56cda4b35757246fd35f7592d4b55974e9813bc4da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddfda6e3d0c8f477fc2d8c33c0a4807f3b9302329221d81dbc6f66a930e80ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4650bbb61f9f47419bd3e39f63ea82efb907060908eaaed1fa944e420e5d97a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301387b4c8716689e610284d2a522bd4646b1c5bc726e92c2a1cd560c87ff3ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3107c49d47bb9e8a75740b586988f425cddb6235d6086898ed77f443d35a0907(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApikeysKeyRestrictionsApiTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793df06eab5a13f35ff41a8aa8a10df2a63371db58fca7dcc738d50638a9e15a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebdf9a3f291dd819eed6de29fa65f81903bc3d9bce021f49dd91ce8b3f86430(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a488277bce65e4e1e6b5fada01b28abecb224a4881a768602fcf25c8cab232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9e5bdb326ce4ad23f6491b270829f96e724d3f8c3a9056d9dc52fe85a15b2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyRestrictionsApiTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ffaa4ef11a0c664d33e4f135e2a57124772f9ff8e2c1534799a721b638b07d(
    *,
    allowed_referrers: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7934e49f59b58d7a4046a653d2f93038c0da60b89ba4738ecea2136f5da7cf51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec2ca471d59211ed02d27a6bf717a373a9424c126d8ee1dcee5e7fb2285e719(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75900fde199d553ed1190e0c04888f951fbfb0f3a7337640d4cbc8a27c92c9f(
    value: typing.Optional[ApikeysKeyRestrictionsBrowserKeyRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e950e0ee910878c5f0705a8c087265587392a74f0fcc26625950f501ccfb3a0(
    *,
    allowed_bundle_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8643c040b19c915405baf6f8128480fd73d801067a94b8e8da3b18e0f9df1d31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35a38abcab69c17dddd1cd3bbbc8138986a689515cd9c201b52087885abeefe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8eaf589457f0fb51062a1c986bc66ee3bc02343d902b01b9bf66dc1edd93b2(
    value: typing.Optional[ApikeysKeyRestrictionsIosKeyRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9a2039dc803303ecd116aba099c2bc4c6a4cd8958fc2fd3a81c3fc900d9098(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c93085272d0f38f54ad9ad6dd2246964903fbe516f644ccb90e3c8d3dc7c6d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApikeysKeyRestrictionsApiTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993f8db9fcd1d4ff30ee30345dd86569b629b422099c93d78b11a01d8e67b112(
    value: typing.Optional[ApikeysKeyRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e2c7ed7a53e1f714d20c1bf5adcb366d2952b42d815a3e77bd858dc36cf991(
    *,
    allowed_ips: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd599208265bcb8149118bbdd00b5af1549d39e96744db1820cb09e5ee5f90ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba103f483b01c50e21271e689b98416007d93c9602e7fc10f1fad5636448edb0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf9a477fd401ad35eb136fb0a6347e6f4d6e0bed71c53a5ffca33878e46fff4(
    value: typing.Optional[ApikeysKeyRestrictionsServerKeyRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8bd51e6e5bb3c78de2ba49d6c99cb150583c571bfed38c9439eac2251ef00f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0b061c7d91c1110ecba0060e6bb4cc6909792be200efe42b04d69c40780a90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef5571940520677069ee27ab9c07e57c06472358c073437d7f4e55c161f06aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6e995a63a0fa922c24bcae498781c9780503567eeab24090a2807f009049a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75f2711f37332c822f9917b86078e4dbb2ce57bd95436c2afd87e1c1a14f148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935659fc373323bb9129edf710c773bca4a337b7cf7cdae8beb51c7bd5e710ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApikeysKeyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
