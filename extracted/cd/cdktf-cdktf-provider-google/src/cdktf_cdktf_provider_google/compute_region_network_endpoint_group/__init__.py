r'''
# `google_compute_region_network_endpoint_group`

Refer to the Terraform Registry for docs: [`google_compute_region_network_endpoint_group`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group).
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


class ComputeRegionNetworkEndpointGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group google_compute_region_network_endpoint_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        region: builtins.str,
        app_engine: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupAppEngine", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_function: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupCloudFunction", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_run: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupCloudRun", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_endpoint_type: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        psc_data: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupPscData", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_target_service: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group google_compute_region_network_endpoint_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#name ComputeRegionNetworkEndpointGroup#name}
        :param region: A reference to the region where the regional NEGs reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#region ComputeRegionNetworkEndpointGroup#region}
        :param app_engine: app_engine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#app_engine ComputeRegionNetworkEndpointGroup#app_engine}
        :param cloud_function: cloud_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#cloud_function ComputeRegionNetworkEndpointGroup#cloud_function}
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#cloud_run ComputeRegionNetworkEndpointGroup#cloud_run}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#description ComputeRegionNetworkEndpointGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#id ComputeRegionNetworkEndpointGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network: This field is only used for PSC and INTERNET NEGs. The URL of the network to which all network endpoints in the NEG belong. Uses "default" project network if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#network ComputeRegionNetworkEndpointGroup#network}
        :param network_endpoint_type: Type of network endpoints in this network endpoint group. Defaults to SERVERLESS. Default value: "SERVERLESS" Possible values: ["SERVERLESS", "PRIVATE_SERVICE_CONNECT", "INTERNET_IP_PORT", "INTERNET_FQDN_PORT", "GCE_VM_IP_PORTMAP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#network_endpoint_type ComputeRegionNetworkEndpointGroup#network_endpoint_type}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#project ComputeRegionNetworkEndpointGroup#project}.
        :param psc_data: psc_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#psc_data ComputeRegionNetworkEndpointGroup#psc_data}
        :param psc_target_service: This field is only used for PSC and INTERNET NEGs. The target service url used to set up private service connection to a Google API or a PSC Producer Service Attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#psc_target_service ComputeRegionNetworkEndpointGroup#psc_target_service}
        :param subnetwork: This field is only used for PSC NEGs. Optional URL of the subnetwork to which all network endpoints in the NEG belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#subnetwork ComputeRegionNetworkEndpointGroup#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#timeouts ComputeRegionNetworkEndpointGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89edb568d6897cc2b0188dec60081e7fb4cad1e7c13e4521e5d2b7a04aa043eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionNetworkEndpointGroupConfig(
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
        '''Generates CDKTF code for importing a ComputeRegionNetworkEndpointGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionNetworkEndpointGroup to import.
        :param import_from_id: The id of the existing ComputeRegionNetworkEndpointGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionNetworkEndpointGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31dfd93580dea4e1db924defa8f477893a410e9fa91d7aacbbf35e6b62ea70d)
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
        :param service: Optional serving service. The service name must be 1-63 characters long, and comply with RFC1035. Example value: "default", "my-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#service ComputeRegionNetworkEndpointGroup#service}
        :param url_mask: A template to parse service and version fields from a request URL. URL mask allows for routing to multiple App Engine services without having to create multiple Network Endpoint Groups and backend services. For example, the request URLs "foo1-dot-appname.appspot.com/v1" and "foo1-dot-appname.appspot.com/v2" can be backed by the same Serverless NEG with URL mask "-dot-appname.appspot.com/". The URL mask will parse them to { service = "foo1", version = "v1" } and { service = "foo1", version = "v2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        :param version: Optional serving version. The version must be 1-63 characters long, and comply with RFC1035. Example value: "v1", "v2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#version ComputeRegionNetworkEndpointGroup#version}
        '''
        value = ComputeRegionNetworkEndpointGroupAppEngine(
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
        :param function: A user-defined name of the Cloud Function. The function name is case-sensitive and must be 1-63 characters long. Example value: "func1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#function ComputeRegionNetworkEndpointGroup#function}
        :param url_mask: A template to parse function field from a request URL. URL mask allows for routing to multiple Cloud Functions without having to create multiple Network Endpoint Groups and backend services. For example, request URLs "mydomain.com/function1" and "mydomain.com/function2" can be backed by the same Serverless NEG with URL mask "/". The URL mask will parse them to { function = "function1" } and { function = "function2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        value = ComputeRegionNetworkEndpointGroupCloudFunction(
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
        :param service: Cloud Run service is the main resource of Cloud Run. The service must be 1-63 characters long, and comply with RFC1035. Example value: "run-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#service ComputeRegionNetworkEndpointGroup#service}
        :param tag: Cloud Run tag represents the "named-revision" to provide additional fine-grained traffic routing information. The tag must be 1-63 characters long, and comply with RFC1035. Example value: "revision-0010". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#tag ComputeRegionNetworkEndpointGroup#tag}
        :param url_mask: A template to parse service and tag fields from a request URL. URL mask allows for routing to multiple Run services without having to create multiple network endpoint groups and backend services. For example, request URLs "foo1.domain.com/bar1" and "foo1.domain.com/bar2" an be backed by the same Serverless Network Endpoint Group (NEG) with URL mask ".domain.com/". The URL mask will parse them to { service="bar1", tag="foo1" } and { service="bar2", tag="foo2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        value = ComputeRegionNetworkEndpointGroupCloudRun(
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
        :param producer_port: The PSC producer port to use when consumer PSC NEG connects to a producer. If this flag isn't specified for a PSC NEG with endpoint type private-service-connect, then PSC NEG will be connected to a first port in the available PSC producer port range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#producer_port ComputeRegionNetworkEndpointGroup#producer_port}
        '''
        value = ComputeRegionNetworkEndpointGroupPscData(producer_port=producer_port)

        return typing.cast(None, jsii.invoke(self, "putPscData", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#create ComputeRegionNetworkEndpointGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#delete ComputeRegionNetworkEndpointGroup#delete}.
        '''
        value = ComputeRegionNetworkEndpointGroupTimeouts(create=create, delete=delete)

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
    def app_engine(self) -> "ComputeRegionNetworkEndpointGroupAppEngineOutputReference":
        return typing.cast("ComputeRegionNetworkEndpointGroupAppEngineOutputReference", jsii.get(self, "appEngine"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunction")
    def cloud_function(
        self,
    ) -> "ComputeRegionNetworkEndpointGroupCloudFunctionOutputReference":
        return typing.cast("ComputeRegionNetworkEndpointGroupCloudFunctionOutputReference", jsii.get(self, "cloudFunction"))

    @builtins.property
    @jsii.member(jsii_name="cloudRun")
    def cloud_run(self) -> "ComputeRegionNetworkEndpointGroupCloudRunOutputReference":
        return typing.cast("ComputeRegionNetworkEndpointGroupCloudRunOutputReference", jsii.get(self, "cloudRun"))

    @builtins.property
    @jsii.member(jsii_name="pscData")
    def psc_data(self) -> "ComputeRegionNetworkEndpointGroupPscDataOutputReference":
        return typing.cast("ComputeRegionNetworkEndpointGroupPscDataOutputReference", jsii.get(self, "pscData"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionNetworkEndpointGroupTimeoutsOutputReference":
        return typing.cast("ComputeRegionNetworkEndpointGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appEngineInput")
    def app_engine_input(
        self,
    ) -> typing.Optional["ComputeRegionNetworkEndpointGroupAppEngine"]:
        return typing.cast(typing.Optional["ComputeRegionNetworkEndpointGroupAppEngine"], jsii.get(self, "appEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionInput")
    def cloud_function_input(
        self,
    ) -> typing.Optional["ComputeRegionNetworkEndpointGroupCloudFunction"]:
        return typing.cast(typing.Optional["ComputeRegionNetworkEndpointGroupCloudFunction"], jsii.get(self, "cloudFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunInput")
    def cloud_run_input(
        self,
    ) -> typing.Optional["ComputeRegionNetworkEndpointGroupCloudRun"]:
        return typing.cast(typing.Optional["ComputeRegionNetworkEndpointGroupCloudRun"], jsii.get(self, "cloudRunInput"))

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
    ) -> typing.Optional["ComputeRegionNetworkEndpointGroupPscData"]:
        return typing.cast(typing.Optional["ComputeRegionNetworkEndpointGroupPscData"], jsii.get(self, "pscDataInput"))

    @builtins.property
    @jsii.member(jsii_name="pscTargetServiceInput")
    def psc_target_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pscTargetServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionNetworkEndpointGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionNetworkEndpointGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3593c7c19283008e547da4b4737549b2bf4dc81c4cdfc1390e34fb065bbf4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85deb4f758f1873cbbb3340eed9658525f6e52620d80790500a25741ee479188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13490bc9760b1124df59ca6b70cdbdc40cb4dd887c4a136e7f56e62a62f6803a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1580c2e2c732f2a3a0382b64c0bddb78cc48ecba7084700379f054d65574b6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkEndpointType")
    def network_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkEndpointType"))

    @network_endpoint_type.setter
    def network_endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf34afe784b44fcf9e170e5cf85e06b0af528fbbed86b73a79ae7210fb612f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkEndpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41220fadb86ade1bf09a4fbc2652460d73be06c03081889a7ce95358c40e099b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pscTargetService")
    def psc_target_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscTargetService"))

    @psc_target_service.setter
    def psc_target_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a53151efb936a0fae0548239d624e85e00a36b796a8307cbf615a58e90b805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscTargetService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adad0f3f90598e442b94e73654cb63dfd1b448b206a508faa690322c4af345b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68a76da5bc92bae4e0face68117cdc270b37e1082c000473f32a9b7f01b21df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupAppEngine",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "url_mask": "urlMask", "version": "version"},
)
class ComputeRegionNetworkEndpointGroupAppEngine:
    def __init__(
        self,
        *,
        service: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Optional serving service. The service name must be 1-63 characters long, and comply with RFC1035. Example value: "default", "my-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#service ComputeRegionNetworkEndpointGroup#service}
        :param url_mask: A template to parse service and version fields from a request URL. URL mask allows for routing to multiple App Engine services without having to create multiple Network Endpoint Groups and backend services. For example, the request URLs "foo1-dot-appname.appspot.com/v1" and "foo1-dot-appname.appspot.com/v2" can be backed by the same Serverless NEG with URL mask "-dot-appname.appspot.com/". The URL mask will parse them to { service = "foo1", version = "v1" } and { service = "foo1", version = "v2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        :param version: Optional serving version. The version must be 1-63 characters long, and comply with RFC1035. Example value: "v1", "v2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#version ComputeRegionNetworkEndpointGroup#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2824648fe93fcd363482272620f1db44d03f42f5f499ec22bcf0aa789a4b728b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#service ComputeRegionNetworkEndpointGroup#service}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional serving version. The version must be 1-63 characters long, and comply with RFC1035. Example value: "v1", "v2".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#version ComputeRegionNetworkEndpointGroup#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkEndpointGroupAppEngine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkEndpointGroupAppEngineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupAppEngineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1348f7b5f4895c8f1f2a2b05a7efbf586871c5d1950ff4778afa1e0bff7ab710)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed2c0a16ab6dd63a6aa6a7f3d55ce1201b12d2c940118f2bfaa35f6306f23a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8e877d66db7900f0639a2fc7bc4433e06c406ca7c205ea88acf02397f2a518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827fa609725d58b5990b97c783a333e3a461099e0cf8ed71a1ceed4980ca3113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkEndpointGroupAppEngine]:
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupAppEngine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkEndpointGroupAppEngine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03cad81b2d916b73f0545f505069b5e2170e8853bace59a81b033fd6e7aa8d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupCloudFunction",
    jsii_struct_bases=[],
    name_mapping={"function": "function", "url_mask": "urlMask"},
)
class ComputeRegionNetworkEndpointGroupCloudFunction:
    def __init__(
        self,
        *,
        function: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function: A user-defined name of the Cloud Function. The function name is case-sensitive and must be 1-63 characters long. Example value: "func1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#function ComputeRegionNetworkEndpointGroup#function}
        :param url_mask: A template to parse function field from a request URL. URL mask allows for routing to multiple Cloud Functions without having to create multiple Network Endpoint Groups and backend services. For example, request URLs "mydomain.com/function1" and "mydomain.com/function2" can be backed by the same Serverless NEG with URL mask "/". The URL mask will parse them to { function = "function1" } and { function = "function2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef96e1e5629b365e873f7f03780e19d947409c8de928b2e0ec0d94ead0a3b39)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#function ComputeRegionNetworkEndpointGroup#function}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkEndpointGroupCloudFunction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkEndpointGroupCloudFunctionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupCloudFunctionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98e1aa7e80bcaa03484ed6f8f10dc15d2a48f3d2ce7be5f64cd864524a471775)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1e3c9b08591ec00b271275abd50db0101315fdb90b83700472836772ec701f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3e51196fbca2ede3ae3ec2cb44cda3dd9d838da97397e9a4fb8e43a9f7d2df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkEndpointGroupCloudFunction]:
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupCloudFunction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkEndpointGroupCloudFunction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad392d622d90d6190288eaf2a238d04d70cdeab377c374e3585a94f241381a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupCloudRun",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "tag": "tag", "url_mask": "urlMask"},
)
class ComputeRegionNetworkEndpointGroupCloudRun:
    def __init__(
        self,
        *,
        service: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        url_mask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Cloud Run service is the main resource of Cloud Run. The service must be 1-63 characters long, and comply with RFC1035. Example value: "run-service". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#service ComputeRegionNetworkEndpointGroup#service}
        :param tag: Cloud Run tag represents the "named-revision" to provide additional fine-grained traffic routing information. The tag must be 1-63 characters long, and comply with RFC1035. Example value: "revision-0010". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#tag ComputeRegionNetworkEndpointGroup#tag}
        :param url_mask: A template to parse service and tag fields from a request URL. URL mask allows for routing to multiple Run services without having to create multiple network endpoint groups and backend services. For example, request URLs "foo1.domain.com/bar1" and "foo1.domain.com/bar2" an be backed by the same Serverless Network Endpoint Group (NEG) with URL mask ".domain.com/". The URL mask will parse them to { service="bar1", tag="foo1" } and { service="bar2", tag="foo2" } respectively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81098f86ecb43c63239af3a8dd84b8393322d217ab5418e9b9292527b83392b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#service ComputeRegionNetworkEndpointGroup#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Cloud Run tag represents the "named-revision" to provide additional fine-grained traffic routing information.

        The tag must be 1-63 characters long, and comply with RFC1035.
        Example value: "revision-0010".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#tag ComputeRegionNetworkEndpointGroup#tag}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#url_mask ComputeRegionNetworkEndpointGroup#url_mask}
        '''
        result = self._values.get("url_mask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkEndpointGroupCloudRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkEndpointGroupCloudRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupCloudRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a02366401c63996184dc43aba03902d402ee324cdc1c069f686ce3a20b079c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ca1030b915be244e267c04eee12d830224ec57cb1c9a3aa38a32bd66a15a7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16597702e9334199c68e2b18d074ea90ed6209ffddea95fae5b4737b27351da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMask")
    def url_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMask"))

    @url_mask.setter
    def url_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4502bcf648a75660f311414f4c476e6b7794a42a7ebc27d65b8a12b8e9ff61d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkEndpointGroupCloudRun]:
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupCloudRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkEndpointGroupCloudRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52abc4dd0be9075a584ccf92ecb2b12b7b454b796bfc132cef4126f503eb339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupConfig",
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
        "subnetwork": "subnetwork",
        "timeouts": "timeouts",
    },
)
class ComputeRegionNetworkEndpointGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_engine: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_function: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_run: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_endpoint_type: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        psc_data: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupPscData", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_target_service: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionNetworkEndpointGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#name ComputeRegionNetworkEndpointGroup#name}
        :param region: A reference to the region where the regional NEGs reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#region ComputeRegionNetworkEndpointGroup#region}
        :param app_engine: app_engine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#app_engine ComputeRegionNetworkEndpointGroup#app_engine}
        :param cloud_function: cloud_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#cloud_function ComputeRegionNetworkEndpointGroup#cloud_function}
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#cloud_run ComputeRegionNetworkEndpointGroup#cloud_run}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#description ComputeRegionNetworkEndpointGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#id ComputeRegionNetworkEndpointGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network: This field is only used for PSC and INTERNET NEGs. The URL of the network to which all network endpoints in the NEG belong. Uses "default" project network if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#network ComputeRegionNetworkEndpointGroup#network}
        :param network_endpoint_type: Type of network endpoints in this network endpoint group. Defaults to SERVERLESS. Default value: "SERVERLESS" Possible values: ["SERVERLESS", "PRIVATE_SERVICE_CONNECT", "INTERNET_IP_PORT", "INTERNET_FQDN_PORT", "GCE_VM_IP_PORTMAP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#network_endpoint_type ComputeRegionNetworkEndpointGroup#network_endpoint_type}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#project ComputeRegionNetworkEndpointGroup#project}.
        :param psc_data: psc_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#psc_data ComputeRegionNetworkEndpointGroup#psc_data}
        :param psc_target_service: This field is only used for PSC and INTERNET NEGs. The target service url used to set up private service connection to a Google API or a PSC Producer Service Attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#psc_target_service ComputeRegionNetworkEndpointGroup#psc_target_service}
        :param subnetwork: This field is only used for PSC NEGs. Optional URL of the subnetwork to which all network endpoints in the NEG belong. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#subnetwork ComputeRegionNetworkEndpointGroup#subnetwork}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#timeouts ComputeRegionNetworkEndpointGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_engine, dict):
            app_engine = ComputeRegionNetworkEndpointGroupAppEngine(**app_engine)
        if isinstance(cloud_function, dict):
            cloud_function = ComputeRegionNetworkEndpointGroupCloudFunction(**cloud_function)
        if isinstance(cloud_run, dict):
            cloud_run = ComputeRegionNetworkEndpointGroupCloudRun(**cloud_run)
        if isinstance(psc_data, dict):
            psc_data = ComputeRegionNetworkEndpointGroupPscData(**psc_data)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionNetworkEndpointGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedbe00ce373430d88e89d40b0808274ff8cf2d1300527c407c7a49ba12d93aa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#name ComputeRegionNetworkEndpointGroup#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''A reference to the region where the regional NEGs reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#region ComputeRegionNetworkEndpointGroup#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_engine(self) -> typing.Optional[ComputeRegionNetworkEndpointGroupAppEngine]:
        '''app_engine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#app_engine ComputeRegionNetworkEndpointGroup#app_engine}
        '''
        result = self._values.get("app_engine")
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupAppEngine], result)

    @builtins.property
    def cloud_function(
        self,
    ) -> typing.Optional[ComputeRegionNetworkEndpointGroupCloudFunction]:
        '''cloud_function block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#cloud_function ComputeRegionNetworkEndpointGroup#cloud_function}
        '''
        result = self._values.get("cloud_function")
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupCloudFunction], result)

    @builtins.property
    def cloud_run(self) -> typing.Optional[ComputeRegionNetworkEndpointGroupCloudRun]:
        '''cloud_run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#cloud_run ComputeRegionNetworkEndpointGroup#cloud_run}
        '''
        result = self._values.get("cloud_run")
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupCloudRun], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#description ComputeRegionNetworkEndpointGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#id ComputeRegionNetworkEndpointGroup#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#network ComputeRegionNetworkEndpointGroup#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Type of network endpoints in this network endpoint group.

        Defaults to SERVERLESS. Default value: "SERVERLESS" Possible values: ["SERVERLESS", "PRIVATE_SERVICE_CONNECT", "INTERNET_IP_PORT", "INTERNET_FQDN_PORT", "GCE_VM_IP_PORTMAP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#network_endpoint_type ComputeRegionNetworkEndpointGroup#network_endpoint_type}
        '''
        result = self._values.get("network_endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#project ComputeRegionNetworkEndpointGroup#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_data(self) -> typing.Optional["ComputeRegionNetworkEndpointGroupPscData"]:
        '''psc_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#psc_data ComputeRegionNetworkEndpointGroup#psc_data}
        '''
        result = self._values.get("psc_data")
        return typing.cast(typing.Optional["ComputeRegionNetworkEndpointGroupPscData"], result)

    @builtins.property
    def psc_target_service(self) -> typing.Optional[builtins.str]:
        '''This field is only used for PSC and INTERNET NEGs.

        The target service url used to set up private service connection to
        a Google API or a PSC Producer Service Attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#psc_target_service ComputeRegionNetworkEndpointGroup#psc_target_service}
        '''
        result = self._values.get("psc_target_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''This field is only used for PSC NEGs.

        Optional URL of the subnetwork to which all network endpoints in the NEG belong.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#subnetwork ComputeRegionNetworkEndpointGroup#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionNetworkEndpointGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#timeouts ComputeRegionNetworkEndpointGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionNetworkEndpointGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkEndpointGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupPscData",
    jsii_struct_bases=[],
    name_mapping={"producer_port": "producerPort"},
)
class ComputeRegionNetworkEndpointGroupPscData:
    def __init__(self, *, producer_port: typing.Optional[builtins.str] = None) -> None:
        '''
        :param producer_port: The PSC producer port to use when consumer PSC NEG connects to a producer. If this flag isn't specified for a PSC NEG with endpoint type private-service-connect, then PSC NEG will be connected to a first port in the available PSC producer port range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#producer_port ComputeRegionNetworkEndpointGroup#producer_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d85f57b0234595569753953ff9297da08f135b8e708729b55e7b6d12b0148c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#producer_port ComputeRegionNetworkEndpointGroup#producer_port}
        '''
        result = self._values.get("producer_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkEndpointGroupPscData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkEndpointGroupPscDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupPscDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fb8a61e2fa583e50ebdf4134f3674eb44513ecb849caf9fc9c1fe99a821610f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00751d30c4d9fa9f4c3be6dc621ac7fcef6c31b6c39e2f5d5268a8efe333df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "producerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionNetworkEndpointGroupPscData]:
        return typing.cast(typing.Optional[ComputeRegionNetworkEndpointGroupPscData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionNetworkEndpointGroupPscData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ff44b00557017051e0bc025e1b51b26907a1d4d9d78965df027aadd969e56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeRegionNetworkEndpointGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#create ComputeRegionNetworkEndpointGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#delete ComputeRegionNetworkEndpointGroup#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0859cf34f053a9a9f137cca6f1978066e5bf6874301438fbb5c710eb57c6490)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#create ComputeRegionNetworkEndpointGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_network_endpoint_group#delete ComputeRegionNetworkEndpointGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionNetworkEndpointGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionNetworkEndpointGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionNetworkEndpointGroup.ComputeRegionNetworkEndpointGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__670fe5d7236046b000dfc4d857d55c6c205c27dd20e80408aae118c328f8dc6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bac752ae9b2528f656017d4b7615348150e8d3e6e8e319043eac7fdcdc280aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3884d9df5936d89d38f35acb9b778c434213770b9a8c7257335ccd844d98f24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkEndpointGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkEndpointGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkEndpointGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f48149e790676ff631b9cce9b6fff4e9e36a610aedce120d9b65f7eecef861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionNetworkEndpointGroup",
    "ComputeRegionNetworkEndpointGroupAppEngine",
    "ComputeRegionNetworkEndpointGroupAppEngineOutputReference",
    "ComputeRegionNetworkEndpointGroupCloudFunction",
    "ComputeRegionNetworkEndpointGroupCloudFunctionOutputReference",
    "ComputeRegionNetworkEndpointGroupCloudRun",
    "ComputeRegionNetworkEndpointGroupCloudRunOutputReference",
    "ComputeRegionNetworkEndpointGroupConfig",
    "ComputeRegionNetworkEndpointGroupPscData",
    "ComputeRegionNetworkEndpointGroupPscDataOutputReference",
    "ComputeRegionNetworkEndpointGroupTimeouts",
    "ComputeRegionNetworkEndpointGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__89edb568d6897cc2b0188dec60081e7fb4cad1e7c13e4521e5d2b7a04aa043eb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    region: builtins.str,
    app_engine: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_function: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_run: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_endpoint_type: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    psc_data: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupPscData, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_target_service: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d31dfd93580dea4e1db924defa8f477893a410e9fa91d7aacbbf35e6b62ea70d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3593c7c19283008e547da4b4737549b2bf4dc81c4cdfc1390e34fb065bbf4cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85deb4f758f1873cbbb3340eed9658525f6e52620d80790500a25741ee479188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13490bc9760b1124df59ca6b70cdbdc40cb4dd887c4a136e7f56e62a62f6803a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1580c2e2c732f2a3a0382b64c0bddb78cc48ecba7084700379f054d65574b6b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf34afe784b44fcf9e170e5cf85e06b0af528fbbed86b73a79ae7210fb612f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41220fadb86ade1bf09a4fbc2652460d73be06c03081889a7ce95358c40e099b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a53151efb936a0fae0548239d624e85e00a36b796a8307cbf615a58e90b805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adad0f3f90598e442b94e73654cb63dfd1b448b206a508faa690322c4af345b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68a76da5bc92bae4e0face68117cdc270b37e1082c000473f32a9b7f01b21df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2824648fe93fcd363482272620f1db44d03f42f5f499ec22bcf0aa789a4b728b(
    *,
    service: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1348f7b5f4895c8f1f2a2b05a7efbf586871c5d1950ff4778afa1e0bff7ab710(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2c0a16ab6dd63a6aa6a7f3d55ce1201b12d2c940118f2bfaa35f6306f23a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8e877d66db7900f0639a2fc7bc4433e06c406ca7c205ea88acf02397f2a518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827fa609725d58b5990b97c783a333e3a461099e0cf8ed71a1ceed4980ca3113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03cad81b2d916b73f0545f505069b5e2170e8853bace59a81b033fd6e7aa8d0(
    value: typing.Optional[ComputeRegionNetworkEndpointGroupAppEngine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef96e1e5629b365e873f7f03780e19d947409c8de928b2e0ec0d94ead0a3b39(
    *,
    function: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e1aa7e80bcaa03484ed6f8f10dc15d2a48f3d2ce7be5f64cd864524a471775(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e3c9b08591ec00b271275abd50db0101315fdb90b83700472836772ec701f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3e51196fbca2ede3ae3ec2cb44cda3dd9d838da97397e9a4fb8e43a9f7d2df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad392d622d90d6190288eaf2a238d04d70cdeab377c374e3585a94f241381a8(
    value: typing.Optional[ComputeRegionNetworkEndpointGroupCloudFunction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81098f86ecb43c63239af3a8dd84b8393322d217ab5418e9b9292527b83392b(
    *,
    service: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    url_mask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a02366401c63996184dc43aba03902d402ee324cdc1c069f686ce3a20b079c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca1030b915be244e267c04eee12d830224ec57cb1c9a3aa38a32bd66a15a7ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16597702e9334199c68e2b18d074ea90ed6209ffddea95fae5b4737b27351da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4502bcf648a75660f311414f4c476e6b7794a42a7ebc27d65b8a12b8e9ff61d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52abc4dd0be9075a584ccf92ecb2b12b7b454b796bfc132cef4126f503eb339(
    value: typing.Optional[ComputeRegionNetworkEndpointGroupCloudRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedbe00ce373430d88e89d40b0808274ff8cf2d1300527c407c7a49ba12d93aa(
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
    app_engine: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_function: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_run: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_endpoint_type: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    psc_data: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupPscData, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_target_service: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionNetworkEndpointGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d85f57b0234595569753953ff9297da08f135b8e708729b55e7b6d12b0148c(
    *,
    producer_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb8a61e2fa583e50ebdf4134f3674eb44513ecb849caf9fc9c1fe99a821610f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00751d30c4d9fa9f4c3be6dc621ac7fcef6c31b6c39e2f5d5268a8efe333df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ff44b00557017051e0bc025e1b51b26907a1d4d9d78965df027aadd969e56e(
    value: typing.Optional[ComputeRegionNetworkEndpointGroupPscData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0859cf34f053a9a9f137cca6f1978066e5bf6874301438fbb5c710eb57c6490(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670fe5d7236046b000dfc4d857d55c6c205c27dd20e80408aae118c328f8dc6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac752ae9b2528f656017d4b7615348150e8d3e6e8e319043eac7fdcdc280aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3884d9df5936d89d38f35acb9b778c434213770b9a8c7257335ccd844d98f24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f48149e790676ff631b9cce9b6fff4e9e36a610aedce120d9b65f7eecef861(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionNetworkEndpointGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
