r'''
# `google_eventarc_trigger`

Refer to the Terraform Registry for docs: [`google_eventarc_trigger`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger).
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


class GoogleEventarcTrigger(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger google_eventarc_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: typing.Union["GoogleEventarcTriggerDestination", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcTriggerMatchingCriteria", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        channel: typing.Optional[builtins.str] = None,
        event_data_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleEventarcTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transport: typing.Optional[typing.Union["GoogleEventarcTriggerTransport", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger google_eventarc_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#destination GoogleEventarcTrigger#destination}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#location GoogleEventarcTrigger#location}
        :param matching_criteria: matching_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#matching_criteria GoogleEventarcTrigger#matching_criteria}
        :param name: Required. The resource name of the trigger. Must be unique within the location on the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#name GoogleEventarcTrigger#name}
        :param channel: Optional. The name of the channel associated with the trigger in 'projects/{project}/locations/{location}/channels/{channel}' format. You must provide a channel to receive events from Eventarc SaaS partners. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#channel GoogleEventarcTrigger#channel}
        :param event_data_content_type: Optional. EventDataContentType specifies the type of payload in MIME format that is expected from the CloudEvent data field. This is set to 'application/json' if the value is not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#event_data_content_type GoogleEventarcTrigger#event_data_content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#id GoogleEventarcTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User labels attached to the triggers that can be used to group resources. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#labels GoogleEventarcTrigger#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#project GoogleEventarcTrigger#project}.
        :param service_account: Optional. The IAM service account email associated with the trigger. The service account represents the identity of the trigger. The principal who calls this API must have 'iam.serviceAccounts.actAs' permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts#sa_common for more information. For Cloud Run destinations, this service account is used to generate identity tokens when invoking the service. See https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account for information on how to invoke authenticated Cloud Run services. In order to create Audit Log triggers, the service account should also have 'roles/eventarc.eventReceiver' IAM role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service_account GoogleEventarcTrigger#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#timeouts GoogleEventarcTrigger#timeouts}
        :param transport: transport block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#transport GoogleEventarcTrigger#transport}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84a8cab80597f6faa035dbca1d487926800e3ec66811380198c7900582f2634)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleEventarcTriggerConfig(
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
        '''Generates CDKTF code for importing a GoogleEventarcTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleEventarcTrigger to import.
        :param import_from_id: The id of the existing GoogleEventarcTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleEventarcTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82815c6f9ac978e0fe4a5ac6b023dc750dd46170272a02c99a0255a8cafb7bd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        cloud_run_service: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationCloudRunService", typing.Dict[builtins.str, typing.Any]]] = None,
        gke: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationGke", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationHttpEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_run_service: cloud_run_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#cloud_run_service GoogleEventarcTrigger#cloud_run_service}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#gke GoogleEventarcTrigger#gke}
        :param http_endpoint: http_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#http_endpoint GoogleEventarcTrigger#http_endpoint}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#network_config GoogleEventarcTrigger#network_config}
        :param workflow: The resource name of the Workflow whose Executions are triggered by the events. The Workflow resource should be deployed in the same project as the trigger. Format: 'projects/{project}/locations/{location}/workflows/{workflow}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#workflow GoogleEventarcTrigger#workflow}
        '''
        value = GoogleEventarcTriggerDestination(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcTriggerMatchingCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afbb8ef31b6693c9cf332e4ac0c7b7ffe170b08ffab0571bfbf9ca3ca740ba7)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#create GoogleEventarcTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#delete GoogleEventarcTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#update GoogleEventarcTrigger#update}.
        '''
        value = GoogleEventarcTriggerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTransport")
    def put_transport(
        self,
        *,
        pubsub: typing.Optional[typing.Union["GoogleEventarcTriggerTransportPubsub", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param pubsub: pubsub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#pubsub GoogleEventarcTrigger#pubsub}
        '''
        value = GoogleEventarcTriggerTransport(pubsub=pubsub)

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
    def destination(self) -> "GoogleEventarcTriggerDestinationOutputReference":
        return typing.cast("GoogleEventarcTriggerDestinationOutputReference", jsii.get(self, "destination"))

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
    def matching_criteria(self) -> "GoogleEventarcTriggerMatchingCriteriaList":
        return typing.cast("GoogleEventarcTriggerMatchingCriteriaList", jsii.get(self, "matchingCriteria"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleEventarcTriggerTimeoutsOutputReference":
        return typing.cast("GoogleEventarcTriggerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> "GoogleEventarcTriggerTransportOutputReference":
        return typing.cast("GoogleEventarcTriggerTransportOutputReference", jsii.get(self, "transport"))

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
    def destination_input(self) -> typing.Optional["GoogleEventarcTriggerDestination"]:
        return typing.cast(typing.Optional["GoogleEventarcTriggerDestination"], jsii.get(self, "destinationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcTriggerMatchingCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcTriggerMatchingCriteria"]]], jsii.get(self, "matchingCriteriaInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleEventarcTriggerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleEventarcTriggerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional["GoogleEventarcTriggerTransport"]:
        return typing.cast(typing.Optional["GoogleEventarcTriggerTransport"], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4858144392c231705fd217d1152c0e3e8e574af9978893fe155591167513ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventDataContentType")
    def event_data_content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventDataContentType"))

    @event_data_content_type.setter
    def event_data_content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12aa5dca8ea5429d73b5143d2af191b78b3952fa1a41920aad3fe5650846a310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDataContentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4044a26236782cb76189d78b9f3c62ce5b904af596506def08bc2ebf03694c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5887d3fa02b402737bd0e56f5372cc96b799ba1f1b4361449a5e06b3d47ee878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5180dddc5c347e4190c0519a94d6d93beb3179ee86cdb993546bc218fe60b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c613e71599d87d0461fa2a870be3b2744f18f5dc67bab280409483f9b896b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dcf4d251d1bd6245d2fd5c0cd5b12e39b9e5324469b9adf384964409bd37262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aef882175206b8345e31b447eafe3afbf4a7a317cb8c44ba05baab4b641019c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerConfig",
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
class GoogleEventarcTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination: typing.Union["GoogleEventarcTriggerDestination", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleEventarcTriggerMatchingCriteria", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        channel: typing.Optional[builtins.str] = None,
        event_data_content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleEventarcTriggerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transport: typing.Optional[typing.Union["GoogleEventarcTriggerTransport", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#destination GoogleEventarcTrigger#destination}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#location GoogleEventarcTrigger#location}
        :param matching_criteria: matching_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#matching_criteria GoogleEventarcTrigger#matching_criteria}
        :param name: Required. The resource name of the trigger. Must be unique within the location on the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#name GoogleEventarcTrigger#name}
        :param channel: Optional. The name of the channel associated with the trigger in 'projects/{project}/locations/{location}/channels/{channel}' format. You must provide a channel to receive events from Eventarc SaaS partners. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#channel GoogleEventarcTrigger#channel}
        :param event_data_content_type: Optional. EventDataContentType specifies the type of payload in MIME format that is expected from the CloudEvent data field. This is set to 'application/json' if the value is not defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#event_data_content_type GoogleEventarcTrigger#event_data_content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#id GoogleEventarcTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. User labels attached to the triggers that can be used to group resources. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#labels GoogleEventarcTrigger#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#project GoogleEventarcTrigger#project}.
        :param service_account: Optional. The IAM service account email associated with the trigger. The service account represents the identity of the trigger. The principal who calls this API must have 'iam.serviceAccounts.actAs' permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts#sa_common for more information. For Cloud Run destinations, this service account is used to generate identity tokens when invoking the service. See https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account for information on how to invoke authenticated Cloud Run services. In order to create Audit Log triggers, the service account should also have 'roles/eventarc.eventReceiver' IAM role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service_account GoogleEventarcTrigger#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#timeouts GoogleEventarcTrigger#timeouts}
        :param transport: transport block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#transport GoogleEventarcTrigger#transport}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = GoogleEventarcTriggerDestination(**destination)
        if isinstance(timeouts, dict):
            timeouts = GoogleEventarcTriggerTimeouts(**timeouts)
        if isinstance(transport, dict):
            transport = GoogleEventarcTriggerTransport(**transport)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17219f38ce8ad4806106a46e31d8a166f0b08664105c525ad28be46fd7760e71)
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
    def destination(self) -> "GoogleEventarcTriggerDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#destination GoogleEventarcTrigger#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("GoogleEventarcTriggerDestination", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#location GoogleEventarcTrigger#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def matching_criteria(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcTriggerMatchingCriteria"]]:
        '''matching_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#matching_criteria GoogleEventarcTrigger#matching_criteria}
        '''
        result = self._values.get("matching_criteria")
        assert result is not None, "Required property 'matching_criteria' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleEventarcTriggerMatchingCriteria"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. The resource name of the trigger. Must be unique within the location on the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#name GoogleEventarcTrigger#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the channel associated with the trigger in 'projects/{project}/locations/{location}/channels/{channel}' format. You must provide a channel to receive events from Eventarc SaaS partners.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#channel GoogleEventarcTrigger#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_data_content_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        EventDataContentType specifies the type of payload in MIME format that is expected from the CloudEvent data field. This is set to 'application/json' if the value is not defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#event_data_content_type GoogleEventarcTrigger#event_data_content_type}
        '''
        result = self._values.get("event_data_content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#id GoogleEventarcTrigger#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#labels GoogleEventarcTrigger#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#project GoogleEventarcTrigger#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The IAM service account email associated with the trigger. The service account represents the identity of the trigger. The principal who calls this API must have 'iam.serviceAccounts.actAs' permission in the service account. See https://cloud.google.com/iam/docs/understanding-service-accounts#sa_common for more information. For Cloud Run destinations, this service account is used to generate identity tokens when invoking the service. See https://cloud.google.com/run/docs/triggering/pubsub-push#create-service-account for information on how to invoke authenticated Cloud Run services. In order to create Audit Log triggers, the service account should also have 'roles/eventarc.eventReceiver' IAM role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service_account GoogleEventarcTrigger#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleEventarcTriggerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#timeouts GoogleEventarcTrigger#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleEventarcTriggerTimeouts"], result)

    @builtins.property
    def transport(self) -> typing.Optional["GoogleEventarcTriggerTransport"]:
        '''transport block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#transport GoogleEventarcTrigger#transport}
        '''
        result = self._values.get("transport")
        return typing.cast(typing.Optional["GoogleEventarcTriggerTransport"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestination",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_run_service": "cloudRunService",
        "gke": "gke",
        "http_endpoint": "httpEndpoint",
        "network_config": "networkConfig",
        "workflow": "workflow",
    },
)
class GoogleEventarcTriggerDestination:
    def __init__(
        self,
        *,
        cloud_run_service: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationCloudRunService", typing.Dict[builtins.str, typing.Any]]] = None,
        gke: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationGke", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationHttpEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleEventarcTriggerDestinationNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_run_service: cloud_run_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#cloud_run_service GoogleEventarcTrigger#cloud_run_service}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#gke GoogleEventarcTrigger#gke}
        :param http_endpoint: http_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#http_endpoint GoogleEventarcTrigger#http_endpoint}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#network_config GoogleEventarcTrigger#network_config}
        :param workflow: The resource name of the Workflow whose Executions are triggered by the events. The Workflow resource should be deployed in the same project as the trigger. Format: 'projects/{project}/locations/{location}/workflows/{workflow}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#workflow GoogleEventarcTrigger#workflow}
        '''
        if isinstance(cloud_run_service, dict):
            cloud_run_service = GoogleEventarcTriggerDestinationCloudRunService(**cloud_run_service)
        if isinstance(gke, dict):
            gke = GoogleEventarcTriggerDestinationGke(**gke)
        if isinstance(http_endpoint, dict):
            http_endpoint = GoogleEventarcTriggerDestinationHttpEndpoint(**http_endpoint)
        if isinstance(network_config, dict):
            network_config = GoogleEventarcTriggerDestinationNetworkConfig(**network_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884feff5d65a66d9b0c01f8aa62fa8d0fb0099a5a3100791c0d737b7b03fa17b)
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
    ) -> typing.Optional["GoogleEventarcTriggerDestinationCloudRunService"]:
        '''cloud_run_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#cloud_run_service GoogleEventarcTrigger#cloud_run_service}
        '''
        result = self._values.get("cloud_run_service")
        return typing.cast(typing.Optional["GoogleEventarcTriggerDestinationCloudRunService"], result)

    @builtins.property
    def gke(self) -> typing.Optional["GoogleEventarcTriggerDestinationGke"]:
        '''gke block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#gke GoogleEventarcTrigger#gke}
        '''
        result = self._values.get("gke")
        return typing.cast(typing.Optional["GoogleEventarcTriggerDestinationGke"], result)

    @builtins.property
    def http_endpoint(
        self,
    ) -> typing.Optional["GoogleEventarcTriggerDestinationHttpEndpoint"]:
        '''http_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#http_endpoint GoogleEventarcTrigger#http_endpoint}
        '''
        result = self._values.get("http_endpoint")
        return typing.cast(typing.Optional["GoogleEventarcTriggerDestinationHttpEndpoint"], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleEventarcTriggerDestinationNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#network_config GoogleEventarcTrigger#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleEventarcTriggerDestinationNetworkConfig"], result)

    @builtins.property
    def workflow(self) -> typing.Optional[builtins.str]:
        '''The resource name of the Workflow whose Executions are triggered by the events.

        The Workflow resource should be deployed in the same project as the trigger. Format: 'projects/{project}/locations/{location}/workflows/{workflow}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#workflow GoogleEventarcTrigger#workflow}
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationCloudRunService",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "path": "path", "region": "region"},
)
class GoogleEventarcTriggerDestinationCloudRunService:
    def __init__(
        self,
        *,
        service: builtins.str,
        path: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Required. The name of the Cloud Run service being addressed. See https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services. Only services located in the same project of the trigger object can be addressed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service GoogleEventarcTrigger#service}
        :param path: Optional. The relative path on the Cloud Run service the events should be sent to. The value must conform to the definition of URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#path GoogleEventarcTrigger#path}
        :param region: Required. The region the Cloud Run service is deployed in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#region GoogleEventarcTrigger#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba86a747428705dc29478c4e188ba1c3c905d539d990eaddda5c731da6ce40c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service GoogleEventarcTrigger#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The relative path on the Cloud Run service the events should be sent to. The value must conform to the definition of URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#path GoogleEventarcTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Required. The region the Cloud Run service is deployed in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#region GoogleEventarcTrigger#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerDestinationCloudRunService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerDestinationCloudRunServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationCloudRunServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46e748fa4974d256cb59b920fd6452268999e458724ba0b6089b993c3b342be1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58f41f3e26bf0b7f7f9c80d12057d78fa4c1ad0479a5c975dde332464d45a539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b73bde5d77d7ac816b818fc64ab78303073542b9351f4fcb788573b8385eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26685754f350a93ece72911f9b6467e91382b6605a5f6e6b1b2ac6858bf03e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcTriggerDestinationCloudRunService]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationCloudRunService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerDestinationCloudRunService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ae03ed89541a3c97d107fbefb0c5eff3e92203207e81a662db996292c23524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationGke",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "location": "location",
        "namespace": "namespace",
        "service": "service",
        "path": "path",
    },
)
class GoogleEventarcTriggerDestinationGke:
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
        :param cluster: Required. The name of the cluster the GKE service is running in. The cluster must be running in the same project as the trigger being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#cluster GoogleEventarcTrigger#cluster}
        :param location: Required. The name of the Google Compute Engine in which the cluster resides, which can either be compute zone (for example, us-central1-a) for the zonal clusters or region (for example, us-central1) for regional clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#location GoogleEventarcTrigger#location}
        :param namespace: Required. The namespace the GKE service is running in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#namespace GoogleEventarcTrigger#namespace}
        :param service: Required. Name of the GKE service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service GoogleEventarcTrigger#service}
        :param path: Optional. The relative path on the GKE service the events should be sent to. The value must conform to the definition of a URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#path GoogleEventarcTrigger#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92bfd5257c77b1210324bd68fcf4119f901a1b3269e08e9a0b447a8ccd9f52c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#cluster GoogleEventarcTrigger#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Required.

        The name of the Google Compute Engine in which the cluster resides, which can either be compute zone (for example, us-central1-a) for the zonal clusters or region (for example, us-central1) for regional clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#location GoogleEventarcTrigger#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Required. The namespace the GKE service is running in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#namespace GoogleEventarcTrigger#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. Name of the GKE service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service GoogleEventarcTrigger#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The relative path on the GKE service the events should be sent to. The value must conform to the definition of a URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#path GoogleEventarcTrigger#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerDestinationGke(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerDestinationGkeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationGkeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd3e3a90a637a1cef09008f1b0775b60653068868fe70fe602801f49262ba6fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f10a15387febd51adbbf4af1914cb3464f56ad43474aaf251e70c228e52805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4754df0bd2a6b8c5dd452b8d656eee4be054af8f1d92c32eeeb16a3beac40239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bc3b68d200faf9cfc1ae51405597eca754b8304b4f35b6bb84bc910d3358d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ffe3fa75c4a3b1849d52ae0f22c6e0dcb568d3b88b458f060cc4e43e550b482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825e2a4f2e768bea283c3408ac303b8aac072ed39fbb51ff3918945cd3d4e275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEventarcTriggerDestinationGke]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationGke], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerDestinationGke],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08880664bb7ef5452ccfb8cb7578a7feb41f83a10910dc1c7530ef67c8f63c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationHttpEndpoint",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleEventarcTriggerDestinationHttpEndpoint:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: Required. The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'http://10.10.10.8:80/route', 'http://svc.us-central1.p.local:8080/'. Only HTTP and HTTPS protocols are supported. The host can be either a static IP addressable from the VPC specified by the network config, or an internal DNS hostname of the service resolvable via Cloud DNS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#uri GoogleEventarcTrigger#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bedbf8c96c4afcbc7ca12af9e876bea35f046595830dd7472f8e79a2bc27ec)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required.

        The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'http://10.10.10.8:80/route', 'http://svc.us-central1.p.local:8080/'. Only HTTP and HTTPS protocols are supported. The host can be either a static IP addressable from the VPC specified by the network config, or an internal DNS hostname of the service resolvable via Cloud DNS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#uri GoogleEventarcTrigger#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerDestinationHttpEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerDestinationHttpEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationHttpEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb252dec902231b18f22987c5ea3e38c7b6a46ed1287fe4b7a288fd494455e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f1dfcaf5949850661326e0b7bb92a0411ec34904edc909fc78408c3c58d7014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcTriggerDestinationHttpEndpoint]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationHttpEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerDestinationHttpEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ce0f799fef2029add0c9a116fc2124c297fac8448379bf17d352096bf8f253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"network_attachment": "networkAttachment"},
)
class GoogleEventarcTriggerDestinationNetworkConfig:
    def __init__(self, *, network_attachment: builtins.str) -> None:
        '''
        :param network_attachment: Required. Name of the NetworkAttachment that allows access to the destination VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#network_attachment GoogleEventarcTrigger#network_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e474a6952b0743acc4ddc3a1d61bb1b195a76763635e549a2fad9e19bb45f8)
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_attachment": network_attachment,
        }

    @builtins.property
    def network_attachment(self) -> builtins.str:
        '''Required. Name of the NetworkAttachment that allows access to the destination VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#network_attachment GoogleEventarcTrigger#network_attachment}
        '''
        result = self._values.get("network_attachment")
        assert result is not None, "Required property 'network_attachment' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerDestinationNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerDestinationNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bab6d2e4c81ca74f1c3cb10af1c03cbdbe8436db9f6083c8db74d1e461511bdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8badb885934f7868ce923691186576d1514d977e67ff0071597253f3661bf9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleEventarcTriggerDestinationNetworkConfig]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerDestinationNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25090d414646fc981d7539c26f929d6bb3eaaadf8bc3742ce35f23349e6f6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcTriggerDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26503bee47510abf8d497dd99eb16d778bf81108bb1e704a60ac56eb41c3adf4)
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
        :param service: Required. The name of the Cloud Run service being addressed. See https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services. Only services located in the same project of the trigger object can be addressed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service GoogleEventarcTrigger#service}
        :param path: Optional. The relative path on the Cloud Run service the events should be sent to. The value must conform to the definition of URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#path GoogleEventarcTrigger#path}
        :param region: Required. The region the Cloud Run service is deployed in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#region GoogleEventarcTrigger#region}
        '''
        value = GoogleEventarcTriggerDestinationCloudRunService(
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
        :param cluster: Required. The name of the cluster the GKE service is running in. The cluster must be running in the same project as the trigger being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#cluster GoogleEventarcTrigger#cluster}
        :param location: Required. The name of the Google Compute Engine in which the cluster resides, which can either be compute zone (for example, us-central1-a) for the zonal clusters or region (for example, us-central1) for regional clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#location GoogleEventarcTrigger#location}
        :param namespace: Required. The namespace the GKE service is running in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#namespace GoogleEventarcTrigger#namespace}
        :param service: Required. Name of the GKE service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#service GoogleEventarcTrigger#service}
        :param path: Optional. The relative path on the GKE service the events should be sent to. The value must conform to the definition of a URI path segment (section 3.3 of RFC2396). Examples: "/route", "route", "route/subroute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#path GoogleEventarcTrigger#path}
        '''
        value = GoogleEventarcTriggerDestinationGke(
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
        :param uri: Required. The URI of the HTTP enpdoint. The value must be a RFC2396 URI string. Examples: 'http://10.10.10.8:80/route', 'http://svc.us-central1.p.local:8080/'. Only HTTP and HTTPS protocols are supported. The host can be either a static IP addressable from the VPC specified by the network config, or an internal DNS hostname of the service resolvable via Cloud DNS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#uri GoogleEventarcTrigger#uri}
        '''
        value = GoogleEventarcTriggerDestinationHttpEndpoint(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putHttpEndpoint", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(self, *, network_attachment: builtins.str) -> None:
        '''
        :param network_attachment: Required. Name of the NetworkAttachment that allows access to the destination VPC. Format: 'projects/{PROJECT_ID}/regions/{REGION}/networkAttachments/{NETWORK_ATTACHMENT_NAME}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#network_attachment GoogleEventarcTrigger#network_attachment}
        '''
        value = GoogleEventarcTriggerDestinationNetworkConfig(
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
    ) -> GoogleEventarcTriggerDestinationCloudRunServiceOutputReference:
        return typing.cast(GoogleEventarcTriggerDestinationCloudRunServiceOutputReference, jsii.get(self, "cloudRunService"))

    @builtins.property
    @jsii.member(jsii_name="gke")
    def gke(self) -> GoogleEventarcTriggerDestinationGkeOutputReference:
        return typing.cast(GoogleEventarcTriggerDestinationGkeOutputReference, jsii.get(self, "gke"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpoint")
    def http_endpoint(
        self,
    ) -> GoogleEventarcTriggerDestinationHttpEndpointOutputReference:
        return typing.cast(GoogleEventarcTriggerDestinationHttpEndpointOutputReference, jsii.get(self, "httpEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> GoogleEventarcTriggerDestinationNetworkConfigOutputReference:
        return typing.cast(GoogleEventarcTriggerDestinationNetworkConfigOutputReference, jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunServiceInput")
    def cloud_run_service_input(
        self,
    ) -> typing.Optional[GoogleEventarcTriggerDestinationCloudRunService]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationCloudRunService], jsii.get(self, "cloudRunServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeInput")
    def gke_input(self) -> typing.Optional[GoogleEventarcTriggerDestinationGke]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationGke], jsii.get(self, "gkeInput"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointInput")
    def http_endpoint_input(
        self,
    ) -> typing.Optional[GoogleEventarcTriggerDestinationHttpEndpoint]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationHttpEndpoint], jsii.get(self, "httpEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional[GoogleEventarcTriggerDestinationNetworkConfig]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestinationNetworkConfig], jsii.get(self, "networkConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__53e7b562a1e13907444c97d038fcb078629a4f063050d8157203521e588aef21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workflow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEventarcTriggerDestination]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927bdfbb97be2e8c590973f6c16c21f459efddd68d7dd087751b87350b8b6912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerMatchingCriteria",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute", "value": "value", "operator": "operator"},
)
class GoogleEventarcTriggerMatchingCriteria:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        value: builtins.str,
        operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: Required. The name of a CloudEvents attribute. Currently, only a subset of attributes are supported for filtering. All triggers MUST provide a filter for the 'type' attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#attribute GoogleEventarcTrigger#attribute}
        :param value: Required. The value for the attribute. See https://cloud.google.com/eventarc/docs/creating-triggers#trigger-gcloud for available values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#value GoogleEventarcTrigger#value}
        :param operator: Optional. The operator used for matching the events with the value of the filter. If not specified, only events that have an exact key-value pair specified in the filter are matched. The only allowed value is 'match-path-pattern'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#operator GoogleEventarcTrigger#operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deee2c6f375df8766f06f55c0901b84ae8045da0e5ef207fdce931918b7feff2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#attribute GoogleEventarcTrigger#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Required. The value for the attribute. See https://cloud.google.com/eventarc/docs/creating-triggers#trigger-gcloud for available values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#value GoogleEventarcTrigger#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The operator used for matching the events with the value of the filter. If not specified, only events that have an exact key-value pair specified in the filter are matched. The only allowed value is 'match-path-pattern'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#operator GoogleEventarcTrigger#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerMatchingCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerMatchingCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerMatchingCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec07f4d3ce13715c5b861632e04eb91ca4d4b3043f7f06d4167a8ff0d2e9c8d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleEventarcTriggerMatchingCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb86d285a845cef454cc794c1caa1aa529e9b775662f82af478c8fea28445cd6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleEventarcTriggerMatchingCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8ff54da33a3c093049fd0e529e26537f2f16c1c573ce7a4a43bf7896d4a05b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eec1c2433e1b42a1fe6c2acc0ddc3e3e1de4827a19be2641234e6ea419db06b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47f4e0567997df4a19e546742edf62fcd3e5c7419f1a6228a53be738ad34793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcTriggerMatchingCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcTriggerMatchingCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcTriggerMatchingCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74a0e13edb6420d2f4134564149dc2c93301c27517bd09f05dd9b937d1d1311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleEventarcTriggerMatchingCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerMatchingCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cbd589ce218388204d048411dbe82a0bd9f392dd9798dbcf6cb93ec5874a60d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5546a76862ab043f7909834dc87e7f5b2ff3040324ebd6cbc202d40020f8f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee80daaa9dd2425b7173a42327cb7a0c327dba591c10270bb6cb7a971143ad37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e82283eae841a29b82b1a1d317f78dfa03c90490e1960d25c3f83d8830964ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerMatchingCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerMatchingCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerMatchingCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240c2df128420e8539122b2afde4e9706ba88a35e0cd4fbdd633d2fd7f0a56c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleEventarcTriggerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#create GoogleEventarcTrigger#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#delete GoogleEventarcTrigger#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#update GoogleEventarcTrigger#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4f6a32a6c62d68d0c622d11ff40770833beca7dbf442fe91e82398c860a145)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#create GoogleEventarcTrigger#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#delete GoogleEventarcTrigger#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#update GoogleEventarcTrigger#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd60d1f66fef9fb02d85252816986f3c2fd8dff1b1c4ded3d97ae88f56fcca0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f66895b289cd8f3be62c251e54a7a7e3cad36e4f046c98a8948b3fdc293ab0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621e2a297f30b0f4754746130d8b411e61b577f60c03ecde04a37af2c1f4d3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dba26cafcc3b0afebe2a62feb0fc83ed98d3cb8290878f7879c644ac748879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6244adcb1e4d5a7ac82a8732c70363b707d469147dcdbe221efc63c9beea56fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerTransport",
    jsii_struct_bases=[],
    name_mapping={"pubsub": "pubsub"},
)
class GoogleEventarcTriggerTransport:
    def __init__(
        self,
        *,
        pubsub: typing.Optional[typing.Union["GoogleEventarcTriggerTransportPubsub", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param pubsub: pubsub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#pubsub GoogleEventarcTrigger#pubsub}
        '''
        if isinstance(pubsub, dict):
            pubsub = GoogleEventarcTriggerTransportPubsub(**pubsub)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283a9366016fb0a110efa7b163492c5dfcd510325f07e9fd3642fc0b8916cd10)
            check_type(argname="argument pubsub", value=pubsub, expected_type=type_hints["pubsub"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pubsub is not None:
            self._values["pubsub"] = pubsub

    @builtins.property
    def pubsub(self) -> typing.Optional["GoogleEventarcTriggerTransportPubsub"]:
        '''pubsub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#pubsub GoogleEventarcTrigger#pubsub}
        '''
        result = self._values.get("pubsub")
        return typing.cast(typing.Optional["GoogleEventarcTriggerTransportPubsub"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerTransport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerTransportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerTransportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc31e48449de8403a592eb1c901a5080fd77c42dbb3a0f63996743d99d38b60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsub")
    def put_pubsub(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: Optional. The name of the Pub/Sub topic created and managed by Eventarc system as a transport for the event delivery. Format: 'projects/{PROJECT_ID}/topics/{TOPIC_NAME}. You may set an existing topic for triggers of the type google.cloud.pubsub.topic.v1.messagePublished' only. The topic you provide here will not be deleted by Eventarc at trigger deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#topic GoogleEventarcTrigger#topic}
        '''
        value = GoogleEventarcTriggerTransportPubsub(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubsub", [value]))

    @jsii.member(jsii_name="resetPubsub")
    def reset_pubsub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsub", []))

    @builtins.property
    @jsii.member(jsii_name="pubsub")
    def pubsub(self) -> "GoogleEventarcTriggerTransportPubsubOutputReference":
        return typing.cast("GoogleEventarcTriggerTransportPubsubOutputReference", jsii.get(self, "pubsub"))

    @builtins.property
    @jsii.member(jsii_name="pubsubInput")
    def pubsub_input(self) -> typing.Optional["GoogleEventarcTriggerTransportPubsub"]:
        return typing.cast(typing.Optional["GoogleEventarcTriggerTransportPubsub"], jsii.get(self, "pubsubInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEventarcTriggerTransport]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerTransport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerTransport],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014236686c255aaf46cffad0af9c3b784bf556424efa391ec60b057d2aebe63e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerTransportPubsub",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class GoogleEventarcTriggerTransportPubsub:
    def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: Optional. The name of the Pub/Sub topic created and managed by Eventarc system as a transport for the event delivery. Format: 'projects/{PROJECT_ID}/topics/{TOPIC_NAME}. You may set an existing topic for triggers of the type google.cloud.pubsub.topic.v1.messagePublished' only. The topic you provide here will not be deleted by Eventarc at trigger deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#topic GoogleEventarcTrigger#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad29f87927589581b906a3f2f6aaf92fad938203dccf127a56a53571e9adb86)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the Pub/Sub topic created and managed by Eventarc system as a transport for the event delivery. Format: 'projects/{PROJECT_ID}/topics/{TOPIC_NAME}. You may set an existing topic for triggers of the type google.cloud.pubsub.topic.v1.messagePublished' only. The topic you provide here will not be deleted by Eventarc at trigger deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_eventarc_trigger#topic GoogleEventarcTrigger#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleEventarcTriggerTransportPubsub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleEventarcTriggerTransportPubsubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleEventarcTrigger.GoogleEventarcTriggerTransportPubsubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d658bab02bfae4cd0cea8fa6c26b32a1b1cd620cf8a6b2262828014cd946487)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e2b438a5c5cc818d52bb186e3e9e78fa5b071113af04f2036b2084c9ad0333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleEventarcTriggerTransportPubsub]:
        return typing.cast(typing.Optional[GoogleEventarcTriggerTransportPubsub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleEventarcTriggerTransportPubsub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9f3f19ef3236131026cbb8de2c83729cf49bf41d633e2cbfb2813572ff4b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleEventarcTrigger",
    "GoogleEventarcTriggerConfig",
    "GoogleEventarcTriggerDestination",
    "GoogleEventarcTriggerDestinationCloudRunService",
    "GoogleEventarcTriggerDestinationCloudRunServiceOutputReference",
    "GoogleEventarcTriggerDestinationGke",
    "GoogleEventarcTriggerDestinationGkeOutputReference",
    "GoogleEventarcTriggerDestinationHttpEndpoint",
    "GoogleEventarcTriggerDestinationHttpEndpointOutputReference",
    "GoogleEventarcTriggerDestinationNetworkConfig",
    "GoogleEventarcTriggerDestinationNetworkConfigOutputReference",
    "GoogleEventarcTriggerDestinationOutputReference",
    "GoogleEventarcTriggerMatchingCriteria",
    "GoogleEventarcTriggerMatchingCriteriaList",
    "GoogleEventarcTriggerMatchingCriteriaOutputReference",
    "GoogleEventarcTriggerTimeouts",
    "GoogleEventarcTriggerTimeoutsOutputReference",
    "GoogleEventarcTriggerTransport",
    "GoogleEventarcTriggerTransportOutputReference",
    "GoogleEventarcTriggerTransportPubsub",
    "GoogleEventarcTriggerTransportPubsubOutputReference",
]

publication.publish()

def _typecheckingstub__f84a8cab80597f6faa035dbca1d487926800e3ec66811380198c7900582f2634(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: typing.Union[GoogleEventarcTriggerDestination, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcTriggerMatchingCriteria, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    channel: typing.Optional[builtins.str] = None,
    event_data_content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleEventarcTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transport: typing.Optional[typing.Union[GoogleEventarcTriggerTransport, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__82815c6f9ac978e0fe4a5ac6b023dc750dd46170272a02c99a0255a8cafb7bd0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afbb8ef31b6693c9cf332e4ac0c7b7ffe170b08ffab0571bfbf9ca3ca740ba7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcTriggerMatchingCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4858144392c231705fd217d1152c0e3e8e574af9978893fe155591167513ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12aa5dca8ea5429d73b5143d2af191b78b3952fa1a41920aad3fe5650846a310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4044a26236782cb76189d78b9f3c62ce5b904af596506def08bc2ebf03694c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5887d3fa02b402737bd0e56f5372cc96b799ba1f1b4361449a5e06b3d47ee878(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5180dddc5c347e4190c0519a94d6d93beb3179ee86cdb993546bc218fe60b94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c613e71599d87d0461fa2a870be3b2744f18f5dc67bab280409483f9b896b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcf4d251d1bd6245d2fd5c0cd5b12e39b9e5324469b9adf384964409bd37262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aef882175206b8345e31b447eafe3afbf4a7a317cb8c44ba05baab4b641019c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17219f38ce8ad4806106a46e31d8a166f0b08664105c525ad28be46fd7760e71(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: typing.Union[GoogleEventarcTriggerDestination, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    matching_criteria: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleEventarcTriggerMatchingCriteria, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    channel: typing.Optional[builtins.str] = None,
    event_data_content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleEventarcTriggerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transport: typing.Optional[typing.Union[GoogleEventarcTriggerTransport, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884feff5d65a66d9b0c01f8aa62fa8d0fb0099a5a3100791c0d737b7b03fa17b(
    *,
    cloud_run_service: typing.Optional[typing.Union[GoogleEventarcTriggerDestinationCloudRunService, typing.Dict[builtins.str, typing.Any]]] = None,
    gke: typing.Optional[typing.Union[GoogleEventarcTriggerDestinationGke, typing.Dict[builtins.str, typing.Any]]] = None,
    http_endpoint: typing.Optional[typing.Union[GoogleEventarcTriggerDestinationHttpEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleEventarcTriggerDestinationNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba86a747428705dc29478c4e188ba1c3c905d539d990eaddda5c731da6ce40c(
    *,
    service: builtins.str,
    path: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e748fa4974d256cb59b920fd6452268999e458724ba0b6089b993c3b342be1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f41f3e26bf0b7f7f9c80d12057d78fa4c1ad0479a5c975dde332464d45a539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b73bde5d77d7ac816b818fc64ab78303073542b9351f4fcb788573b8385eba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26685754f350a93ece72911f9b6467e91382b6605a5f6e6b1b2ac6858bf03e7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ae03ed89541a3c97d107fbefb0c5eff3e92203207e81a662db996292c23524(
    value: typing.Optional[GoogleEventarcTriggerDestinationCloudRunService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92bfd5257c77b1210324bd68fcf4119f901a1b3269e08e9a0b447a8ccd9f52c(
    *,
    cluster: builtins.str,
    location: builtins.str,
    namespace: builtins.str,
    service: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3e3a90a637a1cef09008f1b0775b60653068868fe70fe602801f49262ba6fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f10a15387febd51adbbf4af1914cb3464f56ad43474aaf251e70c228e52805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4754df0bd2a6b8c5dd452b8d656eee4be054af8f1d92c32eeeb16a3beac40239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bc3b68d200faf9cfc1ae51405597eca754b8304b4f35b6bb84bc910d3358d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffe3fa75c4a3b1849d52ae0f22c6e0dcb568d3b88b458f060cc4e43e550b482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825e2a4f2e768bea283c3408ac303b8aac072ed39fbb51ff3918945cd3d4e275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08880664bb7ef5452ccfb8cb7578a7feb41f83a10910dc1c7530ef67c8f63c2b(
    value: typing.Optional[GoogleEventarcTriggerDestinationGke],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bedbf8c96c4afcbc7ca12af9e876bea35f046595830dd7472f8e79a2bc27ec(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb252dec902231b18f22987c5ea3e38c7b6a46ed1287fe4b7a288fd494455e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1dfcaf5949850661326e0b7bb92a0411ec34904edc909fc78408c3c58d7014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ce0f799fef2029add0c9a116fc2124c297fac8448379bf17d352096bf8f253(
    value: typing.Optional[GoogleEventarcTriggerDestinationHttpEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e474a6952b0743acc4ddc3a1d61bb1b195a76763635e549a2fad9e19bb45f8(
    *,
    network_attachment: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab6d2e4c81ca74f1c3cb10af1c03cbdbe8436db9f6083c8db74d1e461511bdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8badb885934f7868ce923691186576d1514d977e67ff0071597253f3661bf9ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25090d414646fc981d7539c26f929d6bb3eaaadf8bc3742ce35f23349e6f6f3(
    value: typing.Optional[GoogleEventarcTriggerDestinationNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26503bee47510abf8d497dd99eb16d778bf81108bb1e704a60ac56eb41c3adf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e7b562a1e13907444c97d038fcb078629a4f063050d8157203521e588aef21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927bdfbb97be2e8c590973f6c16c21f459efddd68d7dd087751b87350b8b6912(
    value: typing.Optional[GoogleEventarcTriggerDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deee2c6f375df8766f06f55c0901b84ae8045da0e5ef207fdce931918b7feff2(
    *,
    attribute: builtins.str,
    value: builtins.str,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec07f4d3ce13715c5b861632e04eb91ca4d4b3043f7f06d4167a8ff0d2e9c8d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb86d285a845cef454cc794c1caa1aa529e9b775662f82af478c8fea28445cd6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8ff54da33a3c093049fd0e529e26537f2f16c1c573ce7a4a43bf7896d4a05b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eec1c2433e1b42a1fe6c2acc0ddc3e3e1de4827a19be2641234e6ea419db06b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47f4e0567997df4a19e546742edf62fcd3e5c7419f1a6228a53be738ad34793(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74a0e13edb6420d2f4134564149dc2c93301c27517bd09f05dd9b937d1d1311(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleEventarcTriggerMatchingCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbd589ce218388204d048411dbe82a0bd9f392dd9798dbcf6cb93ec5874a60d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5546a76862ab043f7909834dc87e7f5b2ff3040324ebd6cbc202d40020f8f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee80daaa9dd2425b7173a42327cb7a0c327dba591c10270bb6cb7a971143ad37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e82283eae841a29b82b1a1d317f78dfa03c90490e1960d25c3f83d8830964ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240c2df128420e8539122b2afde4e9706ba88a35e0cd4fbdd633d2fd7f0a56c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerMatchingCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4f6a32a6c62d68d0c622d11ff40770833beca7dbf442fe91e82398c860a145(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd60d1f66fef9fb02d85252816986f3c2fd8dff1b1c4ded3d97ae88f56fcca0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f66895b289cd8f3be62c251e54a7a7e3cad36e4f046c98a8948b3fdc293ab0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621e2a297f30b0f4754746130d8b411e61b577f60c03ecde04a37af2c1f4d3ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dba26cafcc3b0afebe2a62feb0fc83ed98d3cb8290878f7879c644ac748879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6244adcb1e4d5a7ac82a8732c70363b707d469147dcdbe221efc63c9beea56fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleEventarcTriggerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283a9366016fb0a110efa7b163492c5dfcd510325f07e9fd3642fc0b8916cd10(
    *,
    pubsub: typing.Optional[typing.Union[GoogleEventarcTriggerTransportPubsub, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc31e48449de8403a592eb1c901a5080fd77c42dbb3a0f63996743d99d38b60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014236686c255aaf46cffad0af9c3b784bf556424efa391ec60b057d2aebe63e(
    value: typing.Optional[GoogleEventarcTriggerTransport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad29f87927589581b906a3f2f6aaf92fad938203dccf127a56a53571e9adb86(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d658bab02bfae4cd0cea8fa6c26b32a1b1cd620cf8a6b2262828014cd946487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e2b438a5c5cc818d52bb186e3e9e78fa5b071113af04f2036b2084c9ad0333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9f3f19ef3236131026cbb8de2c83729cf49bf41d633e2cbfb2813572ff4b7f(
    value: typing.Optional[GoogleEventarcTriggerTransportPubsub],
) -> None:
    """Type checking stubs"""
    pass
