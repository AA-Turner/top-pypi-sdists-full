r'''
# `azuread_synchronization_job_provision_on_demand`

Refer to the Terraform Registry for docs: [`azuread_synchronization_job_provision_on_demand`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand).
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


class SynchronizationJobProvisionOnDemand(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemand",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand azuread_synchronization_job_provision_on_demand}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parameter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SynchronizationJobProvisionOnDemandParameter", typing.Dict[builtins.str, typing.Any]]]],
        service_principal_id: builtins.str,
        synchronization_job_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SynchronizationJobProvisionOnDemandTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand azuread_synchronization_job_provision_on_demand} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#parameter SynchronizationJobProvisionOnDemand#parameter}
        :param service_principal_id: The object ID of the service principal for which this synchronization job should be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#service_principal_id SynchronizationJobProvisionOnDemand#service_principal_id}
        :param synchronization_job_id: The identifier for the synchronization jop. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#synchronization_job_id SynchronizationJobProvisionOnDemand#synchronization_job_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#id SynchronizationJobProvisionOnDemand#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#timeouts SynchronizationJobProvisionOnDemand#timeouts}
        :param triggers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#triggers SynchronizationJobProvisionOnDemand#triggers}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa3c79c7a0e18d6f78141284ee300e77b3c9ada0252aae416363ee891ef973a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SynchronizationJobProvisionOnDemandConfig(
            parameter=parameter,
            service_principal_id=service_principal_id,
            synchronization_job_id=synchronization_job_id,
            id=id,
            timeouts=timeouts,
            triggers=triggers,
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
        '''Generates CDKTF code for importing a SynchronizationJobProvisionOnDemand resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SynchronizationJobProvisionOnDemand to import.
        :param import_from_id: The id of the existing SynchronizationJobProvisionOnDemand that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SynchronizationJobProvisionOnDemand to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b439fc6ef448a1af661ca8787f4587424fb400102d797800ae5d48e09086b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SynchronizationJobProvisionOnDemandParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4ff80864cbb3d2f6fd0b2ca266194eef9d927bc3b274dd672f5e251156ce92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#create SynchronizationJobProvisionOnDemand#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#delete SynchronizationJobProvisionOnDemand#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#read SynchronizationJobProvisionOnDemand#read}.
        '''
        value = SynchronizationJobProvisionOnDemandTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTriggers")
    def reset_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggers", []))

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
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> "SynchronizationJobProvisionOnDemandParameterList":
        return typing.cast("SynchronizationJobProvisionOnDemandParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SynchronizationJobProvisionOnDemandTimeoutsOutputReference":
        return typing.cast("SynchronizationJobProvisionOnDemandTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalIdInput")
    def service_principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="synchronizationJobIdInput")
    def synchronization_job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "synchronizationJobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SynchronizationJobProvisionOnDemandTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SynchronizationJobProvisionOnDemandTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddafdb1d08844b7cc0ef936db07c1b6973f4197ccd10d7963710eb1812413ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalId")
    def service_principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalId"))

    @service_principal_id.setter
    def service_principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dd7d7b1a03f48af21dced0448e98360a739c3ae80a5ae6ebb8305dfdfa6f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="synchronizationJobId")
    def synchronization_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "synchronizationJobId"))

    @synchronization_job_id.setter
    def synchronization_job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905bf8119ea09d20ca47dd505f522fd98aa144381c43a2504e9fdfcbbc7d9bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synchronizationJobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "triggers"))

    @triggers.setter
    def triggers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68c36f0f56e52d87f1c226d5d9a0a048f8f87e7455b682859bd4ae61ca8901b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggers", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "parameter": "parameter",
        "service_principal_id": "servicePrincipalId",
        "synchronization_job_id": "synchronizationJobId",
        "id": "id",
        "timeouts": "timeouts",
        "triggers": "triggers",
    },
)
class SynchronizationJobProvisionOnDemandConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parameter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SynchronizationJobProvisionOnDemandParameter", typing.Dict[builtins.str, typing.Any]]]],
        service_principal_id: builtins.str,
        synchronization_job_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SynchronizationJobProvisionOnDemandTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#parameter SynchronizationJobProvisionOnDemand#parameter}
        :param service_principal_id: The object ID of the service principal for which this synchronization job should be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#service_principal_id SynchronizationJobProvisionOnDemand#service_principal_id}
        :param synchronization_job_id: The identifier for the synchronization jop. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#synchronization_job_id SynchronizationJobProvisionOnDemand#synchronization_job_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#id SynchronizationJobProvisionOnDemand#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#timeouts SynchronizationJobProvisionOnDemand#timeouts}
        :param triggers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#triggers SynchronizationJobProvisionOnDemand#triggers}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SynchronizationJobProvisionOnDemandTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d101510df4ba8e773d296f9e75fbe03a0397350ed17b02cca1f86d1d32dccbb3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument service_principal_id", value=service_principal_id, expected_type=type_hints["service_principal_id"])
            check_type(argname="argument synchronization_job_id", value=synchronization_job_id, expected_type=type_hints["synchronization_job_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter": parameter,
            "service_principal_id": service_principal_id,
            "synchronization_job_id": synchronization_job_id,
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
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if triggers is not None:
            self._values["triggers"] = triggers

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
    def parameter(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameter"]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#parameter SynchronizationJobProvisionOnDemand#parameter}
        '''
        result = self._values.get("parameter")
        assert result is not None, "Required property 'parameter' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameter"]], result)

    @builtins.property
    def service_principal_id(self) -> builtins.str:
        '''The object ID of the service principal for which this synchronization job should be provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#service_principal_id SynchronizationJobProvisionOnDemand#service_principal_id}
        '''
        result = self._values.get("service_principal_id")
        assert result is not None, "Required property 'service_principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def synchronization_job_id(self) -> builtins.str:
        '''The identifier for the synchronization jop.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#synchronization_job_id SynchronizationJobProvisionOnDemand#synchronization_job_id}
        '''
        result = self._values.get("synchronization_job_id")
        assert result is not None, "Required property 'synchronization_job_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#id SynchronizationJobProvisionOnDemand#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SynchronizationJobProvisionOnDemandTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#timeouts SynchronizationJobProvisionOnDemand#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SynchronizationJobProvisionOnDemandTimeouts"], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#triggers SynchronizationJobProvisionOnDemand#triggers}.'''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronizationJobProvisionOnDemandConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandParameter",
    jsii_struct_bases=[],
    name_mapping={"rule_id": "ruleId", "subject": "subject"},
)
class SynchronizationJobProvisionOnDemandParameter:
    def __init__(
        self,
        *,
        rule_id: builtins.str,
        subject: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SynchronizationJobProvisionOnDemandParameterSubject", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rule_id: The identifier of the synchronization rule to be applied. This rule ID is defined in the schema for a given synchronization job or template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#rule_id SynchronizationJobProvisionOnDemand#rule_id}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#subject SynchronizationJobProvisionOnDemand#subject}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72f1dbf3b8510e6e4584b657e3db63eae8156fad707b45ca1a0de014a241825)
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_id": rule_id,
            "subject": subject,
        }

    @builtins.property
    def rule_id(self) -> builtins.str:
        '''The identifier of the synchronization rule to be applied.

        This rule ID is defined in the schema for a given synchronization job or template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#rule_id SynchronizationJobProvisionOnDemand#rule_id}
        '''
        result = self._values.get("rule_id")
        assert result is not None, "Required property 'rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameterSubject"]]:
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#subject SynchronizationJobProvisionOnDemand#subject}
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameterSubject"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronizationJobProvisionOnDemandParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynchronizationJobProvisionOnDemandParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a617e196db79a0d41d94bd0cf7b344fc6d2dcd746035b38ed30a81ddd8af7231)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SynchronizationJobProvisionOnDemandParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defb4efafd81abf96248379b0e6b3bf95ec99ceefce2ef21086bf38b3b1e3f99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SynchronizationJobProvisionOnDemandParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331351abe686adb9ee03479716ce00b3a25999e81d8b358491d1626e30cc05cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ef5645360b01415fc3289a488e9de7dfd35aa250b956b785ecf45cce3f61a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26856e54b58830af18d4f74844cce4cf02f52f2941dfa08a7334683ad0ce4884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1da97a2e67c189baca615d91f0aba3dd78b64ceee31d6dc534b19d1ff4127c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SynchronizationJobProvisionOnDemandParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4e8629fccf51b0cb778298eb45addde46eaa6f44c46bd7bc869c8e7d3834486)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSubject")
    def put_subject(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SynchronizationJobProvisionOnDemandParameterSubject", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9441606a3ad5e369fac554608c72e1c04dcb9d75e99c188612567387a38098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubject", [value]))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> "SynchronizationJobProvisionOnDemandParameterSubjectList":
        return typing.cast("SynchronizationJobProvisionOnDemandParameterSubjectList", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="ruleIdInput")
    def rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameterSubject"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SynchronizationJobProvisionOnDemandParameterSubject"]]], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d2f7cb49ffac3b1212049cf9231094ddc7389cc3cb4c1852f3a4c1ce9674f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c417b3f0debf2ee8fbebcf3ea8fe240d1908c8c2c373383b67e8ae7bec690172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandParameterSubject",
    jsii_struct_bases=[],
    name_mapping={"object_id": "objectId", "object_type_name": "objectTypeName"},
)
class SynchronizationJobProvisionOnDemandParameterSubject:
    def __init__(
        self,
        *,
        object_id: builtins.str,
        object_type_name: builtins.str,
    ) -> None:
        '''
        :param object_id: The identifier of an object to which a synchronization job is to be applied. Can be one of the following: (1) An onPremisesDistinguishedName for synchronization from Active Directory to Azure AD. (2) The user ID for synchronization from Azure AD to a third-party. (3) The Worker ID of the Workday worker for synchronization from Workday to either Active Directory or Azure AD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#object_id SynchronizationJobProvisionOnDemand#object_id}
        :param object_type_name: The type of the object to which a synchronization job is to be applied. Can be one of the following: ``user`` for synchronizing between Active Directory and Azure AD, ``User`` for synchronizing a user between Azure AD and a third-party application, ``Worker`` for synchronization a user between Workday and either Active Directory or Azure AD, ``Group`` for synchronizing a group between Azure AD and a third-party application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#object_type_name SynchronizationJobProvisionOnDemand#object_type_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73d18b71676af4abbc61dde6a5e78d3cd69622ca37df8975238689e52a4e7d1)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument object_type_name", value=object_type_name, expected_type=type_hints["object_type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id": object_id,
            "object_type_name": object_type_name,
        }

    @builtins.property
    def object_id(self) -> builtins.str:
        '''The identifier of an object to which a synchronization job is to be applied.

        Can be one of the following: (1) An onPremisesDistinguishedName for synchronization from Active Directory to Azure AD. (2) The user ID for synchronization from Azure AD to a third-party. (3) The Worker ID of the Workday worker for synchronization from Workday to either Active Directory or Azure AD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#object_id SynchronizationJobProvisionOnDemand#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_type_name(self) -> builtins.str:
        '''The type of the object to which a synchronization job is to be applied.

        Can be one of the following: ``user`` for synchronizing between Active Directory and Azure AD, ``User`` for synchronizing a user between Azure AD and a third-party application, ``Worker`` for synchronization a user between Workday and either Active Directory or Azure AD, ``Group`` for synchronizing a group between Azure AD and a third-party application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#object_type_name SynchronizationJobProvisionOnDemand#object_type_name}
        '''
        result = self._values.get("object_type_name")
        assert result is not None, "Required property 'object_type_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronizationJobProvisionOnDemandParameterSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynchronizationJobProvisionOnDemandParameterSubjectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandParameterSubjectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac5c4441c3ff1a17e75082747c3d20b324c028cc26dc20f76808dd8fba42fe4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SynchronizationJobProvisionOnDemandParameterSubjectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768d343dbcaf171a6a443f4e48cb326db4fafadeb34a45d552192b8acf3e7b2f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SynchronizationJobProvisionOnDemandParameterSubjectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a8927ae866ad9acf44f25ff0d0048be934ef79bc5bfa6c867cc5cb1085802e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__162150c1e711817f2d637bfcea5d083b0e8a52304fccb4b9334bbe8428f7d6dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e20286b6dffbdbcecf5334cb1cae515470811a0c47b03729c86e429206ab91f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameterSubject]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameterSubject]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameterSubject]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bdad6fb0fc16bd948c0f8edf707d529037d5f02a608bcf429fd8133af4d389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SynchronizationJobProvisionOnDemandParameterSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandParameterSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31506504907556a9e0ba0d8cc47043e0b7ea9cab19d94090876cd5e41bc99268)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypeNameInput")
    def object_type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcae8cee6cec05552c4f1bed1554050256cc3c35c5e99ac1d216dc03d1c0aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypeName")
    def object_type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypeName"))

    @object_type_name.setter
    def object_type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f155957d4dadbc3b27064d4b48ea5ea729b79add2ea514ba50d5410a9260010c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameterSubject]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameterSubject]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameterSubject]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da72398863c3c7f96703b7ed000395569060a395517731f0c7bf1787347ddc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class SynchronizationJobProvisionOnDemandTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#create SynchronizationJobProvisionOnDemand#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#delete SynchronizationJobProvisionOnDemand#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#read SynchronizationJobProvisionOnDemand#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4856193c8eb3f2902517088e6388426d767c66afe35495060c6ce33b0de62793)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#create SynchronizationJobProvisionOnDemand#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#delete SynchronizationJobProvisionOnDemand#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/synchronization_job_provision_on_demand#read SynchronizationJobProvisionOnDemand#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronizationJobProvisionOnDemandTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynchronizationJobProvisionOnDemandTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.synchronizationJobProvisionOnDemand.SynchronizationJobProvisionOnDemandTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2501b892b1ed434a5ba75fb2fd95d843065a52185c6789c4e9ce3d145d207e03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70113a291b3eb0097213040ac6b6c27cee2201e62761af7aa471441adcdc033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528e81d90ac48cdbc90a8f7888d4168e74e9a95a6ed1324317af49817d225c4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fc3e645e3537bfbe7abfbfce5f427dc5d990cca96116b0ca6bd4648cab3134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81e9669697ff46a0567afc0245ad2a8f2781370424dc26650f3609c4ee7dab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SynchronizationJobProvisionOnDemand",
    "SynchronizationJobProvisionOnDemandConfig",
    "SynchronizationJobProvisionOnDemandParameter",
    "SynchronizationJobProvisionOnDemandParameterList",
    "SynchronizationJobProvisionOnDemandParameterOutputReference",
    "SynchronizationJobProvisionOnDemandParameterSubject",
    "SynchronizationJobProvisionOnDemandParameterSubjectList",
    "SynchronizationJobProvisionOnDemandParameterSubjectOutputReference",
    "SynchronizationJobProvisionOnDemandTimeouts",
    "SynchronizationJobProvisionOnDemandTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5fa3c79c7a0e18d6f78141284ee300e77b3c9ada0252aae416363ee891ef973a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parameter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SynchronizationJobProvisionOnDemandParameter, typing.Dict[builtins.str, typing.Any]]]],
    service_principal_id: builtins.str,
    synchronization_job_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SynchronizationJobProvisionOnDemandTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__b7b439fc6ef448a1af661ca8787f4587424fb400102d797800ae5d48e09086b3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4ff80864cbb3d2f6fd0b2ca266194eef9d927bc3b274dd672f5e251156ce92(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SynchronizationJobProvisionOnDemandParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddafdb1d08844b7cc0ef936db07c1b6973f4197ccd10d7963710eb1812413ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dd7d7b1a03f48af21dced0448e98360a739c3ae80a5ae6ebb8305dfdfa6f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905bf8119ea09d20ca47dd505f522fd98aa144381c43a2504e9fdfcbbc7d9bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68c36f0f56e52d87f1c226d5d9a0a048f8f87e7455b682859bd4ae61ca8901b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d101510df4ba8e773d296f9e75fbe03a0397350ed17b02cca1f86d1d32dccbb3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SynchronizationJobProvisionOnDemandParameter, typing.Dict[builtins.str, typing.Any]]]],
    service_principal_id: builtins.str,
    synchronization_job_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SynchronizationJobProvisionOnDemandTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72f1dbf3b8510e6e4584b657e3db63eae8156fad707b45ca1a0de014a241825(
    *,
    rule_id: builtins.str,
    subject: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SynchronizationJobProvisionOnDemandParameterSubject, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a617e196db79a0d41d94bd0cf7b344fc6d2dcd746035b38ed30a81ddd8af7231(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defb4efafd81abf96248379b0e6b3bf95ec99ceefce2ef21086bf38b3b1e3f99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331351abe686adb9ee03479716ce00b3a25999e81d8b358491d1626e30cc05cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ef5645360b01415fc3289a488e9de7dfd35aa250b956b785ecf45cce3f61a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26856e54b58830af18d4f74844cce4cf02f52f2941dfa08a7334683ad0ce4884(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1da97a2e67c189baca615d91f0aba3dd78b64ceee31d6dc534b19d1ff4127c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e8629fccf51b0cb778298eb45addde46eaa6f44c46bd7bc869c8e7d3834486(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9441606a3ad5e369fac554608c72e1c04dcb9d75e99c188612567387a38098(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SynchronizationJobProvisionOnDemandParameterSubject, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d2f7cb49ffac3b1212049cf9231094ddc7389cc3cb4c1852f3a4c1ce9674f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c417b3f0debf2ee8fbebcf3ea8fe240d1908c8c2c373383b67e8ae7bec690172(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73d18b71676af4abbc61dde6a5e78d3cd69622ca37df8975238689e52a4e7d1(
    *,
    object_id: builtins.str,
    object_type_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5c4441c3ff1a17e75082747c3d20b324c028cc26dc20f76808dd8fba42fe4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768d343dbcaf171a6a443f4e48cb326db4fafadeb34a45d552192b8acf3e7b2f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a8927ae866ad9acf44f25ff0d0048be934ef79bc5bfa6c867cc5cb1085802e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162150c1e711817f2d637bfcea5d083b0e8a52304fccb4b9334bbe8428f7d6dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20286b6dffbdbcecf5334cb1cae515470811a0c47b03729c86e429206ab91f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bdad6fb0fc16bd948c0f8edf707d529037d5f02a608bcf429fd8133af4d389(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SynchronizationJobProvisionOnDemandParameterSubject]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31506504907556a9e0ba0d8cc47043e0b7ea9cab19d94090876cd5e41bc99268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcae8cee6cec05552c4f1bed1554050256cc3c35c5e99ac1d216dc03d1c0aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f155957d4dadbc3b27064d4b48ea5ea729b79add2ea514ba50d5410a9260010c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da72398863c3c7f96703b7ed000395569060a395517731f0c7bf1787347ddc8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandParameterSubject]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4856193c8eb3f2902517088e6388426d767c66afe35495060c6ce33b0de62793(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2501b892b1ed434a5ba75fb2fd95d843065a52185c6789c4e9ce3d145d207e03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70113a291b3eb0097213040ac6b6c27cee2201e62761af7aa471441adcdc033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528e81d90ac48cdbc90a8f7888d4168e74e9a95a6ed1324317af49817d225c4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fc3e645e3537bfbe7abfbfce5f427dc5d990cca96116b0ca6bd4648cab3134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81e9669697ff46a0567afc0245ad2a8f2781370424dc26650f3609c4ee7dab5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynchronizationJobProvisionOnDemandTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
