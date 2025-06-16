r'''
# `google_firebase_hosting_version`

Refer to the Terraform Registry for docs: [`google_firebase_hosting_version`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version).
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


class GoogleFirebaseHostingVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version google_firebase_hosting_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        site_id: builtins.str,
        config: typing.Optional[typing.Union["GoogleFirebaseHostingVersionConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleFirebaseHostingVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version google_firebase_hosting_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param site_id: Required. The ID of the site in which to create this Version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#site_id GoogleFirebaseHostingVersion#site_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#config GoogleFirebaseHostingVersion#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#id GoogleFirebaseHostingVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#timeouts GoogleFirebaseHostingVersion#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d13d9d720f802fbba133ba4b98b0dd20d336680aca16315ee33eab3b84d3345)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = GoogleFirebaseHostingVersionConfig(
            site_id=site_id,
            config=config,
            id=id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a GoogleFirebaseHostingVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleFirebaseHostingVersion to import.
        :param import_from_id: The id of the existing GoogleFirebaseHostingVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleFirebaseHostingVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2447cb9130b43623dc121aa02c0397a8bcf130900aba4557f04723bc24e34734)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigRedirects", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rewrites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigRewrites", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#headers GoogleFirebaseHostingVersion#headers}
        :param redirects: redirects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#redirects GoogleFirebaseHostingVersion#redirects}
        :param rewrites: rewrites block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#rewrites GoogleFirebaseHostingVersion#rewrites}
        '''
        value = GoogleFirebaseHostingVersionConfigA(
            headers=headers, redirects=redirects, rewrites=rewrites
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#create GoogleFirebaseHostingVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#delete GoogleFirebaseHostingVersion#delete}.
        '''
        value = GoogleFirebaseHostingVersionTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "GoogleFirebaseHostingVersionConfigAOutputReference":
        return typing.cast("GoogleFirebaseHostingVersionConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleFirebaseHostingVersionTimeoutsOutputReference":
        return typing.cast("GoogleFirebaseHostingVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["GoogleFirebaseHostingVersionConfigA"]:
        return typing.cast(typing.Optional["GoogleFirebaseHostingVersionConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="siteIdInput")
    def site_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleFirebaseHostingVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleFirebaseHostingVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3987da7e4bb845f6312a2b0584e859aa2cc0811a74cc0088f7c056c0ea2f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteId"))

    @site_id.setter
    def site_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdfd9bda572e5c08580a2ddb707ae14eb18b607552b5db1f5da49f5cf404e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "site_id": "siteId",
        "config": "config",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleFirebaseHostingVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        site_id: builtins.str,
        config: typing.Optional[typing.Union["GoogleFirebaseHostingVersionConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleFirebaseHostingVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param site_id: Required. The ID of the site in which to create this Version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#site_id GoogleFirebaseHostingVersion#site_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#config GoogleFirebaseHostingVersion#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#id GoogleFirebaseHostingVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#timeouts GoogleFirebaseHostingVersion#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = GoogleFirebaseHostingVersionConfigA(**config)
        if isinstance(timeouts, dict):
            timeouts = GoogleFirebaseHostingVersionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de479cda3b1af04db331f0d99f16b5cf63d32e8bde78ba137893601f66e5948)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument site_id", value=site_id, expected_type=type_hints["site_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_id": site_id,
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
        if config is not None:
            self._values["config"] = config
        if id is not None:
            self._values["id"] = id
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
    def site_id(self) -> builtins.str:
        '''Required. The ID of the site in which to create this Version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#site_id GoogleFirebaseHostingVersion#site_id}
        '''
        result = self._values.get("site_id")
        assert result is not None, "Required property 'site_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["GoogleFirebaseHostingVersionConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#config GoogleFirebaseHostingVersion#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleFirebaseHostingVersionConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#id GoogleFirebaseHostingVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleFirebaseHostingVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#timeouts GoogleFirebaseHostingVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleFirebaseHostingVersionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "headers": "headers",
        "redirects": "redirects",
        "rewrites": "rewrites",
    },
)
class GoogleFirebaseHostingVersionConfigA:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigRedirects", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rewrites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigRewrites", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#headers GoogleFirebaseHostingVersion#headers}
        :param redirects: redirects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#redirects GoogleFirebaseHostingVersion#redirects}
        :param rewrites: rewrites block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#rewrites GoogleFirebaseHostingVersion#rewrites}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3855947fecf52c08d151c14c9bb8bc28891eb0e7afa98a8de09483a66a672b16)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument redirects", value=redirects, expected_type=type_hints["redirects"])
            check_type(argname="argument rewrites", value=rewrites, expected_type=type_hints["rewrites"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers
        if redirects is not None:
            self._values["redirects"] = redirects
        if rewrites is not None:
            self._values["rewrites"] = rewrites

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#headers GoogleFirebaseHostingVersion#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigHeaders"]]], result)

    @builtins.property
    def redirects(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRedirects"]]]:
        '''redirects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#redirects GoogleFirebaseHostingVersion#redirects}
        '''
        result = self._values.get("redirects")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRedirects"]]], result)

    @builtins.property
    def rewrites(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRewrites"]]]:
        '''rewrites block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#rewrites GoogleFirebaseHostingVersion#rewrites}
        '''
        result = self._values.get("rewrites")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRewrites"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFirebaseHostingVersionConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835aa58ef1f1b8e3901301856f4ad668eecd829ad0c2e308fa8437ae1f688808)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f480a5382dc0c6cb49a6130d0a52d19a38ccfdda7d02a1f7ac1fb99777dbaafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putRedirects")
    def put_redirects(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigRedirects", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc724ea59ea32784b4c39697cb8c67454a7ab3f3246462274e879914f312290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedirects", [value]))

    @jsii.member(jsii_name="putRewrites")
    def put_rewrites(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleFirebaseHostingVersionConfigRewrites", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d4087654e470be21350668ec9720203dfb911c2cccc5ef322ccc942cdd45aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRewrites", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetRedirects")
    def reset_redirects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirects", []))

    @jsii.member(jsii_name="resetRewrites")
    def reset_rewrites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewrites", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> "GoogleFirebaseHostingVersionConfigHeadersList":
        return typing.cast("GoogleFirebaseHostingVersionConfigHeadersList", jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="redirects")
    def redirects(self) -> "GoogleFirebaseHostingVersionConfigRedirectsList":
        return typing.cast("GoogleFirebaseHostingVersionConfigRedirectsList", jsii.get(self, "redirects"))

    @builtins.property
    @jsii.member(jsii_name="rewrites")
    def rewrites(self) -> "GoogleFirebaseHostingVersionConfigRewritesList":
        return typing.cast("GoogleFirebaseHostingVersionConfigRewritesList", jsii.get(self, "rewrites"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigHeaders"]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectsInput")
    def redirects_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRedirects"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRedirects"]]], jsii.get(self, "redirectsInput"))

    @builtins.property
    @jsii.member(jsii_name="rewritesInput")
    def rewrites_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRewrites"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleFirebaseHostingVersionConfigRewrites"]]], jsii.get(self, "rewritesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleFirebaseHostingVersionConfigA]:
        return typing.cast(typing.Optional[GoogleFirebaseHostingVersionConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFirebaseHostingVersionConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83970e58150d5508bb812168f2a623bf8b87645a895d7ca7d1690aff4570f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigHeaders",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "glob": "glob", "regex": "regex"},
)
class GoogleFirebaseHostingVersionConfigHeaders:
    def __init__(
        self,
        *,
        headers: typing.Mapping[builtins.str, builtins.str],
        glob: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param headers: The additional headers to add to the response. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#headers GoogleFirebaseHostingVersion#headers}
        :param glob: The user-supplied glob to match against the request URL path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#glob GoogleFirebaseHostingVersion#glob}
        :param regex: The user-supplied RE2 regular expression to match against the request URL path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#regex GoogleFirebaseHostingVersion#regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cf0f6795f76bda90686aff48ada944f8502cf1f6f7b48d92e6f5f03ff9b7fd)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument glob", value=glob, expected_type=type_hints["glob"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "headers": headers,
        }
        if glob is not None:
            self._values["glob"] = glob
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The additional headers to add to the response. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#headers GoogleFirebaseHostingVersion#headers}
        '''
        result = self._values.get("headers")
        assert result is not None, "Required property 'headers' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def glob(self) -> typing.Optional[builtins.str]:
        '''The user-supplied glob to match against the request URL path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#glob GoogleFirebaseHostingVersion#glob}
        '''
        result = self._values.get("glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''The user-supplied RE2 regular expression to match against the request URL path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#regex GoogleFirebaseHostingVersion#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionConfigHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFirebaseHostingVersionConfigHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9222f68e474d01b07be2c2a691ffb118087ee09db9cefa3022f2dbad4ccac80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFirebaseHostingVersionConfigHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2efa1fe40c86760772d2b5536bb0a41fe5457c66ff66a4ecc11caea0a88e073)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFirebaseHostingVersionConfigHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d9d876fe08abef4a561692f9f898f6fc960cf7d1dc214fc8f1152c0a52e29a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388bbeb2532a1c830f521eb153bf3f8e7823de8d6c6d0cd25c5289f4eeec2c52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a8df77c46b3fe56d911688b233fa7928da976cd4dd981ec343ac7655ec7d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bf9062d2d8439df993cc3a7b4abc315a7068ce43a769c5fa912819b0fd3f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFirebaseHostingVersionConfigHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a586031d107dd66f1235e26e3b2a7c3121b98f9910c73b15dbbe602f1dfffe9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGlob")
    def reset_glob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlob", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @builtins.property
    @jsii.member(jsii_name="globInput")
    def glob_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="glob")
    def glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "glob"))

    @glob.setter
    def glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa83508340eecff953c3586352a3ca8792b29d4c9095592c30c96a3526093f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "glob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5278d010d6d60659f1f1a25d9210b9ef4d74f82a23f0eff6bb9ca7c6b9b138bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6d70593ca474bb8029da93f804ba40acc15029889bb67c76db2d62f0566c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43f7bd016315dcf7d2c57142d4435ab5b4906f010a6cbf2da6b3a20f32fcccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRedirects",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "status_code": "statusCode",
        "glob": "glob",
        "regex": "regex",
    },
)
class GoogleFirebaseHostingVersionConfigRedirects:
    def __init__(
        self,
        *,
        location: builtins.str,
        status_code: jsii.Number,
        glob: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: The value to put in the HTTP location header of the response. The location can contain capture group values from the pattern using a : prefix to identify the segment and an optional * to capture the rest of the URL. For example:: redirects { glob = "/:capture*" status_code = 302 location = "https://example.com/foo/:capture" } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#location GoogleFirebaseHostingVersion#location}
        :param status_code: The status HTTP code to return in the response. It must be a valid 3xx status code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#status_code GoogleFirebaseHostingVersion#status_code}
        :param glob: The user-supplied glob to match against the request URL path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#glob GoogleFirebaseHostingVersion#glob}
        :param regex: The user-supplied RE2 regular expression to match against the request URL path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#regex GoogleFirebaseHostingVersion#regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd78c497bece651d7033cd6241a6f248165adea8771d4035df0589886120feef)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument glob", value=glob, expected_type=type_hints["glob"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "status_code": status_code,
        }
        if glob is not None:
            self._values["glob"] = glob
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def location(self) -> builtins.str:
        '''The value to put in the HTTP location header of the response.

        The location can contain capture group values from the pattern using a : prefix to identify
        the segment and an optional * to capture the rest of the URL. For example::

           redirects {
             glob = "/:capture*"
             status_code = 302
             location = "https://example.com/foo/:capture"
           }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#location GoogleFirebaseHostingVersion#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> jsii.Number:
        '''The status HTTP code to return in the response. It must be a valid 3xx status code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#status_code GoogleFirebaseHostingVersion#status_code}
        '''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def glob(self) -> typing.Optional[builtins.str]:
        '''The user-supplied glob to match against the request URL path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#glob GoogleFirebaseHostingVersion#glob}
        '''
        result = self._values.get("glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''The user-supplied RE2 regular expression to match against the request URL path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#regex GoogleFirebaseHostingVersion#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionConfigRedirects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFirebaseHostingVersionConfigRedirectsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRedirectsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a3ad54bdb210bd3135594e1466fba317977be8bc41b60a9ea616ecccfd3a99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFirebaseHostingVersionConfigRedirectsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36181271616e602230cecc606a3b0c8e18da89c982df45fd7b1d2ea32450b1af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFirebaseHostingVersionConfigRedirectsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe45393f69737ec4bdf99597e1c0b4681dd4aaa4bf1be0781850bf9b7af369e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a21fc07a4796404ff69691b9f857441d4e7afd0b941c8e570c5097afab4d36b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a5de1b4cb99a694a4c4723d26010c5ae32435f3bbc824c9280f73436876af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRedirects]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRedirects]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRedirects]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca34e2919d617165f55101fd8d8fea204489a08866a86402640ef9b0ad363f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFirebaseHostingVersionConfigRedirectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRedirectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d09db5f53621e67b4abb1dfe88cd699c5f962ae8c996c115cfaa9a1c3326485)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGlob")
    def reset_glob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlob", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @builtins.property
    @jsii.member(jsii_name="globInput")
    def glob_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="glob")
    def glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "glob"))

    @glob.setter
    def glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aab39f5d7f2bf065c198e4b6ae145b24d43fab8a38fd486eb830bad4dc33a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "glob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c9162839e786b3bc74d4101f63290e1af1ee682d2830cf3cf929c7c774f9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3560ca72495dd3a8a687972d4b1e613c1b029e76d4af3d219d26ef2ec87ad683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29bd1362361345a5e154e22527fa8137f98807cbe2a53ab67dd526ee8083b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRedirects]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRedirects]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRedirects]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fde02e4b46c5525818ab9586d0bad2c96d284ee14fef9f18e08f8d4cb5d59ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRewrites",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "glob": "glob",
        "path": "path",
        "regex": "regex",
        "run": "run",
    },
)
class GoogleFirebaseHostingVersionConfigRewrites:
    def __init__(
        self,
        *,
        function: typing.Optional[builtins.str] = None,
        glob: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
        run: typing.Optional[typing.Union["GoogleFirebaseHostingVersionConfigRewritesRun", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param function: The function to proxy requests to. Must match the exported function name exactly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#function GoogleFirebaseHostingVersion#function}
        :param glob: The user-supplied glob to match against the request URL path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#glob GoogleFirebaseHostingVersion#glob}
        :param path: The URL path to rewrite the request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#path GoogleFirebaseHostingVersion#path}
        :param regex: The user-supplied RE2 regular expression to match against the request URL path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#regex GoogleFirebaseHostingVersion#regex}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#run GoogleFirebaseHostingVersion#run}
        '''
        if isinstance(run, dict):
            run = GoogleFirebaseHostingVersionConfigRewritesRun(**run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e43834f56a19f05c9297fdcbf4cc60665462e409f3982eb8f524206d5ed0df)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument glob", value=glob, expected_type=type_hints["glob"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if function is not None:
            self._values["function"] = function
        if glob is not None:
            self._values["glob"] = glob
        if path is not None:
            self._values["path"] = path
        if regex is not None:
            self._values["regex"] = regex
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def function(self) -> typing.Optional[builtins.str]:
        '''The function to proxy requests to. Must match the exported function name exactly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#function GoogleFirebaseHostingVersion#function}
        '''
        result = self._values.get("function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glob(self) -> typing.Optional[builtins.str]:
        '''The user-supplied glob to match against the request URL path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#glob GoogleFirebaseHostingVersion#glob}
        '''
        result = self._values.get("glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URL path to rewrite the request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#path GoogleFirebaseHostingVersion#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''The user-supplied RE2 regular expression to match against the request URL path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#regex GoogleFirebaseHostingVersion#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional["GoogleFirebaseHostingVersionConfigRewritesRun"]:
        '''run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#run GoogleFirebaseHostingVersion#run}
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["GoogleFirebaseHostingVersionConfigRewritesRun"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionConfigRewrites(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFirebaseHostingVersionConfigRewritesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRewritesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8493d9447a7f884b3e213fffe2509266448aecc8a15b84baa455c4b8f12ce7cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleFirebaseHostingVersionConfigRewritesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ee9e39607c28f4d8be74a9c6de821276eed3e3fe3460ea6d186ced4ea4f161)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleFirebaseHostingVersionConfigRewritesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde06913c44f5adcca2c09b378d97c4b8af81b57fd133f69ee268b0a0c539d55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de295f2dd7c0a5e4337a0cf5dc0c72e9f009ec18a9933fe6923d02d21284b20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddc1e2d091ae6ef01f82da1e4b6d7792b09b4d3e004091ab2e8c9c448b0bd38c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRewrites]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRewrites]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRewrites]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f04a13b1b860bc82971bd0fa8658866b878cd4155758ee8fee34183d587f6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleFirebaseHostingVersionConfigRewritesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRewritesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05be7cacaa2e7535880e771c9e2158f0f2ef2027bc131118bc54e1c16e340e9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRun")
    def put_run(
        self,
        *,
        service_id: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_id: User-defined ID of the Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#service_id GoogleFirebaseHostingVersion#service_id}
        :param region: Optional. User-provided region where the Cloud Run service is hosted. Defaults to 'us-central1' if not supplied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#region GoogleFirebaseHostingVersion#region}
        '''
        value = GoogleFirebaseHostingVersionConfigRewritesRun(
            service_id=service_id, region=region
        )

        return typing.cast(None, jsii.invoke(self, "putRun", [value]))

    @jsii.member(jsii_name="resetFunction")
    def reset_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunction", []))

    @jsii.member(jsii_name="resetGlob")
    def reset_glob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlob", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetRun")
    def reset_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRun", []))

    @builtins.property
    @jsii.member(jsii_name="run")
    def run(self) -> "GoogleFirebaseHostingVersionConfigRewritesRunOutputReference":
        return typing.cast("GoogleFirebaseHostingVersionConfigRewritesRunOutputReference", jsii.get(self, "run"))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="globInput")
    def glob_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="runInput")
    def run_input(
        self,
    ) -> typing.Optional["GoogleFirebaseHostingVersionConfigRewritesRun"]:
        return typing.cast(typing.Optional["GoogleFirebaseHostingVersionConfigRewritesRun"], jsii.get(self, "runInput"))

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c087df3c34c022e918ac62e78a1c2be546a6c67fb99961b6cba74d5b0d0fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="glob")
    def glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "glob"))

    @glob.setter
    def glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5b14cbdf82526a168dede4f06750287fdd3364c1ed55bc3547e184db981036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "glob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140ec7f6884323a852bf32c7cf1508ba41fd6406668a12212f690c9723295a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6679247ff6b0aedba7391a4524916841ce99f528a9e69197028c8c46ba7336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRewrites]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRewrites]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRewrites]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ae286f79e3e919e09303a4027e1f6dfaddccac5f81601cbae6c6708c5b7931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRewritesRun",
    jsii_struct_bases=[],
    name_mapping={"service_id": "serviceId", "region": "region"},
)
class GoogleFirebaseHostingVersionConfigRewritesRun:
    def __init__(
        self,
        *,
        service_id: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_id: User-defined ID of the Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#service_id GoogleFirebaseHostingVersion#service_id}
        :param region: Optional. User-provided region where the Cloud Run service is hosted. Defaults to 'us-central1' if not supplied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#region GoogleFirebaseHostingVersion#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9b08fb1bd013042973d640f231ea57fe1e5bbfbd4e408724904f0297595738)
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_id": service_id,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def service_id(self) -> builtins.str:
        '''User-defined ID of the Cloud Run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#service_id GoogleFirebaseHostingVersion#service_id}
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Optional. User-provided region where the Cloud Run service is hosted. Defaults to 'us-central1' if not supplied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#region GoogleFirebaseHostingVersion#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionConfigRewritesRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFirebaseHostingVersionConfigRewritesRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionConfigRewritesRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81ceb7aef650d02695c6281be19b4af219f2794adf6dc660def5ff901ae82178)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIdInput")
    def service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b379e763c33420e94a9e13014c7e3ecc1bd48eaa1ea355e21f68d0ca7cb4ff9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @service_id.setter
    def service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79299924903312f441954c407d04f64e5ac432474c0e620661aa2503e0f93517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleFirebaseHostingVersionConfigRewritesRun]:
        return typing.cast(typing.Optional[GoogleFirebaseHostingVersionConfigRewritesRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleFirebaseHostingVersionConfigRewritesRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d766929180f51720515bcc1fc965efcbf460f44a54667bd8bf5374ab6ce4047d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleFirebaseHostingVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#create GoogleFirebaseHostingVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#delete GoogleFirebaseHostingVersion#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443a7a17c8b875888fdd6967d5aaed564db9d383ed7cd563c45cffd1f4247a07)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#create GoogleFirebaseHostingVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_firebase_hosting_version#delete GoogleFirebaseHostingVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleFirebaseHostingVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleFirebaseHostingVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleFirebaseHostingVersion.GoogleFirebaseHostingVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41563613ce25851e142bd3be5952e3466acc1dd0fd7c69cd0de47611d5f05a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03af37a59c6229c321c3d5ac5b0740179967971e7229812c37a24c6c97008606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d39101bbc27300aa3947f008257f560fc1de4e79cdf799889caf63ed32c2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514d2f231bd31dd0eb9d4651197d22a3b62eb6612fa8a08b17f8db696558aea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleFirebaseHostingVersion",
    "GoogleFirebaseHostingVersionConfig",
    "GoogleFirebaseHostingVersionConfigA",
    "GoogleFirebaseHostingVersionConfigAOutputReference",
    "GoogleFirebaseHostingVersionConfigHeaders",
    "GoogleFirebaseHostingVersionConfigHeadersList",
    "GoogleFirebaseHostingVersionConfigHeadersOutputReference",
    "GoogleFirebaseHostingVersionConfigRedirects",
    "GoogleFirebaseHostingVersionConfigRedirectsList",
    "GoogleFirebaseHostingVersionConfigRedirectsOutputReference",
    "GoogleFirebaseHostingVersionConfigRewrites",
    "GoogleFirebaseHostingVersionConfigRewritesList",
    "GoogleFirebaseHostingVersionConfigRewritesOutputReference",
    "GoogleFirebaseHostingVersionConfigRewritesRun",
    "GoogleFirebaseHostingVersionConfigRewritesRunOutputReference",
    "GoogleFirebaseHostingVersionTimeouts",
    "GoogleFirebaseHostingVersionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9d13d9d720f802fbba133ba4b98b0dd20d336680aca16315ee33eab3b84d3345(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    site_id: builtins.str,
    config: typing.Optional[typing.Union[GoogleFirebaseHostingVersionConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleFirebaseHostingVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2447cb9130b43623dc121aa02c0397a8bcf130900aba4557f04723bc24e34734(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3987da7e4bb845f6312a2b0584e859aa2cc0811a74cc0088f7c056c0ea2f16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdfd9bda572e5c08580a2ddb707ae14eb18b607552b5db1f5da49f5cf404e72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de479cda3b1af04db331f0d99f16b5cf63d32e8bde78ba137893601f66e5948(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    site_id: builtins.str,
    config: typing.Optional[typing.Union[GoogleFirebaseHostingVersionConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleFirebaseHostingVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3855947fecf52c08d151c14c9bb8bc28891eb0e7afa98a8de09483a66a672b16(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFirebaseHostingVersionConfigHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redirects: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFirebaseHostingVersionConfigRedirects, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rewrites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFirebaseHostingVersionConfigRewrites, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835aa58ef1f1b8e3901301856f4ad668eecd829ad0c2e308fa8437ae1f688808(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f480a5382dc0c6cb49a6130d0a52d19a38ccfdda7d02a1f7ac1fb99777dbaafb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFirebaseHostingVersionConfigHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc724ea59ea32784b4c39697cb8c67454a7ab3f3246462274e879914f312290(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFirebaseHostingVersionConfigRedirects, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d4087654e470be21350668ec9720203dfb911c2cccc5ef322ccc942cdd45aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleFirebaseHostingVersionConfigRewrites, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83970e58150d5508bb812168f2a623bf8b87645a895d7ca7d1690aff4570f38(
    value: typing.Optional[GoogleFirebaseHostingVersionConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cf0f6795f76bda90686aff48ada944f8502cf1f6f7b48d92e6f5f03ff9b7fd(
    *,
    headers: typing.Mapping[builtins.str, builtins.str],
    glob: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9222f68e474d01b07be2c2a691ffb118087ee09db9cefa3022f2dbad4ccac80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2efa1fe40c86760772d2b5536bb0a41fe5457c66ff66a4ecc11caea0a88e073(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d9d876fe08abef4a561692f9f898f6fc960cf7d1dc214fc8f1152c0a52e29a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388bbeb2532a1c830f521eb153bf3f8e7823de8d6c6d0cd25c5289f4eeec2c52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a8df77c46b3fe56d911688b233fa7928da976cd4dd981ec343ac7655ec7d44(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bf9062d2d8439df993cc3a7b4abc315a7068ce43a769c5fa912819b0fd3f80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a586031d107dd66f1235e26e3b2a7c3121b98f9910c73b15dbbe602f1dfffe9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa83508340eecff953c3586352a3ca8792b29d4c9095592c30c96a3526093f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5278d010d6d60659f1f1a25d9210b9ef4d74f82a23f0eff6bb9ca7c6b9b138bf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6d70593ca474bb8029da93f804ba40acc15029889bb67c76db2d62f0566c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43f7bd016315dcf7d2c57142d4435ab5b4906f010a6cbf2da6b3a20f32fcccd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd78c497bece651d7033cd6241a6f248165adea8771d4035df0589886120feef(
    *,
    location: builtins.str,
    status_code: jsii.Number,
    glob: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a3ad54bdb210bd3135594e1466fba317977be8bc41b60a9ea616ecccfd3a99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36181271616e602230cecc606a3b0c8e18da89c982df45fd7b1d2ea32450b1af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe45393f69737ec4bdf99597e1c0b4681dd4aaa4bf1be0781850bf9b7af369e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21fc07a4796404ff69691b9f857441d4e7afd0b941c8e570c5097afab4d36b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a5de1b4cb99a694a4c4723d26010c5ae32435f3bbc824c9280f73436876af5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca34e2919d617165f55101fd8d8fea204489a08866a86402640ef9b0ad363f69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRedirects]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d09db5f53621e67b4abb1dfe88cd699c5f962ae8c996c115cfaa9a1c3326485(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aab39f5d7f2bf065c198e4b6ae145b24d43fab8a38fd486eb830bad4dc33a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c9162839e786b3bc74d4101f63290e1af1ee682d2830cf3cf929c7c774f9c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3560ca72495dd3a8a687972d4b1e613c1b029e76d4af3d219d26ef2ec87ad683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29bd1362361345a5e154e22527fa8137f98807cbe2a53ab67dd526ee8083b2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fde02e4b46c5525818ab9586d0bad2c96d284ee14fef9f18e08f8d4cb5d59ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRedirects]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e43834f56a19f05c9297fdcbf4cc60665462e409f3982eb8f524206d5ed0df(
    *,
    function: typing.Optional[builtins.str] = None,
    glob: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
    run: typing.Optional[typing.Union[GoogleFirebaseHostingVersionConfigRewritesRun, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8493d9447a7f884b3e213fffe2509266448aecc8a15b84baa455c4b8f12ce7cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ee9e39607c28f4d8be74a9c6de821276eed3e3fe3460ea6d186ced4ea4f161(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde06913c44f5adcca2c09b378d97c4b8af81b57fd133f69ee268b0a0c539d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de295f2dd7c0a5e4337a0cf5dc0c72e9f009ec18a9933fe6923d02d21284b20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc1e2d091ae6ef01f82da1e4b6d7792b09b4d3e004091ab2e8c9c448b0bd38c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f04a13b1b860bc82971bd0fa8658866b878cd4155758ee8fee34183d587f6a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleFirebaseHostingVersionConfigRewrites]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05be7cacaa2e7535880e771c9e2158f0f2ef2027bc131118bc54e1c16e340e9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c087df3c34c022e918ac62e78a1c2be546a6c67fb99961b6cba74d5b0d0fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5b14cbdf82526a168dede4f06750287fdd3364c1ed55bc3547e184db981036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140ec7f6884323a852bf32c7cf1508ba41fd6406668a12212f690c9723295a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6679247ff6b0aedba7391a4524916841ce99f528a9e69197028c8c46ba7336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ae286f79e3e919e09303a4027e1f6dfaddccac5f81601cbae6c6708c5b7931(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionConfigRewrites]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9b08fb1bd013042973d640f231ea57fe1e5bbfbd4e408724904f0297595738(
    *,
    service_id: builtins.str,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ceb7aef650d02695c6281be19b4af219f2794adf6dc660def5ff901ae82178(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b379e763c33420e94a9e13014c7e3ecc1bd48eaa1ea355e21f68d0ca7cb4ff9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79299924903312f441954c407d04f64e5ac432474c0e620661aa2503e0f93517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d766929180f51720515bcc1fc965efcbf460f44a54667bd8bf5374ab6ce4047d(
    value: typing.Optional[GoogleFirebaseHostingVersionConfigRewritesRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443a7a17c8b875888fdd6967d5aaed564db9d383ed7cd563c45cffd1f4247a07(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41563613ce25851e142bd3be5952e3466acc1dd0fd7c69cd0de47611d5f05a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03af37a59c6229c321c3d5ac5b0740179967971e7229812c37a24c6c97008606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d39101bbc27300aa3947f008257f560fc1de4e79cdf799889caf63ed32c2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514d2f231bd31dd0eb9d4651197d22a3b62eb6612fa8a08b17f8db696558aea3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleFirebaseHostingVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
