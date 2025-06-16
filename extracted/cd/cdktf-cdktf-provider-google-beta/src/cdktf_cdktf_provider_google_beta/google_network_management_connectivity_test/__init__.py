r'''
# `google_network_management_connectivity_test`

Refer to the Terraform Registry for docs: [`google_network_management_connectivity_test`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test).
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


class GoogleNetworkManagementConnectivityTest(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTest",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test google_network_management_connectivity_test}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: typing.Union["GoogleNetworkManagementConnectivityTestDestination", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source: typing.Union["GoogleNetworkManagementConnectivityTestSource", typing.Dict[builtins.str, typing.Any]],
        bypass_firewall_checks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        round_trip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test google_network_management_connectivity_test} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#destination GoogleNetworkManagementConnectivityTest#destination}
        :param name: Unique name for the connectivity test. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#name GoogleNetworkManagementConnectivityTest#name}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#source GoogleNetworkManagementConnectivityTest#source}
        :param bypass_firewall_checks: Whether the analysis should skip firewall checking. Default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#bypass_firewall_checks GoogleNetworkManagementConnectivityTest#bypass_firewall_checks}
        :param description: The user-supplied description of the Connectivity Test. Maximum of 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#description GoogleNetworkManagementConnectivityTest#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#id GoogleNetworkManagementConnectivityTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#labels GoogleNetworkManagementConnectivityTest#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project GoogleNetworkManagementConnectivityTest#project}.
        :param protocol: IP Protocol of the test. When not provided, "TCP" is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#protocol GoogleNetworkManagementConnectivityTest#protocol}
        :param related_projects: Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#related_projects GoogleNetworkManagementConnectivityTest#related_projects}
        :param round_trip: Whether run analysis for the return path from destination to source. Default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#round_trip GoogleNetworkManagementConnectivityTest#round_trip}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#timeouts GoogleNetworkManagementConnectivityTest#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b91e97146b901be15c9379f88665256dc0ed480757098dbcc307237bab5445)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkManagementConnectivityTestConfig(
            destination=destination,
            name=name,
            source=source,
            bypass_firewall_checks=bypass_firewall_checks,
            description=description,
            id=id,
            labels=labels,
            project=project,
            protocol=protocol,
            related_projects=related_projects,
            round_trip=round_trip,
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
        '''Generates CDKTF code for importing a GoogleNetworkManagementConnectivityTest resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkManagementConnectivityTest to import.
        :param import_from_id: The id of the existing GoogleNetworkManagementConnectivityTest that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkManagementConnectivityTest to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669da0158c26c2779f4ec50e2c0036348e413a60b3ddf542f6a6ec363067e284)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        cloud_sql_instance: typing.Optional[builtins.str] = None,
        forwarding_rule: typing.Optional[builtins.str] = None,
        fqdn: typing.Optional[builtins.str] = None,
        gke_master_cluster: typing.Optional[builtins.str] = None,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
        redis_cluster: typing.Optional[builtins.str] = None,
        redis_instance: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_sql_instance: A Cloud SQL instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_sql_instance GoogleNetworkManagementConnectivityTest#cloud_sql_instance}
        :param forwarding_rule: Forwarding rule URI. Forwarding rules are frontends for load balancers, PSC endpoints, and Protocol Forwarding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#forwarding_rule GoogleNetworkManagementConnectivityTest#forwarding_rule}
        :param fqdn: A DNS endpoint of Google Kubernetes Engine cluster control plane. Requires gke_master_cluster to be set, can't be used simultaneoulsly with ip_address or network. Applicable only to destination endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#fqdn GoogleNetworkManagementConnectivityTest#fqdn}
        :param gke_master_cluster: A cluster URI for Google Kubernetes Engine cluster control plane. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#gke_master_cluster GoogleNetworkManagementConnectivityTest#gke_master_cluster}
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#instance GoogleNetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#ip_address GoogleNetworkManagementConnectivityTest#ip_address}
        :param network: A VPC network URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network GoogleNetworkManagementConnectivityTest#network}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#port GoogleNetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The project ID can be derived from the URI if you provide a endpoint or network URI. The following are two cases where you may need to provide the project ID: 1. Only the IP address is specified, and the IP address is within a Google Cloud project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project_id GoogleNetworkManagementConnectivityTest#project_id}
        :param redis_cluster: A Redis Cluster URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#redis_cluster GoogleNetworkManagementConnectivityTest#redis_cluster}
        :param redis_instance: A Redis Instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#redis_instance GoogleNetworkManagementConnectivityTest#redis_instance}
        '''
        value = GoogleNetworkManagementConnectivityTestDestination(
            cloud_sql_instance=cloud_sql_instance,
            forwarding_rule=forwarding_rule,
            fqdn=fqdn,
            gke_master_cluster=gke_master_cluster,
            instance=instance,
            ip_address=ip_address,
            network=network,
            port=port,
            project_id=project_id,
            redis_cluster=redis_cluster,
            redis_instance=redis_instance,
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        app_engine_version: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestSourceAppEngineVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_function: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestSourceCloudFunction", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_run_revision: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestSourceCloudRunRevision", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_sql_instance: typing.Optional[builtins.str] = None,
        gke_master_cluster: typing.Optional[builtins.str] = None,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_engine_version: app_engine_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#app_engine_version GoogleNetworkManagementConnectivityTest#app_engine_version}
        :param cloud_function: cloud_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_function GoogleNetworkManagementConnectivityTest#cloud_function}
        :param cloud_run_revision: cloud_run_revision block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_run_revision GoogleNetworkManagementConnectivityTest#cloud_run_revision}
        :param cloud_sql_instance: A Cloud SQL instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_sql_instance GoogleNetworkManagementConnectivityTest#cloud_sql_instance}
        :param gke_master_cluster: A cluster URI for Google Kubernetes Engine cluster control plane. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#gke_master_cluster GoogleNetworkManagementConnectivityTest#gke_master_cluster}
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#instance GoogleNetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#ip_address GoogleNetworkManagementConnectivityTest#ip_address}
        :param network: A VPC network URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network GoogleNetworkManagementConnectivityTest#network}
        :param network_type: Type of the network where the endpoint is located. Possible values: ["GCP_NETWORK", "NON_GCP_NETWORK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network_type GoogleNetworkManagementConnectivityTest#network_type}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#port GoogleNetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The project ID can be derived from the URI if you provide a endpoint or network URI. The following are two cases where you may need to provide the project ID: 1. Only the IP address is specified, and the IP address is within a Google Cloud project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project_id GoogleNetworkManagementConnectivityTest#project_id}
        '''
        value = GoogleNetworkManagementConnectivityTestSource(
            app_engine_version=app_engine_version,
            cloud_function=cloud_function,
            cloud_run_revision=cloud_run_revision,
            cloud_sql_instance=cloud_sql_instance,
            gke_master_cluster=gke_master_cluster,
            instance=instance,
            ip_address=ip_address,
            network=network,
            network_type=network_type,
            port=port,
            project_id=project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#create GoogleNetworkManagementConnectivityTest#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#delete GoogleNetworkManagementConnectivityTest#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#update GoogleNetworkManagementConnectivityTest#update}.
        '''
        value = GoogleNetworkManagementConnectivityTestTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBypassFirewallChecks")
    def reset_bypass_firewall_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassFirewallChecks", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRelatedProjects")
    def reset_related_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedProjects", []))

    @jsii.member(jsii_name="resetRoundTrip")
    def reset_round_trip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoundTrip", []))

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
    @jsii.member(jsii_name="destination")
    def destination(
        self,
    ) -> "GoogleNetworkManagementConnectivityTestDestinationOutputReference":
        return typing.cast("GoogleNetworkManagementConnectivityTestDestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "GoogleNetworkManagementConnectivityTestSourceOutputReference":
        return typing.cast("GoogleNetworkManagementConnectivityTestSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleNetworkManagementConnectivityTestTimeoutsOutputReference":
        return typing.cast("GoogleNetworkManagementConnectivityTestTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bypassFirewallChecksInput")
    def bypass_firewall_checks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bypassFirewallChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional["GoogleNetworkManagementConnectivityTestDestination"]:
        return typing.cast(typing.Optional["GoogleNetworkManagementConnectivityTestDestination"], jsii.get(self, "destinationInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedProjectsInput")
    def related_projects_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "relatedProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="roundTripInput")
    def round_trip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "roundTripInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["GoogleNetworkManagementConnectivityTestSource"]:
        return typing.cast(typing.Optional["GoogleNetworkManagementConnectivityTestSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkManagementConnectivityTestTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkManagementConnectivityTestTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassFirewallChecks")
    def bypass_firewall_checks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bypassFirewallChecks"))

    @bypass_firewall_checks.setter
    def bypass_firewall_checks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b06f06670c8cc060e3105ee800ea0a0aba60493b295d6677574c106c7e977ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassFirewallChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b26b245d19da35f1897e562a9e2df038950fe2c6fd547ee18a766e1bd38194b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce00f3cfc1fa64b9b329018ec69813140a13e684b70324abfcbe2fab7cd2845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7964acda3c64e58e6a10f5e3f6da44bded08168c735b18401ed63a9e04154bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a80128b044ea824e80d37b154fc31cfa9e01d9f2a3254523fa081d7a2a6a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7162110ed45c02d9b9bfcf0ee2db97372a3578f44ace7b28e887b08aad4768e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c896cee9ec1e959909b368a3fcefb5f48ae1ec958d295eb513ec82fd81d15159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relatedProjects")
    def related_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relatedProjects"))

    @related_projects.setter
    def related_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72e2c002e1a17a59212a110bd2c053724e686db978ce4ef8fcdbfa45fbcbc9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relatedProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roundTrip")
    def round_trip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "roundTrip"))

    @round_trip.setter
    def round_trip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd276ff6c7fd873a865dbcf043a494c436995db4c5f632b7fcb0630f5cf10651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roundTrip", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestConfig",
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
        "name": "name",
        "source": "source",
        "bypass_firewall_checks": "bypassFirewallChecks",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "protocol": "protocol",
        "related_projects": "relatedProjects",
        "round_trip": "roundTrip",
        "timeouts": "timeouts",
    },
)
class GoogleNetworkManagementConnectivityTestConfig(
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
        destination: typing.Union["GoogleNetworkManagementConnectivityTestDestination", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source: typing.Union["GoogleNetworkManagementConnectivityTestSource", typing.Dict[builtins.str, typing.Any]],
        bypass_firewall_checks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        round_trip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#destination GoogleNetworkManagementConnectivityTest#destination}
        :param name: Unique name for the connectivity test. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#name GoogleNetworkManagementConnectivityTest#name}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#source GoogleNetworkManagementConnectivityTest#source}
        :param bypass_firewall_checks: Whether the analysis should skip firewall checking. Default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#bypass_firewall_checks GoogleNetworkManagementConnectivityTest#bypass_firewall_checks}
        :param description: The user-supplied description of the Connectivity Test. Maximum of 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#description GoogleNetworkManagementConnectivityTest#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#id GoogleNetworkManagementConnectivityTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#labels GoogleNetworkManagementConnectivityTest#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project GoogleNetworkManagementConnectivityTest#project}.
        :param protocol: IP Protocol of the test. When not provided, "TCP" is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#protocol GoogleNetworkManagementConnectivityTest#protocol}
        :param related_projects: Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#related_projects GoogleNetworkManagementConnectivityTest#related_projects}
        :param round_trip: Whether run analysis for the return path from destination to source. Default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#round_trip GoogleNetworkManagementConnectivityTest#round_trip}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#timeouts GoogleNetworkManagementConnectivityTest#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = GoogleNetworkManagementConnectivityTestDestination(**destination)
        if isinstance(source, dict):
            source = GoogleNetworkManagementConnectivityTestSource(**source)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkManagementConnectivityTestTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6e9f7ad1d0d17ca98570f95e7a21153cb9f66cccde66854e941669662e7d9d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument bypass_firewall_checks", value=bypass_firewall_checks, expected_type=type_hints["bypass_firewall_checks"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument related_projects", value=related_projects, expected_type=type_hints["related_projects"])
            check_type(argname="argument round_trip", value=round_trip, expected_type=type_hints["round_trip"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "name": name,
            "source": source,
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
        if bypass_firewall_checks is not None:
            self._values["bypass_firewall_checks"] = bypass_firewall_checks
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if protocol is not None:
            self._values["protocol"] = protocol
        if related_projects is not None:
            self._values["related_projects"] = related_projects
        if round_trip is not None:
            self._values["round_trip"] = round_trip
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
    def destination(self) -> "GoogleNetworkManagementConnectivityTestDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#destination GoogleNetworkManagementConnectivityTest#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("GoogleNetworkManagementConnectivityTestDestination", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Unique name for the connectivity test.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#name GoogleNetworkManagementConnectivityTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "GoogleNetworkManagementConnectivityTestSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#source GoogleNetworkManagementConnectivityTest#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("GoogleNetworkManagementConnectivityTestSource", result)

    @builtins.property
    def bypass_firewall_checks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the analysis should skip firewall checking. Default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#bypass_firewall_checks GoogleNetworkManagementConnectivityTest#bypass_firewall_checks}
        '''
        result = self._values.get("bypass_firewall_checks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-supplied description of the Connectivity Test. Maximum of 512 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#description GoogleNetworkManagementConnectivityTest#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#id GoogleNetworkManagementConnectivityTest#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#labels GoogleNetworkManagementConnectivityTest#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project GoogleNetworkManagementConnectivityTest#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''IP Protocol of the test. When not provided, "TCP" is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#protocol GoogleNetworkManagementConnectivityTest#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def related_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#related_projects GoogleNetworkManagementConnectivityTest#related_projects}
        '''
        result = self._values.get("related_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def round_trip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether run analysis for the return path from destination to source. Default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#round_trip GoogleNetworkManagementConnectivityTest#round_trip}
        '''
        result = self._values.get("round_trip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkManagementConnectivityTestTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#timeouts GoogleNetworkManagementConnectivityTest#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkManagementConnectivityTestTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestDestination",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_sql_instance": "cloudSqlInstance",
        "forwarding_rule": "forwardingRule",
        "fqdn": "fqdn",
        "gke_master_cluster": "gkeMasterCluster",
        "instance": "instance",
        "ip_address": "ipAddress",
        "network": "network",
        "port": "port",
        "project_id": "projectId",
        "redis_cluster": "redisCluster",
        "redis_instance": "redisInstance",
    },
)
class GoogleNetworkManagementConnectivityTestDestination:
    def __init__(
        self,
        *,
        cloud_sql_instance: typing.Optional[builtins.str] = None,
        forwarding_rule: typing.Optional[builtins.str] = None,
        fqdn: typing.Optional[builtins.str] = None,
        gke_master_cluster: typing.Optional[builtins.str] = None,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
        redis_cluster: typing.Optional[builtins.str] = None,
        redis_instance: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_sql_instance: A Cloud SQL instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_sql_instance GoogleNetworkManagementConnectivityTest#cloud_sql_instance}
        :param forwarding_rule: Forwarding rule URI. Forwarding rules are frontends for load balancers, PSC endpoints, and Protocol Forwarding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#forwarding_rule GoogleNetworkManagementConnectivityTest#forwarding_rule}
        :param fqdn: A DNS endpoint of Google Kubernetes Engine cluster control plane. Requires gke_master_cluster to be set, can't be used simultaneoulsly with ip_address or network. Applicable only to destination endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#fqdn GoogleNetworkManagementConnectivityTest#fqdn}
        :param gke_master_cluster: A cluster URI for Google Kubernetes Engine cluster control plane. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#gke_master_cluster GoogleNetworkManagementConnectivityTest#gke_master_cluster}
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#instance GoogleNetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#ip_address GoogleNetworkManagementConnectivityTest#ip_address}
        :param network: A VPC network URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network GoogleNetworkManagementConnectivityTest#network}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#port GoogleNetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The project ID can be derived from the URI if you provide a endpoint or network URI. The following are two cases where you may need to provide the project ID: 1. Only the IP address is specified, and the IP address is within a Google Cloud project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project_id GoogleNetworkManagementConnectivityTest#project_id}
        :param redis_cluster: A Redis Cluster URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#redis_cluster GoogleNetworkManagementConnectivityTest#redis_cluster}
        :param redis_instance: A Redis Instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#redis_instance GoogleNetworkManagementConnectivityTest#redis_instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6a6c9835fd8d42c48fb136b0e4913937e3e7a0ac520b8a04b628574836df53)
            check_type(argname="argument cloud_sql_instance", value=cloud_sql_instance, expected_type=type_hints["cloud_sql_instance"])
            check_type(argname="argument forwarding_rule", value=forwarding_rule, expected_type=type_hints["forwarding_rule"])
            check_type(argname="argument fqdn", value=fqdn, expected_type=type_hints["fqdn"])
            check_type(argname="argument gke_master_cluster", value=gke_master_cluster, expected_type=type_hints["gke_master_cluster"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument redis_cluster", value=redis_cluster, expected_type=type_hints["redis_cluster"])
            check_type(argname="argument redis_instance", value=redis_instance, expected_type=type_hints["redis_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_sql_instance is not None:
            self._values["cloud_sql_instance"] = cloud_sql_instance
        if forwarding_rule is not None:
            self._values["forwarding_rule"] = forwarding_rule
        if fqdn is not None:
            self._values["fqdn"] = fqdn
        if gke_master_cluster is not None:
            self._values["gke_master_cluster"] = gke_master_cluster
        if instance is not None:
            self._values["instance"] = instance
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if network is not None:
            self._values["network"] = network
        if port is not None:
            self._values["port"] = port
        if project_id is not None:
            self._values["project_id"] = project_id
        if redis_cluster is not None:
            self._values["redis_cluster"] = redis_cluster
        if redis_instance is not None:
            self._values["redis_instance"] = redis_instance

    @builtins.property
    def cloud_sql_instance(self) -> typing.Optional[builtins.str]:
        '''A Cloud SQL instance URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_sql_instance GoogleNetworkManagementConnectivityTest#cloud_sql_instance}
        '''
        result = self._values.get("cloud_sql_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarding_rule(self) -> typing.Optional[builtins.str]:
        '''Forwarding rule URI. Forwarding rules are frontends for load balancers, PSC endpoints, and Protocol Forwarding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#forwarding_rule GoogleNetworkManagementConnectivityTest#forwarding_rule}
        '''
        result = self._values.get("forwarding_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fqdn(self) -> typing.Optional[builtins.str]:
        '''A DNS endpoint of Google Kubernetes Engine cluster control plane.

        Requires gke_master_cluster to be set, can't be used simultaneoulsly with
        ip_address or network. Applicable only to destination endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#fqdn GoogleNetworkManagementConnectivityTest#fqdn}
        '''
        result = self._values.get("fqdn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_master_cluster(self) -> typing.Optional[builtins.str]:
        '''A cluster URI for Google Kubernetes Engine cluster control plane.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#gke_master_cluster GoogleNetworkManagementConnectivityTest#gke_master_cluster}
        '''
        result = self._values.get("gke_master_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''A Compute Engine instance URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#instance GoogleNetworkManagementConnectivityTest#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the endpoint, which can be an external or internal IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#ip_address GoogleNetworkManagementConnectivityTest#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''A VPC network URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network GoogleNetworkManagementConnectivityTest#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#port GoogleNetworkManagementConnectivityTest#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project ID where the endpoint is located.

        The project ID can be derived from the URI if you provide a endpoint or
        network URI.
        The following are two cases where you may need to provide the project ID:

        1. Only the IP address is specified, and the IP address is within a Google
           Cloud project.
        2. When you are using Shared VPC and the IP address that you provide is
           from the service project. In this case, the network that the IP address
           resides in is defined in the host project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project_id GoogleNetworkManagementConnectivityTest#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_cluster(self) -> typing.Optional[builtins.str]:
        '''A Redis Cluster URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#redis_cluster GoogleNetworkManagementConnectivityTest#redis_cluster}
        '''
        result = self._values.get("redis_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_instance(self) -> typing.Optional[builtins.str]:
        '''A Redis Instance URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#redis_instance GoogleNetworkManagementConnectivityTest#redis_instance}
        '''
        result = self._values.get("redis_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkManagementConnectivityTestDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__399934e38ff2d890e3baf058bd313cb5f5acbe606c1b6bdd2449e51fb68f278b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudSqlInstance")
    def reset_cloud_sql_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlInstance", []))

    @jsii.member(jsii_name="resetForwardingRule")
    def reset_forwarding_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingRule", []))

    @jsii.member(jsii_name="resetFqdn")
    def reset_fqdn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFqdn", []))

    @jsii.member(jsii_name="resetGkeMasterCluster")
    def reset_gke_master_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeMasterCluster", []))

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRedisCluster")
    def reset_redis_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisCluster", []))

    @jsii.member(jsii_name="resetRedisInstance")
    def reset_redis_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisInstance", []))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstanceInput")
    def cloud_sql_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingRuleInput")
    def forwarding_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdnInput")
    def fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeMasterClusterInput")
    def gke_master_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeMasterClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="redisClusterInput")
    def redis_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="redisInstanceInput")
    def redis_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstance")
    def cloud_sql_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlInstance"))

    @cloud_sql_instance.setter
    def cloud_sql_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219719d5979c17c6760d7e5ffe8d3fa5172e85e59a5c814063c6591add13c9ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @forwarding_rule.setter
    def forwarding_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d453c6c2b06c25c4fbcd5ec435063e7aa60bdda6d82ea3ab22dc327df4a6632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @fqdn.setter
    def fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac9210b88fab0c99230d8ab30c4f857624063c9f06c884248b35b9f4f1c6860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeMasterCluster")
    def gke_master_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeMasterCluster"))

    @gke_master_cluster.setter
    def gke_master_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc7a244f13ab1f8c6a92dee89d33bbac7a200d7967aecba2f5c71e942685fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeMasterCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2cbab8e2fdab35cccaf1caea9d83c5e8a4074c3668accee0f45754266a47ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb329c3a33cb7492f57da3e0fc2869716b7cbdd85c59d454f104cd926c8fd10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e95636ecf1003bcc41459da940b49086254006b8982c2f54c28445d1640de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f776f20eaab9397d7263e57c96d0aa13759604ba942eeaedc37e019c18b59ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fb1600c542014d19e04443e444ba5cd4b1e7f3126cfa8021f96e9e00ac7c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisCluster")
    def redis_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisCluster"))

    @redis_cluster.setter
    def redis_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e672c7b053d11426a7ec63c4d841160e306a3478ad5ad1d49e2a612369d331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisInstance")
    def redis_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisInstance"))

    @redis_instance.setter
    def redis_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b22bf6386ed9550c293f374664954060378892b917eee76e1ca71b8770ca892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestDestination]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkManagementConnectivityTestDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2f6bea8617ed9dc0d85543d0cca41caf72c729969d52e41eb0bcf0cc48a229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSource",
    jsii_struct_bases=[],
    name_mapping={
        "app_engine_version": "appEngineVersion",
        "cloud_function": "cloudFunction",
        "cloud_run_revision": "cloudRunRevision",
        "cloud_sql_instance": "cloudSqlInstance",
        "gke_master_cluster": "gkeMasterCluster",
        "instance": "instance",
        "ip_address": "ipAddress",
        "network": "network",
        "network_type": "networkType",
        "port": "port",
        "project_id": "projectId",
    },
)
class GoogleNetworkManagementConnectivityTestSource:
    def __init__(
        self,
        *,
        app_engine_version: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestSourceAppEngineVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_function: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestSourceCloudFunction", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_run_revision: typing.Optional[typing.Union["GoogleNetworkManagementConnectivityTestSourceCloudRunRevision", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_sql_instance: typing.Optional[builtins.str] = None,
        gke_master_cluster: typing.Optional[builtins.str] = None,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_engine_version: app_engine_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#app_engine_version GoogleNetworkManagementConnectivityTest#app_engine_version}
        :param cloud_function: cloud_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_function GoogleNetworkManagementConnectivityTest#cloud_function}
        :param cloud_run_revision: cloud_run_revision block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_run_revision GoogleNetworkManagementConnectivityTest#cloud_run_revision}
        :param cloud_sql_instance: A Cloud SQL instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_sql_instance GoogleNetworkManagementConnectivityTest#cloud_sql_instance}
        :param gke_master_cluster: A cluster URI for Google Kubernetes Engine cluster control plane. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#gke_master_cluster GoogleNetworkManagementConnectivityTest#gke_master_cluster}
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#instance GoogleNetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#ip_address GoogleNetworkManagementConnectivityTest#ip_address}
        :param network: A VPC network URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network GoogleNetworkManagementConnectivityTest#network}
        :param network_type: Type of the network where the endpoint is located. Possible values: ["GCP_NETWORK", "NON_GCP_NETWORK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network_type GoogleNetworkManagementConnectivityTest#network_type}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#port GoogleNetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The project ID can be derived from the URI if you provide a endpoint or network URI. The following are two cases where you may need to provide the project ID: 1. Only the IP address is specified, and the IP address is within a Google Cloud project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project_id GoogleNetworkManagementConnectivityTest#project_id}
        '''
        if isinstance(app_engine_version, dict):
            app_engine_version = GoogleNetworkManagementConnectivityTestSourceAppEngineVersion(**app_engine_version)
        if isinstance(cloud_function, dict):
            cloud_function = GoogleNetworkManagementConnectivityTestSourceCloudFunction(**cloud_function)
        if isinstance(cloud_run_revision, dict):
            cloud_run_revision = GoogleNetworkManagementConnectivityTestSourceCloudRunRevision(**cloud_run_revision)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37df8be600999526659f4404f62a73ba1ca8052f1d3c74e03325f8758f4d1335)
            check_type(argname="argument app_engine_version", value=app_engine_version, expected_type=type_hints["app_engine_version"])
            check_type(argname="argument cloud_function", value=cloud_function, expected_type=type_hints["cloud_function"])
            check_type(argname="argument cloud_run_revision", value=cloud_run_revision, expected_type=type_hints["cloud_run_revision"])
            check_type(argname="argument cloud_sql_instance", value=cloud_sql_instance, expected_type=type_hints["cloud_sql_instance"])
            check_type(argname="argument gke_master_cluster", value=gke_master_cluster, expected_type=type_hints["gke_master_cluster"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_engine_version is not None:
            self._values["app_engine_version"] = app_engine_version
        if cloud_function is not None:
            self._values["cloud_function"] = cloud_function
        if cloud_run_revision is not None:
            self._values["cloud_run_revision"] = cloud_run_revision
        if cloud_sql_instance is not None:
            self._values["cloud_sql_instance"] = cloud_sql_instance
        if gke_master_cluster is not None:
            self._values["gke_master_cluster"] = gke_master_cluster
        if instance is not None:
            self._values["instance"] = instance
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if network is not None:
            self._values["network"] = network
        if network_type is not None:
            self._values["network_type"] = network_type
        if port is not None:
            self._values["port"] = port
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def app_engine_version(
        self,
    ) -> typing.Optional["GoogleNetworkManagementConnectivityTestSourceAppEngineVersion"]:
        '''app_engine_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#app_engine_version GoogleNetworkManagementConnectivityTest#app_engine_version}
        '''
        result = self._values.get("app_engine_version")
        return typing.cast(typing.Optional["GoogleNetworkManagementConnectivityTestSourceAppEngineVersion"], result)

    @builtins.property
    def cloud_function(
        self,
    ) -> typing.Optional["GoogleNetworkManagementConnectivityTestSourceCloudFunction"]:
        '''cloud_function block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_function GoogleNetworkManagementConnectivityTest#cloud_function}
        '''
        result = self._values.get("cloud_function")
        return typing.cast(typing.Optional["GoogleNetworkManagementConnectivityTestSourceCloudFunction"], result)

    @builtins.property
    def cloud_run_revision(
        self,
    ) -> typing.Optional["GoogleNetworkManagementConnectivityTestSourceCloudRunRevision"]:
        '''cloud_run_revision block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_run_revision GoogleNetworkManagementConnectivityTest#cloud_run_revision}
        '''
        result = self._values.get("cloud_run_revision")
        return typing.cast(typing.Optional["GoogleNetworkManagementConnectivityTestSourceCloudRunRevision"], result)

    @builtins.property
    def cloud_sql_instance(self) -> typing.Optional[builtins.str]:
        '''A Cloud SQL instance URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#cloud_sql_instance GoogleNetworkManagementConnectivityTest#cloud_sql_instance}
        '''
        result = self._values.get("cloud_sql_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gke_master_cluster(self) -> typing.Optional[builtins.str]:
        '''A cluster URI for Google Kubernetes Engine cluster control plane.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#gke_master_cluster GoogleNetworkManagementConnectivityTest#gke_master_cluster}
        '''
        result = self._values.get("gke_master_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''A Compute Engine instance URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#instance GoogleNetworkManagementConnectivityTest#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the endpoint, which can be an external or internal IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#ip_address GoogleNetworkManagementConnectivityTest#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''A VPC network URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network GoogleNetworkManagementConnectivityTest#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Type of the network where the endpoint is located. Possible values: ["GCP_NETWORK", "NON_GCP_NETWORK"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#network_type GoogleNetworkManagementConnectivityTest#network_type}
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#port GoogleNetworkManagementConnectivityTest#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project ID where the endpoint is located.

        The project ID can be derived from the URI if you provide a endpoint or
        network URI.
        The following are two cases where you may need to provide the project ID:

        1. Only the IP address is specified, and the IP address is within a Google
           Cloud project.
        2. When you are using Shared VPC and the IP address that you provide is
           from the service project. In this case, the network that the IP address
           resides in is defined in the host project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#project_id GoogleNetworkManagementConnectivityTest#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceAppEngineVersion",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleNetworkManagementConnectivityTestSourceAppEngineVersion:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: An App Engine service version name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb86f8d4b990ee4193d83ad543c81d7fc8040d2f1cc0e5ed7a06c730d64cffc)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''An App Engine service version name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestSourceAppEngineVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkManagementConnectivityTestSourceAppEngineVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceAppEngineVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c089e244d92b6f78d93d044f08f5a284411f4c881ba41a66968318ec39249a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cd368360376e7b8d5baf9ec52aaad006f3d8942c07386308bf11f1ff10b90128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fed572fb1274ee34360d4889acf7e46e92e8021eb8be7c02fad53b888f6722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceCloudFunction",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleNetworkManagementConnectivityTestSourceCloudFunction:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: A Cloud Function name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a18a61a0fd24c24805569662d6857b47a6095708450c226f79981bd4235925f)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''A Cloud Function name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestSourceCloudFunction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkManagementConnectivityTestSourceCloudFunctionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceCloudFunctionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec4f9e581f7dd42953ebd2aa509f32be12364a047e0210b5972130f30f74588d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cb86914f91b63be26acc98b13f0e0b25465d3f6c1ec184ced6f16637d6ab9a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudFunction]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudFunction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudFunction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1d555f1ff854cdca24e3c070757ae8a2dbc15441a075a8319d2318824dd294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceCloudRunRevision",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleNetworkManagementConnectivityTestSourceCloudRunRevision:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: A Cloud Run revision URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df77041184bc29074a8023272484e3e1f74a8a64ddb7c46ff797fafadc2a73c4)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''A Cloud Run revision URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestSourceCloudRunRevision(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkManagementConnectivityTestSourceCloudRunRevisionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceCloudRunRevisionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d454464fd30f28023b011a0c9937472b9ae68be215945f1d63451be11f5ab94d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c3897531f5d510885f681fbd01faed76e9170ac099a3e6eea20fafb8a5fc59ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb40f78bf02cf05117ff2a70484bdd18601e6cd725c95a90d039c5e491e490f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkManagementConnectivityTestSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33c9e0c0130cb5e85193da0294e74f42d65433437774fec86e78c51093d56648)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAppEngineVersion")
    def put_app_engine_version(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: An App Engine service version name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        value = GoogleNetworkManagementConnectivityTestSourceAppEngineVersion(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putAppEngineVersion", [value]))

    @jsii.member(jsii_name="putCloudFunction")
    def put_cloud_function(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: A Cloud Function name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        value = GoogleNetworkManagementConnectivityTestSourceCloudFunction(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putCloudFunction", [value]))

    @jsii.member(jsii_name="putCloudRunRevision")
    def put_cloud_run_revision(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: A Cloud Run revision URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#uri GoogleNetworkManagementConnectivityTest#uri}
        '''
        value = GoogleNetworkManagementConnectivityTestSourceCloudRunRevision(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putCloudRunRevision", [value]))

    @jsii.member(jsii_name="resetAppEngineVersion")
    def reset_app_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngineVersion", []))

    @jsii.member(jsii_name="resetCloudFunction")
    def reset_cloud_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudFunction", []))

    @jsii.member(jsii_name="resetCloudRunRevision")
    def reset_cloud_run_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRunRevision", []))

    @jsii.member(jsii_name="resetCloudSqlInstance")
    def reset_cloud_sql_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlInstance", []))

    @jsii.member(jsii_name="resetGkeMasterCluster")
    def reset_gke_master_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeMasterCluster", []))

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="appEngineVersion")
    def app_engine_version(
        self,
    ) -> GoogleNetworkManagementConnectivityTestSourceAppEngineVersionOutputReference:
        return typing.cast(GoogleNetworkManagementConnectivityTestSourceAppEngineVersionOutputReference, jsii.get(self, "appEngineVersion"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunction")
    def cloud_function(
        self,
    ) -> GoogleNetworkManagementConnectivityTestSourceCloudFunctionOutputReference:
        return typing.cast(GoogleNetworkManagementConnectivityTestSourceCloudFunctionOutputReference, jsii.get(self, "cloudFunction"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunRevision")
    def cloud_run_revision(
        self,
    ) -> GoogleNetworkManagementConnectivityTestSourceCloudRunRevisionOutputReference:
        return typing.cast(GoogleNetworkManagementConnectivityTestSourceCloudRunRevisionOutputReference, jsii.get(self, "cloudRunRevision"))

    @builtins.property
    @jsii.member(jsii_name="appEngineVersionInput")
    def app_engine_version_input(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion], jsii.get(self, "appEngineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionInput")
    def cloud_function_input(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudFunction]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudFunction], jsii.get(self, "cloudFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunRevisionInput")
    def cloud_run_revision_input(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision], jsii.get(self, "cloudRunRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstanceInput")
    def cloud_sql_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeMasterClusterInput")
    def gke_master_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeMasterClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstance")
    def cloud_sql_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlInstance"))

    @cloud_sql_instance.setter
    def cloud_sql_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ff8c6fed29ab55019b49b677b0cef270533407b771e88d3e11bb0f4d21a759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gkeMasterCluster")
    def gke_master_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeMasterCluster"))

    @gke_master_cluster.setter
    def gke_master_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5321ccd5750a728394c16c411bb010a43f6f436c4ddad4994d5ef74f7e8f9266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeMasterCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55b24768d59dda488a1016caf25a0bb327159f71ed290d3638ee02e459f0da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef717819700cd88f877d54dac0afdda5803de3d8a5dcba5300171c20bb718171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320fb6916d5d8287c021ad14fdacd37a0546876049128bdd19a502eddbc5f165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e267d8be72eb45324539a2d4eba9439d07f0e04a4b1a004ae9bb8783a99b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f587ec36e06c2e70c2e59f8ef69292d317cc41ff1bc40e1271fbf97623fd585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed785b7fb3597e18a0cff5db5a4516728db6b2cc59cea999e9b2bd1f8d2d390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkManagementConnectivityTestSource]:
        return typing.cast(typing.Optional[GoogleNetworkManagementConnectivityTestSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkManagementConnectivityTestSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f2fb3a58874d092b084ec639f114bd4b39c0eedf9bb56638f1ad11e7e644d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkManagementConnectivityTestTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#create GoogleNetworkManagementConnectivityTest#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#delete GoogleNetworkManagementConnectivityTest#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#update GoogleNetworkManagementConnectivityTest#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3c88f01ae3166137744e2a58ba62bb56df0f0df69d85c928175850e1b3de9d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#create GoogleNetworkManagementConnectivityTest#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#delete GoogleNetworkManagementConnectivityTest#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_management_connectivity_test#update GoogleNetworkManagementConnectivityTest#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkManagementConnectivityTestTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkManagementConnectivityTestTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkManagementConnectivityTest.GoogleNetworkManagementConnectivityTestTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d92adb49d5b88da9a948f725aaa4d415af3fc2b7aad1671e0378834b94b569b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb4420c44074b3bf2a427daaeffcf34de2a862757f26abca67d2249e537bc9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc70cc0f9d8f4b89ded4d6f0998bd2cbb8989f94cc608604ca7cde1535a0c1e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58c498e9455f91a61d0da80b652c8aac7615949221f3324af61bed21dda901a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkManagementConnectivityTestTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkManagementConnectivityTestTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkManagementConnectivityTestTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ef215e6ed0d1a2e9fcd5b6c97e61cf8be5fbc023001958bc4258d128926451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkManagementConnectivityTest",
    "GoogleNetworkManagementConnectivityTestConfig",
    "GoogleNetworkManagementConnectivityTestDestination",
    "GoogleNetworkManagementConnectivityTestDestinationOutputReference",
    "GoogleNetworkManagementConnectivityTestSource",
    "GoogleNetworkManagementConnectivityTestSourceAppEngineVersion",
    "GoogleNetworkManagementConnectivityTestSourceAppEngineVersionOutputReference",
    "GoogleNetworkManagementConnectivityTestSourceCloudFunction",
    "GoogleNetworkManagementConnectivityTestSourceCloudFunctionOutputReference",
    "GoogleNetworkManagementConnectivityTestSourceCloudRunRevision",
    "GoogleNetworkManagementConnectivityTestSourceCloudRunRevisionOutputReference",
    "GoogleNetworkManagementConnectivityTestSourceOutputReference",
    "GoogleNetworkManagementConnectivityTestTimeouts",
    "GoogleNetworkManagementConnectivityTestTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a9b91e97146b901be15c9379f88665256dc0ed480757098dbcc307237bab5445(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: typing.Union[GoogleNetworkManagementConnectivityTestDestination, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source: typing.Union[GoogleNetworkManagementConnectivityTestSource, typing.Dict[builtins.str, typing.Any]],
    bypass_firewall_checks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    round_trip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkManagementConnectivityTestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__669da0158c26c2779f4ec50e2c0036348e413a60b3ddf542f6a6ec363067e284(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b06f06670c8cc060e3105ee800ea0a0aba60493b295d6677574c106c7e977ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b26b245d19da35f1897e562a9e2df038950fe2c6fd547ee18a766e1bd38194b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce00f3cfc1fa64b9b329018ec69813140a13e684b70324abfcbe2fab7cd2845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7964acda3c64e58e6a10f5e3f6da44bded08168c735b18401ed63a9e04154bbe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a80128b044ea824e80d37b154fc31cfa9e01d9f2a3254523fa081d7a2a6a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7162110ed45c02d9b9bfcf0ee2db97372a3578f44ace7b28e887b08aad4768e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c896cee9ec1e959909b368a3fcefb5f48ae1ec958d295eb513ec82fd81d15159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72e2c002e1a17a59212a110bd2c053724e686db978ce4ef8fcdbfa45fbcbc9d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd276ff6c7fd873a865dbcf043a494c436995db4c5f632b7fcb0630f5cf10651(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6e9f7ad1d0d17ca98570f95e7a21153cb9f66cccde66854e941669662e7d9d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: typing.Union[GoogleNetworkManagementConnectivityTestDestination, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source: typing.Union[GoogleNetworkManagementConnectivityTestSource, typing.Dict[builtins.str, typing.Any]],
    bypass_firewall_checks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    round_trip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkManagementConnectivityTestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6a6c9835fd8d42c48fb136b0e4913937e3e7a0ac520b8a04b628574836df53(
    *,
    cloud_sql_instance: typing.Optional[builtins.str] = None,
    forwarding_rule: typing.Optional[builtins.str] = None,
    fqdn: typing.Optional[builtins.str] = None,
    gke_master_cluster: typing.Optional[builtins.str] = None,
    instance: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    project_id: typing.Optional[builtins.str] = None,
    redis_cluster: typing.Optional[builtins.str] = None,
    redis_instance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399934e38ff2d890e3baf058bd313cb5f5acbe606c1b6bdd2449e51fb68f278b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219719d5979c17c6760d7e5ffe8d3fa5172e85e59a5c814063c6591add13c9ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d453c6c2b06c25c4fbcd5ec435063e7aa60bdda6d82ea3ab22dc327df4a6632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac9210b88fab0c99230d8ab30c4f857624063c9f06c884248b35b9f4f1c6860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc7a244f13ab1f8c6a92dee89d33bbac7a200d7967aecba2f5c71e942685fde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2cbab8e2fdab35cccaf1caea9d83c5e8a4074c3668accee0f45754266a47ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb329c3a33cb7492f57da3e0fc2869716b7cbdd85c59d454f104cd926c8fd10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e95636ecf1003bcc41459da940b49086254006b8982c2f54c28445d1640de2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f776f20eaab9397d7263e57c96d0aa13759604ba942eeaedc37e019c18b59ec2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fb1600c542014d19e04443e444ba5cd4b1e7f3126cfa8021f96e9e00ac7c6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e672c7b053d11426a7ec63c4d841160e306a3478ad5ad1d49e2a612369d331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b22bf6386ed9550c293f374664954060378892b917eee76e1ca71b8770ca892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2f6bea8617ed9dc0d85543d0cca41caf72c729969d52e41eb0bcf0cc48a229(
    value: typing.Optional[GoogleNetworkManagementConnectivityTestDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37df8be600999526659f4404f62a73ba1ca8052f1d3c74e03325f8758f4d1335(
    *,
    app_engine_version: typing.Optional[typing.Union[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_function: typing.Optional[typing.Union[GoogleNetworkManagementConnectivityTestSourceCloudFunction, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_run_revision: typing.Optional[typing.Union[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_sql_instance: typing.Optional[builtins.str] = None,
    gke_master_cluster: typing.Optional[builtins.str] = None,
    instance: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb86f8d4b990ee4193d83ad543c81d7fc8040d2f1cc0e5ed7a06c730d64cffc(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c089e244d92b6f78d93d044f08f5a284411f4c881ba41a66968318ec39249a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd368360376e7b8d5baf9ec52aaad006f3d8942c07386308bf11f1ff10b90128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fed572fb1274ee34360d4889acf7e46e92e8021eb8be7c02fad53b888f6722(
    value: typing.Optional[GoogleNetworkManagementConnectivityTestSourceAppEngineVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a18a61a0fd24c24805569662d6857b47a6095708450c226f79981bd4235925f(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4f9e581f7dd42953ebd2aa509f32be12364a047e0210b5972130f30f74588d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb86914f91b63be26acc98b13f0e0b25465d3f6c1ec184ced6f16637d6ab9a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1d555f1ff854cdca24e3c070757ae8a2dbc15441a075a8319d2318824dd294(
    value: typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudFunction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df77041184bc29074a8023272484e3e1f74a8a64ddb7c46ff797fafadc2a73c4(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d454464fd30f28023b011a0c9937472b9ae68be215945f1d63451be11f5ab94d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3897531f5d510885f681fbd01faed76e9170ac099a3e6eea20fafb8a5fc59ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb40f78bf02cf05117ff2a70484bdd18601e6cd725c95a90d039c5e491e490f(
    value: typing.Optional[GoogleNetworkManagementConnectivityTestSourceCloudRunRevision],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c9e0c0130cb5e85193da0294e74f42d65433437774fec86e78c51093d56648(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ff8c6fed29ab55019b49b677b0cef270533407b771e88d3e11bb0f4d21a759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5321ccd5750a728394c16c411bb010a43f6f436c4ddad4994d5ef74f7e8f9266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55b24768d59dda488a1016caf25a0bb327159f71ed290d3638ee02e459f0da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef717819700cd88f877d54dac0afdda5803de3d8a5dcba5300171c20bb718171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320fb6916d5d8287c021ad14fdacd37a0546876049128bdd19a502eddbc5f165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e267d8be72eb45324539a2d4eba9439d07f0e04a4b1a004ae9bb8783a99b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f587ec36e06c2e70c2e59f8ef69292d317cc41ff1bc40e1271fbf97623fd585(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed785b7fb3597e18a0cff5db5a4516728db6b2cc59cea999e9b2bd1f8d2d390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f2fb3a58874d092b084ec639f114bd4b39c0eedf9bb56638f1ad11e7e644d9(
    value: typing.Optional[GoogleNetworkManagementConnectivityTestSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3c88f01ae3166137744e2a58ba62bb56df0f0df69d85c928175850e1b3de9d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92adb49d5b88da9a948f725aaa4d415af3fc2b7aad1671e0378834b94b569b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb4420c44074b3bf2a427daaeffcf34de2a862757f26abca67d2249e537bc9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc70cc0f9d8f4b89ded4d6f0998bd2cbb8989f94cc608604ca7cde1535a0c1e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58c498e9455f91a61d0da80b652c8aac7615949221f3324af61bed21dda901a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ef215e6ed0d1a2e9fcd5b6c97e61cf8be5fbc023001958bc4258d128926451(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkManagementConnectivityTestTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
