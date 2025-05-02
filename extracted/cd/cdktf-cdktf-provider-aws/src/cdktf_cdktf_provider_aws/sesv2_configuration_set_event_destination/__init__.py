r'''
# `aws_sesv2_configuration_set_event_destination`

Refer to the Terraform Registry for docs: [`aws_sesv2_configuration_set_event_destination`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination).
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


class Sesv2ConfigurationSetEventDestination(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestination",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination aws_sesv2_configuration_set_event_destination}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        configuration_set_name: builtins.str,
        event_destination: typing.Union["Sesv2ConfigurationSetEventDestinationEventDestination", typing.Dict[builtins.str, typing.Any]],
        event_destination_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination aws_sesv2_configuration_set_event_destination} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param configuration_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#configuration_set_name Sesv2ConfigurationSetEventDestination#configuration_set_name}.
        :param event_destination: event_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_destination Sesv2ConfigurationSetEventDestination#event_destination}
        :param event_destination_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_destination_name Sesv2ConfigurationSetEventDestination#event_destination_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#id Sesv2ConfigurationSetEventDestination#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07f8d04197a0080cb9d3ecf0128d0e3ed4cc26598ad26d07d566c4b56aa968c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Sesv2ConfigurationSetEventDestinationConfig(
            configuration_set_name=configuration_set_name,
            event_destination=event_destination,
            event_destination_name=event_destination_name,
            id=id,
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
        '''Generates CDKTF code for importing a Sesv2ConfigurationSetEventDestination resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Sesv2ConfigurationSetEventDestination to import.
        :param import_from_id: The id of the existing Sesv2ConfigurationSetEventDestination that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Sesv2ConfigurationSetEventDestination to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9b6368e286d608a1ee2eceac3264e9eab8d34e01f9fb7c5e200d1c0d18854f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventDestination")
    def put_event_destination(
        self,
        *,
        matching_event_types: typing.Sequence[builtins.str],
        cloud_watch_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_bridge_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_firehose_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        pinpoint_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#matching_event_types Sesv2ConfigurationSetEventDestination#matching_event_types}.
        :param cloud_watch_destination: cloud_watch_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#cloud_watch_destination Sesv2ConfigurationSetEventDestination#cloud_watch_destination}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#enabled Sesv2ConfigurationSetEventDestination#enabled}.
        :param event_bridge_destination: event_bridge_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_bridge_destination Sesv2ConfigurationSetEventDestination#event_bridge_destination}
        :param kinesis_firehose_destination: kinesis_firehose_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#kinesis_firehose_destination Sesv2ConfigurationSetEventDestination#kinesis_firehose_destination}
        :param pinpoint_destination: pinpoint_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#pinpoint_destination Sesv2ConfigurationSetEventDestination#pinpoint_destination}
        :param sns_destination: sns_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#sns_destination Sesv2ConfigurationSetEventDestination#sns_destination}
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestination(
            matching_event_types=matching_event_types,
            cloud_watch_destination=cloud_watch_destination,
            enabled=enabled,
            event_bridge_destination=event_bridge_destination,
            kinesis_firehose_destination=kinesis_firehose_destination,
            pinpoint_destination=pinpoint_destination,
            sns_destination=sns_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putEventDestination", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="eventDestination")
    def event_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference":
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference", jsii.get(self, "eventDestination"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetNameInput")
    def configuration_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDestinationInput")
    def event_destination_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestination"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestination"], jsii.get(self, "eventDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDestinationNameInput")
    def event_destination_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventDestinationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationSetName"))

    @configuration_set_name.setter
    def configuration_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78151cb143c6986efa792563b5d7ac57ba7674d306f65635b1101f2015f47766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDestinationName")
    def event_destination_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDestinationName"))

    @event_destination_name.setter
    def event_destination_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3285bb375e29a737e6c9cd9a42fafb77cfe8bad9f9c4c32cd6a471f9709a6ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDestinationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f08374d7a9cf909ae90be54bdeb1c1ad56a12df7753e99c6c0592167cd8c72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "configuration_set_name": "configurationSetName",
        "event_destination": "eventDestination",
        "event_destination_name": "eventDestinationName",
        "id": "id",
    },
)
class Sesv2ConfigurationSetEventDestinationConfig(
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
        configuration_set_name: builtins.str,
        event_destination: typing.Union["Sesv2ConfigurationSetEventDestinationEventDestination", typing.Dict[builtins.str, typing.Any]],
        event_destination_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param configuration_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#configuration_set_name Sesv2ConfigurationSetEventDestination#configuration_set_name}.
        :param event_destination: event_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_destination Sesv2ConfigurationSetEventDestination#event_destination}
        :param event_destination_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_destination_name Sesv2ConfigurationSetEventDestination#event_destination_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#id Sesv2ConfigurationSetEventDestination#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(event_destination, dict):
            event_destination = Sesv2ConfigurationSetEventDestinationEventDestination(**event_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e05f692cb9ba5a2405ef3f6925aa716850ceaebdb3657f2c5c210abc6e50ee)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            check_type(argname="argument event_destination", value=event_destination, expected_type=type_hints["event_destination"])
            check_type(argname="argument event_destination_name", value=event_destination_name, expected_type=type_hints["event_destination_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_set_name": configuration_set_name,
            "event_destination": event_destination,
            "event_destination_name": event_destination_name,
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
    def configuration_set_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#configuration_set_name Sesv2ConfigurationSetEventDestination#configuration_set_name}.'''
        result = self._values.get("configuration_set_name")
        assert result is not None, "Required property 'configuration_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestination":
        '''event_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_destination Sesv2ConfigurationSetEventDestination#event_destination}
        '''
        result = self._values.get("event_destination")
        assert result is not None, "Required property 'event_destination' is missing"
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestination", result)

    @builtins.property
    def event_destination_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_destination_name Sesv2ConfigurationSetEventDestination#event_destination_name}.'''
        result = self._values.get("event_destination_name")
        assert result is not None, "Required property 'event_destination_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#id Sesv2ConfigurationSetEventDestination#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestination",
    jsii_struct_bases=[],
    name_mapping={
        "matching_event_types": "matchingEventTypes",
        "cloud_watch_destination": "cloudWatchDestination",
        "enabled": "enabled",
        "event_bridge_destination": "eventBridgeDestination",
        "kinesis_firehose_destination": "kinesisFirehoseDestination",
        "pinpoint_destination": "pinpointDestination",
        "sns_destination": "snsDestination",
    },
)
class Sesv2ConfigurationSetEventDestinationEventDestination:
    def __init__(
        self,
        *,
        matching_event_types: typing.Sequence[builtins.str],
        cloud_watch_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_bridge_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_firehose_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        pinpoint_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_destination: typing.Optional[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_event_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#matching_event_types Sesv2ConfigurationSetEventDestination#matching_event_types}.
        :param cloud_watch_destination: cloud_watch_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#cloud_watch_destination Sesv2ConfigurationSetEventDestination#cloud_watch_destination}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#enabled Sesv2ConfigurationSetEventDestination#enabled}.
        :param event_bridge_destination: event_bridge_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_bridge_destination Sesv2ConfigurationSetEventDestination#event_bridge_destination}
        :param kinesis_firehose_destination: kinesis_firehose_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#kinesis_firehose_destination Sesv2ConfigurationSetEventDestination#kinesis_firehose_destination}
        :param pinpoint_destination: pinpoint_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#pinpoint_destination Sesv2ConfigurationSetEventDestination#pinpoint_destination}
        :param sns_destination: sns_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#sns_destination Sesv2ConfigurationSetEventDestination#sns_destination}
        '''
        if isinstance(cloud_watch_destination, dict):
            cloud_watch_destination = Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination(**cloud_watch_destination)
        if isinstance(event_bridge_destination, dict):
            event_bridge_destination = Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination(**event_bridge_destination)
        if isinstance(kinesis_firehose_destination, dict):
            kinesis_firehose_destination = Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination(**kinesis_firehose_destination)
        if isinstance(pinpoint_destination, dict):
            pinpoint_destination = Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination(**pinpoint_destination)
        if isinstance(sns_destination, dict):
            sns_destination = Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination(**sns_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0036d6203c17ce2093e679cf9c942f608696ec640d51d61bec5b516ccd3628be)
            check_type(argname="argument matching_event_types", value=matching_event_types, expected_type=type_hints["matching_event_types"])
            check_type(argname="argument cloud_watch_destination", value=cloud_watch_destination, expected_type=type_hints["cloud_watch_destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_bridge_destination", value=event_bridge_destination, expected_type=type_hints["event_bridge_destination"])
            check_type(argname="argument kinesis_firehose_destination", value=kinesis_firehose_destination, expected_type=type_hints["kinesis_firehose_destination"])
            check_type(argname="argument pinpoint_destination", value=pinpoint_destination, expected_type=type_hints["pinpoint_destination"])
            check_type(argname="argument sns_destination", value=sns_destination, expected_type=type_hints["sns_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matching_event_types": matching_event_types,
        }
        if cloud_watch_destination is not None:
            self._values["cloud_watch_destination"] = cloud_watch_destination
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bridge_destination is not None:
            self._values["event_bridge_destination"] = event_bridge_destination
        if kinesis_firehose_destination is not None:
            self._values["kinesis_firehose_destination"] = kinesis_firehose_destination
        if pinpoint_destination is not None:
            self._values["pinpoint_destination"] = pinpoint_destination
        if sns_destination is not None:
            self._values["sns_destination"] = sns_destination

    @builtins.property
    def matching_event_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#matching_event_types Sesv2ConfigurationSetEventDestination#matching_event_types}.'''
        result = self._values.get("matching_event_types")
        assert result is not None, "Required property 'matching_event_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloud_watch_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination"]:
        '''cloud_watch_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#cloud_watch_destination Sesv2ConfigurationSetEventDestination#cloud_watch_destination}
        '''
        result = self._values.get("cloud_watch_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#enabled Sesv2ConfigurationSetEventDestination#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_bridge_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination"]:
        '''event_bridge_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_bridge_destination Sesv2ConfigurationSetEventDestination#event_bridge_destination}
        '''
        result = self._values.get("event_bridge_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination"], result)

    @builtins.property
    def kinesis_firehose_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination"]:
        '''kinesis_firehose_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#kinesis_firehose_destination Sesv2ConfigurationSetEventDestination#kinesis_firehose_destination}
        '''
        result = self._values.get("kinesis_firehose_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination"], result)

    @builtins.property
    def pinpoint_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"]:
        '''pinpoint_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#pinpoint_destination Sesv2ConfigurationSetEventDestination#pinpoint_destination}
        '''
        result = self._values.get("pinpoint_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"], result)

    @builtins.property
    def sns_destination(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"]:
        '''sns_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#sns_destination Sesv2ConfigurationSetEventDestination#sns_destination}
        '''
        result = self._values.get("sns_destination")
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination",
    jsii_struct_bases=[],
    name_mapping={"dimension_configuration": "dimensionConfiguration"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination:
    def __init__(
        self,
        *,
        dimension_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param dimension_configuration: dimension_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_configuration Sesv2ConfigurationSetEventDestination#dimension_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433bac3fbd58f9facd450b181bcc4ea5bd996d7a1c915c9e8c56c6640e525776)
            check_type(argname="argument dimension_configuration", value=dimension_configuration, expected_type=type_hints["dimension_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dimension_configuration": dimension_configuration,
        }

    @builtins.property
    def dimension_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration"]]:
        '''dimension_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_configuration Sesv2ConfigurationSetEventDestination#dimension_configuration}
        '''
        result = self._values.get("dimension_configuration")
        assert result is not None, "Required property 'dimension_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "default_dimension_value": "defaultDimensionValue",
        "dimension_name": "dimensionName",
        "dimension_value_source": "dimensionValueSource",
    },
)
class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration:
    def __init__(
        self,
        *,
        default_dimension_value: builtins.str,
        dimension_name: builtins.str,
        dimension_value_source: builtins.str,
    ) -> None:
        '''
        :param default_dimension_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#default_dimension_value Sesv2ConfigurationSetEventDestination#default_dimension_value}.
        :param dimension_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_name Sesv2ConfigurationSetEventDestination#dimension_name}.
        :param dimension_value_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_value_source Sesv2ConfigurationSetEventDestination#dimension_value_source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0193bfb2d9985906fae28662b6674a46ef117a0eda16380cd39b5409fd6418d1)
            check_type(argname="argument default_dimension_value", value=default_dimension_value, expected_type=type_hints["default_dimension_value"])
            check_type(argname="argument dimension_name", value=dimension_name, expected_type=type_hints["dimension_name"])
            check_type(argname="argument dimension_value_source", value=dimension_value_source, expected_type=type_hints["dimension_value_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_dimension_value": default_dimension_value,
            "dimension_name": dimension_name,
            "dimension_value_source": dimension_value_source,
        }

    @builtins.property
    def default_dimension_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#default_dimension_value Sesv2ConfigurationSetEventDestination#default_dimension_value}.'''
        result = self._values.get("default_dimension_value")
        assert result is not None, "Required property 'default_dimension_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_name Sesv2ConfigurationSetEventDestination#dimension_name}.'''
        result = self._values.get("dimension_name")
        assert result is not None, "Required property 'dimension_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension_value_source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_value_source Sesv2ConfigurationSetEventDestination#dimension_value_source}.'''
        result = self._values.get("dimension_value_source")
        assert result is not None, "Required property 'dimension_value_source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76723ff37e1ddcf408598008ea6d5e09948a7f473207a2e61c68bc2148e2f348)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f766bb82d5073c59a5a08e4e64b93c41171997ff0c58955cf9600fcdb637da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c12d78c9d2911d2cc0098fe5d5399e6c06cfd5d76e1c14d0f807f3fbd2b4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c2e28185d39cefcbfe591fd4d54690d8da82bbd83f5bc0c90ef8373f6ed7c4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89fcd9cfaa365f2332819975ef0307abd85ef601539ba52f17c682243a34c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3fdb40006c970208102d8354867d77112f8c33f6830d3f4b39538689e84179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98a976bba6bceef310713887d6d0af6de16f91b2714a9c8e55089623431226cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="defaultDimensionValueInput")
    def default_dimension_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDimensionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionNameInput")
    def dimension_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionValueSourceInput")
    def dimension_value_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionValueSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDimensionValue")
    def default_dimension_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDimensionValue"))

    @default_dimension_value.setter
    def default_dimension_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eeccba9311063d2846cbdc8115dfe08f0eeb53f195d130d97e4a03fc9fb7891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDimensionValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensionName")
    def dimension_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionName"))

    @dimension_name.setter
    def dimension_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30785aacc0a3563bd268b0980efb55b5877c9498ebdfe63e22d9291e60d61e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensionValueSource")
    def dimension_value_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionValueSource"))

    @dimension_value_source.setter
    def dimension_value_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14afd891eb2bfbd7e50f6833a2fe3ded9cb2a18bf544fa85deb3e3f56b6689b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionValueSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12a7b33b1245b47b40058d0778deed6bf3c7d11cb0fd1fcad7caa3008eb547f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9b9cb85a8b02c3297acfd9710e0e0b39fe5e0ebbfa7a16507fa60be72a3150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimensionConfiguration")
    def put_dimension_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae2eaa6d064fef46c7469b2d0f2c203f2030b47bb6c13f22f8cc41a377a7c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimensionConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="dimensionConfiguration")
    def dimension_configuration(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList, jsii.get(self, "dimensionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dimensionConfigurationInput")
    def dimension_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]], jsii.get(self, "dimensionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb289c2f55618d1ade5ef33c251c041b0fe7159cb4a8e9c9d8502a76eef1606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination",
    jsii_struct_bases=[],
    name_mapping={"event_bus_arn": "eventBusArn"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination:
    def __init__(self, *, event_bus_arn: builtins.str) -> None:
        '''
        :param event_bus_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_bus_arn Sesv2ConfigurationSetEventDestination#event_bus_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a4a73e67101aea63cd8c9ca5e5c050f951173a226c91077073f8dd96f6385d)
            check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus_arn": event_bus_arn,
        }

    @builtins.property
    def event_bus_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_bus_arn Sesv2ConfigurationSetEventDestination#event_bus_arn}.'''
        result = self._values.get("event_bus_arn")
        assert result is not None, "Required property 'event_bus_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3977f86f38ce6331b7a637107936ec417d5e9b7a34ecd62e348d7c5213dd846d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventBusArnInput")
    def event_bus_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBusArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventBusArn"))

    @event_bus_arn.setter
    def event_bus_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b957f401a8c7a8288e7c7a8c8857ed5aa3da81dc39c7146fcacceabee2dc1236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBusArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a811510c081f51580c4f464e105d08e34b2ee33f789b8162a35553b320b2324b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_arn": "deliveryStreamArn",
        "iam_role_arn": "iamRoleArn",
    },
)
class Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination:
    def __init__(
        self,
        *,
        delivery_stream_arn: builtins.str,
        iam_role_arn: builtins.str,
    ) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#delivery_stream_arn Sesv2ConfigurationSetEventDestination#delivery_stream_arn}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#iam_role_arn Sesv2ConfigurationSetEventDestination#iam_role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f808556451e7b00bcc05eaa96d79e000560696b05e90ab83ba663153696f2eb)
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_arn": delivery_stream_arn,
            "iam_role_arn": iam_role_arn,
        }

    @builtins.property
    def delivery_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#delivery_stream_arn Sesv2ConfigurationSetEventDestination#delivery_stream_arn}.'''
        result = self._values.get("delivery_stream_arn")
        assert result is not None, "Required property 'delivery_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#iam_role_arn Sesv2ConfigurationSetEventDestination#iam_role_arn}.'''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c3aadaab2db19df366e3e591d51e89f42909639fcc773c3173394b4343b6834)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArnInput")
    def delivery_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleArnInput")
    def iam_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @delivery_stream_arn.setter
    def delivery_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478404331d99ddaa0c16b83bdaec86cc9007df17056e58e3dc28a55eba87ea67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb0e7c5ab03afdfe36dbaf175a95e3d6841dd243661e99b14570e43f5f19746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca35a8aece8479443ae5b023a3f154f647e3551c3d23a38b180f7d2d8543c5ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2e024d845954d316ed66f6085b0b5fd12c50d648c83f58edf5f141d2cb7982f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudWatchDestination")
    def put_cloud_watch_destination(
        self,
        *,
        dimension_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param dimension_configuration: dimension_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#dimension_configuration Sesv2ConfigurationSetEventDestination#dimension_configuration}
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination(
            dimension_configuration=dimension_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putCloudWatchDestination", [value]))

    @jsii.member(jsii_name="putEventBridgeDestination")
    def put_event_bridge_destination(self, *, event_bus_arn: builtins.str) -> None:
        '''
        :param event_bus_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#event_bus_arn Sesv2ConfigurationSetEventDestination#event_bus_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination(
            event_bus_arn=event_bus_arn
        )

        return typing.cast(None, jsii.invoke(self, "putEventBridgeDestination", [value]))

    @jsii.member(jsii_name="putKinesisFirehoseDestination")
    def put_kinesis_firehose_destination(
        self,
        *,
        delivery_stream_arn: builtins.str,
        iam_role_arn: builtins.str,
    ) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#delivery_stream_arn Sesv2ConfigurationSetEventDestination#delivery_stream_arn}.
        :param iam_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#iam_role_arn Sesv2ConfigurationSetEventDestination#iam_role_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination(
            delivery_stream_arn=delivery_stream_arn, iam_role_arn=iam_role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehoseDestination", [value]))

    @jsii.member(jsii_name="putPinpointDestination")
    def put_pinpoint_destination(self, *, application_arn: builtins.str) -> None:
        '''
        :param application_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#application_arn Sesv2ConfigurationSetEventDestination#application_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination(
            application_arn=application_arn
        )

        return typing.cast(None, jsii.invoke(self, "putPinpointDestination", [value]))

    @jsii.member(jsii_name="putSnsDestination")
    def put_sns_destination(self, *, topic_arn: builtins.str) -> None:
        '''
        :param topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#topic_arn Sesv2ConfigurationSetEventDestination#topic_arn}.
        '''
        value = Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination(
            topic_arn=topic_arn
        )

        return typing.cast(None, jsii.invoke(self, "putSnsDestination", [value]))

    @jsii.member(jsii_name="resetCloudWatchDestination")
    def reset_cloud_watch_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchDestination", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventBridgeDestination")
    def reset_event_bridge_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBridgeDestination", []))

    @jsii.member(jsii_name="resetKinesisFirehoseDestination")
    def reset_kinesis_firehose_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehoseDestination", []))

    @jsii.member(jsii_name="resetPinpointDestination")
    def reset_pinpoint_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPinpointDestination", []))

    @jsii.member(jsii_name="resetSnsDestination")
    def reset_sns_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnsDestination", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchDestination")
    def cloud_watch_destination(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference, jsii.get(self, "cloudWatchDestination"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeDestination")
    def event_bridge_destination(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference, jsii.get(self, "eventBridgeDestination"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseDestination")
    def kinesis_firehose_destination(
        self,
    ) -> Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference:
        return typing.cast(Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference, jsii.get(self, "kinesisFirehoseDestination"))

    @builtins.property
    @jsii.member(jsii_name="pinpointDestination")
    def pinpoint_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference":
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference", jsii.get(self, "pinpointDestination"))

    @builtins.property
    @jsii.member(jsii_name="snsDestination")
    def sns_destination(
        self,
    ) -> "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference":
        return typing.cast("Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference", jsii.get(self, "snsDestination"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchDestinationInput")
    def cloud_watch_destination_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination], jsii.get(self, "cloudWatchDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeDestinationInput")
    def event_bridge_destination_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination], jsii.get(self, "eventBridgeDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseDestinationInput")
    def kinesis_firehose_destination_input(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination], jsii.get(self, "kinesisFirehoseDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingEventTypesInput")
    def matching_event_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchingEventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="pinpointDestinationInput")
    def pinpoint_destination_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination"], jsii.get(self, "pinpointDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="snsDestinationInput")
    def sns_destination_input(
        self,
    ) -> typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"]:
        return typing.cast(typing.Optional["Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination"], jsii.get(self, "snsDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b4de3e34fec27589b36b71375b109cb42d533979fb5fb87936c999569e7ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchingEventTypes")
    def matching_event_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchingEventTypes"))

    @matching_event_types.setter
    def matching_event_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0a10d4396f66523c197cba2034c1434a7092137c05ac16727cf5ea112dcdad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingEventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a589edbe178cb2cb84d46ed50ad10645b83db403a96cc014badd42b4b677ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination",
    jsii_struct_bases=[],
    name_mapping={"application_arn": "applicationArn"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination:
    def __init__(self, *, application_arn: builtins.str) -> None:
        '''
        :param application_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#application_arn Sesv2ConfigurationSetEventDestination#application_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4feefd829427dccb4aed5f47cbf2a21c0baf2b88117df1724eba0b6cee1a4c01)
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_arn": application_arn,
        }

    @builtins.property
    def application_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#application_arn Sesv2ConfigurationSetEventDestination#application_arn}.'''
        result = self._values.get("application_arn")
        assert result is not None, "Required property 'application_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c78735540d1e9b156e0c7fc775ad4a20cc32f6bb450b23557a84dc5794d23528)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="applicationArnInput")
    def application_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @application_arn.setter
    def application_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105a6c8658a179c8bf3a55b5fcfec54d6b28e3fe61baad8fa9cd261e17918a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcf909dcfc6480aafd6c61e4943a96f92c7fd81b64f32f770608e31bb357089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination",
    jsii_struct_bases=[],
    name_mapping={"topic_arn": "topicArn"},
)
class Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination:
    def __init__(self, *, topic_arn: builtins.str) -> None:
        '''
        :param topic_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#topic_arn Sesv2ConfigurationSetEventDestination#topic_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affd264d7099fb25d867b34f3a5a61d84773420fdca4eb8de5957b7c8d3737b0)
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_arn": topic_arn,
        }

    @builtins.property
    def topic_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sesv2_configuration_set_event_destination#topic_arn Sesv2ConfigurationSetEventDestination#topic_arn}.'''
        result = self._values.get("topic_arn")
        assert result is not None, "Required property 'topic_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sesv2ConfigurationSetEventDestination.Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbf087a28d09edf3af50b56ceb4ceca0494d79d43b8c635edf24cf9bbb518010)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="topicArnInput")
    def topic_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicArn"))

    @topic_arn.setter
    def topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20868b750ffdf915fc5305d1e84418ab8da7c031a98ed46ea153c9d64b8428d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination]:
        return typing.cast(typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bcef80d74da1e35272a9ca1b2471a84e843114068717bf0964d9850822d0cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Sesv2ConfigurationSetEventDestination",
    "Sesv2ConfigurationSetEventDestinationConfig",
    "Sesv2ConfigurationSetEventDestinationEventDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationList",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfigurationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestinationOutputReference",
    "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination",
    "Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestinationOutputReference",
]

publication.publish()

def _typecheckingstub__e07f8d04197a0080cb9d3ecf0128d0e3ed4cc26598ad26d07d566c4b56aa968c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    configuration_set_name: builtins.str,
    event_destination: typing.Union[Sesv2ConfigurationSetEventDestinationEventDestination, typing.Dict[builtins.str, typing.Any]],
    event_destination_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6a9b6368e286d608a1ee2eceac3264e9eab8d34e01f9fb7c5e200d1c0d18854f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78151cb143c6986efa792563b5d7ac57ba7674d306f65635b1101f2015f47766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3285bb375e29a737e6c9cd9a42fafb77cfe8bad9f9c4c32cd6a471f9709a6ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f08374d7a9cf909ae90be54bdeb1c1ad56a12df7753e99c6c0592167cd8c72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e05f692cb9ba5a2405ef3f6925aa716850ceaebdb3657f2c5c210abc6e50ee(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    configuration_set_name: builtins.str,
    event_destination: typing.Union[Sesv2ConfigurationSetEventDestinationEventDestination, typing.Dict[builtins.str, typing.Any]],
    event_destination_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0036d6203c17ce2093e679cf9c942f608696ec640d51d61bec5b516ccd3628be(
    *,
    matching_event_types: typing.Sequence[builtins.str],
    cloud_watch_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_bridge_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_firehose_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    pinpoint_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    sns_destination: typing.Optional[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433bac3fbd58f9facd450b181bcc4ea5bd996d7a1c915c9e8c56c6640e525776(
    *,
    dimension_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0193bfb2d9985906fae28662b6674a46ef117a0eda16380cd39b5409fd6418d1(
    *,
    default_dimension_value: builtins.str,
    dimension_name: builtins.str,
    dimension_value_source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76723ff37e1ddcf408598008ea6d5e09948a7f473207a2e61c68bc2148e2f348(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f766bb82d5073c59a5a08e4e64b93c41171997ff0c58955cf9600fcdb637da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c12d78c9d2911d2cc0098fe5d5399e6c06cfd5d76e1c14d0f807f3fbd2b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2e28185d39cefcbfe591fd4d54690d8da82bbd83f5bc0c90ef8373f6ed7c4d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89fcd9cfaa365f2332819975ef0307abd85ef601539ba52f17c682243a34c49(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3fdb40006c970208102d8354867d77112f8c33f6830d3f4b39538689e84179(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a976bba6bceef310713887d6d0af6de16f91b2714a9c8e55089623431226cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eeccba9311063d2846cbdc8115dfe08f0eeb53f195d130d97e4a03fc9fb7891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30785aacc0a3563bd268b0980efb55b5877c9498ebdfe63e22d9291e60d61e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14afd891eb2bfbd7e50f6833a2fe3ded9cb2a18bf544fa85deb3e3f56b6689b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12a7b33b1245b47b40058d0778deed6bf3c7d11cb0fd1fcad7caa3008eb547f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9b9cb85a8b02c3297acfd9710e0e0b39fe5e0ebbfa7a16507fa60be72a3150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae2eaa6d064fef46c7469b2d0f2c203f2030b47bb6c13f22f8cc41a377a7c5f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestinationDimensionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb289c2f55618d1ade5ef33c251c041b0fe7159cb4a8e9c9d8502a76eef1606(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationCloudWatchDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a4a73e67101aea63cd8c9ca5e5c050f951173a226c91077073f8dd96f6385d(
    *,
    event_bus_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3977f86f38ce6331b7a637107936ec417d5e9b7a34ecd62e348d7c5213dd846d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b957f401a8c7a8288e7c7a8c8857ed5aa3da81dc39c7146fcacceabee2dc1236(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a811510c081f51580c4f464e105d08e34b2ee33f789b8162a35553b320b2324b(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationEventBridgeDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f808556451e7b00bcc05eaa96d79e000560696b05e90ab83ba663153696f2eb(
    *,
    delivery_stream_arn: builtins.str,
    iam_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3aadaab2db19df366e3e591d51e89f42909639fcc773c3173394b4343b6834(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478404331d99ddaa0c16b83bdaec86cc9007df17056e58e3dc28a55eba87ea67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb0e7c5ab03afdfe36dbaf175a95e3d6841dd243661e99b14570e43f5f19746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca35a8aece8479443ae5b023a3f154f647e3551c3d23a38b180f7d2d8543c5ef(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e024d845954d316ed66f6085b0b5fd12c50d648c83f58edf5f141d2cb7982f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b4de3e34fec27589b36b71375b109cb42d533979fb5fb87936c999569e7ad2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0a10d4396f66523c197cba2034c1434a7092137c05ac16727cf5ea112dcdad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a589edbe178cb2cb84d46ed50ad10645b83db403a96cc014badd42b4b677ed7(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feefd829427dccb4aed5f47cbf2a21c0baf2b88117df1724eba0b6cee1a4c01(
    *,
    application_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78735540d1e9b156e0c7fc775ad4a20cc32f6bb450b23557a84dc5794d23528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105a6c8658a179c8bf3a55b5fcfec54d6b28e3fe61baad8fa9cd261e17918a5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcf909dcfc6480aafd6c61e4943a96f92c7fd81b64f32f770608e31bb357089(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationPinpointDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affd264d7099fb25d867b34f3a5a61d84773420fdca4eb8de5957b7c8d3737b0(
    *,
    topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf087a28d09edf3af50b56ceb4ceca0494d79d43b8c635edf24cf9bbb518010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20868b750ffdf915fc5305d1e84418ab8da7c031a98ed46ea153c9d64b8428d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bcef80d74da1e35272a9ca1b2471a84e843114068717bf0964d9850822d0cd(
    value: typing.Optional[Sesv2ConfigurationSetEventDestinationEventDestinationSnsDestination],
) -> None:
    """Type checking stubs"""
    pass
