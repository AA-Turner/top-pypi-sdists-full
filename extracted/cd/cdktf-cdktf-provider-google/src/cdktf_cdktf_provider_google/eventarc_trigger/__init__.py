r'''
# `google_eventarc_trigger`

Refer to the Terraform Registry for docs: [`google_eventarc_trigger`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger).
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


class EventarcTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger google_eventarc_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: typing.Union["EventarcTriggerDestination", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcTriggerMatchingCriteria", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        channel: typing.Optional[builtins.str] = None,
        event_data_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["EventarcTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transport: typing.Optional[typing.Union["EventarcTriggerTransport", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger google_eventarc_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#destination EventarcTrigger#destination}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#location EventarcTrigger#location}
        :param matching_criteria: matching_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#matching_criteria EventarcTrigger#matching_criteria}
        :param name: Required. The resource name of the trigger. Must be unique within the location on the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#name EventarcTrigger#name}
        :param channel: Optional. The name of the channel associated with the trigger in 'projects/{project}/locations/{location}/channels/{channel}' format. You must provide a channel to receive events from Eventarc SaaS partners. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#channel EventarcTrigger#channel}
        :param event_data_content_type: Optional. EventDataContentType specifies the type of payload in MIME format that is expected from the CloudEvent data field. This is set to 'application/json' if the value is not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#event_data_content_type EventarcTrigger#event_data_content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#id EventarcTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User labels attached to the triggers that can be used to group resources. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#labels EventarcTrigger#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#project EventarcTrigger#project}.
        :param service_account: Optional. The IAM service account email associated with the trigger. The service account represents the identity of the trigger. The principal who calls this API must have 'iam.serviceAccounts.actAs' permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts#sa_common for more information. For Cloud Run destinations, this service account is used to generate identity tokens when invoking the service. See https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account for information on how to invoke authenticated Cloud Run services. In order to create Audit Log triggers, the service account should also have 'roles/eventarc.eventReceiver' IAM role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service_account EventarcTrigger#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#timeouts EventarcTrigger#timeouts}
        :param transport: transport block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#transport EventarcTrigger#transport}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dfd0bfab5d5b7cea0710cdd5eb91876cbbe3c632628990347af726286ee6c0d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventarcTriggerConfig(
            destination=destination,
            location=location,
            matching_criteria=matching_criteria,
            name=name,
            channel=channel,
            event_data_content_type=event_data_content_type,
            id=id,
            labels=labels,
            project=project,
            service_account=service_account,
            timeouts=timeouts,
            transport=transport,
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
        '''Generates CDKTF code for importing a EventarcTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventarcTrigger to import.
        :param import_from_id: The id of the existing EventarcTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventarcTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900989b68a5bbf34524c0479c3efbf8df789b29a03dc574b2b9d4f9e3cb4a965)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        cloud_run_service: typing.Optional[typing.Union["EventarcTriggerDestinationCloudRunService", typing.Dict[builtins.str, typing.Any]]] = None,
        gke: typing.Optional[typing.Union["EventarcTriggerDestinationGke", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint: typing.Optional[typing.Union["EventarcTriggerDestinationHttpEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["EventarcTriggerDestinationNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_run_service: cloud_run_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#cloud_run_service EventarcTrigger#cloud_run_service}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#gke EventarcTrigger#gke}
        :param http_endpoint: http_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#http_endpoint EventarcTrigger#http_endpoint}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#network_config EventarcTrigger#network_config}
        :param workflow: The resource name of the Workflow whose Executions are triggered by the events. The Workflow resource should be deployed in the same project as the trigger. Format: 'projects/{project}/locations/{location}/workflows/{workflow}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#workflow EventarcTrigger#workflow}
        '''
        value = EventarcTriggerDestination(
            cloud_run_service=cloud_run_service,
            gke=gke,
            http_endpoint=http_endpoint,
            network_config=network_config,
            workflow=workflow,
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="putMatchingCriteria")
    def put_matching_criteria(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcTriggerMatchingCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca007c42d63ea8be1d9f3689e7fa7fd0e2bba2610e581a6a898bf48fa317c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchingCriteria", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#create EventarcTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#delete EventarcTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#update EventarcTrigger#update}.
        '''
        value = EventarcTriggerTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTransport")
    def put_transport(
        self,
        *,
        pubsub: typing.Optional[typing.Union["EventarcTriggerTransportPubsub", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param pubsub: pubsub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#pubsub EventarcTrigger#pubsub}
        '''
        value = EventarcTriggerTransport(pubsub=pubsub)

        return typing.cast(None, jsii.invoke(self, "putTransport", [value]))

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetEventDataContentType")
    def reset_event_data_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventDataContentType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransport")
    def reset_transport(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransport", []))

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
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> "EventarcTriggerDestinationOutputReference":
        return typing.cast("EventarcTriggerDestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="matchingCriteria")
    def matching_criteria(self) -> "EventarcTriggerMatchingCriteriaList":
        return typing.cast("EventarcTriggerMatchingCriteriaList", jsii.get(self, "matchingCriteria"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EventarcTriggerTimeoutsOutputReference":
        return typing.cast("EventarcTriggerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> "EventarcTriggerTransportOutputReference":
        return typing.cast("EventarcTriggerTransportOutputReference", jsii.get(self, "transport"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional["EventarcTriggerDestination"]:
        return typing.cast(typing.Optional["EventarcTriggerDestination"], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="eventDataContentTypeInput")
    def event_data_content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventDataContentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingCriteriaInput")
    def matching_criteria_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcTriggerMatchingCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcTriggerMatchingCriteria"]]], jsii.get(self, "matchingCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventarcTriggerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EventarcTriggerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional["EventarcTriggerTransport"]:
        return typing.cast(typing.Optional["EventarcTriggerTransport"], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715242e595df1461f2ceee56e8d262feb72ac29cc75326b5b18bec1a55fac068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDataContentType")
    def event_data_content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDataContentType"))

    @event_data_content_type.setter
    def event_data_content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861053e4fed81f1ca805e3a340f9b58b6612147c8b00885715066baa62486916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDataContentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6d2fd785f3c545c09ed01547ea57233c02736b3ebc9c3c4c6f3c86d373b653e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5cf00e8ba89c3f2e6f7af44d80f550c1262fbf6751eeecd6c3c45aea9ef0fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11a9aff2fd59e743b8acf7420facc7b43f7f1bd27c038291e6655b30191c4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2d53d9afbf4a325fd3b4954275613fbb9d3136058a17194f06a76d3207f8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdd41480c5d6f3219b62f302556a7dab4591361b0c7521a28040e4705b2883c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5583d8197067769c39e02983dbff41740533ebc07d2953f44ed26345a1972e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination": "destination",
        "location": "location",
        "matching_criteria": "matchingCriteria",
        "name": "name",
        "channel": "channel",
        "event_data_content_type": "eventDataContentType",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "service_account": "serviceAccount",
        "timeouts": "timeouts",
        "transport": "transport",
    },
)
class EventarcTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination: typing.Union["EventarcTriggerDestination", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventarcTriggerMatchingCriteria", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        channel: typing.Optional[builtins.str] = None,
        event_data_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["EventarcTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transport: typing.Optional[typing.Union["EventarcTriggerTransport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#destination EventarcTrigger#destination}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#location EventarcTrigger#location}
        :param matching_criteria: matching_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#matching_criteria EventarcTrigger#matching_criteria}
        :param name: Required. The resource name of the trigger. Must be unique within the location on the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#name EventarcTrigger#name}
        :param channel: Optional. The name of the channel associated with the trigger in 'projects/{project}/locations/{location}/channels/{channel}' format. You must provide a channel to receive events from Eventarc SaaS partners. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#channel EventarcTrigger#channel}
        :param event_data_content_type: Optional. EventDataContentType specifies the type of payload in MIME format that is expected from the CloudEvent data field. This is set to 'application/json' if the value is not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#event_data_content_type EventarcTrigger#event_data_content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#id EventarcTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User labels attached to the triggers that can be used to group resources. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#labels EventarcTrigger#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#project EventarcTrigger#project}.
        :param service_account: Optional. The IAM service account email associated with the trigger. The service account represents the identity of the trigger. The principal who calls this API must have 'iam.serviceAccounts.actAs' permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts#sa_common for more information. For Cloud Run destinations, this service account is used to generate identity tokens when invoking the service. See https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account for information on how to invoke authenticated Cloud Run services. In order to create Audit Log triggers, the service account should also have 'roles/eventarc.eventReceiver' IAM role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service_account EventarcTrigger#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#timeouts EventarcTrigger#timeouts}
        :param transport: transport block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#transport EventarcTrigger#transport}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = EventarcTriggerDestination(**destination)
        if isinstance(timeouts, dict):
            timeouts = EventarcTriggerTimeouts(**timeouts)
        if isinstance(transport, dict):
            transport = EventarcTriggerTransport(**transport)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea77347f2d90b712a0b2c53c1246348b279c4926eb4fc109baabb3e421f99d11)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument matching_criteria", value=matching_criteria, expected_type=type_hints["matching_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument event_data_content_type", value=event_data_content_type, expected_type=type_hints["event_data_content_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "location": location,
            "matching_criteria": matching_criteria,
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
        if channel is not None:
            self._values["channel"] = channel
        if event_data_content_type is not None:
            self._values["event_data_content_type"] = event_data_content_type
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if service_account is not None:
            self._values["service_account"] = service_account
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transport is not None:
            self._values["transport"] = transport

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
    def destination(self) -> "EventarcTriggerDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#destination EventarcTrigger#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("EventarcTriggerDestination", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#location EventarcTrigger#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def matching_criteria(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcTriggerMatchingCriteria"]]:
        '''matching_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#matching_criteria EventarcTrigger#matching_criteria}
        '''
        result = self._values.get("matching_criteria")
        assert result is not None, "Required property 'matching_criteria' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventarcTriggerMatchingCriteria"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. The resource name of the trigger. Must be unique within the location on the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#name EventarcTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the channel associated with the trigger in 'projects/{project}/locations/{location}/channels/{channel}' format. You must provide a channel to receive events from Eventarc SaaS partners.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#channel EventarcTrigger#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_data_content_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        EventDataContentType specifies the type of payload in MIME format that is expected from the CloudEvent data field. This is set to 'application/json' if the value is not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#event_data_content_type EventarcTrigger#event_data_content_type}
        '''
        result = self._values.get("event_data_content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#id EventarcTrigger#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User labels attached to the triggers that can be used to group resources.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#labels EventarcTrigger#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#project EventarcTrigger#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The IAM service account email associated with the trigger. The service account represents the identity of the trigger. The principal who calls this API must have 'iam.serviceAccounts.actAs' permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts#sa_common for more information. For Cloud Run destinations, this service account is used to generate identity tokens when invoking the service. See https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account for information on how to invoke authenticated Cloud Run services. In order to create Audit Log triggers, the service account should also have 'roles/eventarc.eventReceiver' IAM role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service_account EventarcTrigger#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EventarcTriggerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#timeouts EventarcTrigger#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EventarcTriggerTimeouts"], result)

    @builtins.property
    def transport(self) -> typing.Optional["EventarcTriggerTransport"]:
        '''transport block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#transport EventarcTrigger#transport}
        '''
        result = self._values.get("transport")
        return typing.cast(typing.Optional["EventarcTriggerTransport"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestination",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_run_service": "cloudRunService",
        "gke": "gke",
        "http_endpoint": "httpEndpoint",
        "network_config": "networkConfig",
        "workflow": "workflow",
    },
)
class EventarcTriggerDestination:
    def __init__(
        self,
        *,
        cloud_run_service: typing.Optional[typing.Union["EventarcTriggerDestinationCloudRunService", typing.Dict[builtins.str, typing.Any]]] = None,
        gke: typing.Optional[typing.Union["EventarcTriggerDestinationGke", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint: typing.Optional[typing.Union["EventarcTriggerDestinationHttpEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["EventarcTriggerDestinationNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_run_service: cloud_run_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#cloud_run_service EventarcTrigger#cloud_run_service}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#gke EventarcTrigger#gke}
        :param http_endpoint: http_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#http_endpoint EventarcTrigger#http_endpoint}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#network_config EventarcTrigger#network_config}
        :param workflow: The resource name of the Workflow whose Executions are triggered by the events. The Workflow resource should be deployed in the same project as the trigger. Format: 'projects/{project}/locations/{location}/workflows/{workflow}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#workflow EventarcTrigger#workflow}
        '''
        if isinstance(cloud_run_service, dict):
            cloud_run_service = EventarcTriggerDestinationCloudRunService(**cloud_run_service)
        if isinstance(gke, dict):
            gke = EventarcTriggerDestinationGke(**gke)
        if isinstance(http_endpoint, dict):
            http_endpoint = EventarcTriggerDestinationHttpEndpoint(**http_endpoint)
        if isinstance(network_config, dict):
            network_config = EventarcTriggerDestinationNetworkConfig(**network_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d90c01d956e6ab3fc865a290e481b87d76aeef8ac2a05732e8b068d9bee38e)
            check_type(argname="argument cloud_run_service", value=cloud_run_service, expected_type=type_hints["cloud_run_service"])
            check_type(argname="argument gke", value=gke, expected_type=type_hints["gke"])
            check_type(argname="argument http_endpoint", value=http_endpoint, expected_type=type_hints["http_endpoint"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_run_service is not None:
            self._values["cloud_run_service"] = cloud_run_service
        if gke is not None:
            self._values["gke"] = gke
        if http_endpoint is not None:
            self._values["http_endpoint"] = http_endpoint
        if network_config is not None:
            self._values["network_config"] = network_config
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def cloud_run_service(
        self,
    ) -> typing.Optional["EventarcTriggerDestinationCloudRunService"]:
        '''cloud_run_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#cloud_run_service EventarcTrigger#cloud_run_service}
        '''
        result = self._values.get("cloud_run_service")
        return typing.cast(typing.Optional["EventarcTriggerDestinationCloudRunService"], result)

    @builtins.property
    def gke(self) -> typing.Optional["EventarcTriggerDestinationGke"]:
        '''gke block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#gke EventarcTrigger#gke}
        '''
        result = self._values.get("gke")
        return typing.cast(typing.Optional["EventarcTriggerDestinationGke"], result)

    @builtins.property
    def http_endpoint(
        self,
    ) -> typing.Optional["EventarcTriggerDestinationHttpEndpoint"]:
        '''http_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#http_endpoint EventarcTrigger#http_endpoint}
        '''
        result = self._values.get("http_endpoint")
        return typing.cast(typing.Optional["EventarcTriggerDestinationHttpEndpoint"], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["EventarcTriggerDestinationNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#network_config EventarcTrigger#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["EventarcTriggerDestinationNetworkConfig"], result)

    @builtins.property
    def workflow(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Workflow whose Executions are triggered by the events.

        The Workflow resource should be deployed in the same project as the trigger. Format: 'projects/{project}/locations/{location}/workflows/{workflow}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#workflow EventarcTrigger#workflow}
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationCloudRunService",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "path": "path", "region": "region"},
)
class EventarcTriggerDestinationCloudRunService:
    def __init__(
        self,
        *,
        service: builtins.str,
        path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Required. The name of the Cloud Run service being addressed. See https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services. Only services located in the same project of the trigger object can be addressed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service EventarcTrigger#service}
        :param path: Optional. The relative path on the Cloud Run service the events should be sent to. The value must conform to the definition of URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#path EventarcTrigger#path}
        :param region: Required. The region the Cloud Run service is deployed in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#region EventarcTrigger#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c28df834889a18c0d3a1b35fe0c4339c84952053718bbd810dff9c83a17ba6)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if path is not None:
            self._values["path"] = path
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def service(self) -> builtins.str:
        '''Required.

        The name of the Cloud Run service being addressed. See https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services. Only services located in the same project of the trigger object can be addressed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service EventarcTrigger#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The relative path on the Cloud Run service the events should be sent to. The value must conform to the definition of URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#path EventarcTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Required. The region the Cloud Run service is deployed in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#region EventarcTrigger#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerDestinationCloudRunService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerDestinationCloudRunServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationCloudRunServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a019dc4fe203b55dbbb5b89a4219e243025d0792d85fd6b62fcc0bf770621e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58f40c0b755aa48a4bf4ab34b8ff2b1ae4ebb26a94cc66e78dd5f27caf0b773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9197235b21d345898fd50a6aa55370279f17d57b2e1a560b9065ddef97ffd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01650c43b4d2b52da8e9945485118a126e259c340dea0c99411c27dc49920b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcTriggerDestinationCloudRunService]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationCloudRunService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcTriggerDestinationCloudRunService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595304680ffaf05457ccb04a3246ae0afdd507e22eefb86e259172606e1be4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationGke",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "location": "location",
        "namespace": "namespace",
        "service": "service",
        "path": "path",
    },
)
class EventarcTriggerDestinationGke:
    def __init__(
        self,
        *,
        cluster: builtins.str,
        location: builtins.str,
        namespace: builtins.str,
        service: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Required. The name of the cluster the GKE service is running in. The cluster must be running in the same project as the trigger being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#cluster EventarcTrigger#cluster}
        :param location: Required. The name of the Google Compute Engine in which the cluster resides, which can either be compute zone (for example, us-central1-a) for the zonal clusters or region (for example, us-central1) for regional clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#location EventarcTrigger#location}
        :param namespace: Required. The namespace the GKE service is running in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#namespace EventarcTrigger#namespace}
        :param service: Required. Name of the GKE service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service EventarcTrigger#service}
        :param path: Optional. The relative path on the GKE service the events should be sent to. The value must conform to the definition of a URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#path EventarcTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea9e3b6a743fe69de5f30f820a55c48c61ed14da854fb482d165f0ebdfb1e8a)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "location": location,
            "namespace": namespace,
            "service": service,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def cluster(self) -> builtins.str:
        '''Required.

        The name of the cluster the GKE service is running in. The cluster must be running in the same project as the trigger being created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#cluster EventarcTrigger#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Required.

        The name of the Google Compute Engine in which the cluster resides, which can either be compute zone (for example, us-central1-a) for the zonal clusters or region (for example, us-central1) for regional clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#location EventarcTrigger#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Required. The namespace the GKE service is running in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#namespace EventarcTrigger#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. Name of the GKE service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service EventarcTrigger#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The relative path on the GKE service the events should be sent to. The value must conform to the definition of a URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#path EventarcTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerDestinationGke(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerDestinationGkeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationGkeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__160f709e3e1345414d16a7c3a0732fbf6ea30290a33ec42b96cf334f6633b5a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2509440bbaa6e6706e363f573d56df020e6ca9a5f27269c34084accedae27d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3959bbbb9fbc4c6ddbd4895d79f2a4452b11b16fd2666cd474210b468feffa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d3cb7c129bb67f16c90b713c183d3412ee8b85af2b54797e5b73f8232b5c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034724e9e3c608d36c66c5e7d6160ba8d6bf71ae51cf156b3c954b55d36f9ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5b7fd19a60484a8462800c58b10d4c39f87c4300c74c567a887149f04b73d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcTriggerDestinationGke]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationGke], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcTriggerDestinationGke],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b21c0d1046031a141a2e347fc8d1d085a9eddf29f3276379d9eaa1716b8e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationHttpEndpoint",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class EventarcTriggerDestinationHttpEndpoint:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: Required. The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'http://10.10.10.8:80/route', 'http://svc.us-central1.p.local:8080/'. Only HTTP and HTTPS protocols are supported. The host can be either a static IP addressable from the VPC specified by the network config, or an internal DNS hostname of the service resolvable via Cloud DNS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#uri EventarcTrigger#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d258f047396a23a4a6ece456fff7295561c483ef5b75cd32c844936f6b263ae)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required.

        The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'http://10.10.10.8:80/route', 'http://svc.us-central1.p.local:8080/'. Only HTTP and HTTPS protocols are supported. The host can be either a static IP addressable from the VPC specified by the network config, or an internal DNS hostname of the service resolvable via Cloud DNS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#uri EventarcTrigger#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerDestinationHttpEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerDestinationHttpEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationHttpEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e8679419bbc2fb21856f3cc65166fb314510c8cc064207dd0d04ae85aea32d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0eac87de2d9dc84c73b071fbc61c50c75604b75b93bf9d307903662b20d16b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcTriggerDestinationHttpEndpoint]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationHttpEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcTriggerDestinationHttpEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fbacc9a77dadd03b5cde2bb72989f1bdab771d9679523c2e44d1c74cf6f1443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"network_attachment": "networkAttachment"},
)
class EventarcTriggerDestinationNetworkConfig:
    def __init__(self, *, network_attachment: builtins.str) -> None:
        '''
        :param network_attachment: Required. Name of the NetworkAttachment that allows access to the destination VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#network_attachment EventarcTrigger#network_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5173b463442b84c5f71c32263c372fdfdb3f843befd8a2ed6db2db424abcc1ee)
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_attachment": network_attachment,
        }

    @builtins.property
    def network_attachment(self) -> builtins.str:
        '''Required. Name of the NetworkAttachment that allows access to the destination VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#network_attachment EventarcTrigger#network_attachment}
        '''
        result = self._values.get("network_attachment")
        assert result is not None, "Required property 'network_attachment' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerDestinationNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerDestinationNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24d27d80b4e90f4ca1a5f54514a67af8602df96112f2e0c9023827e7005c89a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentInput")
    def network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7600050a8081de7e502134be6b3ed5c5dfa3593e0ee4b40112cb6e39c330efe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventarcTriggerDestinationNetworkConfig]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcTriggerDestinationNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfa47b5f400a728a1096515b2aa606601276e644e4ef617b1cadeeefcc8861c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcTriggerDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b5af12b7900369fe0755eaa91f43ae4bde2cbe47a64212605f61efc871c827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudRunService")
    def put_cloud_run_service(
        self,
        *,
        service: builtins.str,
        path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Required. The name of the Cloud Run service being addressed. See https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services. Only services located in the same project of the trigger object can be addressed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service EventarcTrigger#service}
        :param path: Optional. The relative path on the Cloud Run service the events should be sent to. The value must conform to the definition of URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#path EventarcTrigger#path}
        :param region: Required. The region the Cloud Run service is deployed in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#region EventarcTrigger#region}
        '''
        value = EventarcTriggerDestinationCloudRunService(
            service=service, path=path, region=region
        )

        return typing.cast(None, jsii.invoke(self, "putCloudRunService", [value]))

    @jsii.member(jsii_name="putGke")
    def put_gke(
        self,
        *,
        cluster: builtins.str,
        location: builtins.str,
        namespace: builtins.str,
        service: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Required. The name of the cluster the GKE service is running in. The cluster must be running in the same project as the trigger being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#cluster EventarcTrigger#cluster}
        :param location: Required. The name of the Google Compute Engine in which the cluster resides, which can either be compute zone (for example, us-central1-a) for the zonal clusters or region (for example, us-central1) for regional clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#location EventarcTrigger#location}
        :param namespace: Required. The namespace the GKE service is running in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#namespace EventarcTrigger#namespace}
        :param service: Required. Name of the GKE service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#service EventarcTrigger#service}
        :param path: Optional. The relative path on the GKE service the events should be sent to. The value must conform to the definition of a URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#path EventarcTrigger#path}
        '''
        value = EventarcTriggerDestinationGke(
            cluster=cluster,
            location=location,
            namespace=namespace,
            service=service,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putGke", [value]))

    @jsii.member(jsii_name="putHttpEndpoint")
    def put_http_endpoint(self, *, uri: builtins.str) -> None:
        '''
        :param uri: Required. The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'http://10.10.10.8:80/route', 'http://svc.us-central1.p.local:8080/'. Only HTTP and HTTPS protocols are supported. The host can be either a static IP addressable from the VPC specified by the network config, or an internal DNS hostname of the service resolvable via Cloud DNS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#uri EventarcTrigger#uri}
        '''
        value = EventarcTriggerDestinationHttpEndpoint(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putHttpEndpoint", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(self, *, network_attachment: builtins.str) -> None:
        '''
        :param network_attachment: Required. Name of the NetworkAttachment that allows access to the destination VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#network_attachment EventarcTrigger#network_attachment}
        '''
        value = EventarcTriggerDestinationNetworkConfig(
            network_attachment=network_attachment
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="resetCloudRunService")
    def reset_cloud_run_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRunService", []))

    @jsii.member(jsii_name="resetGke")
    def reset_gke(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGke", []))

    @jsii.member(jsii_name="resetHttpEndpoint")
    def reset_http_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpEndpoint", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetWorkflow")
    def reset_workflow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflow", []))

    @builtins.property
    @jsii.member(jsii_name="cloudFunction")
    def cloud_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudFunction"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunService")
    def cloud_run_service(
        self,
    ) -> EventarcTriggerDestinationCloudRunServiceOutputReference:
        return typing.cast(EventarcTriggerDestinationCloudRunServiceOutputReference, jsii.get(self, "cloudRunService"))

    @builtins.property
    @jsii.member(jsii_name="gke")
    def gke(self) -> EventarcTriggerDestinationGkeOutputReference:
        return typing.cast(EventarcTriggerDestinationGkeOutputReference, jsii.get(self, "gke"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpoint")
    def http_endpoint(self) -> EventarcTriggerDestinationHttpEndpointOutputReference:
        return typing.cast(EventarcTriggerDestinationHttpEndpointOutputReference, jsii.get(self, "httpEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> EventarcTriggerDestinationNetworkConfigOutputReference:
        return typing.cast(EventarcTriggerDestinationNetworkConfigOutputReference, jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunServiceInput")
    def cloud_run_service_input(
        self,
    ) -> typing.Optional[EventarcTriggerDestinationCloudRunService]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationCloudRunService], jsii.get(self, "cloudRunServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeInput")
    def gke_input(self) -> typing.Optional[EventarcTriggerDestinationGke]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationGke], jsii.get(self, "gkeInput"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointInput")
    def http_endpoint_input(
        self,
    ) -> typing.Optional[EventarcTriggerDestinationHttpEndpoint]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationHttpEndpoint], jsii.get(self, "httpEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional[EventarcTriggerDestinationNetworkConfig]:
        return typing.cast(typing.Optional[EventarcTriggerDestinationNetworkConfig], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowInput")
    def workflow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workflowInput"))

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflow"))

    @workflow.setter
    def workflow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f62cf7a1d6ad19648e8e39fb6719dce2217fd7f4da2f41cb6707baa9989ed70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcTriggerDestination]:
        return typing.cast(typing.Optional[EventarcTriggerDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcTriggerDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7aabd4cfc4a6f79318a2f3449fb320a5b89fd7d0e246e3202bd41f95c42fae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerMatchingCriteria",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute", "value": "value", "operator": "operator"},
)
class EventarcTriggerMatchingCriteria:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        value: builtins.str,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: Required. The name of a CloudEvents attribute. Currently, only a subset of attributes are supported for filtering. All triggers MUST provide a filter for the 'type' attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#attribute EventarcTrigger#attribute}
        :param value: Required. The value for the attribute. See https://cloud.google.com/eventarc/docs/creating-triggers#trigger-gcloud for available values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#value EventarcTrigger#value}
        :param operator: Optional. The operator used for matching the events with the value of the filter. If not specified, only events that have an exact key-value pair specified in the filter are matched. The only allowed value is 'match-path-pattern'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#operator EventarcTrigger#operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88c2fa39d157faa28a8024b7af6c4069d0eae5381f502bf65d15da1d7009436)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute": attribute,
            "value": value,
        }
        if operator is not None:
            self._values["operator"] = operator

    @builtins.property
    def attribute(self) -> builtins.str:
        '''Required.

        The name of a CloudEvents attribute. Currently, only a subset of attributes are supported for filtering. All triggers MUST provide a filter for the 'type' attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#attribute EventarcTrigger#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Required. The value for the attribute. See https://cloud.google.com/eventarc/docs/creating-triggers#trigger-gcloud for available values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#value EventarcTrigger#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The operator used for matching the events with the value of the filter. If not specified, only events that have an exact key-value pair specified in the filter are matched. The only allowed value is 'match-path-pattern'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#operator EventarcTrigger#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerMatchingCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerMatchingCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerMatchingCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6b120486fef4c8547983e80575b147cc1e64bf22751f3d9294c4125fac8a23a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventarcTriggerMatchingCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042ec167edef8c9334685f7eb7f7c09293bfb09020a1c62a2af60d27917e6a10)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventarcTriggerMatchingCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d2972f0b7dc87040ce54dd9ae1b522fa2e525afe47abde4eab99bd79fc704a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__061954e313658fe8e06eb2cf79a073334a2b8588360aede5d07f7a0f6563e66e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__133d7186ba0f4ef6decc7f189f4a1bf6612f5f2dd3d770259247cd34c0fe49a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcTriggerMatchingCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcTriggerMatchingCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcTriggerMatchingCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8e4011557253db8c844a78e0b3c852d4c697d62afd8dbde28487cc7d5e10e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventarcTriggerMatchingCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerMatchingCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3128857dadad820f2ab5351c50c523396c11efe23694baf0b3d6c9da429cb98f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fe02878191f8c9e1c1159ecb6b818ef07a5528e1368a7a35f0c33999c0cacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0450fce43641d91113079b0037046e50b6659ee43c3b49925a0e77c38fa68aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92be92191849d8bf8459c05279285b99e55f0fc7b22c0ea70e40efcc5c68a6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerMatchingCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerMatchingCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerMatchingCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f344924af5b6ac3e7b1c43b31ed22e508874a28b995a60d585e68402f9ce30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EventarcTriggerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#create EventarcTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#delete EventarcTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#update EventarcTrigger#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3a4a5190a2b77fdac07902af27fb7cc35ee44a016b4505b6213c0c255a307d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#create EventarcTrigger#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#delete EventarcTrigger#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#update EventarcTrigger#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7c42fa2c2c2102130162a58ddc3e3a0db74d8be47fc1c4585f5be1acec2e0c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__854833bd90a5ecbb8fee83e24669927321878d3cfe7fdd1e3f01d26855d5a8d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451a06a686a2cc3b3c6022ad0e6351fd9289dbc9e3face45d47c4e7526175d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ab4e40f676cc698b19d619bcfb2f5c2beea90776d5d555b030ec5d7907d39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a1399cdc5db9e7ec393eefa083763c47af5cad880e461384b996fd3b1a99f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerTransport",
    jsii_struct_bases=[],
    name_mapping={"pubsub": "pubsub"},
)
class EventarcTriggerTransport:
    def __init__(
        self,
        *,
        pubsub: typing.Optional[typing.Union["EventarcTriggerTransportPubsub", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param pubsub: pubsub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#pubsub EventarcTrigger#pubsub}
        '''
        if isinstance(pubsub, dict):
            pubsub = EventarcTriggerTransportPubsub(**pubsub)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd105d8c151c5b176dbdbba4975e6c2206cce7b05a07e38b0ac57aa4cd541b22)
            check_type(argname="argument pubsub", value=pubsub, expected_type=type_hints["pubsub"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pubsub is not None:
            self._values["pubsub"] = pubsub

    @builtins.property
    def pubsub(self) -> typing.Optional["EventarcTriggerTransportPubsub"]:
        '''pubsub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#pubsub EventarcTrigger#pubsub}
        '''
        result = self._values.get("pubsub")
        return typing.cast(typing.Optional["EventarcTriggerTransportPubsub"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerTransport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerTransportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerTransportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c04668aecdbe5666d827629ac4761eb7b5d7f5a62b0980e80fcb4a6bc2548bd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsub")
    def put_pubsub(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: Optional. The name of the Pub/Sub topic created and managed by Eventarc system as a transport for the event delivery. Format: 'projects/{PROJECT_ID}/topics/{TOPIC_NAME}. You may set an existing topic for triggers of the type google.cloud.pubsub.topic.v1.messagePublished' only. The topic you provide here will not be deleted by Eventarc at trigger deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#topic EventarcTrigger#topic}
        '''
        value = EventarcTriggerTransportPubsub(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubsub", [value]))

    @jsii.member(jsii_name="resetPubsub")
    def reset_pubsub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsub", []))

    @builtins.property
    @jsii.member(jsii_name="pubsub")
    def pubsub(self) -> "EventarcTriggerTransportPubsubOutputReference":
        return typing.cast("EventarcTriggerTransportPubsubOutputReference", jsii.get(self, "pubsub"))

    @builtins.property
    @jsii.member(jsii_name="pubsubInput")
    def pubsub_input(self) -> typing.Optional["EventarcTriggerTransportPubsub"]:
        return typing.cast(typing.Optional["EventarcTriggerTransportPubsub"], jsii.get(self, "pubsubInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcTriggerTransport]:
        return typing.cast(typing.Optional[EventarcTriggerTransport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EventarcTriggerTransport]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e4dbdbfbd9c73132485b9d17b5a71ebaed6b708ce5550c85c179023fd4ce3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerTransportPubsub",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class EventarcTriggerTransportPubsub:
    def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: Optional. The name of the Pub/Sub topic created and managed by Eventarc system as a transport for the event delivery. Format: 'projects/{PROJECT_ID}/topics/{TOPIC_NAME}. You may set an existing topic for triggers of the type google.cloud.pubsub.topic.v1.messagePublished' only. The topic you provide here will not be deleted by Eventarc at trigger deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#topic EventarcTrigger#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9375c3462cf6edd593879543ed6954d3f69a2c0ac8f135bbc77acafe413cbc)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the Pub/Sub topic created and managed by Eventarc system as a transport for the event delivery. Format: 'projects/{PROJECT_ID}/topics/{TOPIC_NAME}. You may set an existing topic for triggers of the type google.cloud.pubsub.topic.v1.messagePublished' only. The topic you provide here will not be deleted by Eventarc at trigger deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/eventarc_trigger#topic EventarcTrigger#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventarcTriggerTransportPubsub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventarcTriggerTransportPubsubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.eventarcTrigger.EventarcTriggerTransportPubsubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f26259dbf860566b19eaeae21018641ef712005baa39685e61d5fb75c33accb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="subscription")
    def subscription(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscription"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83109e56af18be3fd2214aae21199b4d11b44fa8ea92cdfabc4234a15f40d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventarcTriggerTransportPubsub]:
        return typing.cast(typing.Optional[EventarcTriggerTransportPubsub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventarcTriggerTransportPubsub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b81750a892731a3f804910a00e09cf79d9694a3fab835f9ea53ddacd7e3765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventarcTrigger",
    "EventarcTriggerConfig",
    "EventarcTriggerDestination",
    "EventarcTriggerDestinationCloudRunService",
    "EventarcTriggerDestinationCloudRunServiceOutputReference",
    "EventarcTriggerDestinationGke",
    "EventarcTriggerDestinationGkeOutputReference",
    "EventarcTriggerDestinationHttpEndpoint",
    "EventarcTriggerDestinationHttpEndpointOutputReference",
    "EventarcTriggerDestinationNetworkConfig",
    "EventarcTriggerDestinationNetworkConfigOutputReference",
    "EventarcTriggerDestinationOutputReference",
    "EventarcTriggerMatchingCriteria",
    "EventarcTriggerMatchingCriteriaList",
    "EventarcTriggerMatchingCriteriaOutputReference",
    "EventarcTriggerTimeouts",
    "EventarcTriggerTimeoutsOutputReference",
    "EventarcTriggerTransport",
    "EventarcTriggerTransportOutputReference",
    "EventarcTriggerTransportPubsub",
    "EventarcTriggerTransportPubsubOutputReference",
]

publication.publish()

def _typecheckingstub__4dfd0bfab5d5b7cea0710cdd5eb91876cbbe3c632628990347af726286ee6c0d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: typing.Union[EventarcTriggerDestination, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcTriggerMatchingCriteria, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    channel: typing.Optional[builtins.str] = None,
    event_data_content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[EventarcTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transport: typing.Optional[typing.Union[EventarcTriggerTransport, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__900989b68a5bbf34524c0479c3efbf8df789b29a03dc574b2b9d4f9e3cb4a965(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca007c42d63ea8be1d9f3689e7fa7fd0e2bba2610e581a6a898bf48fa317c72(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcTriggerMatchingCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715242e595df1461f2ceee56e8d262feb72ac29cc75326b5b18bec1a55fac068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861053e4fed81f1ca805e3a340f9b58b6612147c8b00885715066baa62486916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d2fd785f3c545c09ed01547ea57233c02736b3ebc9c3c4c6f3c86d373b653e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5cf00e8ba89c3f2e6f7af44d80f550c1262fbf6751eeecd6c3c45aea9ef0fe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11a9aff2fd59e743b8acf7420facc7b43f7f1bd27c038291e6655b30191c4a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2d53d9afbf4a325fd3b4954275613fbb9d3136058a17194f06a76d3207f8f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdd41480c5d6f3219b62f302556a7dab4591361b0c7521a28040e4705b2883c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5583d8197067769c39e02983dbff41740533ebc07d2953f44ed26345a1972e09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea77347f2d90b712a0b2c53c1246348b279c4926eb4fc109baabb3e421f99d11(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: typing.Union[EventarcTriggerDestination, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventarcTriggerMatchingCriteria, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    channel: typing.Optional[builtins.str] = None,
    event_data_content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[EventarcTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transport: typing.Optional[typing.Union[EventarcTriggerTransport, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d90c01d956e6ab3fc865a290e481b87d76aeef8ac2a05732e8b068d9bee38e(
    *,
    cloud_run_service: typing.Optional[typing.Union[EventarcTriggerDestinationCloudRunService, typing.Dict[builtins.str, typing.Any]]] = None,
    gke: typing.Optional[typing.Union[EventarcTriggerDestinationGke, typing.Dict[builtins.str, typing.Any]]] = None,
    http_endpoint: typing.Optional[typing.Union[EventarcTriggerDestinationHttpEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[EventarcTriggerDestinationNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c28df834889a18c0d3a1b35fe0c4339c84952053718bbd810dff9c83a17ba6(
    *,
    service: builtins.str,
    path: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a019dc4fe203b55dbbb5b89a4219e243025d0792d85fd6b62fcc0bf770621e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58f40c0b755aa48a4bf4ab34b8ff2b1ae4ebb26a94cc66e78dd5f27caf0b773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9197235b21d345898fd50a6aa55370279f17d57b2e1a560b9065ddef97ffd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01650c43b4d2b52da8e9945485118a126e259c340dea0c99411c27dc49920b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595304680ffaf05457ccb04a3246ae0afdd507e22eefb86e259172606e1be4c4(
    value: typing.Optional[EventarcTriggerDestinationCloudRunService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea9e3b6a743fe69de5f30f820a55c48c61ed14da854fb482d165f0ebdfb1e8a(
    *,
    cluster: builtins.str,
    location: builtins.str,
    namespace: builtins.str,
    service: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160f709e3e1345414d16a7c3a0732fbf6ea30290a33ec42b96cf334f6633b5a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2509440bbaa6e6706e363f573d56df020e6ca9a5f27269c34084accedae27d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3959bbbb9fbc4c6ddbd4895d79f2a4452b11b16fd2666cd474210b468feffa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d3cb7c129bb67f16c90b713c183d3412ee8b85af2b54797e5b73f8232b5c9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034724e9e3c608d36c66c5e7d6160ba8d6bf71ae51cf156b3c954b55d36f9ac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5b7fd19a60484a8462800c58b10d4c39f87c4300c74c567a887149f04b73d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b21c0d1046031a141a2e347fc8d1d085a9eddf29f3276379d9eaa1716b8e7d(
    value: typing.Optional[EventarcTriggerDestinationGke],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d258f047396a23a4a6ece456fff7295561c483ef5b75cd32c844936f6b263ae(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e8679419bbc2fb21856f3cc65166fb314510c8cc064207dd0d04ae85aea32d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0eac87de2d9dc84c73b071fbc61c50c75604b75b93bf9d307903662b20d16b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbacc9a77dadd03b5cde2bb72989f1bdab771d9679523c2e44d1c74cf6f1443(
    value: typing.Optional[EventarcTriggerDestinationHttpEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5173b463442b84c5f71c32263c372fdfdb3f843befd8a2ed6db2db424abcc1ee(
    *,
    network_attachment: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d27d80b4e90f4ca1a5f54514a67af8602df96112f2e0c9023827e7005c89a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7600050a8081de7e502134be6b3ed5c5dfa3593e0ee4b40112cb6e39c330efe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfa47b5f400a728a1096515b2aa606601276e644e4ef617b1cadeeefcc8861c(
    value: typing.Optional[EventarcTriggerDestinationNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b5af12b7900369fe0755eaa91f43ae4bde2cbe47a64212605f61efc871c827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f62cf7a1d6ad19648e8e39fb6719dce2217fd7f4da2f41cb6707baa9989ed70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7aabd4cfc4a6f79318a2f3449fb320a5b89fd7d0e246e3202bd41f95c42fae6(
    value: typing.Optional[EventarcTriggerDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88c2fa39d157faa28a8024b7af6c4069d0eae5381f502bf65d15da1d7009436(
    *,
    attribute: builtins.str,
    value: builtins.str,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b120486fef4c8547983e80575b147cc1e64bf22751f3d9294c4125fac8a23a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042ec167edef8c9334685f7eb7f7c09293bfb09020a1c62a2af60d27917e6a10(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d2972f0b7dc87040ce54dd9ae1b522fa2e525afe47abde4eab99bd79fc704a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061954e313658fe8e06eb2cf79a073334a2b8588360aede5d07f7a0f6563e66e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133d7186ba0f4ef6decc7f189f4a1bf6612f5f2dd3d770259247cd34c0fe49a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8e4011557253db8c844a78e0b3c852d4c697d62afd8dbde28487cc7d5e10e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventarcTriggerMatchingCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3128857dadad820f2ab5351c50c523396c11efe23694baf0b3d6c9da429cb98f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fe02878191f8c9e1c1159ecb6b818ef07a5528e1368a7a35f0c33999c0cacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0450fce43641d91113079b0037046e50b6659ee43c3b49925a0e77c38fa68aeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92be92191849d8bf8459c05279285b99e55f0fc7b22c0ea70e40efcc5c68a6a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f344924af5b6ac3e7b1c43b31ed22e508874a28b995a60d585e68402f9ce30e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerMatchingCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3a4a5190a2b77fdac07902af27fb7cc35ee44a016b4505b6213c0c255a307d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c42fa2c2c2102130162a58ddc3e3a0db74d8be47fc1c4585f5be1acec2e0c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854833bd90a5ecbb8fee83e24669927321878d3cfe7fdd1e3f01d26855d5a8d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451a06a686a2cc3b3c6022ad0e6351fd9289dbc9e3face45d47c4e7526175d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ab4e40f676cc698b19d619bcfb2f5c2beea90776d5d555b030ec5d7907d39d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a1399cdc5db9e7ec393eefa083763c47af5cad880e461384b996fd3b1a99f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventarcTriggerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd105d8c151c5b176dbdbba4975e6c2206cce7b05a07e38b0ac57aa4cd541b22(
    *,
    pubsub: typing.Optional[typing.Union[EventarcTriggerTransportPubsub, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04668aecdbe5666d827629ac4761eb7b5d7f5a62b0980e80fcb4a6bc2548bd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e4dbdbfbd9c73132485b9d17b5a71ebaed6b708ce5550c85c179023fd4ce3e(
    value: typing.Optional[EventarcTriggerTransport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9375c3462cf6edd593879543ed6954d3f69a2c0ac8f135bbc77acafe413cbc(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26259dbf860566b19eaeae21018641ef712005baa39685e61d5fb75c33accb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83109e56af18be3fd2214aae21199b4d11b44fa8ea92cdfabc4234a15f40d8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b81750a892731a3f804910a00e09cf79d9694a3fab835f9ea53ddacd7e3765(
    value: typing.Optional[EventarcTriggerTransportPubsub],
) -> None:
    """Type checking stubs"""
    pass
