r'''
# `opentelekomcloud_rms_policy_assignment_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_rms_policy_assignment_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1).
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


class RmsPolicyAssignmentV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1 opentelekomcloud_rms_policy_assignment_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        custom_policy: typing.Optional[typing.Union["RmsPolicyAssignmentV1CustomPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        period: typing.Optional[builtins.str] = None,
        policy_definition_id: typing.Optional[builtins.str] = None,
        policy_filter: typing.Optional[typing.Union["RmsPolicyAssignmentV1PolicyFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["RmsPolicyAssignmentV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1 opentelekomcloud_rms_policy_assignment_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#name RmsPolicyAssignmentV1#name}.
        :param custom_policy: custom_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#custom_policy RmsPolicyAssignmentV1#custom_policy}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#description RmsPolicyAssignmentV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#id RmsPolicyAssignmentV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#parameters RmsPolicyAssignmentV1#parameters}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#period RmsPolicyAssignmentV1#period}.
        :param policy_definition_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#policy_definition_id RmsPolicyAssignmentV1#policy_definition_id}.
        :param policy_filter: policy_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#policy_filter RmsPolicyAssignmentV1#policy_filter}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#status RmsPolicyAssignmentV1#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#timeouts RmsPolicyAssignmentV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa465253044dd57ff34cccf558273b760572b4a362c6492eda34ad88a39d34b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RmsPolicyAssignmentV1Config(
            name=name,
            custom_policy=custom_policy,
            description=description,
            id=id,
            parameters=parameters,
            period=period,
            policy_definition_id=policy_definition_id,
            policy_filter=policy_filter,
            status=status,
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
        '''Generates CDKTF code for importing a RmsPolicyAssignmentV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RmsPolicyAssignmentV1 to import.
        :param import_from_id: The id of the existing RmsPolicyAssignmentV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RmsPolicyAssignmentV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d027ce4fc339eca589920d275a7909194759b0a3e3b5bf642bb5afabd48dcfc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomPolicy")
    def put_custom_policy(
        self,
        *,
        auth_type: builtins.str,
        function_urn: builtins.str,
        auth_value: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#auth_type RmsPolicyAssignmentV1#auth_type}.
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#function_urn RmsPolicyAssignmentV1#function_urn}.
        :param auth_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#auth_value RmsPolicyAssignmentV1#auth_value}.
        '''
        value = RmsPolicyAssignmentV1CustomPolicy(
            auth_type=auth_type, function_urn=function_urn, auth_value=auth_value
        )

        return typing.cast(None, jsii.invoke(self, "putCustomPolicy", [value]))

    @jsii.member(jsii_name="putPolicyFilter")
    def put_policy_filter(
        self,
        *,
        region: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_provider: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#region RmsPolicyAssignmentV1#region}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_id RmsPolicyAssignmentV1#resource_id}.
        :param resource_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_provider RmsPolicyAssignmentV1#resource_provider}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_type RmsPolicyAssignmentV1#resource_type}.
        :param tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#tag_key RmsPolicyAssignmentV1#tag_key}.
        :param tag_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#tag_value RmsPolicyAssignmentV1#tag_value}.
        '''
        value = RmsPolicyAssignmentV1PolicyFilter(
            region=region,
            resource_id=resource_id,
            resource_provider=resource_provider,
            resource_type=resource_type,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyFilter", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#create RmsPolicyAssignmentV1#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#update RmsPolicyAssignmentV1#update}.
        '''
        value = RmsPolicyAssignmentV1Timeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomPolicy")
    def reset_custom_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPolicy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPeriod")
    def reset_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriod", []))

    @jsii.member(jsii_name="resetPolicyDefinitionId")
    def reset_policy_definition_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDefinitionId", []))

    @jsii.member(jsii_name="resetPolicyFilter")
    def reset_policy_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyFilter", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="customPolicy")
    def custom_policy(self) -> "RmsPolicyAssignmentV1CustomPolicyOutputReference":
        return typing.cast("RmsPolicyAssignmentV1CustomPolicyOutputReference", jsii.get(self, "customPolicy"))

    @builtins.property
    @jsii.member(jsii_name="policyFilter")
    def policy_filter(self) -> "RmsPolicyAssignmentV1PolicyFilterOutputReference":
        return typing.cast("RmsPolicyAssignmentV1PolicyFilterOutputReference", jsii.get(self, "policyFilter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RmsPolicyAssignmentV1TimeoutsOutputReference":
        return typing.cast("RmsPolicyAssignmentV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="customPolicyInput")
    def custom_policy_input(
        self,
    ) -> typing.Optional["RmsPolicyAssignmentV1CustomPolicy"]:
        return typing.cast(typing.Optional["RmsPolicyAssignmentV1CustomPolicy"], jsii.get(self, "customPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionIdInput")
    def policy_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyFilterInput")
    def policy_filter_input(
        self,
    ) -> typing.Optional["RmsPolicyAssignmentV1PolicyFilter"]:
        return typing.cast(typing.Optional["RmsPolicyAssignmentV1PolicyFilter"], jsii.get(self, "policyFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RmsPolicyAssignmentV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RmsPolicyAssignmentV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74018a4b8194b69dfaaee8e1f6ee08d5893b928fc17d0c7911c870faf1a956a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b901da474e7828580d2c392c7c414febdcb045baadd50d724dfa09b0accfd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80843828551a9a076e16c8356d509b204c6353d3b970c524548738e81bdb38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a491d969575ab3326775f7cb9dbb0d6c84f02952f257fb987397ca76061d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275f339dd9d2024337471ff17c49fc3778430d516f82299832f540d094a2af43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionId")
    def policy_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDefinitionId"))

    @policy_definition_id.setter
    def policy_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a756deeda3aa1cf215c1fb00afa37b171d095b9c8647d3f4f12cdad135f6c68b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4b5014b93d28dc9c3234e4f2ab540e79a1862e895b841acaecff5af7af7b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1Config",
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
        "custom_policy": "customPolicy",
        "description": "description",
        "id": "id",
        "parameters": "parameters",
        "period": "period",
        "policy_definition_id": "policyDefinitionId",
        "policy_filter": "policyFilter",
        "status": "status",
        "timeouts": "timeouts",
    },
)
class RmsPolicyAssignmentV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_policy: typing.Optional[typing.Union["RmsPolicyAssignmentV1CustomPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        period: typing.Optional[builtins.str] = None,
        policy_definition_id: typing.Optional[builtins.str] = None,
        policy_filter: typing.Optional[typing.Union["RmsPolicyAssignmentV1PolicyFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["RmsPolicyAssignmentV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#name RmsPolicyAssignmentV1#name}.
        :param custom_policy: custom_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#custom_policy RmsPolicyAssignmentV1#custom_policy}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#description RmsPolicyAssignmentV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#id RmsPolicyAssignmentV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#parameters RmsPolicyAssignmentV1#parameters}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#period RmsPolicyAssignmentV1#period}.
        :param policy_definition_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#policy_definition_id RmsPolicyAssignmentV1#policy_definition_id}.
        :param policy_filter: policy_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#policy_filter RmsPolicyAssignmentV1#policy_filter}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#status RmsPolicyAssignmentV1#status}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#timeouts RmsPolicyAssignmentV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_policy, dict):
            custom_policy = RmsPolicyAssignmentV1CustomPolicy(**custom_policy)
        if isinstance(policy_filter, dict):
            policy_filter = RmsPolicyAssignmentV1PolicyFilter(**policy_filter)
        if isinstance(timeouts, dict):
            timeouts = RmsPolicyAssignmentV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0330f24cd3d273a9b92b1f1e9dc83a17bafae1f0766f4f53e16ffe22684019)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument custom_policy", value=custom_policy, expected_type=type_hints["custom_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument policy_definition_id", value=policy_definition_id, expected_type=type_hints["policy_definition_id"])
            check_type(argname="argument policy_filter", value=policy_filter, expected_type=type_hints["policy_filter"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
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
        if custom_policy is not None:
            self._values["custom_policy"] = custom_policy
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if parameters is not None:
            self._values["parameters"] = parameters
        if period is not None:
            self._values["period"] = period
        if policy_definition_id is not None:
            self._values["policy_definition_id"] = policy_definition_id
        if policy_filter is not None:
            self._values["policy_filter"] = policy_filter
        if status is not None:
            self._values["status"] = status
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#name RmsPolicyAssignmentV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_policy(self) -> typing.Optional["RmsPolicyAssignmentV1CustomPolicy"]:
        '''custom_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#custom_policy RmsPolicyAssignmentV1#custom_policy}
        '''
        result = self._values.get("custom_policy")
        return typing.cast(typing.Optional["RmsPolicyAssignmentV1CustomPolicy"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#description RmsPolicyAssignmentV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#id RmsPolicyAssignmentV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#parameters RmsPolicyAssignmentV1#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#period RmsPolicyAssignmentV1#period}.'''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_definition_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#policy_definition_id RmsPolicyAssignmentV1#policy_definition_id}.'''
        result = self._values.get("policy_definition_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_filter(self) -> typing.Optional["RmsPolicyAssignmentV1PolicyFilter"]:
        '''policy_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#policy_filter RmsPolicyAssignmentV1#policy_filter}
        '''
        result = self._values.get("policy_filter")
        return typing.cast(typing.Optional["RmsPolicyAssignmentV1PolicyFilter"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#status RmsPolicyAssignmentV1#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RmsPolicyAssignmentV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#timeouts RmsPolicyAssignmentV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RmsPolicyAssignmentV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsPolicyAssignmentV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1CustomPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "function_urn": "functionUrn",
        "auth_value": "authValue",
    },
)
class RmsPolicyAssignmentV1CustomPolicy:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        function_urn: builtins.str,
        auth_value: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#auth_type RmsPolicyAssignmentV1#auth_type}.
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#function_urn RmsPolicyAssignmentV1#function_urn}.
        :param auth_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#auth_value RmsPolicyAssignmentV1#auth_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a770d790602da82ab9a725823a7c94cd043135bd674623c985311d963ae4d47)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument function_urn", value=function_urn, expected_type=type_hints["function_urn"])
            check_type(argname="argument auth_value", value=auth_value, expected_type=type_hints["auth_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
            "function_urn": function_urn,
        }
        if auth_value is not None:
            self._values["auth_value"] = auth_value

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#auth_type RmsPolicyAssignmentV1#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#function_urn RmsPolicyAssignmentV1#function_urn}.'''
        result = self._values.get("function_urn")
        assert result is not None, "Required property 'function_urn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_value(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#auth_value RmsPolicyAssignmentV1#auth_value}.'''
        result = self._values.get("auth_value")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsPolicyAssignmentV1CustomPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RmsPolicyAssignmentV1CustomPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1CustomPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7bd2f863dcfa793666dd97376d9f5d179fd5987ae476b5620a37961f1773325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthValue")
    def reset_auth_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthValue", []))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authValueInput")
    def auth_value_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "authValueInput"))

    @builtins.property
    @jsii.member(jsii_name="functionUrnInput")
    def function_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158f2c0e0f5d3322981f32dcc3ccecf9efbef6f47cc792b051803030f70ce617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authValue")
    def auth_value(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "authValue"))

    @auth_value.setter
    def auth_value(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167ead5c7460d62a313e71431958287bbcdf71acc61ad49a455e6eeeb8364191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionUrn")
    def function_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionUrn"))

    @function_urn.setter
    def function_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0c6a1a8d15e54717e4003fbf8b31ed046a14b3ae5b7bffc117e00b978901a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RmsPolicyAssignmentV1CustomPolicy]:
        return typing.cast(typing.Optional[RmsPolicyAssignmentV1CustomPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RmsPolicyAssignmentV1CustomPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5570c7b1de60c44db134139de3f772a32c3d84fb0c01a3f4b4eba15ed5549bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1PolicyFilter",
    jsii_struct_bases=[],
    name_mapping={
        "region": "region",
        "resource_id": "resourceId",
        "resource_provider": "resourceProvider",
        "resource_type": "resourceType",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class RmsPolicyAssignmentV1PolicyFilter:
    def __init__(
        self,
        *,
        region: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_provider: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#region RmsPolicyAssignmentV1#region}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_id RmsPolicyAssignmentV1#resource_id}.
        :param resource_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_provider RmsPolicyAssignmentV1#resource_provider}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_type RmsPolicyAssignmentV1#resource_type}.
        :param tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#tag_key RmsPolicyAssignmentV1#tag_key}.
        :param tag_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#tag_value RmsPolicyAssignmentV1#tag_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82e318d19d8e32052431431748b5cf16ec9b1b96d73a05e0abd777023f33167)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_provider", value=resource_provider, expected_type=type_hints["resource_provider"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if region is not None:
            self._values["region"] = region
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_provider is not None:
            self._values["resource_provider"] = resource_provider
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#region RmsPolicyAssignmentV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_id RmsPolicyAssignmentV1#resource_id}.'''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_provider(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_provider RmsPolicyAssignmentV1#resource_provider}.'''
        result = self._values.get("resource_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#resource_type RmsPolicyAssignmentV1#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#tag_key RmsPolicyAssignmentV1#tag_key}.'''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#tag_value RmsPolicyAssignmentV1#tag_value}.'''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsPolicyAssignmentV1PolicyFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RmsPolicyAssignmentV1PolicyFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1PolicyFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20c10f29a10d8fbabc5bf866a2e9ab96e8d4daa7a2af37f1ff37ef9b5741b47e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourceProvider")
    def reset_resource_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceProvider", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceProviderInput")
    def resource_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9956188b6f169f9f589e9f2936b6c6a7d32eb6949b26ba91031978d586a0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4311cd68c3b21e3419c2f661c2c44ce943cbd50a0a3ce80f613aeeb705f6576c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceProvider")
    def resource_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceProvider"))

    @resource_provider.setter
    def resource_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86af051829b09cf6eb31d002b188c724d0a516662267fb058f8252cbecad181d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec351cd37d1868865b35ffec234c31bfe0499ab87df5f51f348d495ca84f361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7ecf7e6642a55210154dc8c6f567fd11e18fc956220dafc2086d39ef08e3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e88c2875309d0a80aebb32df36b3cf3081a7efa60e4dea4347d6e8d152937f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RmsPolicyAssignmentV1PolicyFilter]:
        return typing.cast(typing.Optional[RmsPolicyAssignmentV1PolicyFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RmsPolicyAssignmentV1PolicyFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5ecd9ef47f14ba2f6ae7cd6a250bb32a8302d05378ca71be0074a529ef392d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class RmsPolicyAssignmentV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#create RmsPolicyAssignmentV1#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#update RmsPolicyAssignmentV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace6a343f77fb2602573e97fca080f706b3b2428e3164430c1b318af888bd76d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#create RmsPolicyAssignmentV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rms_policy_assignment_v1#update RmsPolicyAssignmentV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RmsPolicyAssignmentV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RmsPolicyAssignmentV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rmsPolicyAssignmentV1.RmsPolicyAssignmentV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd33600ba9a8df9fe5a12d601249101c3496013203d2997c387524869871f141)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c04f04c48ca39d4c2fe410e1a10144ed938a5bd6751c1d58e0eda5b1a9370e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9977d9d5a0d96fe012e5e26228428cf3c86ec9288216fe123625b4db48f574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RmsPolicyAssignmentV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RmsPolicyAssignmentV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RmsPolicyAssignmentV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93a12505882d95a18b51031f4113dd9b57c7a2a59b023eedfd3bb232d95fab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RmsPolicyAssignmentV1",
    "RmsPolicyAssignmentV1Config",
    "RmsPolicyAssignmentV1CustomPolicy",
    "RmsPolicyAssignmentV1CustomPolicyOutputReference",
    "RmsPolicyAssignmentV1PolicyFilter",
    "RmsPolicyAssignmentV1PolicyFilterOutputReference",
    "RmsPolicyAssignmentV1Timeouts",
    "RmsPolicyAssignmentV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2aa465253044dd57ff34cccf558273b760572b4a362c6492eda34ad88a39d34b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    custom_policy: typing.Optional[typing.Union[RmsPolicyAssignmentV1CustomPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    period: typing.Optional[builtins.str] = None,
    policy_definition_id: typing.Optional[builtins.str] = None,
    policy_filter: typing.Optional[typing.Union[RmsPolicyAssignmentV1PolicyFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[RmsPolicyAssignmentV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d027ce4fc339eca589920d275a7909194759b0a3e3b5bf642bb5afabd48dcfc3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74018a4b8194b69dfaaee8e1f6ee08d5893b928fc17d0c7911c870faf1a956a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b901da474e7828580d2c392c7c414febdcb045baadd50d724dfa09b0accfd5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80843828551a9a076e16c8356d509b204c6353d3b970c524548738e81bdb38a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a491d969575ab3326775f7cb9dbb0d6c84f02952f257fb987397ca76061d81(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275f339dd9d2024337471ff17c49fc3778430d516f82299832f540d094a2af43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a756deeda3aa1cf215c1fb00afa37b171d095b9c8647d3f4f12cdad135f6c68b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4b5014b93d28dc9c3234e4f2ab540e79a1862e895b841acaecff5af7af7b13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0330f24cd3d273a9b92b1f1e9dc83a17bafae1f0766f4f53e16ffe22684019(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    custom_policy: typing.Optional[typing.Union[RmsPolicyAssignmentV1CustomPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    period: typing.Optional[builtins.str] = None,
    policy_definition_id: typing.Optional[builtins.str] = None,
    policy_filter: typing.Optional[typing.Union[RmsPolicyAssignmentV1PolicyFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[RmsPolicyAssignmentV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a770d790602da82ab9a725823a7c94cd043135bd674623c985311d963ae4d47(
    *,
    auth_type: builtins.str,
    function_urn: builtins.str,
    auth_value: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bd2f863dcfa793666dd97376d9f5d179fd5987ae476b5620a37961f1773325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158f2c0e0f5d3322981f32dcc3ccecf9efbef6f47cc792b051803030f70ce617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167ead5c7460d62a313e71431958287bbcdf71acc61ad49a455e6eeeb8364191(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0c6a1a8d15e54717e4003fbf8b31ed046a14b3ae5b7bffc117e00b978901a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5570c7b1de60c44db134139de3f772a32c3d84fb0c01a3f4b4eba15ed5549bec(
    value: typing.Optional[RmsPolicyAssignmentV1CustomPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82e318d19d8e32052431431748b5cf16ec9b1b96d73a05e0abd777023f33167(
    *,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_provider: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c10f29a10d8fbabc5bf866a2e9ab96e8d4daa7a2af37f1ff37ef9b5741b47e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9956188b6f169f9f589e9f2936b6c6a7d32eb6949b26ba91031978d586a0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4311cd68c3b21e3419c2f661c2c44ce943cbd50a0a3ce80f613aeeb705f6576c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86af051829b09cf6eb31d002b188c724d0a516662267fb058f8252cbecad181d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec351cd37d1868865b35ffec234c31bfe0499ab87df5f51f348d495ca84f361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7ecf7e6642a55210154dc8c6f567fd11e18fc956220dafc2086d39ef08e3d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e88c2875309d0a80aebb32df36b3cf3081a7efa60e4dea4347d6e8d152937f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5ecd9ef47f14ba2f6ae7cd6a250bb32a8302d05378ca71be0074a529ef392d(
    value: typing.Optional[RmsPolicyAssignmentV1PolicyFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace6a343f77fb2602573e97fca080f706b3b2428e3164430c1b318af888bd76d(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd33600ba9a8df9fe5a12d601249101c3496013203d2997c387524869871f141(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04f04c48ca39d4c2fe410e1a10144ed938a5bd6751c1d58e0eda5b1a9370e6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9977d9d5a0d96fe012e5e26228428cf3c86ec9288216fe123625b4db48f574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93a12505882d95a18b51031f4113dd9b57c7a2a59b023eedfd3bb232d95fab3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RmsPolicyAssignmentV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
