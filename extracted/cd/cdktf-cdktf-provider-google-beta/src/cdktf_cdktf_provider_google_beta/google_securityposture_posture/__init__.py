r'''
# `google_securityposture_posture`

Refer to the Terraform Registry for docs: [`google_securityposture_posture`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture).
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


class GoogleSecurityposturePosture(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosture",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture google_securityposture_posture}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        parent: builtins.str,
        policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySets", typing.Dict[builtins.str, typing.Any]]]],
        posture_id: builtins.str,
        state: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleSecurityposturePostureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture google_securityposture_posture} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the resource, eg: global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param parent: The parent of the resource, an organization. Format should be 'organizations/{organization_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#parent GoogleSecurityposturePosture#parent}
        :param policy_sets: policy_sets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_sets GoogleSecurityposturePosture#policy_sets}
        :param posture_id: Id of the posture. It is an immutable field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#posture_id GoogleSecurityposturePosture#posture_id}
        :param state: State of the posture. Update to state field should not be triggered along with with other field updates. Possible values: ["DEPRECATED", "DRAFT", "ACTIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#state GoogleSecurityposturePosture#state}
        :param description: Description of the posture. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#id GoogleSecurityposturePosture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#timeouts GoogleSecurityposturePosture#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8314ed92697ebe0ec8be34793f564cccdd010630daa59e288adce19ad2bb691)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleSecurityposturePostureConfig(
            location=location,
            parent=parent,
            policy_sets=policy_sets,
            posture_id=posture_id,
            state=state,
            description=description,
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
        '''Generates CDKTF code for importing a GoogleSecurityposturePosture resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleSecurityposturePosture to import.
        :param import_from_id: The id of the existing GoogleSecurityposturePosture that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleSecurityposturePosture to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272ca6b3922feac754e8aa6dae5910480a4497c608d53c7d9bf54633bb797039)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPolicySets")
    def put_policy_sets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0194bda7fb19e072b6a48d4d9d9a5c1abb4d9e0e8ddd9e9ac7a182f34d0c5b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicySets", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#create GoogleSecurityposturePosture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#delete GoogleSecurityposturePosture#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#update GoogleSecurityposturePosture#update}.
        '''
        value = GoogleSecurityposturePostureTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="policySets")
    def policy_sets(self) -> "GoogleSecurityposturePosturePolicySetsList":
        return typing.cast("GoogleSecurityposturePosturePolicySetsList", jsii.get(self, "policySets"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="revisionId")
    def revision_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleSecurityposturePostureTimeoutsOutputReference":
        return typing.cast("GoogleSecurityposturePostureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="policySetsInput")
    def policy_sets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySets"]]], jsii.get(self, "policySetsInput"))

    @builtins.property
    @jsii.member(jsii_name="postureIdInput")
    def posture_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postureIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSecurityposturePostureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSecurityposturePostureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fca1d25301df521021b0b0c848164f257cfe361f40d5c65edc10efba6e0b986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f0697fd380603247c7e9ce119e120419ab7b62a9a906c70bd8cd49cf54cad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f010e212e86a3115e2921437ad671a52d9493054be51fb9e8c73a819440e4b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c288da0f86501a38725f9610338c6e67116a1d3b9690d51ccc171cda5f3c2046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postureId")
    def posture_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postureId"))

    @posture_id.setter
    def posture_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3abeecd6f0f7f69c8beec727e5f9e6fc5737ca3dafdd095b4488be37347684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32300c893c243c19cec9a78f6fade84efb47785050fc5216c493b32e472f2975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePostureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "parent": "parent",
        "policy_sets": "policySets",
        "posture_id": "postureId",
        "state": "state",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleSecurityposturePostureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        parent: builtins.str,
        policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySets", typing.Dict[builtins.str, typing.Any]]]],
        posture_id: builtins.str,
        state: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleSecurityposturePostureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the resource, eg: global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param parent: The parent of the resource, an organization. Format should be 'organizations/{organization_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#parent GoogleSecurityposturePosture#parent}
        :param policy_sets: policy_sets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_sets GoogleSecurityposturePosture#policy_sets}
        :param posture_id: Id of the posture. It is an immutable field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#posture_id GoogleSecurityposturePosture#posture_id}
        :param state: State of the posture. Update to state field should not be triggered along with with other field updates. Possible values: ["DEPRECATED", "DRAFT", "ACTIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#state GoogleSecurityposturePosture#state}
        :param description: Description of the posture. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#id GoogleSecurityposturePosture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#timeouts GoogleSecurityposturePosture#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleSecurityposturePostureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200fd19f34419dd89eb64010336ccb464b81485387c69556f54283ac2de85220)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument policy_sets", value=policy_sets, expected_type=type_hints["policy_sets"])
            check_type(argname="argument posture_id", value=posture_id, expected_type=type_hints["posture_id"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "parent": parent,
            "policy_sets": policy_sets,
            "posture_id": posture_id,
            "state": state,
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
        if description is not None:
            self._values["description"] = description
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
    def location(self) -> builtins.str:
        '''Location of the resource, eg: global.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the resource, an organization. Format should be 'organizations/{organization_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#parent GoogleSecurityposturePosture#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_sets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySets"]]:
        '''policy_sets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_sets GoogleSecurityposturePosture#policy_sets}
        '''
        result = self._values.get("policy_sets")
        assert result is not None, "Required property 'policy_sets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySets"]], result)

    @builtins.property
    def posture_id(self) -> builtins.str:
        '''Id of the posture. It is an immutable field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#posture_id GoogleSecurityposturePosture#posture_id}
        '''
        result = self._values.get("posture_id")
        assert result is not None, "Required property 'posture_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''State of the posture.

        Update to state field should not be triggered along with
        with other field updates. Possible values: ["DEPRECATED", "DRAFT", "ACTIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#state GoogleSecurityposturePosture#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the posture.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#id GoogleSecurityposturePosture#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleSecurityposturePostureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#timeouts GoogleSecurityposturePosture#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleSecurityposturePostureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePostureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySets",
    jsii_struct_bases=[],
    name_mapping={
        "policies": "policies",
        "policy_set_id": "policySetId",
        "description": "description",
    },
)
class GoogleSecurityposturePosturePolicySets:
    def __init__(
        self,
        *,
        policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        policy_set_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policies: policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policies GoogleSecurityposturePosture#policies}
        :param policy_set_id: ID of the policy set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_set_id GoogleSecurityposturePosture#policy_set_id}
        :param description: Description of the policy set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f862ec37772db2efa107ace92c65d56069611259a0b73dd2253760bc191e1fc)
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument policy_set_id", value=policy_set_id, expected_type=type_hints["policy_set_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policies": policies,
            "policy_set_id": policy_set_id,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPolicies"]]:
        '''policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policies GoogleSecurityposturePosture#policies}
        '''
        result = self._values.get("policies")
        assert result is not None, "Required property 'policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPolicies"]], result)

    @builtins.property
    def policy_set_id(self) -> builtins.str:
        '''ID of the policy set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_set_id GoogleSecurityposturePosture#policy_set_id}
        '''
        result = self._values.get("policy_set_id")
        assert result is not None, "Required property 'policy_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the policy set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29c93721cbdaa35cc270fc578e6c243992bfdc39cf30fea281e2e7d7bf81bef1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecurityposturePosturePolicySetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1e9f1ef1ce5b2c9bb44c6c7f05fc38659a5dcdb4303f1540adffd68e335895)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecurityposturePosturePolicySetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aec57c5cc8732f3ae793b6d568f88787f3cb3f98fe94823ce7a64a908779967)
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
            type_hints = typing.get_type_hints(_typecheckingstub__693cfd72968ac9bcbb1c55bd860e6be99768893465353e727150c51dda09cc7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dd871189e482fd0c37295c68b77e7776968e09375554063736ee6da471e8273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a688b3d42550bf06901721c9c24a3b9bf65e1900ee10a3edb7f09b83a90fcad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fc364bd069abb11160b378739e1b31c96deaab0286b7ed2d6582215c7ab0bb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicies")
    def put_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7867cdd7038fdbf7d01491b41d2be404e0729d3802d6d1cdc40abe54c2e346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicies", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> "GoogleSecurityposturePosturePolicySetsPoliciesList":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesList", jsii.get(self, "policies"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="policiesInput")
    def policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPolicies"]]], jsii.get(self, "policiesInput"))

    @builtins.property
    @jsii.member(jsii_name="policySetIdInput")
    def policy_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policySetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6dae5a184ffb4f912473c1a75d09861bfadafe53ad809ef5681e0c27b80ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policySetId")
    def policy_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policySetId"))

    @policy_set_id.setter
    def policy_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d814f7167d482cb54fdb731ed2897b0aa33c54474ecaa53e146841203be749a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policySetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517b00422a94e854cc89bf753d5b1a7934c30c0dfde83f0a61c646a6e915745d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "constraint": "constraint",
        "policy_id": "policyId",
        "compliance_standards": "complianceStandards",
        "description": "description",
    },
)
class GoogleSecurityposturePosturePolicySetsPolicies:
    def __init__(
        self,
        *,
        constraint: typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraint", typing.Dict[builtins.str, typing.Any]],
        policy_id: builtins.str,
        compliance_standards: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param constraint: constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#constraint GoogleSecurityposturePosture#constraint}
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_id GoogleSecurityposturePosture#policy_id}
        :param compliance_standards: compliance_standards block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#compliance_standards GoogleSecurityposturePosture#compliance_standards}
        :param description: Description of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        if isinstance(constraint, dict):
            constraint = GoogleSecurityposturePosturePolicySetsPoliciesConstraint(**constraint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f479da3059ac31beb63dbc10c1631226f470ce75acfc000e93f5aa1003e5e0b4)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument compliance_standards", value=compliance_standards, expected_type=type_hints["compliance_standards"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "constraint": constraint,
            "policy_id": policy_id,
        }
        if compliance_standards is not None:
            self._values["compliance_standards"] = compliance_standards
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def constraint(self) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraint":
        '''constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#constraint GoogleSecurityposturePosture#constraint}
        '''
        result = self._values.get("constraint")
        assert result is not None, "Required property 'constraint' is missing"
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraint", result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''ID of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_id GoogleSecurityposturePosture#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compliance_standards(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards"]]]:
        '''compliance_standards block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#compliance_standards GoogleSecurityposturePosture#compliance_standards}
        '''
        result = self._values.get("compliance_standards")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards",
    jsii_struct_bases=[],
    name_mapping={"control": "control", "standard": "standard"},
)
class GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards:
    def __init__(
        self,
        *,
        control: typing.Optional[builtins.str] = None,
        standard: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control: Mapping of security controls for the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#control GoogleSecurityposturePosture#control}
        :param standard: Mapping of compliance standards for the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#standard GoogleSecurityposturePosture#standard}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b6d18e852abf4ef59d11fe25b392e8087df61370fedec8026dea99047240e9)
            check_type(argname="argument control", value=control, expected_type=type_hints["control"])
            check_type(argname="argument standard", value=standard, expected_type=type_hints["standard"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control is not None:
            self._values["control"] = control
        if standard is not None:
            self._values["standard"] = standard

    @builtins.property
    def control(self) -> typing.Optional[builtins.str]:
        '''Mapping of security controls for the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#control GoogleSecurityposturePosture#control}
        '''
        result = self._values.get("control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard(self) -> typing.Optional[builtins.str]:
        '''Mapping of compliance standards for the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#standard GoogleSecurityposturePosture#standard}
        '''
        result = self._values.get("standard")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72d35f348e4b207e6e5cbcd2b73ddff47cb745a6b70ff4786e552b1a53df3f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8344a8ddad8bb7422a0529c8d0d9773595cbb0cf30f15b05f9b2d331d885cfe2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5b3728d392998591771126e1515c509f1a1663c701c1126122e7736d96ab88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87752946e43e2a81fb22533377046dcf6d8f09004289acc6073dea5dca6cdd78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76ddb7c9b61526a866d8cd768e15755e65b76cbee3e698af8877d2f826277b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bb97f0ea947aefa66d5869b22b9fceb9bed2cf7179bc05697b23a886373648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0543e784385358022109ebedfdb8583cfe3b64a9c422ddad204609bd755bf66e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetControl")
    def reset_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControl", []))

    @jsii.member(jsii_name="resetStandard")
    def reset_standard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandard", []))

    @builtins.property
    @jsii.member(jsii_name="controlInput")
    def control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlInput"))

    @builtins.property
    @jsii.member(jsii_name="standardInput")
    def standard_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "standardInput"))

    @builtins.property
    @jsii.member(jsii_name="control")
    def control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "control"))

    @control.setter
    def control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9282fe50c374d42ba2450a0be1bc41f9eb1e25880cc8f487a5a91019edba5c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "control", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="standard")
    def standard(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standard"))

    @standard.setter
    def standard(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74d35b7c03277f6af2849c301c3e9c2d299ce967d6f057b9f9968c1bba14041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26ff376bd8c9c6fcf5d992022a94da51454f2e7d11f207aec85607370d2326a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraint",
    jsii_struct_bases=[],
    name_mapping={
        "org_policy_constraint": "orgPolicyConstraint",
        "org_policy_constraint_custom": "orgPolicyConstraintCustom",
        "security_health_analytics_custom_module": "securityHealthAnalyticsCustomModule",
        "security_health_analytics_module": "securityHealthAnalyticsModule",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraint:
    def __init__(
        self,
        *,
        org_policy_constraint: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint", typing.Dict[builtins.str, typing.Any]]] = None,
        org_policy_constraint_custom: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_custom_module: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule", typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_module: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param org_policy_constraint: org_policy_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#org_policy_constraint GoogleSecurityposturePosture#org_policy_constraint}
        :param org_policy_constraint_custom: org_policy_constraint_custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#org_policy_constraint_custom GoogleSecurityposturePosture#org_policy_constraint_custom}
        :param security_health_analytics_custom_module: security_health_analytics_custom_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#security_health_analytics_custom_module GoogleSecurityposturePosture#security_health_analytics_custom_module}
        :param security_health_analytics_module: security_health_analytics_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#security_health_analytics_module GoogleSecurityposturePosture#security_health_analytics_module}
        '''
        if isinstance(org_policy_constraint, dict):
            org_policy_constraint = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint(**org_policy_constraint)
        if isinstance(org_policy_constraint_custom, dict):
            org_policy_constraint_custom = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom(**org_policy_constraint_custom)
        if isinstance(security_health_analytics_custom_module, dict):
            security_health_analytics_custom_module = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule(**security_health_analytics_custom_module)
        if isinstance(security_health_analytics_module, dict):
            security_health_analytics_module = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule(**security_health_analytics_module)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b666e607b8c89cc0c186a30fc79a9ffc23901dd6de15dbc397ad78b106541c)
            check_type(argname="argument org_policy_constraint", value=org_policy_constraint, expected_type=type_hints["org_policy_constraint"])
            check_type(argname="argument org_policy_constraint_custom", value=org_policy_constraint_custom, expected_type=type_hints["org_policy_constraint_custom"])
            check_type(argname="argument security_health_analytics_custom_module", value=security_health_analytics_custom_module, expected_type=type_hints["security_health_analytics_custom_module"])
            check_type(argname="argument security_health_analytics_module", value=security_health_analytics_module, expected_type=type_hints["security_health_analytics_module"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if org_policy_constraint is not None:
            self._values["org_policy_constraint"] = org_policy_constraint
        if org_policy_constraint_custom is not None:
            self._values["org_policy_constraint_custom"] = org_policy_constraint_custom
        if security_health_analytics_custom_module is not None:
            self._values["security_health_analytics_custom_module"] = security_health_analytics_custom_module
        if security_health_analytics_module is not None:
            self._values["security_health_analytics_module"] = security_health_analytics_module

    @builtins.property
    def org_policy_constraint(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint"]:
        '''org_policy_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#org_policy_constraint GoogleSecurityposturePosture#org_policy_constraint}
        '''
        result = self._values.get("org_policy_constraint")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint"], result)

    @builtins.property
    def org_policy_constraint_custom(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom"]:
        '''org_policy_constraint_custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#org_policy_constraint_custom GoogleSecurityposturePosture#org_policy_constraint_custom}
        '''
        result = self._values.get("org_policy_constraint_custom")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom"], result)

    @builtins.property
    def security_health_analytics_custom_module(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"]:
        '''security_health_analytics_custom_module block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#security_health_analytics_custom_module GoogleSecurityposturePosture#security_health_analytics_custom_module}
        '''
        result = self._values.get("security_health_analytics_custom_module")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"], result)

    @builtins.property
    def security_health_analytics_module(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"]:
        '''security_health_analytics_module block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#security_health_analytics_module GoogleSecurityposturePosture#security_health_analytics_module}
        '''
        result = self._values.get("security_health_analytics_module")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint",
    jsii_struct_bases=[],
    name_mapping={
        "canned_constraint_id": "cannedConstraintId",
        "policy_rules": "policyRules",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint:
    def __init__(
        self,
        *,
        canned_constraint_id: builtins.str,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param canned_constraint_id: Organization policy canned constraint Id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#canned_constraint_id GoogleSecurityposturePosture#canned_constraint_id}
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_rules GoogleSecurityposturePosture#policy_rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22aef8fb11c877a1f3cad8906b4009e907dbb19f18bc756c9f962e4fe3355b4)
            check_type(argname="argument canned_constraint_id", value=canned_constraint_id, expected_type=type_hints["canned_constraint_id"])
            check_type(argname="argument policy_rules", value=policy_rules, expected_type=type_hints["policy_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "canned_constraint_id": canned_constraint_id,
            "policy_rules": policy_rules,
        }

    @builtins.property
    def canned_constraint_id(self) -> builtins.str:
        '''Organization policy canned constraint Id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#canned_constraint_id GoogleSecurityposturePosture#canned_constraint_id}
        '''
        result = self._values.get("canned_constraint_id")
        assert result is not None, "Required property 'canned_constraint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]]:
        '''policy_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_rules GoogleSecurityposturePosture#policy_rules}
        '''
        result = self._values.get("policy_rules")
        assert result is not None, "Required property 'policy_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom",
    jsii_struct_bases=[],
    name_mapping={
        "policy_rules": "policyRules",
        "custom_constraint": "customConstraint",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom:
    def __init__(
        self,
        *,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        custom_constraint: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_rules GoogleSecurityposturePosture#policy_rules}
        :param custom_constraint: custom_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#custom_constraint GoogleSecurityposturePosture#custom_constraint}
        '''
        if isinstance(custom_constraint, dict):
            custom_constraint = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint(**custom_constraint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b764a517cd3c1441e76aed5a5bfb28fddbdda46545c2f5d350504d1038f2a5)
            check_type(argname="argument policy_rules", value=policy_rules, expected_type=type_hints["policy_rules"])
            check_type(argname="argument custom_constraint", value=custom_constraint, expected_type=type_hints["custom_constraint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_rules": policy_rules,
        }
        if custom_constraint is not None:
            self._values["custom_constraint"] = custom_constraint

    @builtins.property
    def policy_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]]:
        '''policy_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_rules GoogleSecurityposturePosture#policy_rules}
        '''
        result = self._values.get("policy_rules")
        assert result is not None, "Required property 'policy_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]], result)

    @builtins.property
    def custom_constraint(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint"]:
        '''custom_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#custom_constraint GoogleSecurityposturePosture#custom_constraint}
        '''
        result = self._values.get("custom_constraint")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint",
    jsii_struct_bases=[],
    name_mapping={
        "action_type": "actionType",
        "condition": "condition",
        "method_types": "methodTypes",
        "name": "name",
        "resource_types": "resourceTypes",
        "description": "description",
        "display_name": "displayName",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint:
    def __init__(
        self,
        *,
        action_type: builtins.str,
        condition: builtins.str,
        method_types: typing.Sequence[builtins.str],
        name: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_type: The action to take if the condition is met. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#action_type GoogleSecurityposturePosture#action_type}
        :param condition: A CEL condition that refers to a supported service resource, for example 'resource.management.autoUpgrade == false'. For details about CEL usage, see `Common Expression Language <https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        :param method_types: A list of RESTful methods for which to enforce the constraint. Can be 'CREATE', 'UPDATE', or both. Not all Google Cloud services support both methods. To see supported methods for each service, find the service in `Supported services <https://cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#method_types GoogleSecurityposturePosture#method_types}
        :param name: Immutable. The name of the custom constraint. This is unique within the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#name GoogleSecurityposturePosture#name}
        :param resource_types: Immutable. The fully qualified name of the Google Cloud REST resource containing the object and field you want to restrict. For example, 'container.googleapis.com/NodePool'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_types GoogleSecurityposturePosture#resource_types}
        :param description: A human-friendly description of the constraint to display as an error message when the policy is violated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param display_name: A human-friendly name for the constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#display_name GoogleSecurityposturePosture#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4aaeacbdc3bc282fa84a151e8a96de77a0372f8df7b94926243148f620f618)
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument method_types", value=method_types, expected_type=type_hints["method_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_type": action_type,
            "condition": condition,
            "method_types": method_types,
            "name": name,
            "resource_types": resource_types,
        }
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def action_type(self) -> builtins.str:
        '''The action to take if the condition is met. Possible values: ["ALLOW", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#action_type GoogleSecurityposturePosture#action_type}
        '''
        result = self._values.get("action_type")
        assert result is not None, "Required property 'action_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> builtins.str:
        '''A CEL condition that refers to a supported service resource, for example 'resource.management.autoUpgrade == false'. For details about CEL usage, see `Common Expression Language <https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def method_types(self) -> typing.List[builtins.str]:
        '''A list of RESTful methods for which to enforce the constraint.

        Can be 'CREATE', 'UPDATE', or both. Not all Google Cloud services support both methods. To see supported methods for each service, find the service in `Supported services <https://cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#method_types GoogleSecurityposturePosture#method_types}
        '''
        result = self._values.get("method_types")
        assert result is not None, "Required property 'method_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Immutable. The name of the custom constraint. This is unique within the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#name GoogleSecurityposturePosture#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''Immutable.

        The fully qualified name of the Google Cloud REST resource containing the object and field you want to restrict. For example, 'container.googleapis.com/NodePool'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_types GoogleSecurityposturePosture#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-friendly description of the constraint to display as an error message when the policy is violated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A human-friendly name for the constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#display_name GoogleSecurityposturePosture#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5cb9958a98ad16f9e02111ba58859143f083fa0ed3a17a614e9278aba17c75d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="actionTypeInput")
    def action_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="methodTypesInput")
    def method_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionType"))

    @action_type.setter
    def action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311b1a7cbf41d0f2f4bdb66b6e210bb7c51bf646e884f05a81053623a68f7abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f5becdba05659c69856b3e57eb4779b8260ac8b1e40aaba38ac3d02a86b22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c8cc7e0fd4eaf3ef59f59737528882efc33f0360fa00c1e6311d78a699468b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35657f08b5206450a5e14786b3df30e0879e43034cdb61601876feb8f71dc8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="methodTypes")
    def method_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methodTypes"))

    @method_types.setter
    def method_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419a4f711d970c4a54db947a6fad86d8b92a1371e392b948d4d46c0819f7c212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methodTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69fe69b27eac7e8171a489260e9cd6e84a8acab42e678fe43861fcb8e225a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b12b0d197ff10f10be9b3539e76753274eb9053042bb12b22bb6ec49124af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959896430eabae5a3a9879a3f4a250f42f099b4dbc54f28b100b3908a53e4927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d860dd5f84cdca209e1d8a734a58252a1371c9bb375a924a12c4f9affcba087c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomConstraint")
    def put_custom_constraint(
        self,
        *,
        action_type: builtins.str,
        condition: builtins.str,
        method_types: typing.Sequence[builtins.str],
        name: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_type: The action to take if the condition is met. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#action_type GoogleSecurityposturePosture#action_type}
        :param condition: A CEL condition that refers to a supported service resource, for example 'resource.management.autoUpgrade == false'. For details about CEL usage, see `Common Expression Language <https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        :param method_types: A list of RESTful methods for which to enforce the constraint. Can be 'CREATE', 'UPDATE', or both. Not all Google Cloud services support both methods. To see supported methods for each service, find the service in `Supported services <https://cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#method_types GoogleSecurityposturePosture#method_types}
        :param name: Immutable. The name of the custom constraint. This is unique within the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#name GoogleSecurityposturePosture#name}
        :param resource_types: Immutable. The fully qualified name of the Google Cloud REST resource containing the object and field you want to restrict. For example, 'container.googleapis.com/NodePool'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_types GoogleSecurityposturePosture#resource_types}
        :param description: A human-friendly description of the constraint to display as an error message when the policy is violated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param display_name: A human-friendly name for the constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#display_name GoogleSecurityposturePosture#display_name}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint(
            action_type=action_type,
            condition=condition,
            method_types=method_types,
            name=name,
            resource_types=resource_types,
            description=description,
            display_name=display_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConstraint", [value]))

    @jsii.member(jsii_name="putPolicyRules")
    def put_policy_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff318d0d3d38bf0aff42437260d560221c18f71c66a63239b2d27f5020ed01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyRules", [value]))

    @jsii.member(jsii_name="resetCustomConstraint")
    def reset_custom_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConstraint", []))

    @builtins.property
    @jsii.member(jsii_name="customConstraint")
    def custom_constraint(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference, jsii.get(self, "customConstraint"))

    @builtins.property
    @jsii.member(jsii_name="policyRules")
    def policy_rules(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList", jsii.get(self, "policyRules"))

    @builtins.property
    @jsii.member(jsii_name="customConstraintInput")
    def custom_constraint_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint], jsii.get(self, "customConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="policyRulesInput")
    def policy_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]]], jsii.get(self, "policyRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99fc3f3a37914890eb3e3ec42802d09208f7ecda2e6c5ccf5776ab2e1d72d508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all": "allowAll",
        "condition": "condition",
        "deny_all": "denyAll",
        "enforce": "enforce",
        "values": "values",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        condition: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to true means that all values are allowed. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allow_all GoogleSecurityposturePosture#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        :param deny_all: Setting this to true means that all values are denied. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#deny_all GoogleSecurityposturePosture#deny_all}
        :param enforce: If 'true', then the policy is enforced. If 'false', then any configuration is acceptable. This field can be set only in policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#enforce GoogleSecurityposturePosture#enforce}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#values GoogleSecurityposturePosture#values}
        '''
        if isinstance(condition, dict):
            condition = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition(**condition)
        if isinstance(values, dict):
            values = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed8e92edb5bf04d51ab2f69f67c23c6db9148182c13734011fa65d6cfe078c1)
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument deny_all", value=deny_all, expected_type=type_hints["deny_all"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if condition is not None:
            self._values["condition"] = condition
        if deny_all is not None:
            self._values["deny_all"] = deny_all
        if enforce is not None:
            self._values["enforce"] = enforce
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def allow_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are allowed.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allow_all GoogleSecurityposturePosture#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition"], result)

    @builtins.property
    def deny_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are denied.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#deny_all GoogleSecurityposturePosture#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', then the policy is enforced.

        If 'false', then any configuration is acceptable.
        This field can be set only in policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#enforce GoogleSecurityposturePosture#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#values GoogleSecurityposturePosture#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bdaae01616505e9af562d2390dec48f860d8830f5687d69df5e071dbb16376)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c66e239f57fe087b8e85eb43543dcfc4fcb859d34b6831591f4520aec7a33c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc73f2adc2ff39365eeb3c49a929c0f9980eda1250ff78ca438973804662c4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2b8251093933f5383ef82ce368c91b0a06d1b960cf0618addfd6ec36db2679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795a80def983f0c1e93dfa410efc7b5159afc353228f1d0b7342ddd1faf3292f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdbe4996c85844e4a357c7e00b1296b543d22cc2fa471f0cf98552820ea067d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2198e8d268a5ff66f202dbf6607e87da81fed9047c69572c7ffe9429712807e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac95059868d971dff56ba1bf5c34ab5dc5c8e9d004c6d2ecd5e94c72e0a28d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25df980c211f28db5ae4915d5a7a5e6a5ea97b8f34b9dbc0923de2b8bdfe20c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df8df573643d9c3cf748b312453c6f233a11457e2cdb0ca09306e2bbd87681c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58d472445a1f6b0cabdb30a78112ce6535c173135327438cd5dcb5e53594e3b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9734a80fdd1ab8cc9808af7c7e440093884647ceea5693e3ee12b59bb9bc79c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97cc5bcace00a426451fdc5973aaffcd1bf13013f36a717a313ec8b57c31528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__670e91de115990a6fd2ed2a38f06d88feba2711f1ef8d0374133d653690fcfea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allowed_values GoogleSecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#denied_values GoogleSecurityposturePosture#denied_values}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues(
            allowed_values=allowed_values, denied_values=denied_values
        )

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDenyAll")
    def reset_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyAll", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="denyAllInput")
    def deny_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "denyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dac88b3ce0466c5a95788d7e107908b436b6fad2407b78826af90cb0b18eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f097cbb3a96a4e6ae67e6409de3cf3ae7a6ad4167eea0b16cdb38589b621bfa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ba6cbd3eab9d4529f53baa2b8d4cda22b9386c6ae3d651e55b67159c631efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7647dce4a915cd61d7795b43c287ce1ded0b295da04c014a8f2840cebdbd933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allowed_values GoogleSecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#denied_values GoogleSecurityposturePosture#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c1ab8506e112e6593987fb3ec28a851f7fb1fcff985be4d6f9ca225247bf00)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument denied_values", value=denied_values, expected_type=type_hints["denied_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if denied_values is not None:
            self._values["denied_values"] = denied_values

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values allowed at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allowed_values GoogleSecurityposturePosture#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#denied_values GoogleSecurityposturePosture#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18521f120710b63ed480d8516cd79dbb85a3342756151f2eec2a81b161e868ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedValues")
    def reset_allowed_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedValues", []))

    @jsii.member(jsii_name="resetDeniedValues")
    def reset_denied_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedValues", []))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedValuesInput")
    def denied_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedValues"))

    @allowed_values.setter
    def allowed_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb49adb5c2b3d63c4bd5c69e411ac8abbf73c1a741f49e2f8a9b7ad077c4e40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad696d7c848076967929b9913eb8a866ba779b7ab61b4a6722b5f5125ce6c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf2d634deb00ccec21594fcddb4c06d753be42487ddc83f2eaecbf104093dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__765544f5479936ec663b6ffa92c501b3569d9313da33ec751d4f305bcc1914eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyRules")
    def put_policy_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc47084ce7fdd52b61073f863a4d40556965bc2288e8259526c069293d923b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyRules", [value]))

    @builtins.property
    @jsii.member(jsii_name="policyRules")
    def policy_rules(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList", jsii.get(self, "policyRules"))

    @builtins.property
    @jsii.member(jsii_name="cannedConstraintIdInput")
    def canned_constraint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedConstraintIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyRulesInput")
    def policy_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]]], jsii.get(self, "policyRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedConstraintId")
    def canned_constraint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedConstraintId"))

    @canned_constraint_id.setter
    def canned_constraint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f8b63141b655015ec9f6cfc73d07b6a450d9b0349d7853eb8a15988d762f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedConstraintId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069d2f3c416551e9fb8c4c8cb49ae1f542c838a847bf2b12dbb2fa2f5d7d6edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all": "allowAll",
        "condition": "condition",
        "deny_all": "denyAll",
        "enforce": "enforce",
        "values": "values",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        condition: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to true means that all values are allowed. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allow_all GoogleSecurityposturePosture#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        :param deny_all: Setting this to true means that all values are denied. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#deny_all GoogleSecurityposturePosture#deny_all}
        :param enforce: If 'true', then the policy is enforced. If 'false', then any configuration is acceptable. This field can be set only in policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#enforce GoogleSecurityposturePosture#enforce}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#values GoogleSecurityposturePosture#values}
        '''
        if isinstance(condition, dict):
            condition = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition(**condition)
        if isinstance(values, dict):
            values = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d418ce146be11f6c5c17ad1f980bdb72080e7e4e49d1fe6c75bf8212b60fe8cd)
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument deny_all", value=deny_all, expected_type=type_hints["deny_all"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if condition is not None:
            self._values["condition"] = condition
        if deny_all is not None:
            self._values["deny_all"] = deny_all
        if enforce is not None:
            self._values["enforce"] = enforce
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def allow_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are allowed.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allow_all GoogleSecurityposturePosture#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#condition GoogleSecurityposturePosture#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition"], result)

    @builtins.property
    def deny_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are denied.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#deny_all GoogleSecurityposturePosture#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', then the policy is enforced.

        If 'false', then any configuration is acceptable.
        This field can be set only in policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#enforce GoogleSecurityposturePosture#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#values GoogleSecurityposturePosture#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c008f565d0863fbfbdfa40a67116fbdb3b3882fbce0f232875929abb6b5af12d)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7211ea6f88193d2eecff1eebaf1b60fc26ecd174d48679ee71761878d9de236)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00040a6fc471bafa8dc6caccefd644c24eb369e184a76d71d65290e20af8c94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643e64cde3a843e56a4bda6a86e5f8e86d01203aa05e2a6bf29dab68c32c3da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fb15211567e5484fda8d74cda0e51cf8b1a7401a220408f809abcd1d6a92ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ffd92f3d2e5cbe49a5a47d7d85f2ca696f03e9860f9b15bad1e9d8e05ae293d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f2bb35fdec1fbb3f61225db09b0cc0f41c1c2b209f422849f674b4d1ec4c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae7e62c6075c96c662fdf306fcd9aa2374178a32549db93a00ca0e66929db41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2007be03d8e306263a8527759b90b52ea92c6fc94d4a7ddb1872b74dfe5775d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29acbc9e4ec33870e1051cc84bb772f95d9d94f9990ff6cc0b890bd609319df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e78f9deba8d376f772a9922f079c76b864366d5908ed3ba7e82790efc47240e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6128f14d0f98bb30662e90536dd3a568c81880610fd49f8b990e7aedd9efc01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f93f965370b3bdb27efa873812fcd2417cde77a5aaaa42bfc546bb9d6b527f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17eb47e2f726309b7de00e04cc4b7cf42be00b115c2b14f60472aa0c9422f49c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allowed_values GoogleSecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#denied_values GoogleSecurityposturePosture#denied_values}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues(
            allowed_values=allowed_values, denied_values=denied_values
        )

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDenyAll")
    def reset_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyAll", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="denyAllInput")
    def deny_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "denyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584f69a75444c5bb99b617903bdf78d5fc5a68b75bb1cb13395d09c09c537170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091644424de58ace14bf184606a411406553f1416b69491ff1f119943fe9827a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a99ce96bc5d560a66b1553d340843a9623a4d6f4056b0253917f7e06451882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5969766c576c83fd5e7c32b97f097cf94d389182a3ce2dcf9c799d784cb07c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allowed_values GoogleSecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#denied_values GoogleSecurityposturePosture#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08e62a464d491503e058568b3c0c574dd433b26e821c34d1b8fa64f3d1983dd)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument denied_values", value=denied_values, expected_type=type_hints["denied_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if denied_values is not None:
            self._values["denied_values"] = denied_values

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values allowed at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#allowed_values GoogleSecurityposturePosture#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#denied_values GoogleSecurityposturePosture#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3081efafe9cfd43d6857010a5c17ee9fd9796f525aa6313a1a3e352583b3862c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedValues")
    def reset_allowed_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedValues", []))

    @jsii.member(jsii_name="resetDeniedValues")
    def reset_denied_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedValues", []))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedValuesInput")
    def denied_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedValues"))

    @allowed_values.setter
    def allowed_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cde33c8cdeb5f5836bc2daaf0c91991fb83741f9521ecb48613ea9042d9e237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9abd9e70a6feb914a682d2a924835c9624629c2f90bdf004e74ceb4aacd591d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651ff3819c8d467668b3e1921120429544f077ff3fb2d44b918434eab4657221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e5497c42a48ff8b2721ad48ac832a742f49da79353f129f4bc452250671e101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOrgPolicyConstraint")
    def put_org_policy_constraint(
        self,
        *,
        canned_constraint_id: builtins.str,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param canned_constraint_id: Organization policy canned constraint Id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#canned_constraint_id GoogleSecurityposturePosture#canned_constraint_id}
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_rules GoogleSecurityposturePosture#policy_rules}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint(
            canned_constraint_id=canned_constraint_id, policy_rules=policy_rules
        )

        return typing.cast(None, jsii.invoke(self, "putOrgPolicyConstraint", [value]))

    @jsii.member(jsii_name="putOrgPolicyConstraintCustom")
    def put_org_policy_constraint_custom(
        self,
        *,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
        custom_constraint: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#policy_rules GoogleSecurityposturePosture#policy_rules}
        :param custom_constraint: custom_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#custom_constraint GoogleSecurityposturePosture#custom_constraint}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom(
            policy_rules=policy_rules, custom_constraint=custom_constraint
        )

        return typing.cast(None, jsii.invoke(self, "putOrgPolicyConstraintCustom", [value]))

    @jsii.member(jsii_name="putSecurityHealthAnalyticsCustomModule")
    def put_security_health_analytics_custom_module(
        self,
        *,
        config: typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: typing.Optional[builtins.str] = None,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#config GoogleSecurityposturePosture#config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#display_name GoogleSecurityposturePosture#display_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_enablement_state GoogleSecurityposturePosture#module_enablement_state}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule(
            config=config,
            display_name=display_name,
            module_enablement_state=module_enablement_state,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHealthAnalyticsCustomModule", [value]))

    @jsii.member(jsii_name="putSecurityHealthAnalyticsModule")
    def put_security_health_analytics_module(
        self,
        *,
        module_name: builtins.str,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module_name: The name of the module eg: BIGQUERY_TABLE_CMEK_DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_name GoogleSecurityposturePosture#module_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_enablement_state GoogleSecurityposturePosture#module_enablement_state}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule(
            module_name=module_name, module_enablement_state=module_enablement_state
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHealthAnalyticsModule", [value]))

    @jsii.member(jsii_name="resetOrgPolicyConstraint")
    def reset_org_policy_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgPolicyConstraint", []))

    @jsii.member(jsii_name="resetOrgPolicyConstraintCustom")
    def reset_org_policy_constraint_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgPolicyConstraintCustom", []))

    @jsii.member(jsii_name="resetSecurityHealthAnalyticsCustomModule")
    def reset_security_health_analytics_custom_module(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHealthAnalyticsCustomModule", []))

    @jsii.member(jsii_name="resetSecurityHealthAnalyticsModule")
    def reset_security_health_analytics_module(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHealthAnalyticsModule", []))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraint")
    def org_policy_constraint(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference, jsii.get(self, "orgPolicyConstraint"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraintCustom")
    def org_policy_constraint_custom(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference, jsii.get(self, "orgPolicyConstraintCustom"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsCustomModule")
    def security_health_analytics_custom_module(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference", jsii.get(self, "securityHealthAnalyticsCustomModule"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsModule")
    def security_health_analytics_module(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference", jsii.get(self, "securityHealthAnalyticsModule"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraintCustomInput")
    def org_policy_constraint_custom_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom], jsii.get(self, "orgPolicyConstraintCustomInput"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraintInput")
    def org_policy_constraint_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint], jsii.get(self, "orgPolicyConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsCustomModuleInput")
    def security_health_analytics_custom_module_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"], jsii.get(self, "securityHealthAnalyticsCustomModuleInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsModuleInput")
    def security_health_analytics_module_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"], jsii.get(self, "securityHealthAnalyticsModuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraint]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78875e340230d7bdf06bc1119ceb14075178057d95b34c2652f93b2d39f04cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "display_name": "displayName",
        "module_enablement_state": "moduleEnablementState",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule:
    def __init__(
        self,
        *,
        config: typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: typing.Optional[builtins.str] = None,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#config GoogleSecurityposturePosture#config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#display_name GoogleSecurityposturePosture#display_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_enablement_state GoogleSecurityposturePosture#module_enablement_state}
        '''
        if isinstance(config, dict):
            config = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b8ffcebbe3c9c8da585749fe4a95bc9225d49096b7694e522988c7a59a82c6)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument module_enablement_state", value=module_enablement_state, expected_type=type_hints["module_enablement_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if module_enablement_state is not None:
            self._values["module_enablement_state"] = module_enablement_state

    @builtins.property
    def config(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#config GoogleSecurityposturePosture#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig", result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Security Health Analytics custom module.

        This
        display name becomes the finding category for all findings that are
        returned by this custom module.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#display_name GoogleSecurityposturePosture#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_enablement_state(self) -> typing.Optional[builtins.str]:
        '''The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_enablement_state GoogleSecurityposturePosture#module_enablement_state}
        '''
        result = self._values.get("module_enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "predicate": "predicate",
        "resource_selector": "resourceSelector",
        "severity": "severity",
        "custom_output": "customOutput",
        "description": "description",
        "recommendation": "recommendation",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig:
    def __init__(
        self,
        *,
        predicate: typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        resource_selector: typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        recommendation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#predicate GoogleSecurityposturePosture#predicate}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_selector GoogleSecurityposturePosture#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["SEVERITY_UNSPECIFIED", "CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#severity GoogleSecurityposturePosture#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#custom_output GoogleSecurityposturePosture#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#recommendation GoogleSecurityposturePosture#recommendation}
        '''
        if isinstance(predicate, dict):
            predicate = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate(**predicate)
        if isinstance(resource_selector, dict):
            resource_selector = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector(**resource_selector)
        if isinstance(custom_output, dict):
            custom_output = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput(**custom_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef874cacd33ed1d749e05591c60c1966429ed6877d6b57bf7f109330c5cde27)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument resource_selector", value=resource_selector, expected_type=type_hints["resource_selector"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument custom_output", value=custom_output, expected_type=type_hints["custom_output"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "predicate": predicate,
            "resource_selector": resource_selector,
            "severity": severity,
        }
        if custom_output is not None:
            self._values["custom_output"] = custom_output
        if description is not None:
            self._values["description"] = description
        if recommendation is not None:
            self._values["recommendation"] = recommendation

    @builtins.property
    def predicate(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate":
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#predicate GoogleSecurityposturePosture#predicate}
        '''
        result = self._values.get("predicate")
        assert result is not None, "Required property 'predicate' is missing"
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate", result)

    @builtins.property
    def resource_selector(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector":
        '''resource_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_selector GoogleSecurityposturePosture#resource_selector}
        '''
        result = self._values.get("resource_selector")
        assert result is not None, "Required property 'resource_selector' is missing"
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector", result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''The severity to assign to findings generated by the module. Possible values: ["SEVERITY_UNSPECIFIED", "CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#severity GoogleSecurityposturePosture#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_output(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput"]:
        '''custom_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#custom_output GoogleSecurityposturePosture#custom_output}
        '''
        result = self._values.get("custom_output")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text that describes the vulnerability or misconfiguration that the custom module detects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recommendation(self) -> typing.Optional[builtins.str]:
        '''An explanation of the recommended steps that security teams can take to resolve the detected issue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#recommendation GoogleSecurityposturePosture#recommendation}
        '''
        result = self._values.get("recommendation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties"},
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput:
    def __init__(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#properties GoogleSecurityposturePosture#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b8ed7496afd1796724d9341ebb109f63bc951d828cd39531c52da97f90bd5b)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#properties GoogleSecurityposturePosture#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c489948193a428da8151cb668878a9396a551cd5482a9c41b660df1f2587042b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827279d6ec8bdcbf9ef6ae82bf84bd7abcc3a05f72553e5a283bb85d1a437335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce844984c434a3edade87326db2f17f16b63b48dc68f053986bf1fbb0a181a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value_expression": "valueExpression"},
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties:
    def __init__(
        self,
        *,
        name: builtins.str,
        value_expression: typing.Optional[typing.Union["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the property for the custom output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#name GoogleSecurityposturePosture#name}
        :param value_expression: value_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#value_expression GoogleSecurityposturePosture#value_expression}
        '''
        if isinstance(value_expression, dict):
            value_expression = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression(**value_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e14ad51cc7eea36cb6fa0862afad2b04dc70a7a5b26143ac9ed354c9abe3052)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value_expression", value=value_expression, expected_type=type_hints["value_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value_expression is not None:
            self._values["value_expression"] = value_expression

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the property for the custom output.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#name GoogleSecurityposturePosture#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_expression(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"]:
        '''value_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#value_expression GoogleSecurityposturePosture#value_expression}
        '''
        result = self._values.get("value_expression")
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a024506444b2b8fe376963fd6de7b6e3462243a3c64b90255068e96bc1d18b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63ea8b7877fa40f9db9370534928c28e0117c00c137466fbda92c71b7a9a987)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0cc5478cbd863efdb0e8d7ad2eaaa87f5ad24bbdfe41692e752a46c7cf13efb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__535901339fb690b6cdb9f2228e44d1b2af5cc5121f0d09544a142534cf7432d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff552ab804c9fed0a9f2c7ff6ec8b51f62b8e2b9d2772129f369d051b9514b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855eca14031c626a60452354f5537ec3cf5bf2a087af9911370aba20c3b926fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48791fb7241e8948c48d955810e467a9cb8d4bd4fff3e6e3e37f4cce226721ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueExpression")
    def put_value_expression(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putValueExpression", [value]))

    @jsii.member(jsii_name="resetValueExpression")
    def reset_value_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueExpression", []))

    @builtins.property
    @jsii.member(jsii_name="valueExpression")
    def value_expression(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference", jsii.get(self, "valueExpression"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExpressionInput")
    def value_expression_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"], jsii.get(self, "valueExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c8bcb20ef3e0d2424cf3a79e4a724a962e3697a79bd4cc89387a14992cf691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83d5f9d12c6a42f30c94687d270f68fae3cd6d93e7800ae071e369e44025f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1739fa9fc03abc10c4973b31977dbd321518cc0abc4282ee06460bbf452de357)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b872d7ab38052f8433486c0c4db83b4383c0f843ed24023033939d82c0b6b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476893bb5cfb99f4d136b93e056f72eba321a52d7a3b9bb720d8916dc5030c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84a14234845e2f1cd57ef944a7784747814eb3ef5078e15e6e3d418ce2b2116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0c45d785257f377f1c88df7109923d93c3df0736e6e1227f135d44165dea7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aeb55b38d6efdd59cda80d9cf189c61d0d1b53699e19320e0889153a5061f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2099306967021d4349e8b1e90a8e5e0cce2d00ca5f0b9c30fbdc758ca7aa641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7b480a92831fb336c8c5cb2d516e8cc5e2ddd7d17a2b02d1acc9cdd27c6ed12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomOutput")
    def put_custom_output(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#properties GoogleSecurityposturePosture#properties}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput(
            properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomOutput", [value]))

    @jsii.member(jsii_name="putPredicate")
    def put_predicate(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putPredicate", [value]))

    @jsii.member(jsii_name="putResourceSelector")
    def put_resource_selector(
        self,
        *,
        resource_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_types GoogleSecurityposturePosture#resource_types}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector(
            resource_types=resource_types
        )

        return typing.cast(None, jsii.invoke(self, "putResourceSelector", [value]))

    @jsii.member(jsii_name="resetCustomOutput")
    def reset_custom_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOutput", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRecommendation")
    def reset_recommendation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendation", []))

    @builtins.property
    @jsii.member(jsii_name="customOutput")
    def custom_output(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference, jsii.get(self, "customOutput"))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelector")
    def resource_selector(
        self,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference":
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference", jsii.get(self, "resourceSelector"))

    @builtins.property
    @jsii.member(jsii_name="customOutputInput")
    def custom_output_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput], jsii.get(self, "customOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate"], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationInput")
    def recommendation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelectorInput")
    def resource_selector_input(
        self,
    ) -> typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector"]:
        return typing.cast(typing.Optional["GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector"], jsii.get(self, "resourceSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c89ffcdfcfc58f71a46fc3cb420f500ba1a5dde9ed0f81ecab85dc6b39de2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @recommendation.setter
    def recommendation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657beadc484ed038f667e84630047e8743c7b263fafb44e834d667f41bc6c002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8743424e6a6c5bf4211e82dcd9084e45763d194fdc24568d14aa05a054d186d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e502be6a643180ff60ac8236f12d4c212cf72305e39fccc3b9007cc7a6486fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1a002c97c1354d373d047f517e3ad30c7252203ac28f3cc4b8ec6e7c9216b6)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#expression GoogleSecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#location GoogleSecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#title GoogleSecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08ac166ea3c6b7950eb0dedd6e68852fcd3126e679c72c1d26b268f42afc64eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81c6c754713253ca59a15c31669ad6437e198cdf006256fd030c33a7c209347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c278aafc02e7856be5c13223c24e19220581208ca98cf7c00f9f16a0a399e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747aeda6d0b702398b4807f9bb9aa1cfcd93502b901df93ca298b1cd3b6042df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ba787007a8ca4849af8899682921335b8275f62ced4dd3244f427da4bb91c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea7eddcc0e1e4220de4eff61df204e205e9e896355cb855a7a8b9050094df2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector:
    def __init__(self, *, resource_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_types GoogleSecurityposturePosture#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2d92c34554046907433f2ad9428b37ae1694d41e2b1573cca85a2431539890)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_types": resource_types,
        }

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''The resource types to run the detector on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_types GoogleSecurityposturePosture#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e17f9b3c3322172d0010cbd288949de8046033bcce722f2f6b5549d3336cfb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46986435ffe43ee584272d65894ca2b80e72fae40ffd2847c91691724ad56bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1fc504b0bcd5697c0bc1adab4fe8b96247a0641b5c606286a0529fa973ee66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6802e0094a8e49d33d1242798cb68d246f7c19a294f75ea02b7577f54a1d1acf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        predicate: typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate, typing.Dict[builtins.str, typing.Any]],
        resource_selector: typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        recommendation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#predicate GoogleSecurityposturePosture#predicate}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#resource_selector GoogleSecurityposturePosture#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["SEVERITY_UNSPECIFIED", "CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#severity GoogleSecurityposturePosture#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#custom_output GoogleSecurityposturePosture#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#description GoogleSecurityposturePosture#description}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#recommendation GoogleSecurityposturePosture#recommendation}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig(
            predicate=predicate,
            resource_selector=resource_selector,
            severity=severity,
            custom_output=custom_output,
            description=description,
            recommendation=recommendation,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetModuleEnablementState")
    def reset_module_enablement_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModuleEnablementState", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementStateInput")
    def module_enablement_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleEnablementStateInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5cac15f1e551ef0bcb6ff7c7f6cbd968482503f9bd1e454aad599f37381644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementState")
    def module_enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleEnablementState"))

    @module_enablement_state.setter
    def module_enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f5c0dcdaca9287f27e2e438e7d1faa5a502690c1f1145c817db8d689869948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleEnablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b071abc01114b52db7c15d8293a567c92f98127b09319864ee4879c5552e2c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule",
    jsii_struct_bases=[],
    name_mapping={
        "module_name": "moduleName",
        "module_enablement_state": "moduleEnablementState",
    },
)
class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule:
    def __init__(
        self,
        *,
        module_name: builtins.str,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module_name: The name of the module eg: BIGQUERY_TABLE_CMEK_DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_name GoogleSecurityposturePosture#module_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_enablement_state GoogleSecurityposturePosture#module_enablement_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10be9c52f3fc1fb596869c3d06a0596a6c84228f24b9ae2791d70135fbab77e1)
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument module_enablement_state", value=module_enablement_state, expected_type=type_hints["module_enablement_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module_name": module_name,
        }
        if module_enablement_state is not None:
            self._values["module_enablement_state"] = module_enablement_state

    @builtins.property
    def module_name(self) -> builtins.str:
        '''The name of the module eg: BIGQUERY_TABLE_CMEK_DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_name GoogleSecurityposturePosture#module_name}
        '''
        result = self._values.get("module_name")
        assert result is not None, "Required property 'module_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def module_enablement_state(self) -> typing.Optional[builtins.str]:
        '''The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#module_enablement_state GoogleSecurityposturePosture#module_enablement_state}
        '''
        result = self._values.get("module_enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f144146a814b4a629785751e4e934b8c1000771caf5455aa4587ef0e4c0208e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModuleEnablementState")
    def reset_module_enablement_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModuleEnablementState", []))

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementStateInput")
    def module_enablement_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleEnablementStateInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleNameInput")
    def module_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementState")
    def module_enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleEnablementState"))

    @module_enablement_state.setter
    def module_enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfe51309945e9211961a9c200a9b5ed1ba1e132a564fcb7646d6ebcd75c1205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleEnablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="moduleName")
    def module_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleName"))

    @module_name.setter
    def module_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2cb3863b0b1024f7bc930c1b418c80d8aaa3b02dc3793d15b0efd52a7411949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d192edb061f4f527b32d839010997f922be8a4fd7d7f9c7e78e960a7af8abefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__226720b4bf6f90b0c4f8328b9abd6c22b1bdc6d8dc5ee87f6841ca50a45bc74a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecurityposturePosturePolicySetsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f80a9d04498ba7ebbafcc83974878cef2275093e48749ce3148c3ae4ec8c41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecurityposturePosturePolicySetsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0f4fe5a5fdf7f03a41674cdab8d9c8a2e603fb7be3d7fdee1067825ab109cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d8e1bb2d669867e597f7b66d2cba011cebf5d8d29c9d166bf5998e25cab79d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c26960d14d295b62a44f1f01d2bb53ea4ab2b8d9fd880d16a451665fe5f5a1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243b3d35a7d1e91d53aed7352efde3736197f5feff54e4c78797b70057c9293f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecurityposturePosturePolicySetsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePosturePolicySetsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1563daff05647b0b00b976ed7b66032bdb8abb7b55ce23dd0f01f202973bc081)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putComplianceStandards")
    def put_compliance_standards(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61792e6f863c383772e7a948f1ad0de14781087af326af5a293cbeda97cee274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComplianceStandards", [value]))

    @jsii.member(jsii_name="putConstraint")
    def put_constraint(
        self,
        *,
        org_policy_constraint: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
        org_policy_constraint_custom: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom, typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_custom_module: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule, typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_module: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param org_policy_constraint: org_policy_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#org_policy_constraint GoogleSecurityposturePosture#org_policy_constraint}
        :param org_policy_constraint_custom: org_policy_constraint_custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#org_policy_constraint_custom GoogleSecurityposturePosture#org_policy_constraint_custom}
        :param security_health_analytics_custom_module: security_health_analytics_custom_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#security_health_analytics_custom_module GoogleSecurityposturePosture#security_health_analytics_custom_module}
        :param security_health_analytics_module: security_health_analytics_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#security_health_analytics_module GoogleSecurityposturePosture#security_health_analytics_module}
        '''
        value = GoogleSecurityposturePosturePolicySetsPoliciesConstraint(
            org_policy_constraint=org_policy_constraint,
            org_policy_constraint_custom=org_policy_constraint_custom,
            security_health_analytics_custom_module=security_health_analytics_custom_module,
            security_health_analytics_module=security_health_analytics_module,
        )

        return typing.cast(None, jsii.invoke(self, "putConstraint", [value]))

    @jsii.member(jsii_name="resetComplianceStandards")
    def reset_compliance_standards(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceStandards", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="complianceStandards")
    def compliance_standards(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsList:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsList, jsii.get(self, "complianceStandards"))

    @builtins.property
    @jsii.member(jsii_name="constraint")
    def constraint(
        self,
    ) -> GoogleSecurityposturePosturePolicySetsPoliciesConstraintOutputReference:
        return typing.cast(GoogleSecurityposturePosturePolicySetsPoliciesConstraintOutputReference, jsii.get(self, "constraint"))

    @builtins.property
    @jsii.member(jsii_name="complianceStandardsInput")
    def compliance_standards_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]], jsii.get(self, "complianceStandardsInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintInput")
    def constraint_input(
        self,
    ) -> typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraint]:
        return typing.cast(typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraint], jsii.get(self, "constraintInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86842fdeb2534ed465d277060201cf18b1ab18ad4baeab8ee2e61ff22ac2e56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0ff8fdc6925e3db332c40ca337b4d29afb1c34f50e165f903a0fc5b4fbc37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8d43ba4614b2985bc55a991422ace84d880111eeea6a35d11fa79b8119ccf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePostureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleSecurityposturePostureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#create GoogleSecurityposturePosture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#delete GoogleSecurityposturePosture#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#update GoogleSecurityposturePosture#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89271ed40d094a12b0d91a8a5170da2833de2d1d343199705194fd502794c36b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#create GoogleSecurityposturePosture#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#delete GoogleSecurityposturePosture#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_securityposture_posture#update GoogleSecurityposturePosture#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecurityposturePostureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecurityposturePostureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecurityposturePosture.GoogleSecurityposturePostureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__668906c4b03091769db0af0b4a9347d3eeed27e382b4ea65b9b491c7237115cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dbba46cfe5cec86be0fbaef8a0aa28976c4cada4263d334373209d533c44dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc397bbc81c5a93df3b5d16eea2f6e2f3dbb6614df912a94772813f830a31fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e60c1dec8f16af0d77d71587e6392459dd5ae865342515a9f93702a1651434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePostureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePostureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePostureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e45ffb3c3c19c4b1fd511c85e02d903d41f99bb530bf76cb4f21f3c78479e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleSecurityposturePosture",
    "GoogleSecurityposturePostureConfig",
    "GoogleSecurityposturePosturePolicySets",
    "GoogleSecurityposturePosturePolicySetsList",
    "GoogleSecurityposturePosturePolicySetsOutputReference",
    "GoogleSecurityposturePosturePolicySetsPolicies",
    "GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards",
    "GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsList",
    "GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraint",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule",
    "GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference",
    "GoogleSecurityposturePosturePolicySetsPoliciesList",
    "GoogleSecurityposturePosturePolicySetsPoliciesOutputReference",
    "GoogleSecurityposturePostureTimeouts",
    "GoogleSecurityposturePostureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f8314ed92697ebe0ec8be34793f564cccdd010630daa59e288adce19ad2bb691(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    parent: builtins.str,
    policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySets, typing.Dict[builtins.str, typing.Any]]]],
    posture_id: builtins.str,
    state: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleSecurityposturePostureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__272ca6b3922feac754e8aa6dae5910480a4497c608d53c7d9bf54633bb797039(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0194bda7fb19e072b6a48d4d9d9a5c1abb4d9e0e8ddd9e9ac7a182f34d0c5b68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fca1d25301df521021b0b0c848164f257cfe361f40d5c65edc10efba6e0b986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f0697fd380603247c7e9ce119e120419ab7b62a9a906c70bd8cd49cf54cad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f010e212e86a3115e2921437ad671a52d9493054be51fb9e8c73a819440e4b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c288da0f86501a38725f9610338c6e67116a1d3b9690d51ccc171cda5f3c2046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3abeecd6f0f7f69c8beec727e5f9e6fc5737ca3dafdd095b4488be37347684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32300c893c243c19cec9a78f6fade84efb47785050fc5216c493b32e472f2975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200fd19f34419dd89eb64010336ccb464b81485387c69556f54283ac2de85220(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    parent: builtins.str,
    policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySets, typing.Dict[builtins.str, typing.Any]]]],
    posture_id: builtins.str,
    state: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleSecurityposturePostureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f862ec37772db2efa107ace92c65d56069611259a0b73dd2253760bc191e1fc(
    *,
    policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    policy_set_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c93721cbdaa35cc270fc578e6c243992bfdc39cf30fea281e2e7d7bf81bef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1e9f1ef1ce5b2c9bb44c6c7f05fc38659a5dcdb4303f1540adffd68e335895(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aec57c5cc8732f3ae793b6d568f88787f3cb3f98fe94823ce7a64a908779967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693cfd72968ac9bcbb1c55bd860e6be99768893465353e727150c51dda09cc7b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd871189e482fd0c37295c68b77e7776968e09375554063736ee6da471e8273(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a688b3d42550bf06901721c9c24a3b9bf65e1900ee10a3edb7f09b83a90fcad9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc364bd069abb11160b378739e1b31c96deaab0286b7ed2d6582215c7ab0bb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7867cdd7038fdbf7d01491b41d2be404e0729d3802d6d1cdc40abe54c2e346(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6dae5a184ffb4f912473c1a75d09861bfadafe53ad809ef5681e0c27b80ee9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d814f7167d482cb54fdb731ed2897b0aa33c54474ecaa53e146841203be749a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517b00422a94e854cc89bf753d5b1a7934c30c0dfde83f0a61c646a6e915745d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f479da3059ac31beb63dbc10c1631226f470ce75acfc000e93f5aa1003e5e0b4(
    *,
    constraint: typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraint, typing.Dict[builtins.str, typing.Any]],
    policy_id: builtins.str,
    compliance_standards: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b6d18e852abf4ef59d11fe25b392e8087df61370fedec8026dea99047240e9(
    *,
    control: typing.Optional[builtins.str] = None,
    standard: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d35f348e4b207e6e5cbcd2b73ddff47cb745a6b70ff4786e552b1a53df3f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8344a8ddad8bb7422a0529c8d0d9773595cbb0cf30f15b05f9b2d331d885cfe2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5b3728d392998591771126e1515c509f1a1663c701c1126122e7736d96ab88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87752946e43e2a81fb22533377046dcf6d8f09004289acc6073dea5dca6cdd78(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76ddb7c9b61526a866d8cd768e15755e65b76cbee3e698af8877d2f826277b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bb97f0ea947aefa66d5869b22b9fceb9bed2cf7179bc05697b23a886373648(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0543e784385358022109ebedfdb8583cfe3b64a9c422ddad204609bd755bf66e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9282fe50c374d42ba2450a0be1bc41f9eb1e25880cc8f487a5a91019edba5c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74d35b7c03277f6af2849c301c3e9c2d299ce967d6f057b9f9968c1bba14041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26ff376bd8c9c6fcf5d992022a94da51454f2e7d11f207aec85607370d2326a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b666e607b8c89cc0c186a30fc79a9ffc23901dd6de15dbc397ad78b106541c(
    *,
    org_policy_constraint: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
    org_policy_constraint_custom: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    security_health_analytics_custom_module: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule, typing.Dict[builtins.str, typing.Any]]] = None,
    security_health_analytics_module: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22aef8fb11c877a1f3cad8906b4009e907dbb19f18bc756c9f962e4fe3355b4(
    *,
    canned_constraint_id: builtins.str,
    policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b764a517cd3c1441e76aed5a5bfb28fddbdda46545c2f5d350504d1038f2a5(
    *,
    policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    custom_constraint: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4aaeacbdc3bc282fa84a151e8a96de77a0372f8df7b94926243148f620f618(
    *,
    action_type: builtins.str,
    condition: builtins.str,
    method_types: typing.Sequence[builtins.str],
    name: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5cb9958a98ad16f9e02111ba58859143f083fa0ed3a17a614e9278aba17c75d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311b1a7cbf41d0f2f4bdb66b6e210bb7c51bf646e884f05a81053623a68f7abd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f5becdba05659c69856b3e57eb4779b8260ac8b1e40aaba38ac3d02a86b22d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c8cc7e0fd4eaf3ef59f59737528882efc33f0360fa00c1e6311d78a699468b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35657f08b5206450a5e14786b3df30e0879e43034cdb61601876feb8f71dc8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419a4f711d970c4a54db947a6fad86d8b92a1371e392b948d4d46c0819f7c212(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69fe69b27eac7e8171a489260e9cd6e84a8acab42e678fe43861fcb8e225a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b12b0d197ff10f10be9b3539e76753274eb9053042bb12b22bb6ec49124af4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959896430eabae5a3a9879a3f4a250f42f099b4dbc54f28b100b3908a53e4927(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d860dd5f84cdca209e1d8a734a58252a1371c9bb375a924a12c4f9affcba087c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff318d0d3d38bf0aff42437260d560221c18f71c66a63239b2d27f5020ed01a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fc3f3a37914890eb3e3ec42802d09208f7ecda2e6c5ccf5776ab2e1d72d508(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed8e92edb5bf04d51ab2f69f67c23c6db9148182c13734011fa65d6cfe078c1(
    *,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    condition: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bdaae01616505e9af562d2390dec48f860d8830f5687d69df5e071dbb16376(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c66e239f57fe087b8e85eb43543dcfc4fcb859d34b6831591f4520aec7a33c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc73f2adc2ff39365eeb3c49a929c0f9980eda1250ff78ca438973804662c4d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2b8251093933f5383ef82ce368c91b0a06d1b960cf0618addfd6ec36db2679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795a80def983f0c1e93dfa410efc7b5159afc353228f1d0b7342ddd1faf3292f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbe4996c85844e4a357c7e00b1296b543d22cc2fa471f0cf98552820ea067d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2198e8d268a5ff66f202dbf6607e87da81fed9047c69572c7ffe9429712807e(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac95059868d971dff56ba1bf5c34ab5dc5c8e9d004c6d2ecd5e94c72e0a28d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25df980c211f28db5ae4915d5a7a5e6a5ea97b8f34b9dbc0923de2b8bdfe20c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df8df573643d9c3cf748b312453c6f233a11457e2cdb0ca09306e2bbd87681c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d472445a1f6b0cabdb30a78112ce6535c173135327438cd5dcb5e53594e3b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9734a80fdd1ab8cc9808af7c7e440093884647ceea5693e3ee12b59bb9bc79c9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97cc5bcace00a426451fdc5973aaffcd1bf13013f36a717a313ec8b57c31528(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670e91de115990a6fd2ed2a38f06d88feba2711f1ef8d0374133d653690fcfea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dac88b3ce0466c5a95788d7e107908b436b6fad2407b78826af90cb0b18eaf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f097cbb3a96a4e6ae67e6409de3cf3ae7a6ad4167eea0b16cdb38589b621bfa1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ba6cbd3eab9d4529f53baa2b8d4cda22b9386c6ae3d651e55b67159c631efa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7647dce4a915cd61d7795b43c287ce1ded0b295da04c014a8f2840cebdbd933(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c1ab8506e112e6593987fb3ec28a851f7fb1fcff985be4d6f9ca225247bf00(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18521f120710b63ed480d8516cd79dbb85a3342756151f2eec2a81b161e868ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb49adb5c2b3d63c4bd5c69e411ac8abbf73c1a741f49e2f8a9b7ad077c4e40f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad696d7c848076967929b9913eb8a866ba779b7ab61b4a6722b5f5125ce6c05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf2d634deb00ccec21594fcddb4c06d753be42487ddc83f2eaecbf104093dc3(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765544f5479936ec663b6ffa92c501b3569d9313da33ec751d4f305bcc1914eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc47084ce7fdd52b61073f863a4d40556965bc2288e8259526c069293d923b80(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f8b63141b655015ec9f6cfc73d07b6a450d9b0349d7853eb8a15988d762f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069d2f3c416551e9fb8c4c8cb49ae1f542c838a847bf2b12dbb2fa2f5d7d6edc(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d418ce146be11f6c5c17ad1f980bdb72080e7e4e49d1fe6c75bf8212b60fe8cd(
    *,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    condition: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c008f565d0863fbfbdfa40a67116fbdb3b3882fbce0f232875929abb6b5af12d(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7211ea6f88193d2eecff1eebaf1b60fc26ecd174d48679ee71761878d9de236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00040a6fc471bafa8dc6caccefd644c24eb369e184a76d71d65290e20af8c94a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643e64cde3a843e56a4bda6a86e5f8e86d01203aa05e2a6bf29dab68c32c3da1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fb15211567e5484fda8d74cda0e51cf8b1a7401a220408f809abcd1d6a92ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffd92f3d2e5cbe49a5a47d7d85f2ca696f03e9860f9b15bad1e9d8e05ae293d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f2bb35fdec1fbb3f61225db09b0cc0f41c1c2b209f422849f674b4d1ec4c5a(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae7e62c6075c96c662fdf306fcd9aa2374178a32549db93a00ca0e66929db41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2007be03d8e306263a8527759b90b52ea92c6fc94d4a7ddb1872b74dfe5775d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29acbc9e4ec33870e1051cc84bb772f95d9d94f9990ff6cc0b890bd609319df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e78f9deba8d376f772a9922f079c76b864366d5908ed3ba7e82790efc47240e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6128f14d0f98bb30662e90536dd3a568c81880610fd49f8b990e7aedd9efc01a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f93f965370b3bdb27efa873812fcd2417cde77a5aaaa42bfc546bb9d6b527f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17eb47e2f726309b7de00e04cc4b7cf42be00b115c2b14f60472aa0c9422f49c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584f69a75444c5bb99b617903bdf78d5fc5a68b75bb1cb13395d09c09c537170(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091644424de58ace14bf184606a411406553f1416b69491ff1f119943fe9827a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a99ce96bc5d560a66b1553d340843a9623a4d6f4056b0253917f7e06451882(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5969766c576c83fd5e7c32b97f097cf94d389182a3ce2dcf9c799d784cb07c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08e62a464d491503e058568b3c0c574dd433b26e821c34d1b8fa64f3d1983dd(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3081efafe9cfd43d6857010a5c17ee9fd9796f525aa6313a1a3e352583b3862c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cde33c8cdeb5f5836bc2daaf0c91991fb83741f9521ecb48613ea9042d9e237(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9abd9e70a6feb914a682d2a924835c9624629c2f90bdf004e74ceb4aacd591d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651ff3819c8d467668b3e1921120429544f077ff3fb2d44b918434eab4657221(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5497c42a48ff8b2721ad48ac832a742f49da79353f129f4bc452250671e101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78875e340230d7bdf06bc1119ceb14075178057d95b34c2652f93b2d39f04cc4(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b8ffcebbe3c9c8da585749fe4a95bc9225d49096b7694e522988c7a59a82c6(
    *,
    config: typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig, typing.Dict[builtins.str, typing.Any]],
    display_name: typing.Optional[builtins.str] = None,
    module_enablement_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef874cacd33ed1d749e05591c60c1966429ed6877d6b57bf7f109330c5cde27(
    *,
    predicate: typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate, typing.Dict[builtins.str, typing.Any]],
    resource_selector: typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
    severity: builtins.str,
    custom_output: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    recommendation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b8ed7496afd1796724d9341ebb109f63bc951d828cd39531c52da97f90bd5b(
    *,
    properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c489948193a428da8151cb668878a9396a551cd5482a9c41b660df1f2587042b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827279d6ec8bdcbf9ef6ae82bf84bd7abcc3a05f72553e5a283bb85d1a437335(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce844984c434a3edade87326db2f17f16b63b48dc68f053986bf1fbb0a181a5(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e14ad51cc7eea36cb6fa0862afad2b04dc70a7a5b26143ac9ed354c9abe3052(
    *,
    name: builtins.str,
    value_expression: typing.Optional[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a024506444b2b8fe376963fd6de7b6e3462243a3c64b90255068e96bc1d18b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63ea8b7877fa40f9db9370534928c28e0117c00c137466fbda92c71b7a9a987(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0cc5478cbd863efdb0e8d7ad2eaaa87f5ad24bbdfe41692e752a46c7cf13efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535901339fb690b6cdb9f2228e44d1b2af5cc5121f0d09544a142534cf7432d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff552ab804c9fed0a9f2c7ff6ec8b51f62b8e2b9d2772129f369d051b9514b94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855eca14031c626a60452354f5537ec3cf5bf2a087af9911370aba20c3b926fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48791fb7241e8948c48d955810e467a9cb8d4bd4fff3e6e3e37f4cce226721ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c8bcb20ef3e0d2424cf3a79e4a724a962e3697a79bd4cc89387a14992cf691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83d5f9d12c6a42f30c94687d270f68fae3cd6d93e7800ae071e369e44025f0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1739fa9fc03abc10c4973b31977dbd321518cc0abc4282ee06460bbf452de357(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b872d7ab38052f8433486c0c4db83b4383c0f843ed24023033939d82c0b6b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476893bb5cfb99f4d136b93e056f72eba321a52d7a3b9bb720d8916dc5030c3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84a14234845e2f1cd57ef944a7784747814eb3ef5078e15e6e3d418ce2b2116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0c45d785257f377f1c88df7109923d93c3df0736e6e1227f135d44165dea7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeb55b38d6efdd59cda80d9cf189c61d0d1b53699e19320e0889153a5061f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2099306967021d4349e8b1e90a8e5e0cce2d00ca5f0b9c30fbdc758ca7aa641(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b480a92831fb336c8c5cb2d516e8cc5e2ddd7d17a2b02d1acc9cdd27c6ed12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c89ffcdfcfc58f71a46fc3cb420f500ba1a5dde9ed0f81ecab85dc6b39de2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657beadc484ed038f667e84630047e8743c7b263fafb44e834d667f41bc6c002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8743424e6a6c5bf4211e82dcd9084e45763d194fdc24568d14aa05a054d186d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e502be6a643180ff60ac8236f12d4c212cf72305e39fccc3b9007cc7a6486fdf(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1a002c97c1354d373d047f517e3ad30c7252203ac28f3cc4b8ec6e7c9216b6(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ac166ea3c6b7950eb0dedd6e68852fcd3126e679c72c1d26b268f42afc64eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81c6c754713253ca59a15c31669ad6437e198cdf006256fd030c33a7c209347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c278aafc02e7856be5c13223c24e19220581208ca98cf7c00f9f16a0a399e5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747aeda6d0b702398b4807f9bb9aa1cfcd93502b901df93ca298b1cd3b6042df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ba787007a8ca4849af8899682921335b8275f62ced4dd3244f427da4bb91c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea7eddcc0e1e4220de4eff61df204e205e9e896355cb855a7a8b9050094df2c(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2d92c34554046907433f2ad9428b37ae1694d41e2b1573cca85a2431539890(
    *,
    resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e17f9b3c3322172d0010cbd288949de8046033bcce722f2f6b5549d3336cfb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46986435ffe43ee584272d65894ca2b80e72fae40ffd2847c91691724ad56bb0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1fc504b0bcd5697c0bc1adab4fe8b96247a0641b5c606286a0529fa973ee66(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6802e0094a8e49d33d1242798cb68d246f7c19a294f75ea02b7577f54a1d1acf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5cac15f1e551ef0bcb6ff7c7f6cbd968482503f9bd1e454aad599f37381644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f5c0dcdaca9287f27e2e438e7d1faa5a502690c1f1145c817db8d689869948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b071abc01114b52db7c15d8293a567c92f98127b09319864ee4879c5552e2c0a(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10be9c52f3fc1fb596869c3d06a0596a6c84228f24b9ae2791d70135fbab77e1(
    *,
    module_name: builtins.str,
    module_enablement_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f144146a814b4a629785751e4e934b8c1000771caf5455aa4587ef0e4c0208e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfe51309945e9211961a9c200a9b5ed1ba1e132a564fcb7646d6ebcd75c1205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cb3863b0b1024f7bc930c1b418c80d8aaa3b02dc3793d15b0efd52a7411949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d192edb061f4f527b32d839010997f922be8a4fd7d7f9c7e78e960a7af8abefb(
    value: typing.Optional[GoogleSecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226720b4bf6f90b0c4f8328b9abd6c22b1bdc6d8dc5ee87f6841ca50a45bc74a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f80a9d04498ba7ebbafcc83974878cef2275093e48749ce3148c3ae4ec8c41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0f4fe5a5fdf7f03a41674cdab8d9c8a2e603fb7be3d7fdee1067825ab109cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8e1bb2d669867e597f7b66d2cba011cebf5d8d29c9d166bf5998e25cab79d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26960d14d295b62a44f1f01d2bb53ea4ab2b8d9fd880d16a451665fe5f5a1b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243b3d35a7d1e91d53aed7352efde3736197f5feff54e4c78797b70057c9293f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecurityposturePosturePolicySetsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1563daff05647b0b00b976ed7b66032bdb8abb7b55ce23dd0f01f202973bc081(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61792e6f863c383772e7a948f1ad0de14781087af326af5a293cbeda97cee274(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecurityposturePosturePolicySetsPoliciesComplianceStandards, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86842fdeb2534ed465d277060201cf18b1ab18ad4baeab8ee2e61ff22ac2e56d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0ff8fdc6925e3db332c40ca337b4d29afb1c34f50e165f903a0fc5b4fbc37b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8d43ba4614b2985bc55a991422ace84d880111eeea6a35d11fa79b8119ccf9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePosturePolicySetsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89271ed40d094a12b0d91a8a5170da2833de2d1d343199705194fd502794c36b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668906c4b03091769db0af0b4a9347d3eeed27e382b4ea65b9b491c7237115cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbba46cfe5cec86be0fbaef8a0aa28976c4cada4263d334373209d533c44dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc397bbc81c5a93df3b5d16eea2f6e2f3dbb6614df912a94772813f830a31fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e60c1dec8f16af0d77d71587e6392459dd5ae865342515a9f93702a1651434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e45ffb3c3c19c4b1fd511c85e02d903d41f99bb530bf76cb4f21f3c78479e0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecurityposturePostureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
