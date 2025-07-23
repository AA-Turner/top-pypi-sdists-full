r'''
# `google_gke_hub_fleet`

Refer to the Terraform Registry for docs: [`google_gke_hub_fleet`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet).
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


class GkeHubFleet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet google_gke_hub_fleet}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_cluster_config: typing.Optional[typing.Union["GkeHubFleetDefaultClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFleetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet google_gke_hub_fleet} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_cluster_config: default_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#default_cluster_config GkeHubFleet#default_cluster_config}
        :param display_name: A user-assigned display name of the Fleet. When present, it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, single-quote, double-quote, space, and exclamation point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#display_name GkeHubFleet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#id GkeHubFleet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#project GkeHubFleet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#timeouts GkeHubFleet#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5233c0bbb879935715253b49f99050ed30d60847898ced7fef0c7c21af9a5366)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeHubFleetConfig(
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
        '''Generates CDKTF code for importing a GkeHubFleet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeHubFleet to import.
        :param import_from_id: The id of the existing GkeHubFleet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeHubFleet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2af38a03d406ed31dcf4a6895546257caced5fa0723e1348c21b4969a47d9c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultClusterConfig")
    def put_default_cluster_config(
        self,
        *,
        binary_authorization_config: typing.Optional[typing.Union["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["GkeHubFleetDefaultClusterConfigSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param binary_authorization_config: binary_authorization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#binary_authorization_config GkeHubFleet#binary_authorization_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#security_posture_config GkeHubFleet#security_posture_config}
        '''
        value = GkeHubFleetDefaultClusterConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#create GkeHubFleet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#delete GkeHubFleet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#update GkeHubFleet#update}.
        '''
        value = GkeHubFleetTimeouts(create=create, delete=delete, update=update)

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
    ) -> "GkeHubFleetDefaultClusterConfigOutputReference":
        return typing.cast("GkeHubFleetDefaultClusterConfigOutputReference", jsii.get(self, "defaultClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GkeHubFleetStateList":
        return typing.cast("GkeHubFleetStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeHubFleetTimeoutsOutputReference":
        return typing.cast("GkeHubFleetTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GkeHubFleetDefaultClusterConfig"]:
        return typing.cast(typing.Optional["GkeHubFleetDefaultClusterConfig"], jsii.get(self, "defaultClusterConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFleetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFleetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa51dc2df1665bc5f7fa0ea17c8d6c2bad056bad8117a6ebfadfed7d8b1b307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d1515b0b35adacaa77ca0f15678208f442d88bde49c4cc2bbaec3a4d842681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6153792e2f8c77ec5efb2cf4235d932d69793d8d6206c004079b4250a8e53cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetConfig",
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
class GkeHubFleetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_cluster_config: typing.Optional[typing.Union["GkeHubFleetDefaultClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFleetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_cluster_config: default_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#default_cluster_config GkeHubFleet#default_cluster_config}
        :param display_name: A user-assigned display name of the Fleet. When present, it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, single-quote, double-quote, space, and exclamation point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#display_name GkeHubFleet#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#id GkeHubFleet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#project GkeHubFleet#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#timeouts GkeHubFleet#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_cluster_config, dict):
            default_cluster_config = GkeHubFleetDefaultClusterConfig(**default_cluster_config)
        if isinstance(timeouts, dict):
            timeouts = GkeHubFleetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c21e6e3427a1c36e4293ac959a25a824d8f113fd730cd59ba8b5877d616b24)
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
    ) -> typing.Optional["GkeHubFleetDefaultClusterConfig"]:
        '''default_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#default_cluster_config GkeHubFleet#default_cluster_config}
        '''
        result = self._values.get("default_cluster_config")
        return typing.cast(typing.Optional["GkeHubFleetDefaultClusterConfig"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-assigned display name of the Fleet.

        When present, it must be between 4 to 30 characters.
        Allowed characters are: lowercase and uppercase letters, numbers, hyphen, single-quote, double-quote, space, and exclamation point.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#display_name GkeHubFleet#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#id GkeHubFleet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#project GkeHubFleet#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeHubFleetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#timeouts GkeHubFleet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeHubFleetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "binary_authorization_config": "binaryAuthorizationConfig",
        "security_posture_config": "securityPostureConfig",
    },
)
class GkeHubFleetDefaultClusterConfig:
    def __init__(
        self,
        *,
        binary_authorization_config: typing.Optional[typing.Union["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_posture_config: typing.Optional[typing.Union["GkeHubFleetDefaultClusterConfigSecurityPostureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param binary_authorization_config: binary_authorization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#binary_authorization_config GkeHubFleet#binary_authorization_config}
        :param security_posture_config: security_posture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#security_posture_config GkeHubFleet#security_posture_config}
        '''
        if isinstance(binary_authorization_config, dict):
            binary_authorization_config = GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig(**binary_authorization_config)
        if isinstance(security_posture_config, dict):
            security_posture_config = GkeHubFleetDefaultClusterConfigSecurityPostureConfig(**security_posture_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b650f4d5ef8a4c38573faf7832ab7aab0d63995b37e5cf1db997984dee69fa)
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
    ) -> typing.Optional["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig"]:
        '''binary_authorization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#binary_authorization_config GkeHubFleet#binary_authorization_config}
        '''
        result = self._values.get("binary_authorization_config")
        return typing.cast(typing.Optional["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig"], result)

    @builtins.property
    def security_posture_config(
        self,
    ) -> typing.Optional["GkeHubFleetDefaultClusterConfigSecurityPostureConfig"]:
        '''security_posture_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#security_posture_config GkeHubFleet#security_posture_config}
        '''
        result = self._values.get("security_posture_config")
        return typing.cast(typing.Optional["GkeHubFleetDefaultClusterConfigSecurityPostureConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetDefaultClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_mode": "evaluationMode",
        "policy_bindings": "policyBindings",
    },
)
class GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
        policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. Possible values: ["DISABLED", "POLICY_BINDINGS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#evaluation_mode GkeHubFleet#evaluation_mode}
        :param policy_bindings: policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#policy_bindings GkeHubFleet#policy_bindings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1109c1139bcb2d9f0564441f02f02c7b309b83ae0c336f75d951e78d208e62)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#evaluation_mode GkeHubFleet#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_bindings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]]:
        '''policy_bindings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#policy_bindings GkeHubFleet#policy_bindings}
        '''
        result = self._values.get("policy_bindings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__feb894d4258aa25363ca760cc2d938a1733df1bd505ad5002beea9a5ef5be328)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyBindings")
    def put_policy_bindings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f821b383ab9ed8468585df755d09c4f01da5b400a6e67e40aee107ff11e5afff)
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
    ) -> "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList":
        return typing.cast("GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList", jsii.get(self, "policyBindings"))

    @builtins.property
    @jsii.member(jsii_name="evaluationModeInput")
    def evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyBindingsInput")
    def policy_bindings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings"]]], jsii.get(self, "policyBindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7841682953d4923f6de89077931944966b47178681618c0ecc1cda7b176e25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig]:
        return typing.cast(typing.Optional[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa02fc33096fea90cc835681ccf37cf5f6359270a5b294c4856378b52cd62b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: The relative resource name of the binauthz platform policy to audit. GKE platform policies have the following format: 'projects/{project_number}/platforms/gke/policies/{policy_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#name GkeHubFleet#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434dbdf1e6e1bd4c95d2082f63078527624ba135388dfb36477ea119028692c2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The relative resource name of the binauthz platform policy to audit. GKE platform policies have the following format: 'projects/{project_number}/platforms/gke/policies/{policy_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#name GkeHubFleet#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1ef1c4d884a6aaaead5b2b3cfc4491bfc9442d008a9df8811d56b9cd21ad53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4a2a3ed01d8d3e63056da04cc7646f61eada1ad49f0d1c7eba5d153e11181d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18d75771ffe4903142ea5fad641c8082726e30a61fe708034fcdd39174773f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8626f416c64ff11e8a24a3e58b966f979640fea6c5cc61eea5f9829b93e7ae1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac256cf8d46ba59b2a995a28f797c41b22bf1055345611cbdaa7ebc7e48a2128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90707bb9cac9e3ea73073cb0de45ae731b682d858d4a8f5c06abcabf5e4d4f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4fe4be32054e0b81e7506e2da97d5b0bb9252d583120865863437ffd61d7af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8debb1b1bcbc47e0a5679441e9a0cecf94afdcc0a1aa8224f68023b34ee77782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4254849a82035a5b17a208dffc649639878eaf444682be3ade6186bd3f942a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFleetDefaultClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8a517b45cbdc28cd57156995cf7be7ea73714da64850ebd492278a46bda3581)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBinaryAuthorizationConfig")
    def put_binary_authorization_config(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
        policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for binauthz policy evaluation. Possible values: ["DISABLED", "POLICY_BINDINGS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#evaluation_mode GkeHubFleet#evaluation_mode}
        :param policy_bindings: policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#policy_bindings GkeHubFleet#policy_bindings}
        '''
        value = GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig(
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
        :param mode: Sets which mode to use for Security Posture features. Possible values: ["DISABLED", "BASIC", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#mode GkeHubFleet#mode}
        :param vulnerability_mode: Sets which mode to use for vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_BASIC", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#vulnerability_mode GkeHubFleet#vulnerability_mode}
        '''
        value = GkeHubFleetDefaultClusterConfigSecurityPostureConfig(
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
    ) -> GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference:
        return typing.cast(GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference, jsii.get(self, "binaryAuthorizationConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfig")
    def security_posture_config(
        self,
    ) -> "GkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference":
        return typing.cast("GkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference", jsii.get(self, "securityPostureConfig"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationConfigInput")
    def binary_authorization_config_input(
        self,
    ) -> typing.Optional[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig]:
        return typing.cast(typing.Optional[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig], jsii.get(self, "binaryAuthorizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPostureConfigInput")
    def security_posture_config_input(
        self,
    ) -> typing.Optional["GkeHubFleetDefaultClusterConfigSecurityPostureConfig"]:
        return typing.cast(typing.Optional["GkeHubFleetDefaultClusterConfigSecurityPostureConfig"], jsii.get(self, "securityPostureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFleetDefaultClusterConfig]:
        return typing.cast(typing.Optional[GkeHubFleetDefaultClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFleetDefaultClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b0176242a6ad48dcfd3e8a7ba5f936757b8ed141197eff762d6d53f9f2a939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigSecurityPostureConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "vulnerability_mode": "vulnerabilityMode"},
)
class GkeHubFleetDefaultClusterConfigSecurityPostureConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        vulnerability_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Sets which mode to use for Security Posture features. Possible values: ["DISABLED", "BASIC", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#mode GkeHubFleet#mode}
        :param vulnerability_mode: Sets which mode to use for vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_BASIC", "VULNERABILITY_ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#vulnerability_mode GkeHubFleet#vulnerability_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c906ec4c1f2e01043415003e8dc00eb9219e24b568c1d4c844663bf7f986b7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#mode GkeHubFleet#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vulnerability_mode(self) -> typing.Optional[builtins.str]:
        '''Sets which mode to use for vulnerability scanning. Possible values: ["VULNERABILITY_DISABLED", "VULNERABILITY_BASIC", "VULNERABILITY_ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#vulnerability_mode GkeHubFleet#vulnerability_mode}
        '''
        result = self._values.get("vulnerability_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetDefaultClusterConfigSecurityPostureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d62f22070ddb39b284fbb46f96f8a6b85827c2a975d206fe9b980c4fcabde1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a25a821179dc30d39dc9ae43dafc64e0699b205f3114890e77b459bc419fa34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityMode")
    def vulnerability_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vulnerabilityMode"))

    @vulnerability_mode.setter
    def vulnerability_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a895f9ee7b7f31d7889da1b590d772e323291b1c0ad669d98b08af499f3ba11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFleetDefaultClusterConfigSecurityPostureConfig]:
        return typing.cast(typing.Optional[GkeHubFleetDefaultClusterConfigSecurityPostureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFleetDefaultClusterConfigSecurityPostureConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0cec1d267d61764c9ba220035536418e11891772e428fa6b095af49d51059c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFleetState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFleetStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc911e1e7c05e3173f74bd08dd09c87fd85ec22417bf38ff1d98b3901f44335f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFleetStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7218337296f016aa5be6362f5374a90e1d4e9003b7517f07e2ba6b309a1e1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFleetStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1ed97e24326663d61ec93817d6fd9f333eae858a1105f1652de147cc0c14fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab7d597c4b172bfd1857a1b83492245dbc03a17d228be08d44fadaef2079b893)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24436bb8114bee773f541b077dd929f895f9132e6e277037a1f9419b930b0db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeHubFleetStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2bb9e70d12143d44c10cbce28be6da23b356b9e9cc14edba452c09ad7dca1f1)
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
    def internal_value(self) -> typing.Optional[GkeHubFleetState]:
        return typing.cast(typing.Optional[GkeHubFleetState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFleetState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437a250b2df3c84568930bc9154fd0032d49127f6eb2bfe8e0a11a156d1317ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeHubFleetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#create GkeHubFleet#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#delete GkeHubFleet#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#update GkeHubFleet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76228feeaf3e18b65cb6c5e698e050b0ab7aec4a0555a63adb5332f9d989901)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#create GkeHubFleet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#delete GkeHubFleet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_fleet#update GkeHubFleet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFleetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFleetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFleet.GkeHubFleetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c223aa76bd760bae2ee1c694bb516fd843d0cc71b58efde83e36b75d80fc8b14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae088bf3099e055d042653d33ac6356745806c7ffa5d375c46e60e6891d325a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94472d682630e156debb84abe31722f77e818eec314fcfa47eaf7e2579b86b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0250101ad851ae70c416b9f4607697824de165caf8f649dbd090a5f7fe8920b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc9cec36f3768a870353977630f30e793256fef1d417d74465d606dd3527e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeHubFleet",
    "GkeHubFleetConfig",
    "GkeHubFleetDefaultClusterConfig",
    "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig",
    "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigOutputReference",
    "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings",
    "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsList",
    "GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindingsOutputReference",
    "GkeHubFleetDefaultClusterConfigOutputReference",
    "GkeHubFleetDefaultClusterConfigSecurityPostureConfig",
    "GkeHubFleetDefaultClusterConfigSecurityPostureConfigOutputReference",
    "GkeHubFleetState",
    "GkeHubFleetStateList",
    "GkeHubFleetStateOutputReference",
    "GkeHubFleetTimeouts",
    "GkeHubFleetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5233c0bbb879935715253b49f99050ed30d60847898ced7fef0c7c21af9a5366(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_cluster_config: typing.Optional[typing.Union[GkeHubFleetDefaultClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFleetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b2af38a03d406ed31dcf4a6895546257caced5fa0723e1348c21b4969a47d9c1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa51dc2df1665bc5f7fa0ea17c8d6c2bad056bad8117a6ebfadfed7d8b1b307(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d1515b0b35adacaa77ca0f15678208f442d88bde49c4cc2bbaec3a4d842681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6153792e2f8c77ec5efb2cf4235d932d69793d8d6206c004079b4250a8e53cfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c21e6e3427a1c36e4293ac959a25a824d8f113fd730cd59ba8b5877d616b24(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_cluster_config: typing.Optional[typing.Union[GkeHubFleetDefaultClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFleetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b650f4d5ef8a4c38573faf7832ab7aab0d63995b37e5cf1db997984dee69fa(
    *,
    binary_authorization_config: typing.Optional[typing.Union[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_posture_config: typing.Optional[typing.Union[GkeHubFleetDefaultClusterConfigSecurityPostureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1109c1139bcb2d9f0564441f02f02c7b309b83ae0c336f75d951e78d208e62(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
    policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb894d4258aa25363ca760cc2d938a1733df1bd505ad5002beea9a5ef5be328(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f821b383ab9ed8468585df755d09c4f01da5b400a6e67e40aee107ff11e5afff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7841682953d4923f6de89077931944966b47178681618c0ecc1cda7b176e25f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa02fc33096fea90cc835681ccf37cf5f6359270a5b294c4856378b52cd62b7(
    value: typing.Optional[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434dbdf1e6e1bd4c95d2082f63078527624ba135388dfb36477ea119028692c2(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1ef1c4d884a6aaaead5b2b3cfc4491bfc9442d008a9df8811d56b9cd21ad53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4a2a3ed01d8d3e63056da04cc7646f61eada1ad49f0d1c7eba5d153e11181d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18d75771ffe4903142ea5fad641c8082726e30a61fe708034fcdd39174773f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8626f416c64ff11e8a24a3e58b966f979640fea6c5cc61eea5f9829b93e7ae1f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac256cf8d46ba59b2a995a28f797c41b22bf1055345611cbdaa7ebc7e48a2128(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90707bb9cac9e3ea73073cb0de45ae731b682d858d4a8f5c06abcabf5e4d4f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4fe4be32054e0b81e7506e2da97d5b0bb9252d583120865863437ffd61d7af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8debb1b1bcbc47e0a5679441e9a0cecf94afdcc0a1aa8224f68023b34ee77782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4254849a82035a5b17a208dffc649639878eaf444682be3ade6186bd3f942a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetDefaultClusterConfigBinaryAuthorizationConfigPolicyBindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a517b45cbdc28cd57156995cf7be7ea73714da64850ebd492278a46bda3581(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b0176242a6ad48dcfd3e8a7ba5f936757b8ed141197eff762d6d53f9f2a939(
    value: typing.Optional[GkeHubFleetDefaultClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c906ec4c1f2e01043415003e8dc00eb9219e24b568c1d4c844663bf7f986b7(
    *,
    mode: typing.Optional[builtins.str] = None,
    vulnerability_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d62f22070ddb39b284fbb46f96f8a6b85827c2a975d206fe9b980c4fcabde1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a25a821179dc30d39dc9ae43dafc64e0699b205f3114890e77b459bc419fa34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a895f9ee7b7f31d7889da1b590d772e323291b1c0ad669d98b08af499f3ba11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0cec1d267d61764c9ba220035536418e11891772e428fa6b095af49d51059c(
    value: typing.Optional[GkeHubFleetDefaultClusterConfigSecurityPostureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc911e1e7c05e3173f74bd08dd09c87fd85ec22417bf38ff1d98b3901f44335f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7218337296f016aa5be6362f5374a90e1d4e9003b7517f07e2ba6b309a1e1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1ed97e24326663d61ec93817d6fd9f333eae858a1105f1652de147cc0c14fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7d597c4b172bfd1857a1b83492245dbc03a17d228be08d44fadaef2079b893(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24436bb8114bee773f541b077dd929f895f9132e6e277037a1f9419b930b0db2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bb9e70d12143d44c10cbce28be6da23b356b9e9cc14edba452c09ad7dca1f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437a250b2df3c84568930bc9154fd0032d49127f6eb2bfe8e0a11a156d1317ff(
    value: typing.Optional[GkeHubFleetState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76228feeaf3e18b65cb6c5e698e050b0ab7aec4a0555a63adb5332f9d989901(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c223aa76bd760bae2ee1c694bb516fd843d0cc71b58efde83e36b75d80fc8b14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae088bf3099e055d042653d33ac6356745806c7ffa5d375c46e60e6891d325a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94472d682630e156debb84abe31722f77e818eec314fcfa47eaf7e2579b86b75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0250101ad851ae70c416b9f4607697824de165caf8f649dbd090a5f7fe8920b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc9cec36f3768a870353977630f30e793256fef1d417d74465d606dd3527e49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFleetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
