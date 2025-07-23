r'''
# `google_firebase_app_hosting_traffic`

Refer to the Terraform Registry for docs: [`google_firebase_app_hosting_traffic`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic).
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


class FirebaseAppHostingTraffic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTraffic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic google_firebase_app_hosting_traffic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backend: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rollout_policy: typing.Optional[typing.Union["FirebaseAppHostingTrafficRolloutPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Union["FirebaseAppHostingTrafficTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FirebaseAppHostingTrafficTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic google_firebase_app_hosting_traffic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backend: Id of the backend that this Traffic config applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#backend FirebaseAppHostingTraffic#backend}
        :param location: The location the Backend that this Traffic config applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#location FirebaseAppHostingTraffic#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#id FirebaseAppHostingTraffic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#project FirebaseAppHostingTraffic#project}.
        :param rollout_policy: rollout_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#rollout_policy FirebaseAppHostingTraffic#rollout_policy}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#target FirebaseAppHostingTraffic#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#timeouts FirebaseAppHostingTraffic#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73b4f0ec382521c1bde3544024c6b37f7d6f6f79ac57ac7a7af5a1f37e2b971)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FirebaseAppHostingTrafficConfig(
            backend=backend,
            location=location,
            id=id,
            project=project,
            rollout_policy=rollout_policy,
            target=target,
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
        '''Generates CDKTF code for importing a FirebaseAppHostingTraffic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FirebaseAppHostingTraffic to import.
        :param import_from_id: The id of the existing FirebaseAppHostingTraffic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FirebaseAppHostingTraffic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28f9928a35e44b7046523f7f44a10a3b297baf7ea7ed86f7e15d14b49ae5e40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRolloutPolicy")
    def put_rollout_policy(
        self,
        *,
        codebase_branch: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param codebase_branch: Specifies a branch that triggers a new build to be started with this policy. If not set, no automatic rollouts will happen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#codebase_branch FirebaseAppHostingTraffic#codebase_branch}
        :param disabled: A flag that, if true, prevents rollouts from being created via this RolloutPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#disabled FirebaseAppHostingTraffic#disabled}
        '''
        value = FirebaseAppHostingTrafficRolloutPolicy(
            codebase_branch=codebase_branch, disabled=disabled
        )

        return typing.cast(None, jsii.invoke(self, "putRolloutPolicy", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        splits: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirebaseAppHostingTrafficTargetSplits", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param splits: splits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#splits FirebaseAppHostingTraffic#splits}
        '''
        value = FirebaseAppHostingTrafficTarget(splits=splits)

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#create FirebaseAppHostingTraffic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#delete FirebaseAppHostingTraffic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#update FirebaseAppHostingTraffic#update}.
        '''
        value = FirebaseAppHostingTrafficTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRolloutPolicy")
    def reset_rollout_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutPolicy", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

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
    @jsii.member(jsii_name="current")
    def current(self) -> "FirebaseAppHostingTrafficCurrentList":
        return typing.cast("FirebaseAppHostingTrafficCurrentList", jsii.get(self, "current"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="rolloutPolicy")
    def rollout_policy(self) -> "FirebaseAppHostingTrafficRolloutPolicyOutputReference":
        return typing.cast("FirebaseAppHostingTrafficRolloutPolicyOutputReference", jsii.get(self, "rolloutPolicy"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "FirebaseAppHostingTrafficTargetOutputReference":
        return typing.cast("FirebaseAppHostingTrafficTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FirebaseAppHostingTrafficTimeoutsOutputReference":
        return typing.cast("FirebaseAppHostingTrafficTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutPolicyInput")
    def rollout_policy_input(
        self,
    ) -> typing.Optional["FirebaseAppHostingTrafficRolloutPolicy"]:
        return typing.cast(typing.Optional["FirebaseAppHostingTrafficRolloutPolicy"], jsii.get(self, "rolloutPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional["FirebaseAppHostingTrafficTarget"]:
        return typing.cast(typing.Optional["FirebaseAppHostingTrafficTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirebaseAppHostingTrafficTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirebaseAppHostingTrafficTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backend")
    def backend(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backend"))

    @backend.setter
    def backend(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0dfe2f30d81649c3e94cc16f2ea53af002e87ad07d3e15b64f67530d7189b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbc7a9e6b5cf0d44d79ad326a3b083b4d1eaf6dda8d9ea25b13b8b4cafbe44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ca77573b307cec30e0ac5c1ce7a98289eb07854c9ec95bc7991ab741f56574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b9da45e4286712ad3f643511397d51544fec49bddd8cdf663935d7bd61fb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backend": "backend",
        "location": "location",
        "id": "id",
        "project": "project",
        "rollout_policy": "rolloutPolicy",
        "target": "target",
        "timeouts": "timeouts",
    },
)
class FirebaseAppHostingTrafficConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rollout_policy: typing.Optional[typing.Union["FirebaseAppHostingTrafficRolloutPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Union["FirebaseAppHostingTrafficTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FirebaseAppHostingTrafficTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backend: Id of the backend that this Traffic config applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#backend FirebaseAppHostingTraffic#backend}
        :param location: The location the Backend that this Traffic config applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#location FirebaseAppHostingTraffic#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#id FirebaseAppHostingTraffic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#project FirebaseAppHostingTraffic#project}.
        :param rollout_policy: rollout_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#rollout_policy FirebaseAppHostingTraffic#rollout_policy}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#target FirebaseAppHostingTraffic#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#timeouts FirebaseAppHostingTraffic#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rollout_policy, dict):
            rollout_policy = FirebaseAppHostingTrafficRolloutPolicy(**rollout_policy)
        if isinstance(target, dict):
            target = FirebaseAppHostingTrafficTarget(**target)
        if isinstance(timeouts, dict):
            timeouts = FirebaseAppHostingTrafficTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94eea4d475b1a10d4bae7e6f1c19c10d7f1da735b63e02f627f0b637f4a93536)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rollout_policy", value=rollout_policy, expected_type=type_hints["rollout_policy"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend": backend,
            "location": location,
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
        if project is not None:
            self._values["project"] = project
        if rollout_policy is not None:
            self._values["rollout_policy"] = rollout_policy
        if target is not None:
            self._values["target"] = target
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
    def backend(self) -> builtins.str:
        '''Id of the backend that this Traffic config applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#backend FirebaseAppHostingTraffic#backend}
        '''
        result = self._values.get("backend")
        assert result is not None, "Required property 'backend' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location the Backend that this Traffic config applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#location FirebaseAppHostingTraffic#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#id FirebaseAppHostingTraffic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#project FirebaseAppHostingTraffic#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollout_policy(
        self,
    ) -> typing.Optional["FirebaseAppHostingTrafficRolloutPolicy"]:
        '''rollout_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#rollout_policy FirebaseAppHostingTraffic#rollout_policy}
        '''
        result = self._values.get("rollout_policy")
        return typing.cast(typing.Optional["FirebaseAppHostingTrafficRolloutPolicy"], result)

    @builtins.property
    def target(self) -> typing.Optional["FirebaseAppHostingTrafficTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#target FirebaseAppHostingTraffic#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["FirebaseAppHostingTrafficTarget"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FirebaseAppHostingTrafficTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#timeouts FirebaseAppHostingTraffic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FirebaseAppHostingTrafficTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficCurrent",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingTrafficCurrent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficCurrent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingTrafficCurrentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficCurrentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ddfb5cf0e2e32c939f3379799f67a7299796f290551fd54b0dfec8e94257afc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingTrafficCurrentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ecff14e29012c2b150dc77e771d208d32b5ff7a0ba3f1a8b51f5ae453eae8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingTrafficCurrentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294ac58ad944253cdc119240fddafac71cb1802608c23afb2dbdb9153a605a10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11b4932cbdd0486f399be833fd914ad989a9bedca0a8612fe1d4cd06ca4176e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f568d1c9b24abf9fc6ca868f2a1985ebf37b5371e5127700781144277d1c6b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingTrafficCurrentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficCurrentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b5d47e7a7b79bc2db252b5c6cf7ec0733302e4811c51b1801cff82588056b77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="splits")
    def splits(self) -> "FirebaseAppHostingTrafficCurrentSplitsList":
        return typing.cast("FirebaseAppHostingTrafficCurrentSplitsList", jsii.get(self, "splits"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirebaseAppHostingTrafficCurrent]:
        return typing.cast(typing.Optional[FirebaseAppHostingTrafficCurrent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingTrafficCurrent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6707f656c585a332b6040cd92e58ff8bdbd1ad185f39733ca6565a145c486024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficCurrentSplits",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingTrafficCurrentSplits:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficCurrentSplits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingTrafficCurrentSplitsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficCurrentSplitsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__990457d2fc784d94a5611aa58b65e5798d55a7a49893e32718a937d536cf09de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingTrafficCurrentSplitsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72639edc33bf6ae930de59414f1035bd0d5fd83dbd33d1ec7cd41fa2ec1e4c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingTrafficCurrentSplitsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a44d22872e22fad79eade7b4187179b8ea59d2e95ba9adf16de7cf545fa5cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54361ad03b02acb7cb7c192f34ec5bc6255fe7436a194f312a1479a9013fab66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b5ad7440271c5ddfaf9573960d79f858761edd1b178546c29df64fa8457b066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingTrafficCurrentSplitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficCurrentSplitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__368d80798b2d073f1e89d3ea5a9b96b1b67d516aff12017f728e3bc735f35705)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirebaseAppHostingTrafficCurrentSplits]:
        return typing.cast(typing.Optional[FirebaseAppHostingTrafficCurrentSplits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingTrafficCurrentSplits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae48e1be806828461f3ff6d5109835bd3a0c7f008a9ebd62d7708781b18d6f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficRolloutPolicy",
    jsii_struct_bases=[],
    name_mapping={"codebase_branch": "codebaseBranch", "disabled": "disabled"},
)
class FirebaseAppHostingTrafficRolloutPolicy:
    def __init__(
        self,
        *,
        codebase_branch: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param codebase_branch: Specifies a branch that triggers a new build to be started with this policy. If not set, no automatic rollouts will happen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#codebase_branch FirebaseAppHostingTraffic#codebase_branch}
        :param disabled: A flag that, if true, prevents rollouts from being created via this RolloutPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#disabled FirebaseAppHostingTraffic#disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84680334b652952edcf42417f2a6ec90663ae0613cd0444aae9926b933ee259a)
            check_type(argname="argument codebase_branch", value=codebase_branch, expected_type=type_hints["codebase_branch"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if codebase_branch is not None:
            self._values["codebase_branch"] = codebase_branch
        if disabled is not None:
            self._values["disabled"] = disabled

    @builtins.property
    def codebase_branch(self) -> typing.Optional[builtins.str]:
        '''Specifies a branch that triggers a new build to be started with this policy.

        If not set, no automatic rollouts will happen.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#codebase_branch FirebaseAppHostingTraffic#codebase_branch}
        '''
        result = self._values.get("codebase_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag that, if true, prevents rollouts from being created via this RolloutPolicy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#disabled FirebaseAppHostingTraffic#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficRolloutPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingTrafficRolloutPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficRolloutPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bf64622f5bfc4e6349299db14d8001ba7fa06a6a278b168787f0e36aaffb917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCodebaseBranch")
    def reset_codebase_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodebaseBranch", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="disabledTime")
    def disabled_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disabledTime"))

    @builtins.property
    @jsii.member(jsii_name="codebaseBranchInput")
    def codebase_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codebaseBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="codebaseBranch")
    def codebase_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codebaseBranch"))

    @codebase_branch.setter
    def codebase_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ef3b45f73d227ae1cb33f589b5d2f1605ba2546305b44edb41f3692912d111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codebaseBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97facc051cb5bcbdfcae3a57d3f2cd7844ca84c5de52aebb3ef42bf3d0b2c9b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirebaseAppHostingTrafficRolloutPolicy]:
        return typing.cast(typing.Optional[FirebaseAppHostingTrafficRolloutPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingTrafficRolloutPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b1126b060ec31fb15ab09b4243ff7911d57602622d03511883df7169400575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTarget",
    jsii_struct_bases=[],
    name_mapping={"splits": "splits"},
)
class FirebaseAppHostingTrafficTarget:
    def __init__(
        self,
        *,
        splits: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirebaseAppHostingTrafficTargetSplits", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param splits: splits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#splits FirebaseAppHostingTraffic#splits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1814bef3e391df9c0e95ec56579244ff2d766f7dd5a20a70a5b65d6b63a763)
            check_type(argname="argument splits", value=splits, expected_type=type_hints["splits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "splits": splits,
        }

    @builtins.property
    def splits(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirebaseAppHostingTrafficTargetSplits"]]:
        '''splits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#splits FirebaseAppHostingTraffic#splits}
        '''
        result = self._values.get("splits")
        assert result is not None, "Required property 'splits' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirebaseAppHostingTrafficTargetSplits"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingTrafficTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa9cb28731344131439bf8ee4b171831852b4033e632116bd043699ad8838fca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSplits")
    def put_splits(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirebaseAppHostingTrafficTargetSplits", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd8a82b293997efcc84d0b8aa95877785bd6280130ece4e44a27c864cab8133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSplits", [value]))

    @builtins.property
    @jsii.member(jsii_name="splits")
    def splits(self) -> "FirebaseAppHostingTrafficTargetSplitsList":
        return typing.cast("FirebaseAppHostingTrafficTargetSplitsList", jsii.get(self, "splits"))

    @builtins.property
    @jsii.member(jsii_name="splitsInput")
    def splits_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirebaseAppHostingTrafficTargetSplits"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirebaseAppHostingTrafficTargetSplits"]]], jsii.get(self, "splitsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirebaseAppHostingTrafficTarget]:
        return typing.cast(typing.Optional[FirebaseAppHostingTrafficTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingTrafficTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e863f066392368fe3110c5c20e3432c70dc6cfa0a764c35bfb2620df71cc4c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTargetSplits",
    jsii_struct_bases=[],
    name_mapping={"build_attribute": "buildAttribute", "percent": "percent"},
)
class FirebaseAppHostingTrafficTargetSplits:
    def __init__(self, *, build_attribute: builtins.str, percent: jsii.Number) -> None:
        '''
        :param build_attribute: The build that traffic is being routed to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#build FirebaseAppHostingTraffic#build}
        :param percent: The percentage of traffic to send to the build. Currently must be 100 or 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#percent FirebaseAppHostingTraffic#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8404fbb11763d1e670a5aa7305b9ba994930f8c4e0597fffe4d95ff045f96eba)
            check_type(argname="argument build_attribute", value=build_attribute, expected_type=type_hints["build_attribute"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "build_attribute": build_attribute,
            "percent": percent,
        }

    @builtins.property
    def build_attribute(self) -> builtins.str:
        '''The build that traffic is being routed to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#build FirebaseAppHostingTraffic#build}
        '''
        result = self._values.get("build_attribute")
        assert result is not None, "Required property 'build_attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def percent(self) -> jsii.Number:
        '''The percentage of traffic to send to the build. Currently must be 100 or 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#percent FirebaseAppHostingTraffic#percent}
        '''
        result = self._values.get("percent")
        assert result is not None, "Required property 'percent' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficTargetSplits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingTrafficTargetSplitsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTargetSplitsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abfbf250c56b7de56ff2fd8b2a768e57eef9cd66ce36b01a7f625cf7eb404f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingTrafficTargetSplitsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c80a42b973260d9b5cc282c73eee7bcd3502b19c2c942114b9dcb297a2d0a13)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingTrafficTargetSplitsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8af9ca717e05fa020d8e23e22c9bc86892359dd53c9e7e629777b4ef8cbfd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62120eff7ee6199dd3632403ea3bacbcf6b8af61315ef20b4154e65d5b33cd32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1baa6015b19fe8dcf1bc04169f3a40cc56b9170e11d2522f77721340a3e969a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirebaseAppHostingTrafficTargetSplits]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirebaseAppHostingTrafficTargetSplits]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirebaseAppHostingTrafficTargetSplits]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3ac3e7f834f4036f94ec7e93307683ad1267a004539a611f5022ddaee3a968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingTrafficTargetSplitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTargetSplitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee180d941a720ed444683fbb93b9ecbe6ff059a18a589d943f2540df4fa0ca20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="buildAttributeInput")
    def build_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildAttribute"))

    @build_attribute.setter
    def build_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd164a26e8f911fc63ed8aa6dd2254f2c5a23d146303458ee8ff17416970eaf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a5e2200f6bd7be5395a3c9f07422844f9e40820cf9f5b98ea2df4d812799e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTargetSplits]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTargetSplits]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTargetSplits]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c8d653567021ce6bd967611ac1a22fb03921195fff01273fd19bf1e558b5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FirebaseAppHostingTrafficTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#create FirebaseAppHostingTraffic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#delete FirebaseAppHostingTraffic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#update FirebaseAppHostingTraffic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87961e98fa4065ae91a69db124f0c92f4317db66cbee97233ea0e3668b716e8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#create FirebaseAppHostingTraffic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#delete FirebaseAppHostingTraffic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_traffic#update FirebaseAppHostingTraffic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingTrafficTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingTrafficTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingTraffic.FirebaseAppHostingTrafficTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15d3b4b98f9d383e4e2be8003ce53554e97e01735da2dfac3b991402abb149d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb27cd0b7df6ed7c0d71547c9146240e2f4331e91d496a3b6d4fa72d8e22585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e158bafee9672f32b29ad833ebf2d8a9022ddb4d13fc3f1958e606995e62773c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47aacc2fb2efcda45d4c0ddace50edf39c08db946ce443a82439f9baee66c88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce13f8b135b7c46899c3c9beb328946a6ac89364a9c68bf63ca2acee0fa45a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FirebaseAppHostingTraffic",
    "FirebaseAppHostingTrafficConfig",
    "FirebaseAppHostingTrafficCurrent",
    "FirebaseAppHostingTrafficCurrentList",
    "FirebaseAppHostingTrafficCurrentOutputReference",
    "FirebaseAppHostingTrafficCurrentSplits",
    "FirebaseAppHostingTrafficCurrentSplitsList",
    "FirebaseAppHostingTrafficCurrentSplitsOutputReference",
    "FirebaseAppHostingTrafficRolloutPolicy",
    "FirebaseAppHostingTrafficRolloutPolicyOutputReference",
    "FirebaseAppHostingTrafficTarget",
    "FirebaseAppHostingTrafficTargetOutputReference",
    "FirebaseAppHostingTrafficTargetSplits",
    "FirebaseAppHostingTrafficTargetSplitsList",
    "FirebaseAppHostingTrafficTargetSplitsOutputReference",
    "FirebaseAppHostingTrafficTimeouts",
    "FirebaseAppHostingTrafficTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e73b4f0ec382521c1bde3544024c6b37f7d6f6f79ac57ac7a7af5a1f37e2b971(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backend: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rollout_policy: typing.Optional[typing.Union[FirebaseAppHostingTrafficRolloutPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Union[FirebaseAppHostingTrafficTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FirebaseAppHostingTrafficTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f28f9928a35e44b7046523f7f44a10a3b297baf7ea7ed86f7e15d14b49ae5e40(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0dfe2f30d81649c3e94cc16f2ea53af002e87ad07d3e15b64f67530d7189b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbc7a9e6b5cf0d44d79ad326a3b083b4d1eaf6dda8d9ea25b13b8b4cafbe44b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ca77573b307cec30e0ac5c1ce7a98289eb07854c9ec95bc7991ab741f56574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b9da45e4286712ad3f643511397d51544fec49bddd8cdf663935d7bd61fb1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94eea4d475b1a10d4bae7e6f1c19c10d7f1da735b63e02f627f0b637f4a93536(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rollout_policy: typing.Optional[typing.Union[FirebaseAppHostingTrafficRolloutPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Union[FirebaseAppHostingTrafficTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FirebaseAppHostingTrafficTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddfb5cf0e2e32c939f3379799f67a7299796f290551fd54b0dfec8e94257afc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ecff14e29012c2b150dc77e771d208d32b5ff7a0ba3f1a8b51f5ae453eae8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294ac58ad944253cdc119240fddafac71cb1802608c23afb2dbdb9153a605a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b4932cbdd0486f399be833fd914ad989a9bedca0a8612fe1d4cd06ca4176e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f568d1c9b24abf9fc6ca868f2a1985ebf37b5371e5127700781144277d1c6b55(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5d47e7a7b79bc2db252b5c6cf7ec0733302e4811c51b1801cff82588056b77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6707f656c585a332b6040cd92e58ff8bdbd1ad185f39733ca6565a145c486024(
    value: typing.Optional[FirebaseAppHostingTrafficCurrent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990457d2fc784d94a5611aa58b65e5798d55a7a49893e32718a937d536cf09de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72639edc33bf6ae930de59414f1035bd0d5fd83dbd33d1ec7cd41fa2ec1e4c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a44d22872e22fad79eade7b4187179b8ea59d2e95ba9adf16de7cf545fa5cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54361ad03b02acb7cb7c192f34ec5bc6255fe7436a194f312a1479a9013fab66(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5ad7440271c5ddfaf9573960d79f858761edd1b178546c29df64fa8457b066(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368d80798b2d073f1e89d3ea5a9b96b1b67d516aff12017f728e3bc735f35705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae48e1be806828461f3ff6d5109835bd3a0c7f008a9ebd62d7708781b18d6f8a(
    value: typing.Optional[FirebaseAppHostingTrafficCurrentSplits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84680334b652952edcf42417f2a6ec90663ae0613cd0444aae9926b933ee259a(
    *,
    codebase_branch: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf64622f5bfc4e6349299db14d8001ba7fa06a6a278b168787f0e36aaffb917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ef3b45f73d227ae1cb33f589b5d2f1605ba2546305b44edb41f3692912d111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97facc051cb5bcbdfcae3a57d3f2cd7844ca84c5de52aebb3ef42bf3d0b2c9b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b1126b060ec31fb15ab09b4243ff7911d57602622d03511883df7169400575(
    value: typing.Optional[FirebaseAppHostingTrafficRolloutPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1814bef3e391df9c0e95ec56579244ff2d766f7dd5a20a70a5b65d6b63a763(
    *,
    splits: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirebaseAppHostingTrafficTargetSplits, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9cb28731344131439bf8ee4b171831852b4033e632116bd043699ad8838fca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd8a82b293997efcc84d0b8aa95877785bd6280130ece4e44a27c864cab8133(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirebaseAppHostingTrafficTargetSplits, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e863f066392368fe3110c5c20e3432c70dc6cfa0a764c35bfb2620df71cc4c27(
    value: typing.Optional[FirebaseAppHostingTrafficTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8404fbb11763d1e670a5aa7305b9ba994930f8c4e0597fffe4d95ff045f96eba(
    *,
    build_attribute: builtins.str,
    percent: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfbf250c56b7de56ff2fd8b2a768e57eef9cd66ce36b01a7f625cf7eb404f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c80a42b973260d9b5cc282c73eee7bcd3502b19c2c942114b9dcb297a2d0a13(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8af9ca717e05fa020d8e23e22c9bc86892359dd53c9e7e629777b4ef8cbfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62120eff7ee6199dd3632403ea3bacbcf6b8af61315ef20b4154e65d5b33cd32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1baa6015b19fe8dcf1bc04169f3a40cc56b9170e11d2522f77721340a3e969a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3ac3e7f834f4036f94ec7e93307683ad1267a004539a611f5022ddaee3a968(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirebaseAppHostingTrafficTargetSplits]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee180d941a720ed444683fbb93b9ecbe6ff059a18a589d943f2540df4fa0ca20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd164a26e8f911fc63ed8aa6dd2254f2c5a23d146303458ee8ff17416970eaf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a5e2200f6bd7be5395a3c9f07422844f9e40820cf9f5b98ea2df4d812799e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c8d653567021ce6bd967611ac1a22fb03921195fff01273fd19bf1e558b5c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTargetSplits]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87961e98fa4065ae91a69db124f0c92f4317db66cbee97233ea0e3668b716e8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d3b4b98f9d383e4e2be8003ce53554e97e01735da2dfac3b991402abb149d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb27cd0b7df6ed7c0d71547c9146240e2f4331e91d496a3b6d4fa72d8e22585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e158bafee9672f32b29ad833ebf2d8a9022ddb4d13fc3f1958e606995e62773c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47aacc2fb2efcda45d4c0ddace50edf39c08db946ce443a82439f9baee66c88a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce13f8b135b7c46899c3c9beb328946a6ac89364a9c68bf63ca2acee0fa45a26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingTrafficTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
