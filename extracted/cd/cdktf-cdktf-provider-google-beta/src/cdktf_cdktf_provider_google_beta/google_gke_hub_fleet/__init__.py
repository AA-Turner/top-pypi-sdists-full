r'''
# `google_gke_hub_fleet`

Refer to the Terraform Registry for docs: [`google_gke_hub_fleet`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet).
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


class GoogleGkeHubFleet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet google_gke_hub_fleet}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_cluster_config: typing.Optional[typing.Union["GoogleGkeHubFleetDefaultClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFleetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet google_gke_hub_fleet} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_cluster_config: default_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#default_cluster_config GoogleGkeHubFleet#default_cluster_config}
        :param display_name: A user-assigned display name of the Fleet. When present, it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, single-quote, double-quote, space, and exclamation point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#display_name GoogleGkeHubFleet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#id GoogleGkeHubFleet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#project GoogleGkeHubFleet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#timeouts GoogleGkeHubFleet#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8a07833d3f8e531daf03b304546b87a1e7628d30386ed55b01f752ab4b1f09)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeHubFleetConfig(
            default_cluster_config=default_cluster_config,
            display_name=display_name,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleGkeHubFleet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeHubFleet to import.
        :param import_from_id: The id of the existing GoogleGkeHubFleet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeHubFleet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72c485dbbbced467aacc8f89cc4e27c732e69fbdd6157f9d07aa09f6518bef1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultClusterConfig")
    def put_default_cluster_config(
        self,
        *,
        binary_authorization_config: typing.Optional[typing.Union["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param binary_authorization_config: binary_authorization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#binary_authorization_config GoogleGkeHubFleet#binary_authorization_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#security_posture_config GoogleGkeHubFleet#security_posture_config}
        '''
        value = GoogleGkeHubFleetDefaultClusterConfig(
            binary_authorization_config=binary_authorization_config,
            security_posture_config=security_posture_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultClusterConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#create GoogleGkeHubFleet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#delete GoogleGkeHubFleet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#update GoogleGkeHubFleet#update}.
        '''
        value = GoogleGkeHubFleetTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDefaultClusterConfig")
    def reset_default_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultClusterConfig", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="defaultClusterConfig")
    def default_cluster_config(
        self,
    ) -> "GoogleGkeHubFleetDefaultClusterConfigOutputReference":
        return typing.cast("GoogleGkeHubFleetDefaultClusterConfigOutputReference", jsii.get(self, "defaultClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GoogleGkeHubFleetStateList":
        return typing.cast("GoogleGkeHubFleetStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeHubFleetTimeoutsOutputReference":
        return typing.cast("GoogleGkeHubFleetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="defaultClusterConfigInput")
    def default_cluster_config_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFleetDefaultClusterConfig"]:
        return typing.cast(typing.Optional["GoogleGkeHubFleetDefaultClusterConfig"], jsii.get(self, "defaultClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFleetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFleetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf2b385e180e9d613142f3164b49a0ccd518f17dc2e2ce3696c7ac62f0d4baa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08429080368c671d421320e5ffcbec3d24a44a609cc99a328291c736769a2f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae3f4397922f9624c5fe8e71d68eb09c4994e2ad14d48dffa26dffdc90db675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_cluster_config": "defaultClusterConfig",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleGkeHubFleetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_cluster_config: typing.Optional[typing.Union["GoogleGkeHubFleetDefaultClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFleetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_cluster_config: default_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#default_cluster_config GoogleGkeHubFleet#default_cluster_config}
        :param display_name: A user-assigned display name of the Fleet. When present, it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, single-quote, double-quote, space, and exclamation point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#display_name GoogleGkeHubFleet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#id GoogleGkeHubFleet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#project GoogleGkeHubFleet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#timeouts GoogleGkeHubFleet#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_cluster_config, dict):
            default_cluster_config = GoogleGkeHubFleetDefaultClusterConfig(**default_cluster_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeHubFleetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d3b22db889bbb4bb14a5b5e4ab241bbe637f04712415b16875ed8ba5ac54a8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_cluster_config", value=default_cluster_config, expected_type=type_hints["default_cluster_config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if default_cluster_config is not None:
            self._values["default_cluster_config"] = default_cluster_config
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def default_cluster_config(
        self,
    ) -> typing.Optional["GoogleGkeHubFleetDefaultClusterConfig"]:
        '''default_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#default_cluster_config GoogleGkeHubFleet#default_cluster_config}
        '''
        result = self._values.get("default_cluster_config")
        return typing.cast(typing.Optional["GoogleGkeHubFleetDefaultClusterConfig"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-assigned display name of the Fleet.

        When present, it must be between 4 to 30 characters.
        Allowed characters are: lowercase and uppercase letters, numbers, hyphen, single-quote, double-quote, space, and exclamation point.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#display_name GoogleGkeHubFleet#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#id GoogleGkeHubFleet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#project GoogleGkeHubFleet#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeHubFleetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#timeouts GoogleGkeHubFleet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeHubFleetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "binary_authorization_config": "binaryAuthorizationConfig",
        "security_posture_config": "securityPostureConfig",
    },
)
class GoogleGkeHubFleetDefaultClusterConfig:
    def __init__(
        self,
        *,
        binary_authorization_config: typing.Optional[typing.Union["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param binary_authorization_config: binary_authorization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#binary_authorization_config GoogleGkeHubFleet#binary_authorization_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#security_posture_config GoogleGkeHubFleet#security_posture_config}
        '''
        if isinstance(binary_authorization_config, dict):
            binary_authorization_config = GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig(**binary_authorization_config)
        if isinstance(security_posture_config, dict):
            security_posture_config = GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig(**security_posture_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3665d7bed1f8a8fb7a18ab4649b7569f0d9a6e2cbcca4bc94a576a7b16697b2c)
            check_type(argname="argument binary_authorization_config", value=binary_authorization_config, expected_type=type_hints["binary_authorization_config"])
            check_type(argname="argument security_posture_config", value=security_posture_config, expected_type=type_hints["security_posture_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if binary_authorization_config is not None:
            self._values["binary_authorization_config"] = binary_authorization_config
        if security_posture_config is not None:
            self._values["security_posture_config"] = security_posture_config

    @builtins.property
    def binary_authorization_config(
        self,
    ) -> typing.Optional["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig"]:
        '''binary_authorization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#binary_authorization_config GoogleGkeHubFleet#binary_authorization_config}
        '''
        result = self._values.get("binary_authorization_config")
        return typing.cast(typing.Optional["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig"], result)

    @builtins.property
    def security_posture_config(
        self,
    ) -> typing.Optional["GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig"]:
        '''security_posture_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#security_posture_config GoogleGkeHubFleet#security_posture_config}
        '''
        result = self._values.get("security_posture_config")
        return typing.cast(typing.Optional["GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetDefaultClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_mode": "evaluationMode",
        "policy_bindings": "policyBindings",
    },
)
class GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
        policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. Possible values: ["DISABLED", "POLICY_BINDINGS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#evaluation_mode GoogleGkeHubFleet#evaluation_mode}
        :param policy_bindings: policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#policy_bindings GoogleGkeHubFleet#policy_bindings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186d9643eb1dff696f937eb06784987f4195082a2260a498aa5aacebbb70c6f1)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
            check_type(argname="argument policy_bindings", value=policy_bindings, expected_type=type_hints["policy_bindings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode
        if policy_bindings is not None:
            self._values["policy_bindings"] = policy_bindings

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Mode of operation for binauthz policy evaluation. Possible values: ["DISABLED", "POLICY_BINDINGS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#evaluation_mode GoogleGkeHubFleet#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_bindings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]]:
        '''policy_bindings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#policy_bindings GoogleGkeHubFleet#policy_bindings}
        '''
        result = self._values.get("policy_bindings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6814763a294e8a69d3b950b3a7a484b38713fde5fe06e5cedad65159f5cb2ec9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyBindings")
    def put_policy_bindings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55cdd1aa5a70857261545c1e0b8456303e955174422cad3430e9976a5029cb28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyBindings", [value]))

    @jsii.member(jsii_name="resetEvaluationMode")
    def reset_evaluation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationMode", []))

    @jsii.member(jsii_name="resetPolicyBindings")
    def reset_policy_bindings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyBindings", []))

    @builtins.property
    @jsii.member(jsii_name="policyBindings")
    def policy_bindings(
        self,
    ) -> "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList":
        return typing.cast("GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList", jsii.get(self, "policyBindings"))

    @builtins.property
    @jsii.member(jsii_name="evaluationModeInput")
    def evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyBindingsInput")
    def policy_bindings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]], jsii.get(self, "policyBindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90eda3c59e671cbca42ac5c64893ea8ccfbb0e24a3d4faf6a0b039dc2a15234d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4779cab56d9acac1e32466a23053ef2b3b79b0b902926bd079cad3bc199ffab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The relative resource name of the binauthz platform policy to audit. GKE platform policies have the following format: 'projects/{project_number}/platforms/gke/policies/{policy_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#name GoogleGkeHubFleet#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebe811ee11992d12120933b1b2cbd98bb6a5284f76d72615cc4e05caffe9098)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The relative resource name of the binauthz platform policy to audit. GKE platform policies have the following format: 'projects/{project_number}/platforms/gke/policies/{policy_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#name GoogleGkeHubFleet#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__872d1e31c302235a0ba26a78cc5885354527be92fdfffc83e90916343793d710)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb002db6c4177823cb6868aabc288411a16258ade19b79cd0dec76aeb828520d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f418ccdeb1c7a9d9dcd4813f57bd8b683d071df229d8fc45d7e5bea4d2729a7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07dd0d59d14cd3a5ac07afd3ecfe4bd9254a90fac338e18763b9abe8ce246546)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70eea5ef2209190201fe109ecf9f7628a42023f16c954d0ee8fa8d028cf2ccd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c515ec7684cd3089df295c384ae34d4fc1f0529b0b6d70845188c7ffc2cc93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__294f523fd20a8a72e420599ed828ee00a0fa2a5d1d61d83ada75295caf9b30ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10e15c88eaf6286247bd96b8aed43289c8a00cbee3a749fcf5dfdb60db51974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69997188c4464e0e69eff0db7f7afa438121b5ec26cfb239467565a0f631381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFleetDefaultClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e3e659524430e4c4c5d2912f3393fc0bf86fb78d891338848a7c386ee858cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBinaryAuthorizationConfig")
    def put_binary_authorization_config(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
        policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. Possible values: ["DISABLED", "POLICY_BINDINGS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#evaluation_mode GoogleGkeHubFleet#evaluation_mode}
        :param policy_bindings: policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#policy_bindings GoogleGkeHubFleet#policy_bindings}
        '''
        value = GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig(
            evaluation_mode=evaluation_mode, policy_bindings=policy_bindings
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorizationConfig", [value]))

    @jsii.member(jsii_name="putSecurityPostureConfig")
    def put_security_posture_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        vulnerability_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Sets which mode to use for Security Posture features. Possible values: ["DISABLED", "BASIC", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#mode GoogleGkeHubFleet#mode}
        :param vulnerability_mode: Sets which mode to use for vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_BASIC", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#vulnerability_mode GoogleGkeHubFleet#vulnerability_mode}
        '''
        value = GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig(
            mode=mode, vulnerability_mode=vulnerability_mode
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityPostureConfig", [value]))

    @jsii.member(jsii_name="resetBinaryAuthorizationConfig")
    def reset_binary_authorization_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorizationConfig", []))

    @jsii.member(jsii_name="resetSecurityPostureConfig")
    def reset_security_posture_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPostureConfig", []))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationConfig")
    def binary_authorization_config(
        self,
    ) -> GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference:
        return typing.cast(GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference, jsii.get(self, "binaryAuthorizationConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfig")
    def security_posture_config(
        self,
    ) -> "GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference":
        return typing.cast("GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference", jsii.get(self, "securityPostureConfig"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationConfigInput")
    def binary_authorization_config_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig], jsii.get(self, "binaryAuthorizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfigInput")
    def security_posture_config_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig"]:
        return typing.cast(typing.Optional["GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig"], jsii.get(self, "securityPostureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFleetDefaultClusterConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFleetDefaultClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFleetDefaultClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8996fa6dc81abe8246f7b61012181231125d31dd024658aa8257c22617cd7263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "vulnerability_mode": "vulnerabilityMode"},
)
class GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        vulnerability_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Sets which mode to use for Security Posture features. Possible values: ["DISABLED", "BASIC", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#mode GoogleGkeHubFleet#mode}
        :param vulnerability_mode: Sets which mode to use for vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_BASIC", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#vulnerability_mode GoogleGkeHubFleet#vulnerability_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda6a8d7862a2c280eccfd43155da467cf0775fb5f43595178cdc06e982fdd16)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument vulnerability_mode", value=vulnerability_mode, expected_type=type_hints["vulnerability_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if vulnerability_mode is not None:
            self._values["vulnerability_mode"] = vulnerability_mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Sets which mode to use for Security Posture features. Possible values: ["DISABLED", "BASIC", "ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#mode GoogleGkeHubFleet#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vulnerability_mode(self) -> typing.Optional[builtins.str]:
        '''Sets which mode to use for vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_BASIC", "VULNERABILITY_ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#vulnerability_mode GoogleGkeHubFleet#vulnerability_mode}
        '''
        result = self._values.get("vulnerability_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7592c742cec550a12e24652e3d25d2fa8d38f6714085ed7f47153252509951a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetVulnerabilityMode")
    def reset_vulnerability_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVulnerabilityMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityModeInput")
    def vulnerability_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vulnerabilityModeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af95fb990ab3d0aaa233b1e66d7f6a54abc242dee0673847fd26531983fd22c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityMode")
    def vulnerability_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vulnerabilityMode"))

    @vulnerability_mode.setter
    def vulnerability_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f28ed2f8a470738fe2954d20f2ebffcc0fec97c40b8806dbeb0e3d34917578b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fb3d604ce718509bf4fed06dda092ad6d629aaf17adedb53d330576cbe9f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeHubFleetState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFleetStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb1ea30534e601e1c3bbc144ce653a01f21d8e2234cd0acde7432969547f71e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleGkeHubFleetStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b3441c4a4a2c197c0fba3e447bea49fe00ba7ca86276519cc10c1835e52354)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFleetStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087c8d5567b415c0f66189839be108244ac0cec5f132ab412fa7395fe7a62289)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a57e5ad0fc815e8934d28b2576b8fc81d244b30e56da0a3b7673e6c2af8051d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab7acb2e540c2adb944e373b3380b890aa331820c3d842e1a5145954d1eab5a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFleetStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d75ee8512dd13d594bf5160422331fd1c0a5f03304d63bb7a9bf8a71ab9bbd83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFleetState]:
        return typing.cast(typing.Optional[GoogleGkeHubFleetState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleGkeHubFleetState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8689e21d5fd0c89113d39f73a010053a6e780602bd29a6b1ad6bdedee8768a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeHubFleetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#create GoogleGkeHubFleet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#delete GoogleGkeHubFleet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#update GoogleGkeHubFleet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f316dd53edd19a63db3d3232c0cc26a2761b1d7b2d0a852aad0d8ee9ada8d460)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#create GoogleGkeHubFleet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#delete GoogleGkeHubFleet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_fleet#update GoogleGkeHubFleet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFleetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFleetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFleet.GoogleGkeHubFleetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77fd1f0e01f4d45ad6cae0e01f6ecf6bbeeb451279e9c2c167e55a7eca8133e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca80d52addaaf2f47cc109ece51e9cf4fed4ae22a5e2e4a063d45a770540a934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3994b122965cef1e9536ea29774bf18671e150c26c90e9fe164f243ffed954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19e9f3aa41dca1aa9a7ff53a196046d21dabe98cf971ba3f8b199bcfaf247e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2dd46273d9f5b578caa2e223cf4ef612621e6b5dcaa70db946adc5b3396b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeHubFleet",
    "GoogleGkeHubFleetConfig",
    "GoogleGkeHubFleetDefaultClusterConfig",
    "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig",
    "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference",
    "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings",
    "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList",
    "GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference",
    "GoogleGkeHubFleetDefaultClusterConfigOutputReference",
    "GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig",
    "GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference",
    "GoogleGkeHubFleetState",
    "GoogleGkeHubFleetStateList",
    "GoogleGkeHubFleetStateOutputReference",
    "GoogleGkeHubFleetTimeouts",
    "GoogleGkeHubFleetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__eb8a07833d3f8e531daf03b304546b87a1e7628d30386ed55b01f752ab4b1f09(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_cluster_config: typing.Optional[typing.Union[GoogleGkeHubFleetDefaultClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFleetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d72c485dbbbced467aacc8f89cc4e27c732e69fbdd6157f9d07aa09f6518bef1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf2b385e180e9d613142f3164b49a0ccd518f17dc2e2ce3696c7ac62f0d4baa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08429080368c671d421320e5ffcbec3d24a44a609cc99a328291c736769a2f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae3f4397922f9624c5fe8e71d68eb09c4994e2ad14d48dffa26dffdc90db675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d3b22db889bbb4bb14a5b5e4ab241bbe637f04712415b16875ed8ba5ac54a8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_cluster_config: typing.Optional[typing.Union[GoogleGkeHubFleetDefaultClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFleetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3665d7bed1f8a8fb7a18ab4649b7569f0d9a6e2cbcca4bc94a576a7b16697b2c(
    *,
    binary_authorization_config: typing.Optional[typing.Union[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_posture_config: typing.Optional[typing.Union[GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186d9643eb1dff696f937eb06784987f4195082a2260a498aa5aacebbb70c6f1(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
    policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6814763a294e8a69d3b950b3a7a484b38713fde5fe06e5cedad65159f5cb2ec9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cdd1aa5a70857261545c1e0b8456303e955174422cad3430e9976a5029cb28(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90eda3c59e671cbca42ac5c64893ea8ccfbb0e24a3d4faf6a0b039dc2a15234d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4779cab56d9acac1e32466a23053ef2b3b79b0b902926bd079cad3bc199ffab(
    value: typing.Optional[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebe811ee11992d12120933b1b2cbd98bb6a5284f76d72615cc4e05caffe9098(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872d1e31c302235a0ba26a78cc5885354527be92fdfffc83e90916343793d710(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb002db6c4177823cb6868aabc288411a16258ade19b79cd0dec76aeb828520d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f418ccdeb1c7a9d9dcd4813f57bd8b683d071df229d8fc45d7e5bea4d2729a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07dd0d59d14cd3a5ac07afd3ecfe4bd9254a90fac338e18763b9abe8ce246546(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70eea5ef2209190201fe109ecf9f7628a42023f16c954d0ee8fa8d028cf2ccd7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c515ec7684cd3089df295c384ae34d4fc1f0529b0b6d70845188c7ffc2cc93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294f523fd20a8a72e420599ed828ee00a0fa2a5d1d61d83ada75295caf9b30ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10e15c88eaf6286247bd96b8aed43289c8a00cbee3a749fcf5dfdb60db51974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69997188c4464e0e69eff0db7f7afa438121b5ec26cfb239467565a0f631381(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e3e659524430e4c4c5d2912f3393fc0bf86fb78d891338848a7c386ee858cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8996fa6dc81abe8246f7b61012181231125d31dd024658aa8257c22617cd7263(
    value: typing.Optional[GoogleGkeHubFleetDefaultClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda6a8d7862a2c280eccfd43155da467cf0775fb5f43595178cdc06e982fdd16(
    *,
    mode: typing.Optional[builtins.str] = None,
    vulnerability_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7592c742cec550a12e24652e3d25d2fa8d38f6714085ed7f47153252509951a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af95fb990ab3d0aaa233b1e66d7f6a54abc242dee0673847fd26531983fd22c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f28ed2f8a470738fe2954d20f2ebffcc0fec97c40b8806dbeb0e3d34917578b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fb3d604ce718509bf4fed06dda092ad6d629aaf17adedb53d330576cbe9f16(
    value: typing.Optional[GoogleGkeHubFleetDefaultClusterConfigSecurityPostureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1ea30534e601e1c3bbc144ce653a01f21d8e2234cd0acde7432969547f71e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b3441c4a4a2c197c0fba3e447bea49fe00ba7ca86276519cc10c1835e52354(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087c8d5567b415c0f66189839be108244ac0cec5f132ab412fa7395fe7a62289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a57e5ad0fc815e8934d28b2576b8fc81d244b30e56da0a3b7673e6c2af8051d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7acb2e540c2adb944e373b3380b890aa331820c3d842e1a5145954d1eab5a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75ee8512dd13d594bf5160422331fd1c0a5f03304d63bb7a9bf8a71ab9bbd83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8689e21d5fd0c89113d39f73a010053a6e780602bd29a6b1ad6bdedee8768a30(
    value: typing.Optional[GoogleGkeHubFleetState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f316dd53edd19a63db3d3232c0cc26a2761b1d7b2d0a852aad0d8ee9ada8d460(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fd1f0e01f4d45ad6cae0e01f6ecf6bbeeb451279e9c2c167e55a7eca8133e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca80d52addaaf2f47cc109ece51e9cf4fed4ae22a5e2e4a063d45a770540a934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3994b122965cef1e9536ea29774bf18671e150c26c90e9fe164f243ffed954(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19e9f3aa41dca1aa9a7ff53a196046d21dabe98cf971ba3f8b199bcfaf247e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2dd46273d9f5b578caa2e223cf4ef612621e6b5dcaa70db946adc5b3396b69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFleetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
