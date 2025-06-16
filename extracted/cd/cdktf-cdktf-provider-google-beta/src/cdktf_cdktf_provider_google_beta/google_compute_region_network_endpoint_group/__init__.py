r'''
# `google_compute_region_network_endpoint_group`

Refer to the Terraform Registry for docs: [`google_compute_region_network_endpoint_group`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group).
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


class GoogleComputeRegionNetworkEndpointGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group google_compute_region_network_endpoint_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        region: builtins.str,
        app_engine: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupAppEngine", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_function: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupCloudFunction", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_run: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupCloudRun", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_endpoint_type: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        psc_data: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupPscData", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_target_service: typing.Optional[builtins.str] = None,
        serverless_deployment: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupServerlessDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group google_compute_region_network_endpoint_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#name GoogleComputeRegionNetworkEndpointGroup#name}
        :param region: A reference to the region where the regional NEGs reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#region GoogleComputeRegionNetworkEndpointGroup#region}
        :param app_engine: app_engine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#app_engine GoogleComputeRegionNetworkEndpointGroup#app_engine}
        :param cloud_function: cloud_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#cloud_function GoogleComputeRegionNetworkEndpointGroup#cloud_function}
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#cloud_run GoogleComputeRegionNetworkEndpointGroup#cloud_run}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#description GoogleComputeRegionNetworkEndpointGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#id GoogleComputeRegionNetworkEndpointGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network: This field is only used for PSC and INTERNET NEGs. The URL of the network to which all network endpoints in the NEG belong. Uses "default" project network if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#network GoogleComputeRegionNetworkEndpointGroup#network}
        :param network_endpoint_type: Type of network endpoints in this network endpoint group. Defaults to SERVERLESS. Default value: "SERVERLESS" Possible values: ["SERVERLESS", "PRIVATE_SERVICE_CONNECT", "INTERNET_IP_PORT", "INTERNET_FQDN_PORT", "GCE_VM_IP_PORTMAP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#network_endpoint_type GoogleComputeRegionNetworkEndpointGroup#network_endpoint_type}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#project GoogleComputeRegionNetworkEndpointGroup#project}.
        :param psc_data: psc_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#psc_data GoogleComputeRegionNetworkEndpointGroup#psc_data}
        :param psc_target_service: This field is only used for PSC and INTERNET NEGs. The target service url used to set up private service connection to a Google API or a PSC Producer Service Attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#psc_target_service GoogleComputeRegionNetworkEndpointGroup#psc_target_service}
        :param serverless_deployment: serverless_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#serverless_deployment GoogleComputeRegionNetworkEndpointGroup#serverless_deployment}
        :param subnetwork: This field is only used for PSC NEGs. Optional URL of the subnetwork to which all network endpoints in the NEG belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#subnetwork GoogleComputeRegionNetworkEndpointGroup#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#timeouts GoogleComputeRegionNetworkEndpointGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2aeaea7a4fbd3697f4d3cddfaaae113f436e2e798b38f6b54c51885c4264ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRegionNetworkEndpointGroupConfig(
            name=name,
            region=region,
            app_engine=app_engine,
            cloud_function=cloud_function,
            cloud_run=cloud_run,
            description=description,
            id=id,
            network=network,
            network_endpoint_type=network_endpoint_type,
            project=project,
            psc_data=psc_data,
            psc_target_service=psc_target_service,
            serverless_deployment=serverless_deployment,
            subnetwork=subnetwork,
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
        '''Generates CDKTF code for importing a GoogleComputeRegionNetworkEndpointGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeRegionNetworkEndpointGroup to import.
        :param import_from_id: The id of the existing GoogleComputeRegionNetworkEndpointGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeRegionNetworkEndpointGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74d7e96aaf39d8f422b55802e054a8dea10de8c4c036e84b63708af171a3776)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAppEngine")
    def put_app_engine(
        self,
        *,
        service: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Optional serving service. The service name must be 1-63 characters long, and comply with RFC1035. Example value: "default", "my-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#service GoogleComputeRegionNetworkEndpointGroup#service}
        :param url_mask: A template to parse service and version fields from a request URL. URL mask allows for routing to multiple App Engine services without having to create multiple Network Endpoint Groups and backend services. For example, the request URLs "foo1-dot-appname.appspot.com/v1" and "foo1-dot-appname.appspot.com/v2" can be backed by the same Serverless NEG with URL mask "-dot-appname.appspot.com/". The URL mask will parse them to { service = "foo1", version = "v1" } and { service = "foo1", version = "v2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        :param version: Optional serving version. The version must be 1-63 characters long, and comply with RFC1035. Example value: "v1", "v2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#version GoogleComputeRegionNetworkEndpointGroup#version}
        '''
        value = GoogleComputeRegionNetworkEndpointGroupAppEngine(
            service=service, url_mask=url_mask, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngine", [value]))

    @jsii.member(jsii_name="putCloudFunction")
    def put_cloud_function(
        self,
        *,
        function: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function: A user-defined name of the Cloud Function. The function name is case-sensitive and must be 1-63 characters long. Example value: "func1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#function GoogleComputeRegionNetworkEndpointGroup#function}
        :param url_mask: A template to parse function field from a request URL. URL mask allows for routing to multiple Cloud Functions without having to create multiple Network Endpoint Groups and backend services. For example, request URLs "mydomain.com/function1" and "mydomain.com/function2" can be backed by the same Serverless NEG with URL mask "/". The URL mask will parse them to { function = "function1" } and { function = "function2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        value = GoogleComputeRegionNetworkEndpointGroupCloudFunction(
            function=function, url_mask=url_mask
        )

        return typing.cast(None, jsii.invoke(self, "putCloudFunction", [value]))

    @jsii.member(jsii_name="putCloudRun")
    def put_cloud_run(
        self,
        *,
        service: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Cloud Run service is the main resource of Cloud Run. The service must be 1-63 characters long, and comply with RFC1035. Example value: "run-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#service GoogleComputeRegionNetworkEndpointGroup#service}
        :param tag: Cloud Run tag represents the "named-revision" to provide additional fine-grained traffic routing information. The tag must be 1-63 characters long, and comply with RFC1035. Example value: "revision-0010". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#tag GoogleComputeRegionNetworkEndpointGroup#tag}
        :param url_mask: A template to parse service and tag fields from a request URL. URL mask allows for routing to multiple Run services without having to create multiple network endpoint groups and backend services. For example, request URLs "foo1.domain.com/bar1" and "foo1.domain.com/bar2" an be backed by the same Serverless Network Endpoint Group (NEG) with URL mask ".domain.com/". The URL mask will parse them to { service="bar1", tag="foo1" } and { service="bar2", tag="foo2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        value = GoogleComputeRegionNetworkEndpointGroupCloudRun(
            service=service, tag=tag, url_mask=url_mask
        )

        return typing.cast(None, jsii.invoke(self, "putCloudRun", [value]))

    @jsii.member(jsii_name="putPscData")
    def put_psc_data(
        self,
        *,
        producer_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param producer_port: The PSC producer port to use when consumer PSC NEG connects to a producer. If this flag isn't specified for a PSC NEG with endpoint type private-service-connect, then PSC NEG will be connected to a first port in the available PSC producer port range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#producer_port GoogleComputeRegionNetworkEndpointGroup#producer_port}
        '''
        value = GoogleComputeRegionNetworkEndpointGroupPscData(
            producer_port=producer_port
        )

        return typing.cast(None, jsii.invoke(self, "putPscData", [value]))

    @jsii.member(jsii_name="putServerlessDeployment")
    def put_serverless_deployment(
        self,
        *,
        platform: builtins.str,
        resource: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param platform: The platform of the NEG backend target(s). Possible values: API Gateway: apigateway.googleapis.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#platform GoogleComputeRegionNetworkEndpointGroup#platform}
        :param resource: The user-defined name of the workload/instance. This value must be provided explicitly or in the urlMask. The resource identified by this value is platform-specific and is as follows: API Gateway: The gateway ID, App Engine: The service name, Cloud Functions: The function name, Cloud Run: The service name Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#resource GoogleComputeRegionNetworkEndpointGroup#resource}
        :param url_mask: A template to parse platform-specific fields from a request URL. URL mask allows for routing to multiple resources on the same serverless platform without having to create multiple Network Endpoint Groups and backend resources. The fields parsed by this template are platform-specific and are as follows: API Gateway: The gateway ID, App Engine: The service and version, Cloud Functions: The function name, Cloud Run: The service and tag Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        :param version: The optional resource version. The version identified by this value is platform-specific and is follows: API Gateway: Unused, App Engine: The service version, Cloud Functions: Unused, Cloud Run: The service tag Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#version GoogleComputeRegionNetworkEndpointGroup#version}
        '''
        value = GoogleComputeRegionNetworkEndpointGroupServerlessDeployment(
            platform=platform, resource=resource, url_mask=url_mask, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putServerlessDeployment", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#create GoogleComputeRegionNetworkEndpointGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#delete GoogleComputeRegionNetworkEndpointGroup#delete}.
        '''
        value = GoogleComputeRegionNetworkEndpointGroupTimeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppEngine")
    def reset_app_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngine", []))

    @jsii.member(jsii_name="resetCloudFunction")
    def reset_cloud_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudFunction", []))

    @jsii.member(jsii_name="resetCloudRun")
    def reset_cloud_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRun", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkEndpointType")
    def reset_network_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkEndpointType", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPscData")
    def reset_psc_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscData", []))

    @jsii.member(jsii_name="resetPscTargetService")
    def reset_psc_target_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscTargetService", []))

    @jsii.member(jsii_name="resetServerlessDeployment")
    def reset_serverless_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessDeployment", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

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
    @jsii.member(jsii_name="appEngine")
    def app_engine(
        self,
    ) -> "GoogleComputeRegionNetworkEndpointGroupAppEngineOutputReference":
        return typing.cast("GoogleComputeRegionNetworkEndpointGroupAppEngineOutputReference", jsii.get(self, "appEngine"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunction")
    def cloud_function(
        self,
    ) -> "GoogleComputeRegionNetworkEndpointGroupCloudFunctionOutputReference":
        return typing.cast("GoogleComputeRegionNetworkEndpointGroupCloudFunctionOutputReference", jsii.get(self, "cloudFunction"))

    @builtins.property
    @jsii.member(jsii_name="cloudRun")
    def cloud_run(
        self,
    ) -> "GoogleComputeRegionNetworkEndpointGroupCloudRunOutputReference":
        return typing.cast("GoogleComputeRegionNetworkEndpointGroupCloudRunOutputReference", jsii.get(self, "cloudRun"))

    @builtins.property
    @jsii.member(jsii_name="pscData")
    def psc_data(
        self,
    ) -> "GoogleComputeRegionNetworkEndpointGroupPscDataOutputReference":
        return typing.cast("GoogleComputeRegionNetworkEndpointGroupPscDataOutputReference", jsii.get(self, "pscData"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serverlessDeployment")
    def serverless_deployment(
        self,
    ) -> "GoogleComputeRegionNetworkEndpointGroupServerlessDeploymentOutputReference":
        return typing.cast("GoogleComputeRegionNetworkEndpointGroupServerlessDeploymentOutputReference", jsii.get(self, "serverlessDeployment"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleComputeRegionNetworkEndpointGroupTimeoutsOutputReference":
        return typing.cast("GoogleComputeRegionNetworkEndpointGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appEngineInput")
    def app_engine_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupAppEngine"]:
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupAppEngine"], jsii.get(self, "appEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionInput")
    def cloud_function_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupCloudFunction"]:
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupCloudFunction"], jsii.get(self, "cloudFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunInput")
    def cloud_run_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupCloudRun"]:
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupCloudRun"], jsii.get(self, "cloudRunInput"))

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
    @jsii.member(jsii_name="networkEndpointTypeInput")
    def network_endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkEndpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscDataInput")
    def psc_data_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupPscData"]:
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupPscData"], jsii.get(self, "pscDataInput"))

    @builtins.property
    @jsii.member(jsii_name="pscTargetServiceInput")
    def psc_target_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pscTargetServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessDeploymentInput")
    def serverless_deployment_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupServerlessDeployment"]:
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupServerlessDeployment"], jsii.get(self, "serverlessDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionNetworkEndpointGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionNetworkEndpointGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1241ba789a6f482f46233d2694a3124e4dc12c1e43b9cff5a1aed70321bd0187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66230cf94cad80a52c6d76cfd6b045a32c72c34bc0c2d9a52e1b503ab7fb0463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1172566b8f6c22d16bedbc989e610400f868b17f03d526c237c1b1508b44f781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4663ef77d544a37f11318a7e75bd5df01ef5c9d54bacc0dfc62b41b76fdebb35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkEndpointType")
    def network_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkEndpointType"))

    @network_endpoint_type.setter
    def network_endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850ae39a816f421ef7a0c88e2555932af27852f4d36fc7bff2e80025106d7505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkEndpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f56e660faf921c296d3a46ea9b2a0844b7b43225a08eb339e3ad17872450fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pscTargetService")
    def psc_target_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscTargetService"))

    @psc_target_service.setter
    def psc_target_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2818ad4470ef434a9aa093933d5938ec34d5ae87643ab24dd46fc76f2b0289b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscTargetService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8aaf4aa9e0329bb03190ff9b4ec67f19cc8c240580acb2c5e370281c377cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8b0f7d0b6de4ea39b124211aac3b27f3bdeac605fa0fc3ec87ea9c65c54ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupAppEngine",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "url_mask": "urlMask", "version": "version"},
)
class GoogleComputeRegionNetworkEndpointGroupAppEngine:
    def __init__(
        self,
        *,
        service: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Optional serving service. The service name must be 1-63 characters long, and comply with RFC1035. Example value: "default", "my-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#service GoogleComputeRegionNetworkEndpointGroup#service}
        :param url_mask: A template to parse service and version fields from a request URL. URL mask allows for routing to multiple App Engine services without having to create multiple Network Endpoint Groups and backend services. For example, the request URLs "foo1-dot-appname.appspot.com/v1" and "foo1-dot-appname.appspot.com/v2" can be backed by the same Serverless NEG with URL mask "-dot-appname.appspot.com/". The URL mask will parse them to { service = "foo1", version = "v1" } and { service = "foo1", version = "v2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        :param version: Optional serving version. The version must be 1-63 characters long, and comply with RFC1035. Example value: "v1", "v2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#version GoogleComputeRegionNetworkEndpointGroup#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e7571c87b084b4e1931b70f0750945f6aa57b94414bf88b206cfb426e37ede)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument url_mask", value=url_mask, expected_type=type_hints["url_mask"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service is not None:
            self._values["service"] = service
        if url_mask is not None:
            self._values["url_mask"] = url_mask
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Optional serving service. The service name must be 1-63 characters long, and comply with RFC1035. Example value: "default", "my-service".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#service GoogleComputeRegionNetworkEndpointGroup#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_mask(self) -> typing.Optional[builtins.str]:
        '''A template to parse service and version fields from a request URL.

        URL mask allows for routing to multiple App Engine services without
        having to create multiple Network Endpoint Groups and backend services.

        For example, the request URLs "foo1-dot-appname.appspot.com/v1" and
        "foo1-dot-appname.appspot.com/v2" can be backed by the same Serverless NEG with
        URL mask "-dot-appname.appspot.com/". The URL mask will parse
        them to { service = "foo1", version = "v1" } and { service = "foo1", version = "v2" } respectively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional serving version. The version must be 1-63 characters long, and comply with RFC1035. Example value: "v1", "v2".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#version GoogleComputeRegionNetworkEndpointGroup#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupAppEngine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionNetworkEndpointGroupAppEngineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupAppEngineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db13ff2e39cd9009d9f3d6d8522c7ada865f7f6db5f48622eec719cad598866b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetUrlMask")
    def reset_url_mask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlMask", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="urlMaskInput")
    def url_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad1ec0d13fce4418fe5c5ee1d5614fe58ffb724ca9553b3c27da2a1a9728b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f820a655cbd876c89ecbb44eeb01da39829e010d9e090fda17200c61041844a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c776292f01fcc2b848d1883d4f3a747a94469f539739336ac7a2afe5fb67a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupAppEngine]:
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupAppEngine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupAppEngine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676a110fc389f0c0a258779a4bc124ba367b310844a27a03a00820c15e798da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupCloudFunction",
    jsii_struct_bases=[],
    name_mapping={"function": "function", "url_mask": "urlMask"},
)
class GoogleComputeRegionNetworkEndpointGroupCloudFunction:
    def __init__(
        self,
        *,
        function: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function: A user-defined name of the Cloud Function. The function name is case-sensitive and must be 1-63 characters long. Example value: "func1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#function GoogleComputeRegionNetworkEndpointGroup#function}
        :param url_mask: A template to parse function field from a request URL. URL mask allows for routing to multiple Cloud Functions without having to create multiple Network Endpoint Groups and backend services. For example, request URLs "mydomain.com/function1" and "mydomain.com/function2" can be backed by the same Serverless NEG with URL mask "/". The URL mask will parse them to { function = "function1" } and { function = "function2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6e9da7805a3c90fb4a2071c51bff6c2af3e642bbeb3584e1518e7a82423ab2)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument url_mask", value=url_mask, expected_type=type_hints["url_mask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if function is not None:
            self._values["function"] = function
        if url_mask is not None:
            self._values["url_mask"] = url_mask

    @builtins.property
    def function(self) -> typing.Optional[builtins.str]:
        '''A user-defined name of the Cloud Function. The function name is case-sensitive and must be 1-63 characters long. Example value: "func1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#function GoogleComputeRegionNetworkEndpointGroup#function}
        '''
        result = self._values.get("function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_mask(self) -> typing.Optional[builtins.str]:
        '''A template to parse function field from a request URL.

        URL mask allows
        for routing to multiple Cloud Functions without having to create
        multiple Network Endpoint Groups and backend services.

        For example, request URLs "mydomain.com/function1" and "mydomain.com/function2"
        can be backed by the same Serverless NEG with URL mask "/". The URL mask
        will parse them to { function = "function1" } and { function = "function2" } respectively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupCloudFunction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionNetworkEndpointGroupCloudFunctionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupCloudFunctionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c154f043322b2df2ea33717b84877051976ee984b854dcc79f6aeb8ac9bb4001)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFunction")
    def reset_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunction", []))

    @jsii.member(jsii_name="resetUrlMask")
    def reset_url_mask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlMask", []))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlMaskInput")
    def url_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b23ec357c2b8c93c82bd45522f95b712fefc210f775af26d32eabacfed003b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee4d540a0403b1ca22c4ff43d2668e66227632ac438c3da6b65c4b2c3a758fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudFunction]:
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudFunction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudFunction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe47174bf24ce99132920d38ba893b81e052c4aa3dae6b132cd937bbcdf25026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupCloudRun",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "tag": "tag", "url_mask": "urlMask"},
)
class GoogleComputeRegionNetworkEndpointGroupCloudRun:
    def __init__(
        self,
        *,
        service: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Cloud Run service is the main resource of Cloud Run. The service must be 1-63 characters long, and comply with RFC1035. Example value: "run-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#service GoogleComputeRegionNetworkEndpointGroup#service}
        :param tag: Cloud Run tag represents the "named-revision" to provide additional fine-grained traffic routing information. The tag must be 1-63 characters long, and comply with RFC1035. Example value: "revision-0010". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#tag GoogleComputeRegionNetworkEndpointGroup#tag}
        :param url_mask: A template to parse service and tag fields from a request URL. URL mask allows for routing to multiple Run services without having to create multiple network endpoint groups and backend services. For example, request URLs "foo1.domain.com/bar1" and "foo1.domain.com/bar2" an be backed by the same Serverless Network Endpoint Group (NEG) with URL mask ".domain.com/". The URL mask will parse them to { service="bar1", tag="foo1" } and { service="bar2", tag="foo2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1dc30b9467ca40a4f58f4e0a42821a24d06b1e41da6c4a971599db2849ee54)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument url_mask", value=url_mask, expected_type=type_hints["url_mask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service is not None:
            self._values["service"] = service
        if tag is not None:
            self._values["tag"] = tag
        if url_mask is not None:
            self._values["url_mask"] = url_mask

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Cloud Run service is the main resource of Cloud Run.

        The service must be 1-63 characters long, and comply with RFC1035.
        Example value: "run-service".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#service GoogleComputeRegionNetworkEndpointGroup#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Cloud Run tag represents the "named-revision" to provide additional fine-grained traffic routing information.

        The tag must be 1-63 characters long, and comply with RFC1035.
        Example value: "revision-0010".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#tag GoogleComputeRegionNetworkEndpointGroup#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_mask(self) -> typing.Optional[builtins.str]:
        '''A template to parse service and tag fields from a request URL.

        URL mask allows for routing to multiple Run services without having
        to create multiple network endpoint groups and backend services.

        For example, request URLs "foo1.domain.com/bar1" and "foo1.domain.com/bar2"
        an be backed by the same Serverless Network Endpoint Group (NEG) with
        URL mask ".domain.com/". The URL mask will parse them to { service="bar1", tag="foo1" }
        and { service="bar2", tag="foo2" } respectively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupCloudRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionNetworkEndpointGroupCloudRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupCloudRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c0c00c9e53141c648be38654d9f626692528978dcdd7ba6d9ad81fdec2e06a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetUrlMask")
    def reset_url_mask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlMask", []))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="urlMaskInput")
    def url_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de13e49e6088e0ed666d36e0c35cefd295411f51d41a48bee615f1be092a837f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3c522b74827ade3e17c7d83f8f3d827b7cfab51bf94547f251ff86021f77a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873eccc307634c69f4b013a73285dd08ac097d3a544929b1e7dd39a3ae7dbd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudRun]:
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc167d9457ab1adaf727e75c45a55a54cdc1a5d59c73a5179a3d89aa3da143b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupConfig",
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
        "region": "region",
        "app_engine": "appEngine",
        "cloud_function": "cloudFunction",
        "cloud_run": "cloudRun",
        "description": "description",
        "id": "id",
        "network": "network",
        "network_endpoint_type": "networkEndpointType",
        "project": "project",
        "psc_data": "pscData",
        "psc_target_service": "pscTargetService",
        "serverless_deployment": "serverlessDeployment",
        "subnetwork": "subnetwork",
        "timeouts": "timeouts",
    },
)
class GoogleComputeRegionNetworkEndpointGroupConfig(
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
        name: builtins.str,
        region: builtins.str,
        app_engine: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_function: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_run: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_endpoint_type: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        psc_data: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupPscData", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_target_service: typing.Optional[builtins.str] = None,
        serverless_deployment: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupServerlessDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionNetworkEndpointGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#name GoogleComputeRegionNetworkEndpointGroup#name}
        :param region: A reference to the region where the regional NEGs reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#region GoogleComputeRegionNetworkEndpointGroup#region}
        :param app_engine: app_engine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#app_engine GoogleComputeRegionNetworkEndpointGroup#app_engine}
        :param cloud_function: cloud_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#cloud_function GoogleComputeRegionNetworkEndpointGroup#cloud_function}
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#cloud_run GoogleComputeRegionNetworkEndpointGroup#cloud_run}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#description GoogleComputeRegionNetworkEndpointGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#id GoogleComputeRegionNetworkEndpointGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network: This field is only used for PSC and INTERNET NEGs. The URL of the network to which all network endpoints in the NEG belong. Uses "default" project network if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#network GoogleComputeRegionNetworkEndpointGroup#network}
        :param network_endpoint_type: Type of network endpoints in this network endpoint group. Defaults to SERVERLESS. Default value: "SERVERLESS" Possible values: ["SERVERLESS", "PRIVATE_SERVICE_CONNECT", "INTERNET_IP_PORT", "INTERNET_FQDN_PORT", "GCE_VM_IP_PORTMAP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#network_endpoint_type GoogleComputeRegionNetworkEndpointGroup#network_endpoint_type}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#project GoogleComputeRegionNetworkEndpointGroup#project}.
        :param psc_data: psc_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#psc_data GoogleComputeRegionNetworkEndpointGroup#psc_data}
        :param psc_target_service: This field is only used for PSC and INTERNET NEGs. The target service url used to set up private service connection to a Google API or a PSC Producer Service Attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#psc_target_service GoogleComputeRegionNetworkEndpointGroup#psc_target_service}
        :param serverless_deployment: serverless_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#serverless_deployment GoogleComputeRegionNetworkEndpointGroup#serverless_deployment}
        :param subnetwork: This field is only used for PSC NEGs. Optional URL of the subnetwork to which all network endpoints in the NEG belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#subnetwork GoogleComputeRegionNetworkEndpointGroup#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#timeouts GoogleComputeRegionNetworkEndpointGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_engine, dict):
            app_engine = GoogleComputeRegionNetworkEndpointGroupAppEngine(**app_engine)
        if isinstance(cloud_function, dict):
            cloud_function = GoogleComputeRegionNetworkEndpointGroupCloudFunction(**cloud_function)
        if isinstance(cloud_run, dict):
            cloud_run = GoogleComputeRegionNetworkEndpointGroupCloudRun(**cloud_run)
        if isinstance(psc_data, dict):
            psc_data = GoogleComputeRegionNetworkEndpointGroupPscData(**psc_data)
        if isinstance(serverless_deployment, dict):
            serverless_deployment = GoogleComputeRegionNetworkEndpointGroupServerlessDeployment(**serverless_deployment)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRegionNetworkEndpointGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79f309fb3b98cc61490624a804f9d0b4ca76b9f80591810cbf3b4009da351e2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument app_engine", value=app_engine, expected_type=type_hints["app_engine"])
            check_type(argname="argument cloud_function", value=cloud_function, expected_type=type_hints["cloud_function"])
            check_type(argname="argument cloud_run", value=cloud_run, expected_type=type_hints["cloud_run"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_endpoint_type", value=network_endpoint_type, expected_type=type_hints["network_endpoint_type"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument psc_data", value=psc_data, expected_type=type_hints["psc_data"])
            check_type(argname="argument psc_target_service", value=psc_target_service, expected_type=type_hints["psc_target_service"])
            check_type(argname="argument serverless_deployment", value=serverless_deployment, expected_type=type_hints["serverless_deployment"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "region": region,
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
        if app_engine is not None:
            self._values["app_engine"] = app_engine
        if cloud_function is not None:
            self._values["cloud_function"] = cloud_function
        if cloud_run is not None:
            self._values["cloud_run"] = cloud_run
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if network is not None:
            self._values["network"] = network
        if network_endpoint_type is not None:
            self._values["network_endpoint_type"] = network_endpoint_type
        if project is not None:
            self._values["project"] = project
        if psc_data is not None:
            self._values["psc_data"] = psc_data
        if psc_target_service is not None:
            self._values["psc_target_service"] = psc_target_service
        if serverless_deployment is not None:
            self._values["serverless_deployment"] = serverless_deployment
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
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
        '''Name of the resource;

        provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#name GoogleComputeRegionNetworkEndpointGroup#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''A reference to the region where the regional NEGs reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#region GoogleComputeRegionNetworkEndpointGroup#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupAppEngine]:
        '''app_engine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#app_engine GoogleComputeRegionNetworkEndpointGroup#app_engine}
        '''
        result = self._values.get("app_engine")
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupAppEngine], result)

    @builtins.property
    def cloud_function(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudFunction]:
        '''cloud_function block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#cloud_function GoogleComputeRegionNetworkEndpointGroup#cloud_function}
        '''
        result = self._values.get("cloud_function")
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudFunction], result)

    @builtins.property
    def cloud_run(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudRun]:
        '''cloud_run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#cloud_run GoogleComputeRegionNetworkEndpointGroup#cloud_run}
        '''
        result = self._values.get("cloud_run")
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudRun], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#description GoogleComputeRegionNetworkEndpointGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#id GoogleComputeRegionNetworkEndpointGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''This field is only used for PSC and INTERNET NEGs.

        The URL of the network to which all network endpoints in the NEG belong. Uses
        "default" project network if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#network GoogleComputeRegionNetworkEndpointGroup#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Type of network endpoints in this network endpoint group.

        Defaults to SERVERLESS. Default value: "SERVERLESS" Possible values: ["SERVERLESS", "PRIVATE_SERVICE_CONNECT", "INTERNET_IP_PORT", "INTERNET_FQDN_PORT", "GCE_VM_IP_PORTMAP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#network_endpoint_type GoogleComputeRegionNetworkEndpointGroup#network_endpoint_type}
        '''
        result = self._values.get("network_endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#project GoogleComputeRegionNetworkEndpointGroup#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_data(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupPscData"]:
        '''psc_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#psc_data GoogleComputeRegionNetworkEndpointGroup#psc_data}
        '''
        result = self._values.get("psc_data")
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupPscData"], result)

    @builtins.property
    def psc_target_service(self) -> typing.Optional[builtins.str]:
        '''This field is only used for PSC and INTERNET NEGs.

        The target service url used to set up private service connection to
        a Google API or a PSC Producer Service Attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#psc_target_service GoogleComputeRegionNetworkEndpointGroup#psc_target_service}
        '''
        result = self._values.get("psc_target_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverless_deployment(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupServerlessDeployment"]:
        '''serverless_deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#serverless_deployment GoogleComputeRegionNetworkEndpointGroup#serverless_deployment}
        '''
        result = self._values.get("serverless_deployment")
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupServerlessDeployment"], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''This field is only used for PSC NEGs.

        Optional URL of the subnetwork to which all network endpoints in the NEG belong.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#subnetwork GoogleComputeRegionNetworkEndpointGroup#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleComputeRegionNetworkEndpointGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#timeouts GoogleComputeRegionNetworkEndpointGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRegionNetworkEndpointGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupPscData",
    jsii_struct_bases=[],
    name_mapping={"producer_port": "producerPort"},
)
class GoogleComputeRegionNetworkEndpointGroupPscData:
    def __init__(self, *, producer_port: typing.Optional[builtins.str] = None) -> None:
        '''
        :param producer_port: The PSC producer port to use when consumer PSC NEG connects to a producer. If this flag isn't specified for a PSC NEG with endpoint type private-service-connect, then PSC NEG will be connected to a first port in the available PSC producer port range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#producer_port GoogleComputeRegionNetworkEndpointGroup#producer_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fece371bd86394b60fd898ab882bd7ccc16fab949c4765f6287540d14d5c976)
            check_type(argname="argument producer_port", value=producer_port, expected_type=type_hints["producer_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if producer_port is not None:
            self._values["producer_port"] = producer_port

    @builtins.property
    def producer_port(self) -> typing.Optional[builtins.str]:
        '''The PSC producer port to use when consumer PSC NEG connects to a producer.

        If
        this flag isn't specified for a PSC NEG with endpoint type
        private-service-connect, then PSC NEG will be connected to a first port in the
        available PSC producer port range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#producer_port GoogleComputeRegionNetworkEndpointGroup#producer_port}
        '''
        result = self._values.get("producer_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupPscData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionNetworkEndpointGroupPscDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupPscDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30465b695765d0c9a7dbbd5b48579c9746ec9e66bdda33d7a92c6cd11c895900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProducerPort")
    def reset_producer_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProducerPort", []))

    @builtins.property
    @jsii.member(jsii_name="producerPortInput")
    def producer_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "producerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="producerPort")
    def producer_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "producerPort"))

    @producer_port.setter
    def producer_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8d137dde75df1840e1de9144cee201fe47a4ba9bba0d274930f667da212615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "producerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupPscData]:
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupPscData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupPscData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c31d184da599301715aa71525666e680fdbcd28a3b91ff13c1e9406d54c0b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupServerlessDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "platform": "platform",
        "resource": "resource",
        "url_mask": "urlMask",
        "version": "version",
    },
)
class GoogleComputeRegionNetworkEndpointGroupServerlessDeployment:
    def __init__(
        self,
        *,
        platform: builtins.str,
        resource: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param platform: The platform of the NEG backend target(s). Possible values: API Gateway: apigateway.googleapis.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#platform GoogleComputeRegionNetworkEndpointGroup#platform}
        :param resource: The user-defined name of the workload/instance. This value must be provided explicitly or in the urlMask. The resource identified by this value is platform-specific and is as follows: API Gateway: The gateway ID, App Engine: The service name, Cloud Functions: The function name, Cloud Run: The service name Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#resource GoogleComputeRegionNetworkEndpointGroup#resource}
        :param url_mask: A template to parse platform-specific fields from a request URL. URL mask allows for routing to multiple resources on the same serverless platform without having to create multiple Network Endpoint Groups and backend resources. The fields parsed by this template are platform-specific and are as follows: API Gateway: The gateway ID, App Engine: The service and version, Cloud Functions: The function name, Cloud Run: The service and tag Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        :param version: The optional resource version. The version identified by this value is platform-specific and is follows: API Gateway: Unused, App Engine: The service version, Cloud Functions: Unused, Cloud Run: The service tag Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#version GoogleComputeRegionNetworkEndpointGroup#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18cc1d943aaf40b6471c81857ae2a92b1bd5235a2080b640e9c20db26aac05a)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument url_mask", value=url_mask, expected_type=type_hints["url_mask"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform": platform,
        }
        if resource is not None:
            self._values["resource"] = resource
        if url_mask is not None:
            self._values["url_mask"] = url_mask
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def platform(self) -> builtins.str:
        '''The platform of the NEG backend target(s). Possible values: API Gateway: apigateway.googleapis.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#platform GoogleComputeRegionNetworkEndpointGroup#platform}
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''The user-defined name of the workload/instance.

        This value must be provided explicitly or in the urlMask.
        The resource identified by this value is platform-specific and is as follows: API Gateway: The gateway ID, App Engine: The service name,
        Cloud Functions: The function name, Cloud Run: The service name

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#resource GoogleComputeRegionNetworkEndpointGroup#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_mask(self) -> typing.Optional[builtins.str]:
        '''A template to parse platform-specific fields from a request URL.

        URL mask allows for routing to multiple resources
        on the same serverless platform without having to create multiple Network Endpoint Groups and backend resources.
        The fields parsed by this template are platform-specific and are as follows: API Gateway: The gateway ID,
        App Engine: The service and version, Cloud Functions: The function name, Cloud Run: The service and tag

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#url_mask GoogleComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The optional resource version.

        The version identified by this value is platform-specific and is follows:
        API Gateway: Unused, App Engine: The service version, Cloud Functions: Unused, Cloud Run: The service tag

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#version GoogleComputeRegionNetworkEndpointGroup#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupServerlessDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionNetworkEndpointGroupServerlessDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupServerlessDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae2998aef2b3ce1a99f4dc361ef594ca364477173d11711a60ed4bcf9567e45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @jsii.member(jsii_name="resetUrlMask")
    def reset_url_mask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlMask", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="urlMaskInput")
    def url_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd00e547ae0cfb4f499aa0cc9c924417b250fa526117b7c0cf68c5024954dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d50470f2079b1c0ffebd3a22eb6656614fbe6b79e4e3e9068b4dc60511749d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf10aa014003b31acb0005da863964aa9350a2905b2e3b86fc0c0798452e034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1061ee2baeb1a6be67ffe9b8f67a7fa3db5ee037ad581d0717cce96729c7f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionNetworkEndpointGroupServerlessDeployment]:
        return typing.cast(typing.Optional[GoogleComputeRegionNetworkEndpointGroupServerlessDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupServerlessDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe71b715f1e68b8e6ee18135b53e6824c4ca510fc6ac783c64f1dc985ee550d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleComputeRegionNetworkEndpointGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#create GoogleComputeRegionNetworkEndpointGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#delete GoogleComputeRegionNetworkEndpointGroup#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896738c888c05f32236ca8c958dc7fdc4feccb4c755c03e6925100c2124585d1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#create GoogleComputeRegionNetworkEndpointGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_network_endpoint_group#delete GoogleComputeRegionNetworkEndpointGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionNetworkEndpointGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionNetworkEndpointGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionNetworkEndpointGroup.GoogleComputeRegionNetworkEndpointGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e65b5e453e5977da8a36a996af51e27507c8f60b208e5624c310ab89f43ad50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34ed537ddae828103004bff10f2a66802474ca77ece4d3517b91e6034b70ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1379e48b9ba91dfebe88037433532ce661d6ad8f6504cd17631368af905152b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionNetworkEndpointGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionNetworkEndpointGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionNetworkEndpointGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45f1200e5f50d9cfed4b1bc2bcfcac8083bff8158caab054887377d6b39cce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeRegionNetworkEndpointGroup",
    "GoogleComputeRegionNetworkEndpointGroupAppEngine",
    "GoogleComputeRegionNetworkEndpointGroupAppEngineOutputReference",
    "GoogleComputeRegionNetworkEndpointGroupCloudFunction",
    "GoogleComputeRegionNetworkEndpointGroupCloudFunctionOutputReference",
    "GoogleComputeRegionNetworkEndpointGroupCloudRun",
    "GoogleComputeRegionNetworkEndpointGroupCloudRunOutputReference",
    "GoogleComputeRegionNetworkEndpointGroupConfig",
    "GoogleComputeRegionNetworkEndpointGroupPscData",
    "GoogleComputeRegionNetworkEndpointGroupPscDataOutputReference",
    "GoogleComputeRegionNetworkEndpointGroupServerlessDeployment",
    "GoogleComputeRegionNetworkEndpointGroupServerlessDeploymentOutputReference",
    "GoogleComputeRegionNetworkEndpointGroupTimeouts",
    "GoogleComputeRegionNetworkEndpointGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2b2aeaea7a4fbd3697f4d3cddfaaae113f436e2e798b38f6b54c51885c4264ce(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    region: builtins.str,
    app_engine: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_function: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_run: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_endpoint_type: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    psc_data: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupPscData, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_target_service: typing.Optional[builtins.str] = None,
    serverless_deployment: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupServerlessDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f74d7e96aaf39d8f422b55802e054a8dea10de8c4c036e84b63708af171a3776(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1241ba789a6f482f46233d2694a3124e4dc12c1e43b9cff5a1aed70321bd0187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66230cf94cad80a52c6d76cfd6b045a32c72c34bc0c2d9a52e1b503ab7fb0463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1172566b8f6c22d16bedbc989e610400f868b17f03d526c237c1b1508b44f781(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4663ef77d544a37f11318a7e75bd5df01ef5c9d54bacc0dfc62b41b76fdebb35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850ae39a816f421ef7a0c88e2555932af27852f4d36fc7bff2e80025106d7505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f56e660faf921c296d3a46ea9b2a0844b7b43225a08eb339e3ad17872450fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2818ad4470ef434a9aa093933d5938ec34d5ae87643ab24dd46fc76f2b0289b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8aaf4aa9e0329bb03190ff9b4ec67f19cc8c240580acb2c5e370281c377cad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8b0f7d0b6de4ea39b124211aac3b27f3bdeac605fa0fc3ec87ea9c65c54ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e7571c87b084b4e1931b70f0750945f6aa57b94414bf88b206cfb426e37ede(
    *,
    service: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db13ff2e39cd9009d9f3d6d8522c7ada865f7f6db5f48622eec719cad598866b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad1ec0d13fce4418fe5c5ee1d5614fe58ffb724ca9553b3c27da2a1a9728b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f820a655cbd876c89ecbb44eeb01da39829e010d9e090fda17200c61041844a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c776292f01fcc2b848d1883d4f3a747a94469f539739336ac7a2afe5fb67a68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676a110fc389f0c0a258779a4bc124ba367b310844a27a03a00820c15e798da7(
    value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupAppEngine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6e9da7805a3c90fb4a2071c51bff6c2af3e642bbeb3584e1518e7a82423ab2(
    *,
    function: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c154f043322b2df2ea33717b84877051976ee984b854dcc79f6aeb8ac9bb4001(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b23ec357c2b8c93c82bd45522f95b712fefc210f775af26d32eabacfed003b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee4d540a0403b1ca22c4ff43d2668e66227632ac438c3da6b65c4b2c3a758fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe47174bf24ce99132920d38ba893b81e052c4aa3dae6b132cd937bbcdf25026(
    value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudFunction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1dc30b9467ca40a4f58f4e0a42821a24d06b1e41da6c4a971599db2849ee54(
    *,
    service: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0c00c9e53141c648be38654d9f626692528978dcdd7ba6d9ad81fdec2e06a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de13e49e6088e0ed666d36e0c35cefd295411f51d41a48bee615f1be092a837f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3c522b74827ade3e17c7d83f8f3d827b7cfab51bf94547f251ff86021f77a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873eccc307634c69f4b013a73285dd08ac097d3a544929b1e7dd39a3ae7dbd90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc167d9457ab1adaf727e75c45a55a54cdc1a5d59c73a5179a3d89aa3da143b(
    value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupCloudRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79f309fb3b98cc61490624a804f9d0b4ca76b9f80591810cbf3b4009da351e2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    region: builtins.str,
    app_engine: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_function: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_run: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_endpoint_type: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    psc_data: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupPscData, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_target_service: typing.Optional[builtins.str] = None,
    serverless_deployment: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupServerlessDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionNetworkEndpointGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fece371bd86394b60fd898ab882bd7ccc16fab949c4765f6287540d14d5c976(
    *,
    producer_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30465b695765d0c9a7dbbd5b48579c9746ec9e66bdda33d7a92c6cd11c895900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8d137dde75df1840e1de9144cee201fe47a4ba9bba0d274930f667da212615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c31d184da599301715aa71525666e680fdbcd28a3b91ff13c1e9406d54c0b90(
    value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupPscData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18cc1d943aaf40b6471c81857ae2a92b1bd5235a2080b640e9c20db26aac05a(
    *,
    platform: builtins.str,
    resource: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae2998aef2b3ce1a99f4dc361ef594ca364477173d11711a60ed4bcf9567e45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd00e547ae0cfb4f499aa0cc9c924417b250fa526117b7c0cf68c5024954dff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d50470f2079b1c0ffebd3a22eb6656614fbe6b79e4e3e9068b4dc60511749d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf10aa014003b31acb0005da863964aa9350a2905b2e3b86fc0c0798452e034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1061ee2baeb1a6be67ffe9b8f67a7fa3db5ee037ad581d0717cce96729c7f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe71b715f1e68b8e6ee18135b53e6824c4ca510fc6ac783c64f1dc985ee550d4(
    value: typing.Optional[GoogleComputeRegionNetworkEndpointGroupServerlessDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896738c888c05f32236ca8c958dc7fdc4feccb4c755c03e6925100c2124585d1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e65b5e453e5977da8a36a996af51e27507c8f60b208e5624c310ab89f43ad50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34ed537ddae828103004bff10f2a66802474ca77ece4d3517b91e6034b70ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1379e48b9ba91dfebe88037433532ce661d6ad8f6504cd17631368af905152b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45f1200e5f50d9cfed4b1bc2bcfcac8083bff8158caab054887377d6b39cce0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionNetworkEndpointGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
