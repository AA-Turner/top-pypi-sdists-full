r'''
# `google_compute_service_attachment`

Refer to the Terraform Registry for docs: [`google_compute_service_attachment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment).
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


class ComputeServiceAttachment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment google_compute_service_attachment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_preference: builtins.str,
        enable_proxy_protocol: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        nat_subnets: typing.Sequence[builtins.str],
        target_service: builtins.str,
        consumer_accept_lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeServiceAttachmentConsumerAcceptLists", typing.Dict[builtins.str, typing.Any]]]]] = None,
        consumer_reject_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        propagated_connection_limit: typing.Optional[jsii.Number] = None,
        reconcile_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        send_propagated_connection_limit_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeServiceAttachmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment google_compute_service_attachment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_preference: The connection preference to use for this service attachment. Valid values include "ACCEPT_AUTOMATIC", "ACCEPT_MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#connection_preference ComputeServiceAttachment#connection_preference}
        :param enable_proxy_protocol: If true, enable the proxy protocol which is for supplying client TCP/IP address data in TCP connections that traverse proxies on their way to destination servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#enable_proxy_protocol ComputeServiceAttachment#enable_proxy_protocol}
        :param name: Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#name ComputeServiceAttachment#name}
        :param nat_subnets: An array of subnets that is provided for NAT in this service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#nat_subnets ComputeServiceAttachment#nat_subnets}
        :param target_service: The URL of a service serving the endpoint identified by this service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#target_service ComputeServiceAttachment#target_service}
        :param consumer_accept_lists: consumer_accept_lists block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#consumer_accept_lists ComputeServiceAttachment#consumer_accept_lists}
        :param consumer_reject_lists: An array of projects that are not allowed to connect to this service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#consumer_reject_lists ComputeServiceAttachment#consumer_reject_lists}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#description ComputeServiceAttachment#description}
        :param domain_names: If specified, the domain name will be used during the integration between the PSC connected endpoints and the Cloud DNS. For example, this is a valid domain name: "p.mycompany.com.". Current max number of domain names supported is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#domain_names ComputeServiceAttachment#domain_names}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#id ComputeServiceAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#project ComputeServiceAttachment#project}.
        :param propagated_connection_limit: The number of consumer spokes that connected Private Service Connect endpoints can be propagated to through Network Connectivity Center. This limit lets the service producer limit how many propagated Private Service Connect connections can be established to this service attachment from a single consumer. If the connection preference of the service attachment is ACCEPT_MANUAL, the limit applies to each project or network that is listed in the consumer accept list. If the connection preference of the service attachment is ACCEPT_AUTOMATIC, the limit applies to each project that contains a connected endpoint. If unspecified, the default propagated connection limit is 250. To explicitly send a zero value, set 'send_propagated_connection_limit_if_zero = true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#propagated_connection_limit ComputeServiceAttachment#propagated_connection_limit}
        :param reconcile_connections: This flag determines whether a consumer accept/reject list change can reconcile the statuses of existing ACCEPTED or REJECTED PSC endpoints. If false, connection policy update will only affect existing PENDING PSC endpoints. Existing ACCEPTED/REJECTED endpoints will remain untouched regardless how the connection policy is modified . If true, update will affect both PENDING and ACCEPTED/REJECTED PSC endpoints. For example, an ACCEPTED PSC endpoint will be moved to REJECTED if its project is added to the reject list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#reconcile_connections ComputeServiceAttachment#reconcile_connections}
        :param region: URL of the region where the resource resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#region ComputeServiceAttachment#region}
        :param send_propagated_connection_limit_if_zero: Controls the behavior of propagated_connection_limit. When false, setting propagated_connection_limit to zero causes the provider to use to the API's default value. When true, the provider will set propagated_connection_limit to zero. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#send_propagated_connection_limit_if_zero ComputeServiceAttachment#send_propagated_connection_limit_if_zero}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#timeouts ComputeServiceAttachment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41ec140610d154cdadef1c5f1774e185cb5041a553e15790f38699ff2d2d97b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeServiceAttachmentConfig(
            connection_preference=connection_preference,
            enable_proxy_protocol=enable_proxy_protocol,
            name=name,
            nat_subnets=nat_subnets,
            target_service=target_service,
            consumer_accept_lists=consumer_accept_lists,
            consumer_reject_lists=consumer_reject_lists,
            description=description,
            domain_names=domain_names,
            id=id,
            project=project,
            propagated_connection_limit=propagated_connection_limit,
            reconcile_connections=reconcile_connections,
            region=region,
            send_propagated_connection_limit_if_zero=send_propagated_connection_limit_if_zero,
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
        '''Generates CDKTF code for importing a ComputeServiceAttachment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeServiceAttachment to import.
        :param import_from_id: The id of the existing ComputeServiceAttachment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeServiceAttachment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a87a4c5db83bc677ac8157cdfc3aa00fab978f450979ad707ca74f67c9b7a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConsumerAcceptLists")
    def put_consumer_accept_lists(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeServiceAttachmentConsumerAcceptLists", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ca0a324f059f12c0f8be90042c0e590836773918eced3b5d4cc389c20bcb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConsumerAcceptLists", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#create ComputeServiceAttachment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#delete ComputeServiceAttachment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#update ComputeServiceAttachment#update}.
        '''
        value = ComputeServiceAttachmentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConsumerAcceptLists")
    def reset_consumer_accept_lists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerAcceptLists", []))

    @jsii.member(jsii_name="resetConsumerRejectLists")
    def reset_consumer_reject_lists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerRejectLists", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDomainNames")
    def reset_domain_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainNames", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPropagatedConnectionLimit")
    def reset_propagated_connection_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagatedConnectionLimit", []))

    @jsii.member(jsii_name="resetReconcileConnections")
    def reset_reconcile_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReconcileConnections", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSendPropagatedConnectionLimitIfZero")
    def reset_send_propagated_connection_limit_if_zero(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendPropagatedConnectionLimitIfZero", []))

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
    @jsii.member(jsii_name="connectedEndpoints")
    def connected_endpoints(self) -> "ComputeServiceAttachmentConnectedEndpointsList":
        return typing.cast("ComputeServiceAttachmentConnectedEndpointsList", jsii.get(self, "connectedEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="consumerAcceptLists")
    def consumer_accept_lists(
        self,
    ) -> "ComputeServiceAttachmentConsumerAcceptListsList":
        return typing.cast("ComputeServiceAttachmentConsumerAcceptListsList", jsii.get(self, "consumerAcceptLists"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeServiceAttachmentTimeoutsOutputReference":
        return typing.cast("ComputeServiceAttachmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="connectionPreferenceInput")
    def connection_preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerAcceptListsInput")
    def consumer_accept_lists_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeServiceAttachmentConsumerAcceptLists"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeServiceAttachmentConsumerAcceptLists"]]], jsii.get(self, "consumerAcceptListsInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerRejectListsInput")
    def consumer_reject_lists_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "consumerRejectListsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNamesInput")
    def domain_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableProxyProtocolInput")
    def enable_proxy_protocol_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableProxyProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="natSubnetsInput")
    def nat_subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "natSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="propagatedConnectionLimitInput")
    def propagated_connection_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "propagatedConnectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="reconcileConnectionsInput")
    def reconcile_connections_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reconcileConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sendPropagatedConnectionLimitIfZeroInput")
    def send_propagated_connection_limit_if_zero_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendPropagatedConnectionLimitIfZeroInput"))

    @builtins.property
    @jsii.member(jsii_name="targetServiceInput")
    def target_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeServiceAttachmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeServiceAttachmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionPreference")
    def connection_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionPreference"))

    @connection_preference.setter
    def connection_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f633aae85f0383b5fe8d82181e68b736cb57cd9d70f1cc495a29c70ace2e834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionPreference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerRejectLists")
    def consumer_reject_lists(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "consumerRejectLists"))

    @consumer_reject_lists.setter
    def consumer_reject_lists(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a43cc0684ac47fa37129674c07ba7066cc4f5c0d5b2c3e21cf94170b0ff0232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerRejectLists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b194d2976b7e09a865adc23386b2a3072594ccc9f4d8a10394e25e334e92e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainNames")
    def domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainNames"))

    @domain_names.setter
    def domain_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a6279aab30b5a83567b285b6fa3ddb9cf0974a47e40c658960723e0ede1eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableProxyProtocol")
    def enable_proxy_protocol(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableProxyProtocol"))

    @enable_proxy_protocol.setter
    def enable_proxy_protocol(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfaf6773cd6cd9ef4b24392b684541c5adb7e613c8731532f4263078205af6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableProxyProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688a2c47c228849738a3b7acc64eb17bffdf1a4224e1ee8441bb7ce8da6ef34c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35243c4421638c239b05db645f9d44b70e1cca4497d30115e881f139e6074ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natSubnets")
    def nat_subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "natSubnets"))

    @nat_subnets.setter
    def nat_subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5695c3a13c300a2dbe79a5a70fe6086d0563aed21207f806a8f79888732d0f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691eb79b19e67a0855a515fb1d58d4d548a368b4c712bdbd0908fd2587f37e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="propagatedConnectionLimit")
    def propagated_connection_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "propagatedConnectionLimit"))

    @propagated_connection_limit.setter
    def propagated_connection_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96f950857971cab3d8a3d4e12002b74940791b44d93da02fa046da174b96b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagatedConnectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reconcileConnections")
    def reconcile_connections(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reconcileConnections"))

    @reconcile_connections.setter
    def reconcile_connections(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f423c6c53c62ad9e083bfb75f6449fa6089dcf5cdc3b5d9ebf9b9529c3b8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reconcileConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3f7cc053a3173090ee9fc2918fd3420fba8a0ba1416b753372662d62be80f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendPropagatedConnectionLimitIfZero")
    def send_propagated_connection_limit_if_zero(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendPropagatedConnectionLimitIfZero"))

    @send_propagated_connection_limit_if_zero.setter
    def send_propagated_connection_limit_if_zero(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc338e63317081edc7fee6355b3cbf58abcc21e09fcb60c28810b22bf4ac50a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendPropagatedConnectionLimitIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetService")
    def target_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetService"))

    @target_service.setter
    def target_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f269d6d531940ffeda1eb110ddac85d434a101459e86abb9886be8cd7258414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetService", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_preference": "connectionPreference",
        "enable_proxy_protocol": "enableProxyProtocol",
        "name": "name",
        "nat_subnets": "natSubnets",
        "target_service": "targetService",
        "consumer_accept_lists": "consumerAcceptLists",
        "consumer_reject_lists": "consumerRejectLists",
        "description": "description",
        "domain_names": "domainNames",
        "id": "id",
        "project": "project",
        "propagated_connection_limit": "propagatedConnectionLimit",
        "reconcile_connections": "reconcileConnections",
        "region": "region",
        "send_propagated_connection_limit_if_zero": "sendPropagatedConnectionLimitIfZero",
        "timeouts": "timeouts",
    },
)
class ComputeServiceAttachmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_preference: builtins.str,
        enable_proxy_protocol: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        nat_subnets: typing.Sequence[builtins.str],
        target_service: builtins.str,
        consumer_accept_lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeServiceAttachmentConsumerAcceptLists", typing.Dict[builtins.str, typing.Any]]]]] = None,
        consumer_reject_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        propagated_connection_limit: typing.Optional[jsii.Number] = None,
        reconcile_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        send_propagated_connection_limit_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeServiceAttachmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_preference: The connection preference to use for this service attachment. Valid values include "ACCEPT_AUTOMATIC", "ACCEPT_MANUAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#connection_preference ComputeServiceAttachment#connection_preference}
        :param enable_proxy_protocol: If true, enable the proxy protocol which is for supplying client TCP/IP address data in TCP connections that traverse proxies on their way to destination servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#enable_proxy_protocol ComputeServiceAttachment#enable_proxy_protocol}
        :param name: Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#name ComputeServiceAttachment#name}
        :param nat_subnets: An array of subnets that is provided for NAT in this service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#nat_subnets ComputeServiceAttachment#nat_subnets}
        :param target_service: The URL of a service serving the endpoint identified by this service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#target_service ComputeServiceAttachment#target_service}
        :param consumer_accept_lists: consumer_accept_lists block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#consumer_accept_lists ComputeServiceAttachment#consumer_accept_lists}
        :param consumer_reject_lists: An array of projects that are not allowed to connect to this service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#consumer_reject_lists ComputeServiceAttachment#consumer_reject_lists}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#description ComputeServiceAttachment#description}
        :param domain_names: If specified, the domain name will be used during the integration between the PSC connected endpoints and the Cloud DNS. For example, this is a valid domain name: "p.mycompany.com.". Current max number of domain names supported is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#domain_names ComputeServiceAttachment#domain_names}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#id ComputeServiceAttachment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#project ComputeServiceAttachment#project}.
        :param propagated_connection_limit: The number of consumer spokes that connected Private Service Connect endpoints can be propagated to through Network Connectivity Center. This limit lets the service producer limit how many propagated Private Service Connect connections can be established to this service attachment from a single consumer. If the connection preference of the service attachment is ACCEPT_MANUAL, the limit applies to each project or network that is listed in the consumer accept list. If the connection preference of the service attachment is ACCEPT_AUTOMATIC, the limit applies to each project that contains a connected endpoint. If unspecified, the default propagated connection limit is 250. To explicitly send a zero value, set 'send_propagated_connection_limit_if_zero = true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#propagated_connection_limit ComputeServiceAttachment#propagated_connection_limit}
        :param reconcile_connections: This flag determines whether a consumer accept/reject list change can reconcile the statuses of existing ACCEPTED or REJECTED PSC endpoints. If false, connection policy update will only affect existing PENDING PSC endpoints. Existing ACCEPTED/REJECTED endpoints will remain untouched regardless how the connection policy is modified . If true, update will affect both PENDING and ACCEPTED/REJECTED PSC endpoints. For example, an ACCEPTED PSC endpoint will be moved to REJECTED if its project is added to the reject list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#reconcile_connections ComputeServiceAttachment#reconcile_connections}
        :param region: URL of the region where the resource resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#region ComputeServiceAttachment#region}
        :param send_propagated_connection_limit_if_zero: Controls the behavior of propagated_connection_limit. When false, setting propagated_connection_limit to zero causes the provider to use to the API's default value. When true, the provider will set propagated_connection_limit to zero. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#send_propagated_connection_limit_if_zero ComputeServiceAttachment#send_propagated_connection_limit_if_zero}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#timeouts ComputeServiceAttachment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeServiceAttachmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac8f29528ebe42d0217defa3c9cead47c833b19c65d05af35bdd01463290e2a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_preference", value=connection_preference, expected_type=type_hints["connection_preference"])
            check_type(argname="argument enable_proxy_protocol", value=enable_proxy_protocol, expected_type=type_hints["enable_proxy_protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nat_subnets", value=nat_subnets, expected_type=type_hints["nat_subnets"])
            check_type(argname="argument target_service", value=target_service, expected_type=type_hints["target_service"])
            check_type(argname="argument consumer_accept_lists", value=consumer_accept_lists, expected_type=type_hints["consumer_accept_lists"])
            check_type(argname="argument consumer_reject_lists", value=consumer_reject_lists, expected_type=type_hints["consumer_reject_lists"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument propagated_connection_limit", value=propagated_connection_limit, expected_type=type_hints["propagated_connection_limit"])
            check_type(argname="argument reconcile_connections", value=reconcile_connections, expected_type=type_hints["reconcile_connections"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument send_propagated_connection_limit_if_zero", value=send_propagated_connection_limit_if_zero, expected_type=type_hints["send_propagated_connection_limit_if_zero"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_preference": connection_preference,
            "enable_proxy_protocol": enable_proxy_protocol,
            "name": name,
            "nat_subnets": nat_subnets,
            "target_service": target_service,
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
        if consumer_accept_lists is not None:
            self._values["consumer_accept_lists"] = consumer_accept_lists
        if consumer_reject_lists is not None:
            self._values["consumer_reject_lists"] = consumer_reject_lists
        if description is not None:
            self._values["description"] = description
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if propagated_connection_limit is not None:
            self._values["propagated_connection_limit"] = propagated_connection_limit
        if reconcile_connections is not None:
            self._values["reconcile_connections"] = reconcile_connections
        if region is not None:
            self._values["region"] = region
        if send_propagated_connection_limit_if_zero is not None:
            self._values["send_propagated_connection_limit_if_zero"] = send_propagated_connection_limit_if_zero
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
    def connection_preference(self) -> builtins.str:
        '''The connection preference to use for this service attachment. Valid values include "ACCEPT_AUTOMATIC", "ACCEPT_MANUAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#connection_preference ComputeServiceAttachment#connection_preference}
        '''
        result = self._values.get("connection_preference")
        assert result is not None, "Required property 'connection_preference' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_proxy_protocol(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, enable the proxy protocol which is for supplying client TCP/IP address data in TCP connections that traverse proxies on their way to destination servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#enable_proxy_protocol ComputeServiceAttachment#enable_proxy_protocol}
        '''
        result = self._values.get("enable_proxy_protocol")
        assert result is not None, "Required property 'enable_proxy_protocol' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#name ComputeServiceAttachment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nat_subnets(self) -> typing.List[builtins.str]:
        '''An array of subnets that is provided for NAT in this service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#nat_subnets ComputeServiceAttachment#nat_subnets}
        '''
        result = self._values.get("nat_subnets")
        assert result is not None, "Required property 'nat_subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_service(self) -> builtins.str:
        '''The URL of a service serving the endpoint identified by this service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#target_service ComputeServiceAttachment#target_service}
        '''
        result = self._values.get("target_service")
        assert result is not None, "Required property 'target_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_accept_lists(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeServiceAttachmentConsumerAcceptLists"]]]:
        '''consumer_accept_lists block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#consumer_accept_lists ComputeServiceAttachment#consumer_accept_lists}
        '''
        result = self._values.get("consumer_accept_lists")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeServiceAttachmentConsumerAcceptLists"]]], result)

    @builtins.property
    def consumer_reject_lists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of projects that are not allowed to connect to this service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#consumer_reject_lists ComputeServiceAttachment#consumer_reject_lists}
        '''
        result = self._values.get("consumer_reject_lists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#description ComputeServiceAttachment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified, the domain name will be used during the integration between the PSC connected endpoints and the Cloud DNS.

        For example, this is a
        valid domain name: "p.mycompany.com.". Current max number of domain names
        supported is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#domain_names ComputeServiceAttachment#domain_names}
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#id ComputeServiceAttachment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#project ComputeServiceAttachment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagated_connection_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of consumer spokes that connected Private Service Connect endpoints can be propagated to through Network Connectivity Center.

        This limit lets the service producer limit how many propagated Private Service Connect connections can be established to this service attachment from a single consumer.

        If the connection preference of the service attachment is ACCEPT_MANUAL, the limit applies to each project or network that is listed in the consumer accept list.
        If the connection preference of the service attachment is ACCEPT_AUTOMATIC, the limit applies to each project that contains a connected endpoint.

        If unspecified, the default propagated connection limit is 250. To explicitly send a zero value, set 'send_propagated_connection_limit_if_zero = true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#propagated_connection_limit ComputeServiceAttachment#propagated_connection_limit}
        '''
        result = self._values.get("propagated_connection_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reconcile_connections(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag determines whether a consumer accept/reject list change can reconcile the statuses of existing ACCEPTED or REJECTED PSC endpoints.

        If false, connection policy update will only affect existing PENDING PSC endpoints. Existing ACCEPTED/REJECTED endpoints will remain untouched regardless how the connection policy is modified .
        If true, update will affect both PENDING and ACCEPTED/REJECTED PSC endpoints. For example, an ACCEPTED PSC endpoint will be moved to REJECTED if its project is added to the reject list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#reconcile_connections ComputeServiceAttachment#reconcile_connections}
        '''
        result = self._values.get("reconcile_connections")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''URL of the region where the resource resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#region ComputeServiceAttachment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_propagated_connection_limit_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls the behavior of propagated_connection_limit.

        When false, setting propagated_connection_limit to zero causes the provider to use to the API's default value.
        When true, the provider will set propagated_connection_limit to zero.
        Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#send_propagated_connection_limit_if_zero ComputeServiceAttachment#send_propagated_connection_limit_if_zero}
        '''
        result = self._values.get("send_propagated_connection_limit_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeServiceAttachmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#timeouts ComputeServiceAttachment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeServiceAttachmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeServiceAttachmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConnectedEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeServiceAttachmentConnectedEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeServiceAttachmentConnectedEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeServiceAttachmentConnectedEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConnectedEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c45f031a24d1109d2ad7235274a10aee930f699192393ae9b8e5432bb58d24f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeServiceAttachmentConnectedEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e636375b34aeb21798ea9bacb044fabb722614a742b4f1c98da350c1edfd8042)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeServiceAttachmentConnectedEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e833dec45c81ce0f9b62d13360ee006e9de83782d9508345fee84e34c6a1dd39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a148cf7376dcf57f258331b5c233ca85c2bf975b02c1d90d64dbd83fd0bffb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a1fa830accd3c07b4f0ce5ce2e751ec354d483f02f3f7a9f59a968bcaa9def7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeServiceAttachmentConnectedEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConnectedEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__231056fb01b2f0efccf154fbd5982a39f88777966c77462b379fe9a66d326d4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="consumerNetwork")
    def consumer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerNetwork"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="propagatedConnectionCount")
    def propagated_connection_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "propagatedConnectionCount"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeServiceAttachmentConnectedEndpoints]:
        return typing.cast(typing.Optional[ComputeServiceAttachmentConnectedEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeServiceAttachmentConnectedEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb6280e34da8940e489f76a35f9a6a8f316b1b841673ec0cbc1bdea96745d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConsumerAcceptLists",
    jsii_struct_bases=[],
    name_mapping={
        "connection_limit": "connectionLimit",
        "network_url": "networkUrl",
        "project_id_or_num": "projectIdOrNum",
    },
)
class ComputeServiceAttachmentConsumerAcceptLists:
    def __init__(
        self,
        *,
        connection_limit: jsii.Number,
        network_url: typing.Optional[builtins.str] = None,
        project_id_or_num: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection_limit: The number of consumer forwarding rules the consumer project can create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#connection_limit ComputeServiceAttachment#connection_limit}
        :param network_url: The network that is allowed to connect to this service attachment. Only one of project_id_or_num and network_url may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#network_url ComputeServiceAttachment#network_url}
        :param project_id_or_num: A project that is allowed to connect to this service attachment. Only one of project_id_or_num and network_url may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#project_id_or_num ComputeServiceAttachment#project_id_or_num}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b9530e27975b6b40af1e0c65ab2d6d8339d1f69996e3ecb0010d31ab81867f)
            check_type(argname="argument connection_limit", value=connection_limit, expected_type=type_hints["connection_limit"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument project_id_or_num", value=project_id_or_num, expected_type=type_hints["project_id_or_num"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_limit": connection_limit,
        }
        if network_url is not None:
            self._values["network_url"] = network_url
        if project_id_or_num is not None:
            self._values["project_id_or_num"] = project_id_or_num

    @builtins.property
    def connection_limit(self) -> jsii.Number:
        '''The number of consumer forwarding rules the consumer project can create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#connection_limit ComputeServiceAttachment#connection_limit}
        '''
        result = self._values.get("connection_limit")
        assert result is not None, "Required property 'connection_limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def network_url(self) -> typing.Optional[builtins.str]:
        '''The network that is allowed to connect to this service attachment. Only one of project_id_or_num and network_url may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#network_url ComputeServiceAttachment#network_url}
        '''
        result = self._values.get("network_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id_or_num(self) -> typing.Optional[builtins.str]:
        '''A project that is allowed to connect to this service attachment. Only one of project_id_or_num and network_url may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#project_id_or_num ComputeServiceAttachment#project_id_or_num}
        '''
        result = self._values.get("project_id_or_num")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeServiceAttachmentConsumerAcceptLists(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeServiceAttachmentConsumerAcceptListsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConsumerAcceptListsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c2ea8c7545b05cc45eeddb475d56900b54c256acfc491aec2eb18f76658faf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeServiceAttachmentConsumerAcceptListsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce852ae337d7da3e52cabdc134a3d955d6440a93b348fdffebab62af412dc619)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeServiceAttachmentConsumerAcceptListsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1adc8eb9d04e647d7d87d494fe0e621c8860ab97e7d5b7c0c68405df99e5b4d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dac726d641968ea44277e89742b4cd663ff2b67c53e270ee8d5c5583b8ca1055)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f217360823f7d1d73035d53efe794f2b2e12b1061752e30ad8dc4d16ed75ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeServiceAttachmentConsumerAcceptLists]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeServiceAttachmentConsumerAcceptLists]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeServiceAttachmentConsumerAcceptLists]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af7e084061c45999fe1328107936a0f903c3a46e441fd7ce2f414bd4861ed32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeServiceAttachmentConsumerAcceptListsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentConsumerAcceptListsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54e8cfc21015b352ac16d7532e4f862ea00720e2378fd926b2a68affe6d2a73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetworkUrl")
    def reset_network_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkUrl", []))

    @jsii.member(jsii_name="resetProjectIdOrNum")
    def reset_project_id_or_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectIdOrNum", []))

    @builtins.property
    @jsii.member(jsii_name="connectionLimitInput")
    def connection_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdOrNumInput")
    def project_id_or_num_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdOrNumInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionLimit")
    def connection_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionLimit"))

    @connection_limit.setter
    def connection_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875a5d7942dda7962ef18b55a3ac36f6f0bfb8eb5bb92696429fe28f3a6166b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55b03fb2040d09502b113688dce0659505adee8908f5cd7e69b2fd89bc47584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectIdOrNum")
    def project_id_or_num(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectIdOrNum"))

    @project_id_or_num.setter
    def project_id_or_num(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdff63d2e46f84fc93713a3f395a07e66ea8477ed902d4c8ebdfa05a381dabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectIdOrNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentConsumerAcceptLists]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentConsumerAcceptLists]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentConsumerAcceptLists]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15b696d3ee11c225993c0f095e5ec4f274981c4da55607d61b27703fe42adee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeServiceAttachmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#create ComputeServiceAttachment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#delete ComputeServiceAttachment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#update ComputeServiceAttachment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629008a49e23151c175437f81d0f6d9b5a9a22f23f804773e72706c094ecd8a9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#create ComputeServiceAttachment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#delete ComputeServiceAttachment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_service_attachment#update ComputeServiceAttachment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeServiceAttachmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeServiceAttachmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeServiceAttachment.ComputeServiceAttachmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__654dde128b1e8ea855aa9d0f23e768c60a3e4ffa477831f1aed8699a3099412c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd84f1ac2aa0d3681cf073fad58da920669360d5c48961554421087ac05191f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77e0cfccb42a261e58c9eacd4f1ed2b27ac9b0ec6c610321a16406e9510da98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629db2560fe7989eff2b8bd16ad67be3d628e64891e088010999f746fd236644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba262495576eece5420657c5e753aed1830cf844232b4df387a49c097bb67e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeServiceAttachment",
    "ComputeServiceAttachmentConfig",
    "ComputeServiceAttachmentConnectedEndpoints",
    "ComputeServiceAttachmentConnectedEndpointsList",
    "ComputeServiceAttachmentConnectedEndpointsOutputReference",
    "ComputeServiceAttachmentConsumerAcceptLists",
    "ComputeServiceAttachmentConsumerAcceptListsList",
    "ComputeServiceAttachmentConsumerAcceptListsOutputReference",
    "ComputeServiceAttachmentTimeouts",
    "ComputeServiceAttachmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c41ec140610d154cdadef1c5f1774e185cb5041a553e15790f38699ff2d2d97b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_preference: builtins.str,
    enable_proxy_protocol: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    nat_subnets: typing.Sequence[builtins.str],
    target_service: builtins.str,
    consumer_accept_lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeServiceAttachmentConsumerAcceptLists, typing.Dict[builtins.str, typing.Any]]]]] = None,
    consumer_reject_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    propagated_connection_limit: typing.Optional[jsii.Number] = None,
    reconcile_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    send_propagated_connection_limit_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeServiceAttachmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__92a87a4c5db83bc677ac8157cdfc3aa00fab978f450979ad707ca74f67c9b7a3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ca0a324f059f12c0f8be90042c0e590836773918eced3b5d4cc389c20bcb85(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeServiceAttachmentConsumerAcceptLists, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f633aae85f0383b5fe8d82181e68b736cb57cd9d70f1cc495a29c70ace2e834(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a43cc0684ac47fa37129674c07ba7066cc4f5c0d5b2c3e21cf94170b0ff0232(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b194d2976b7e09a865adc23386b2a3072594ccc9f4d8a10394e25e334e92e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a6279aab30b5a83567b285b6fa3ddb9cf0974a47e40c658960723e0ede1eb8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfaf6773cd6cd9ef4b24392b684541c5adb7e613c8731532f4263078205af6e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688a2c47c228849738a3b7acc64eb17bffdf1a4224e1ee8441bb7ce8da6ef34c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35243c4421638c239b05db645f9d44b70e1cca4497d30115e881f139e6074ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5695c3a13c300a2dbe79a5a70fe6086d0563aed21207f806a8f79888732d0f97(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691eb79b19e67a0855a515fb1d58d4d548a368b4c712bdbd0908fd2587f37e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96f950857971cab3d8a3d4e12002b74940791b44d93da02fa046da174b96b87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f423c6c53c62ad9e083bfb75f6449fa6089dcf5cdc3b5d9ebf9b9529c3b8bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3f7cc053a3173090ee9fc2918fd3420fba8a0ba1416b753372662d62be80f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc338e63317081edc7fee6355b3cbf58abcc21e09fcb60c28810b22bf4ac50a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f269d6d531940ffeda1eb110ddac85d434a101459e86abb9886be8cd7258414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac8f29528ebe42d0217defa3c9cead47c833b19c65d05af35bdd01463290e2a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_preference: builtins.str,
    enable_proxy_protocol: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    nat_subnets: typing.Sequence[builtins.str],
    target_service: builtins.str,
    consumer_accept_lists: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeServiceAttachmentConsumerAcceptLists, typing.Dict[builtins.str, typing.Any]]]]] = None,
    consumer_reject_lists: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    propagated_connection_limit: typing.Optional[jsii.Number] = None,
    reconcile_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    send_propagated_connection_limit_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeServiceAttachmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c45f031a24d1109d2ad7235274a10aee930f699192393ae9b8e5432bb58d24f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e636375b34aeb21798ea9bacb044fabb722614a742b4f1c98da350c1edfd8042(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e833dec45c81ce0f9b62d13360ee006e9de83782d9508345fee84e34c6a1dd39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a148cf7376dcf57f258331b5c233ca85c2bf975b02c1d90d64dbd83fd0bffb2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1fa830accd3c07b4f0ce5ce2e751ec354d483f02f3f7a9f59a968bcaa9def7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231056fb01b2f0efccf154fbd5982a39f88777966c77462b379fe9a66d326d4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb6280e34da8940e489f76a35f9a6a8f316b1b841673ec0cbc1bdea96745d70(
    value: typing.Optional[ComputeServiceAttachmentConnectedEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b9530e27975b6b40af1e0c65ab2d6d8339d1f69996e3ecb0010d31ab81867f(
    *,
    connection_limit: jsii.Number,
    network_url: typing.Optional[builtins.str] = None,
    project_id_or_num: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2ea8c7545b05cc45eeddb475d56900b54c256acfc491aec2eb18f76658faf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce852ae337d7da3e52cabdc134a3d955d6440a93b348fdffebab62af412dc619(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adc8eb9d04e647d7d87d494fe0e621c8860ab97e7d5b7c0c68405df99e5b4d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac726d641968ea44277e89742b4cd663ff2b67c53e270ee8d5c5583b8ca1055(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f217360823f7d1d73035d53efe794f2b2e12b1061752e30ad8dc4d16ed75ba9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af7e084061c45999fe1328107936a0f903c3a46e441fd7ce2f414bd4861ed32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeServiceAttachmentConsumerAcceptLists]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54e8cfc21015b352ac16d7532e4f862ea00720e2378fd926b2a68affe6d2a73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875a5d7942dda7962ef18b55a3ac36f6f0bfb8eb5bb92696429fe28f3a6166b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55b03fb2040d09502b113688dce0659505adee8908f5cd7e69b2fd89bc47584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdff63d2e46f84fc93713a3f395a07e66ea8477ed902d4c8ebdfa05a381dabb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15b696d3ee11c225993c0f095e5ec4f274981c4da55607d61b27703fe42adee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentConsumerAcceptLists]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629008a49e23151c175437f81d0f6d9b5a9a22f23f804773e72706c094ecd8a9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654dde128b1e8ea855aa9d0f23e768c60a3e4ffa477831f1aed8699a3099412c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd84f1ac2aa0d3681cf073fad58da920669360d5c48961554421087ac05191f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77e0cfccb42a261e58c9eacd4f1ed2b27ac9b0ec6c610321a16406e9510da98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629db2560fe7989eff2b8bd16ad67be3d628e64891e088010999f746fd236644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba262495576eece5420657c5e753aed1830cf844232b4df387a49c097bb67e20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeServiceAttachmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
