r'''
# `google_vmwareengine_private_cloud`

Refer to the Terraform Registry for docs: [`google_vmwareengine_private_cloud`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud).
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


class GoogleVmwareenginePrivateCloud(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloud",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud google_vmwareengine_private_cloud}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        management_cluster: typing.Union["GoogleVmwareenginePrivateCloudManagementCluster", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network_config: typing.Union["GoogleVmwareenginePrivateCloudNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        deletion_delay_hours: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud google_vmwareengine_private_cloud} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location where the PrivateCloud should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#location GoogleVmwareenginePrivateCloud#location}
        :param management_cluster: management_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#management_cluster GoogleVmwareenginePrivateCloud#management_cluster}
        :param name: The ID of the PrivateCloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#name GoogleVmwareenginePrivateCloud#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#network_config GoogleVmwareenginePrivateCloud#network_config}
        :param deletion_delay_hours: The number of hours to delay this request. You can set this value to an hour between 0 to 8, where setting it to 0 starts the deletion request immediately. If no value is set, a default value is set at the API Level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#deletion_delay_hours GoogleVmwareenginePrivateCloud#deletion_delay_hours}
        :param description: User-provided description for this private cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#description GoogleVmwareenginePrivateCloud#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#id GoogleVmwareenginePrivateCloud#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#project GoogleVmwareenginePrivateCloud#project}.
        :param send_deletion_delay_hours_if_zero: While set true, deletion_delay_hours value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the deletion_delay_hours field. It can be used both alone and together with deletion_delay_hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#send_deletion_delay_hours_if_zero GoogleVmwareenginePrivateCloud#send_deletion_delay_hours_if_zero}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#timeouts GoogleVmwareenginePrivateCloud#timeouts}
        :param type: Initial type of the private cloud. Possible values: ["STANDARD", "TIME_LIMITED", "STRETCHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#type GoogleVmwareenginePrivateCloud#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2287f49ce23cb9e9f7fd9e71ba0958498a7a3a038f9a562a2e2ab8c1f1dc1b91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVmwareenginePrivateCloudConfig(
            location=location,
            management_cluster=management_cluster,
            name=name,
            network_config=network_config,
            deletion_delay_hours=deletion_delay_hours,
            description=description,
            id=id,
            project=project,
            send_deletion_delay_hours_if_zero=send_deletion_delay_hours_if_zero,
            timeouts=timeouts,
            type=type,
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
        '''Generates CDKTF code for importing a GoogleVmwareenginePrivateCloud resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVmwareenginePrivateCloud to import.
        :param import_from_id: The id of the existing GoogleVmwareenginePrivateCloud that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVmwareenginePrivateCloud to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910220e86cd9a900908b6737633546cb90495f61e97451b5b1d22d912995c209)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putManagementCluster")
    def put_management_cluster(
        self,
        *,
        cluster_id: builtins.str,
        autoscaling_settings: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stretched_cluster_config: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: The user-provided identifier of the new Cluster. The identifier must meet the following requirements: - Only contains 1-63 alphanumeric characters and hyphens - Begins with an alphabetical character - Ends with a non-hyphen character - Not formatted as a UUID - Complies with RFC 1034 (https://datatracker.ietf.org/doc/html/rfc1034) (section 3.5) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cluster_id GoogleVmwareenginePrivateCloud#cluster_id}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscaling_settings GoogleVmwareenginePrivateCloud#autoscaling_settings}
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_configs GoogleVmwareenginePrivateCloud#node_type_configs}
        :param stretched_cluster_config: stretched_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#stretched_cluster_config GoogleVmwareenginePrivateCloud#stretched_cluster_config}
        '''
        value = GoogleVmwareenginePrivateCloudManagementCluster(
            cluster_id=cluster_id,
            autoscaling_settings=autoscaling_settings,
            node_type_configs=node_type_configs,
            stretched_cluster_config=stretched_cluster_config,
        )

        return typing.cast(None, jsii.invoke(self, "putManagementCluster", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        management_cidr: builtins.str,
        vmware_engine_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param management_cidr: Management CIDR used by VMware management appliances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#management_cidr GoogleVmwareenginePrivateCloud#management_cidr}
        :param vmware_engine_network: The relative resource name of the VMware Engine network attached to the private cloud. Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project} can either be a project number or a project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#vmware_engine_network GoogleVmwareenginePrivateCloud#vmware_engine_network}
        '''
        value = GoogleVmwareenginePrivateCloudNetworkConfig(
            management_cidr=management_cidr,
            vmware_engine_network=vmware_engine_network,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#create GoogleVmwareenginePrivateCloud#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#delete GoogleVmwareenginePrivateCloud#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#update GoogleVmwareenginePrivateCloud#update}.
        '''
        value = GoogleVmwareenginePrivateCloudTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionDelayHours")
    def reset_deletion_delay_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionDelayHours", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSendDeletionDelayHoursIfZero")
    def reset_send_deletion_delay_hours_if_zero(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendDeletionDelayHoursIfZero", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="hcx")
    def hcx(self) -> "GoogleVmwareenginePrivateCloudHcxList":
        return typing.cast("GoogleVmwareenginePrivateCloudHcxList", jsii.get(self, "hcx"))

    @builtins.property
    @jsii.member(jsii_name="managementCluster")
    def management_cluster(
        self,
    ) -> "GoogleVmwareenginePrivateCloudManagementClusterOutputReference":
        return typing.cast("GoogleVmwareenginePrivateCloudManagementClusterOutputReference", jsii.get(self, "managementCluster"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GoogleVmwareenginePrivateCloudNetworkConfigOutputReference":
        return typing.cast("GoogleVmwareenginePrivateCloudNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nsx")
    def nsx(self) -> "GoogleVmwareenginePrivateCloudNsxList":
        return typing.cast("GoogleVmwareenginePrivateCloudNsxList", jsii.get(self, "nsx"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVmwareenginePrivateCloudTimeoutsOutputReference":
        return typing.cast("GoogleVmwareenginePrivateCloudTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="vcenter")
    def vcenter(self) -> "GoogleVmwareenginePrivateCloudVcenterList":
        return typing.cast("GoogleVmwareenginePrivateCloudVcenterList", jsii.get(self, "vcenter"))

    @builtins.property
    @jsii.member(jsii_name="deletionDelayHoursInput")
    def deletion_delay_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deletionDelayHoursInput"))

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
    @jsii.member(jsii_name="managementClusterInput")
    def management_cluster_input(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementCluster"]:
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementCluster"], jsii.get(self, "managementClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sendDeletionDelayHoursIfZeroInput")
    def send_deletion_delay_hours_if_zero_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendDeletionDelayHoursIfZeroInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVmwareenginePrivateCloudTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVmwareenginePrivateCloudTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionDelayHours")
    def deletion_delay_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deletionDelayHours"))

    @deletion_delay_hours.setter
    def deletion_delay_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937e524e72079a0eb41caa308d0f75c9d1e717096de9fc9ffdedf7bc0d9b794c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionDelayHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbd7d68e5c7a125688bfc70fd1da8441d21e2268810242b98f387872dd1c9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a5a3d3761e2dd32dd8f35ee8eb4710363ea304f0f7b4ef5e3832676d6347f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308486ad451c55c9de138b8d8e4caa5b8edc1cfdcb1b5bf40fa0fb77153e994f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc590156adb7194209cd440fcdfbc115e8a677c2cad769df9eaca03349fa748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46655afdb8710738741e2eed232ffd6a45d95e79f2f90845b8f48371cf5121ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendDeletionDelayHoursIfZero")
    def send_deletion_delay_hours_if_zero(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendDeletionDelayHoursIfZero"))

    @send_deletion_delay_hours_if_zero.setter
    def send_deletion_delay_hours_if_zero(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb72ee018f368e73db8f086831f7dec093a56af202ae007d4e507c665c6fc5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendDeletionDelayHoursIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252778e8d77f9b6452a3cc3ae3562b92cfd8ad8768668e214eb6ed9653f7201e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudConfig",
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
        "management_cluster": "managementCluster",
        "name": "name",
        "network_config": "networkConfig",
        "deletion_delay_hours": "deletionDelayHours",
        "description": "description",
        "id": "id",
        "project": "project",
        "send_deletion_delay_hours_if_zero": "sendDeletionDelayHoursIfZero",
        "timeouts": "timeouts",
        "type": "type",
    },
)
class GoogleVmwareenginePrivateCloudConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        management_cluster: typing.Union["GoogleVmwareenginePrivateCloudManagementCluster", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network_config: typing.Union["GoogleVmwareenginePrivateCloudNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        deletion_delay_hours: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location where the PrivateCloud should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#location GoogleVmwareenginePrivateCloud#location}
        :param management_cluster: management_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#management_cluster GoogleVmwareenginePrivateCloud#management_cluster}
        :param name: The ID of the PrivateCloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#name GoogleVmwareenginePrivateCloud#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#network_config GoogleVmwareenginePrivateCloud#network_config}
        :param deletion_delay_hours: The number of hours to delay this request. You can set this value to an hour between 0 to 8, where setting it to 0 starts the deletion request immediately. If no value is set, a default value is set at the API Level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#deletion_delay_hours GoogleVmwareenginePrivateCloud#deletion_delay_hours}
        :param description: User-provided description for this private cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#description GoogleVmwareenginePrivateCloud#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#id GoogleVmwareenginePrivateCloud#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#project GoogleVmwareenginePrivateCloud#project}.
        :param send_deletion_delay_hours_if_zero: While set true, deletion_delay_hours value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the deletion_delay_hours field. It can be used both alone and together with deletion_delay_hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#send_deletion_delay_hours_if_zero GoogleVmwareenginePrivateCloud#send_deletion_delay_hours_if_zero}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#timeouts GoogleVmwareenginePrivateCloud#timeouts}
        :param type: Initial type of the private cloud. Possible values: ["STANDARD", "TIME_LIMITED", "STRETCHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#type GoogleVmwareenginePrivateCloud#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(management_cluster, dict):
            management_cluster = GoogleVmwareenginePrivateCloudManagementCluster(**management_cluster)
        if isinstance(network_config, dict):
            network_config = GoogleVmwareenginePrivateCloudNetworkConfig(**network_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVmwareenginePrivateCloudTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee04f524d445b6ab7bdee68ea828f764b44a923d807e33c72303595c1591d8db)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument management_cluster", value=management_cluster, expected_type=type_hints["management_cluster"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument deletion_delay_hours", value=deletion_delay_hours, expected_type=type_hints["deletion_delay_hours"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument send_deletion_delay_hours_if_zero", value=send_deletion_delay_hours_if_zero, expected_type=type_hints["send_deletion_delay_hours_if_zero"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "management_cluster": management_cluster,
            "name": name,
            "network_config": network_config,
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
        if deletion_delay_hours is not None:
            self._values["deletion_delay_hours"] = deletion_delay_hours
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if send_deletion_delay_hours_if_zero is not None:
            self._values["send_deletion_delay_hours_if_zero"] = send_deletion_delay_hours_if_zero
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type

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
        '''The location where the PrivateCloud should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#location GoogleVmwareenginePrivateCloud#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def management_cluster(self) -> "GoogleVmwareenginePrivateCloudManagementCluster":
        '''management_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#management_cluster GoogleVmwareenginePrivateCloud#management_cluster}
        '''
        result = self._values.get("management_cluster")
        assert result is not None, "Required property 'management_cluster' is missing"
        return typing.cast("GoogleVmwareenginePrivateCloudManagementCluster", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The ID of the PrivateCloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#name GoogleVmwareenginePrivateCloud#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_config(self) -> "GoogleVmwareenginePrivateCloudNetworkConfig":
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#network_config GoogleVmwareenginePrivateCloud#network_config}
        '''
        result = self._values.get("network_config")
        assert result is not None, "Required property 'network_config' is missing"
        return typing.cast("GoogleVmwareenginePrivateCloudNetworkConfig", result)

    @builtins.property
    def deletion_delay_hours(self) -> typing.Optional[jsii.Number]:
        '''The number of hours to delay this request.

        You can set this value to an hour between 0 to 8, where setting it to 0 starts the deletion request immediately. If no value is set, a default value is set at the API Level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#deletion_delay_hours GoogleVmwareenginePrivateCloud#deletion_delay_hours}
        '''
        result = self._values.get("deletion_delay_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description for this private cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#description GoogleVmwareenginePrivateCloud#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#id GoogleVmwareenginePrivateCloud#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#project GoogleVmwareenginePrivateCloud#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_deletion_delay_hours_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, deletion_delay_hours value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the deletion_delay_hours field. It can be used both alone and together with deletion_delay_hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#send_deletion_delay_hours_if_zero GoogleVmwareenginePrivateCloud#send_deletion_delay_hours_if_zero}
        '''
        result = self._values.get("send_deletion_delay_hours_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleVmwareenginePrivateCloudTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#timeouts GoogleVmwareenginePrivateCloud#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Initial type of the private cloud. Possible values: ["STANDARD", "TIME_LIMITED", "STRETCHED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#type GoogleVmwareenginePrivateCloud#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudHcx",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVmwareenginePrivateCloudHcx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudHcx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudHcxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudHcxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac9f4963ee8c8c8303ebc305db70bc319f560592b1dfd14eb3b9ea1225879b27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareenginePrivateCloudHcxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0793e598b9a4da069d35bec797ec093ded7cc43a599ce26d35ee5df5eb66339b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareenginePrivateCloudHcxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ff6819d693a95083fd25b31dcfbfb1ec2580709563b18cfac39cc5d848d813)
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
            type_hints = typing.get_type_hints(_typecheckingstub__631f81888e2b0a89922eb7831561c7d6fcbe6e1fad08ba5084ad477b6960a646)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b05c8fbdaff024324cf447bcfe3201f3c09a38a0a379c3a2a57f5a22e91bad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudHcxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudHcxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__414eea0a77380e0c4550f6f60d3ae011cfd3ffc2d40a2ef8cacc70fb099aa314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIp"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleVmwareenginePrivateCloudHcx]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudHcx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudHcx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46545b1925e4fd790a8ab4a0980ff6b413b5cf0d98abdb58cbebcf4f87362b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementCluster",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "autoscaling_settings": "autoscalingSettings",
        "node_type_configs": "nodeTypeConfigs",
        "stretched_cluster_config": "stretchedClusterConfig",
    },
)
class GoogleVmwareenginePrivateCloudManagementCluster:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        autoscaling_settings: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stretched_cluster_config: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: The user-provided identifier of the new Cluster. The identifier must meet the following requirements: - Only contains 1-63 alphanumeric characters and hyphens - Begins with an alphabetical character - Ends with a non-hyphen character - Not formatted as a UUID - Complies with RFC 1034 (https://datatracker.ietf.org/doc/html/rfc1034) (section 3.5) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cluster_id GoogleVmwareenginePrivateCloud#cluster_id}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscaling_settings GoogleVmwareenginePrivateCloud#autoscaling_settings}
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_configs GoogleVmwareenginePrivateCloud#node_type_configs}
        :param stretched_cluster_config: stretched_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#stretched_cluster_config GoogleVmwareenginePrivateCloud#stretched_cluster_config}
        '''
        if isinstance(autoscaling_settings, dict):
            autoscaling_settings = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings(**autoscaling_settings)
        if isinstance(stretched_cluster_config, dict):
            stretched_cluster_config = GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig(**stretched_cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e429c4e7e31683f4a5b31ee9177b744c7256d97166f7ad87745b03b65b50b8)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument autoscaling_settings", value=autoscaling_settings, expected_type=type_hints["autoscaling_settings"])
            check_type(argname="argument node_type_configs", value=node_type_configs, expected_type=type_hints["node_type_configs"])
            check_type(argname="argument stretched_cluster_config", value=stretched_cluster_config, expected_type=type_hints["stretched_cluster_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
        }
        if autoscaling_settings is not None:
            self._values["autoscaling_settings"] = autoscaling_settings
        if node_type_configs is not None:
            self._values["node_type_configs"] = node_type_configs
        if stretched_cluster_config is not None:
            self._values["stretched_cluster_config"] = stretched_cluster_config

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''The user-provided identifier of the new Cluster.

        The identifier must meet the following requirements:

        - Only contains 1-63 alphanumeric characters and hyphens
        - Begins with an alphabetical character
        - Ends with a non-hyphen character
        - Not formatted as a UUID
        - Complies with RFC 1034 (https://datatracker.ietf.org/doc/html/rfc1034) (section 3.5)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cluster_id GoogleVmwareenginePrivateCloud#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_settings(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings"]:
        '''autoscaling_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscaling_settings GoogleVmwareenginePrivateCloud#autoscaling_settings}
        '''
        result = self._values.get("autoscaling_settings")
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings"], result)

    @builtins.property
    def node_type_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs"]]]:
        '''node_type_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_configs GoogleVmwareenginePrivateCloud#node_type_configs}
        '''
        result = self._values.get("node_type_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs"]]], result)

    @builtins.property
    def stretched_cluster_config(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig"]:
        '''stretched_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#stretched_cluster_config GoogleVmwareenginePrivateCloud#stretched_cluster_config}
        '''
        result = self._values.get("stretched_cluster_config")
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_policies": "autoscalingPolicies",
        "cool_down_period": "coolDownPeriod",
        "max_cluster_node_count": "maxClusterNodeCount",
        "min_cluster_node_count": "minClusterNodeCount",
    },
)
class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings:
    def __init__(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies", typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscaling_policies GoogleVmwareenginePrivateCloud#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cool_down_period GoogleVmwareenginePrivateCloud#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#max_cluster_node_count GoogleVmwareenginePrivateCloud#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#min_cluster_node_count GoogleVmwareenginePrivateCloud#min_cluster_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8963e4446786394ff545264986547c697c6cfbe2034fb99b41bf62c5ab894d58)
            check_type(argname="argument autoscaling_policies", value=autoscaling_policies, expected_type=type_hints["autoscaling_policies"])
            check_type(argname="argument cool_down_period", value=cool_down_period, expected_type=type_hints["cool_down_period"])
            check_type(argname="argument max_cluster_node_count", value=max_cluster_node_count, expected_type=type_hints["max_cluster_node_count"])
            check_type(argname="argument min_cluster_node_count", value=min_cluster_node_count, expected_type=type_hints["min_cluster_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscaling_policies": autoscaling_policies,
        }
        if cool_down_period is not None:
            self._values["cool_down_period"] = cool_down_period
        if max_cluster_node_count is not None:
            self._values["max_cluster_node_count"] = max_cluster_node_count
        if min_cluster_node_count is not None:
            self._values["min_cluster_node_count"] = min_cluster_node_count

    @builtins.property
    def autoscaling_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies"]]:
        '''autoscaling_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscaling_policies GoogleVmwareenginePrivateCloud#autoscaling_policies}
        '''
        result = self._values.get("autoscaling_policies")
        assert result is not None, "Required property 'autoscaling_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies"]], result)

    @builtins.property
    def cool_down_period(self) -> typing.Optional[builtins.str]:
        '''The minimum duration between consecutive autoscale operations.

        It starts once addition or removal of nodes is fully completed.
        Minimum cool down period is 30m.
        Cool down period must be in whole minutes (for example, 30m, 31m, 50m).
        Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cool_down_period GoogleVmwareenginePrivateCloud#cool_down_period}
        '''
        result = self._values.get("cool_down_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#max_cluster_node_count GoogleVmwareenginePrivateCloud#max_cluster_node_count}
        '''
        result = self._values.get("max_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#min_cluster_node_count GoogleVmwareenginePrivateCloud#min_cluster_node_count}
        '''
        result = self._values.get("min_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "autoscale_policy_id": "autoscalePolicyId",
        "node_type_id": "nodeTypeId",
        "scale_out_size": "scaleOutSize",
        "consumed_memory_thresholds": "consumedMemoryThresholds",
        "cpu_thresholds": "cpuThresholds",
        "storage_thresholds": "storageThresholds",
    },
)
class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies:
    def __init__(
        self,
        *,
        autoscale_policy_id: builtins.str,
        node_type_id: builtins.str,
        scale_out_size: jsii.Number,
        consumed_memory_thresholds: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        cpu_thresholds: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_thresholds: typing.Optional[typing.Union["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscale_policy_id GoogleVmwareenginePrivateCloud#autoscale_policy_id}.
        :param node_type_id: The canonical identifier of the node type to add or remove. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_id GoogleVmwareenginePrivateCloud#node_type_id}
        :param scale_out_size: Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out_size GoogleVmwareenginePrivateCloud#scale_out_size}
        :param consumed_memory_thresholds: consumed_memory_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#consumed_memory_thresholds GoogleVmwareenginePrivateCloud#consumed_memory_thresholds}
        :param cpu_thresholds: cpu_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cpu_thresholds GoogleVmwareenginePrivateCloud#cpu_thresholds}
        :param storage_thresholds: storage_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#storage_thresholds GoogleVmwareenginePrivateCloud#storage_thresholds}
        '''
        if isinstance(consumed_memory_thresholds, dict):
            consumed_memory_thresholds = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(**consumed_memory_thresholds)
        if isinstance(cpu_thresholds, dict):
            cpu_thresholds = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(**cpu_thresholds)
        if isinstance(storage_thresholds, dict):
            storage_thresholds = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(**storage_thresholds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74cf810b094bf65720a0391e159748545b2b153cd8fff851fdff76c1e4e5460)
            check_type(argname="argument autoscale_policy_id", value=autoscale_policy_id, expected_type=type_hints["autoscale_policy_id"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument scale_out_size", value=scale_out_size, expected_type=type_hints["scale_out_size"])
            check_type(argname="argument consumed_memory_thresholds", value=consumed_memory_thresholds, expected_type=type_hints["consumed_memory_thresholds"])
            check_type(argname="argument cpu_thresholds", value=cpu_thresholds, expected_type=type_hints["cpu_thresholds"])
            check_type(argname="argument storage_thresholds", value=storage_thresholds, expected_type=type_hints["storage_thresholds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscale_policy_id": autoscale_policy_id,
            "node_type_id": node_type_id,
            "scale_out_size": scale_out_size,
        }
        if consumed_memory_thresholds is not None:
            self._values["consumed_memory_thresholds"] = consumed_memory_thresholds
        if cpu_thresholds is not None:
            self._values["cpu_thresholds"] = cpu_thresholds
        if storage_thresholds is not None:
            self._values["storage_thresholds"] = storage_thresholds

    @builtins.property
    def autoscale_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscale_policy_id GoogleVmwareenginePrivateCloud#autoscale_policy_id}.'''
        result = self._values.get("autoscale_policy_id")
        assert result is not None, "Required property 'autoscale_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''The canonical identifier of the node type to add or remove.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_id GoogleVmwareenginePrivateCloud#node_type_id}
        '''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_out_size(self) -> jsii.Number:
        '''Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out_size GoogleVmwareenginePrivateCloud#scale_out_size}
        '''
        result = self._values.get("scale_out_size")
        assert result is not None, "Required property 'scale_out_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def consumed_memory_thresholds(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"]:
        '''consumed_memory_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#consumed_memory_thresholds GoogleVmwareenginePrivateCloud#consumed_memory_thresholds}
        '''
        result = self._values.get("consumed_memory_thresholds")
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"], result)

    @builtins.property
    def cpu_thresholds(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"]:
        '''cpu_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cpu_thresholds GoogleVmwareenginePrivateCloud#cpu_thresholds}
        '''
        result = self._values.get("cpu_thresholds")
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"], result)

    @builtins.property
    def storage_thresholds(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        '''storage_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#storage_thresholds GoogleVmwareenginePrivateCloud#storage_thresholds}
        '''
        result = self._values.get("storage_thresholds")
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dcf218e7876dffaea41e514eea0ee6948c8dc9a00760d63073444da1a37388)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__952f919a02f40f8ce4f75f2522efca98739bfe2c413d741bae84a1c3fc5afdfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scaleInInput")
    def scale_in_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutInput")
    def scale_out_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleIn")
    def scale_in(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleIn"))

    @scale_in.setter
    def scale_in(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85774d575e59337c878a4c9fb3961cc9194e822b5a081349998681182ae98b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cdc92f5c135bde64b7b36aa8ac72fc49fced3d80398d72ca6efc7a6487981b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db72429117c8c026b466579a74c6b257473e16949924784eed29b36c93da2cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0877b57acc44c5e8127a53a1fcb52da6014c5f23f877c0a2b46caf5e4a4b522f)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e444a1865f764ec618de11acb35e6758f8d4d0365a017da9f8b462265fcb2b0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scaleInInput")
    def scale_in_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutInput")
    def scale_out_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleIn")
    def scale_in(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleIn"))

    @scale_in.setter
    def scale_in(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6021a92e11546e6a8fe7be2f18bc860ba9d64aaf1808095f0aaa91995f3eab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829726644e865122d8aab2f302ae9eadeaf9091e8fb0acfc28f88229729f2333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6172358596b4295c68e19b58c71af39d482311af28586c1be908dca3dd6e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64aae60108c227542f677d943ce72761968f7309c800bf4f37f0c12e6c95f75a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5a07548e6df3583957723cc46c3c32539cc01e34816e6f367364735714882b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc59b33375088d50f35d4404b9ec33d15915496fccce4e9231250658b36dd2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e426e4c11d85a5b10ede648a5b4d2b822fa7b93f2289878dd009b36db92dad8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82db595cd7f9be191cfc9be141912b2fabdaabddca70f0d038c822a7489de392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b434e8e09b2e591c8906143cde0cfc7fa4a2538353f3e76285290f8b093ff71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cefa5d34a739ed38c5fbfcd4ffecc99f9aa6f4bbd852b716270b8c8b97583859)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConsumedMemoryThresholds")
    def put_consumed_memory_thresholds(
        self,
        *,
        scale_in: jsii.Number,
        scale_out: jsii.Number,
    ) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        value = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(
            scale_in=scale_in, scale_out=scale_out
        )

        return typing.cast(None, jsii.invoke(self, "putConsumedMemoryThresholds", [value]))

    @jsii.member(jsii_name="putCpuThresholds")
    def put_cpu_thresholds(
        self,
        *,
        scale_in: jsii.Number,
        scale_out: jsii.Number,
    ) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        value = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(
            scale_in=scale_in, scale_out=scale_out
        )

        return typing.cast(None, jsii.invoke(self, "putCpuThresholds", [value]))

    @jsii.member(jsii_name="putStorageThresholds")
    def put_storage_thresholds(
        self,
        *,
        scale_in: jsii.Number,
        scale_out: jsii.Number,
    ) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        value = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(
            scale_in=scale_in, scale_out=scale_out
        )

        return typing.cast(None, jsii.invoke(self, "putStorageThresholds", [value]))

    @jsii.member(jsii_name="resetConsumedMemoryThresholds")
    def reset_consumed_memory_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumedMemoryThresholds", []))

    @jsii.member(jsii_name="resetCpuThresholds")
    def reset_cpu_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuThresholds", []))

    @jsii.member(jsii_name="resetStorageThresholds")
    def reset_storage_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageThresholds", []))

    @builtins.property
    @jsii.member(jsii_name="consumedMemoryThresholds")
    def consumed_memory_thresholds(
        self,
    ) -> GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference:
        return typing.cast(GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference, jsii.get(self, "consumedMemoryThresholds"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholds")
    def cpu_thresholds(
        self,
    ) -> GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference:
        return typing.cast(GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference, jsii.get(self, "cpuThresholds"))

    @builtins.property
    @jsii.member(jsii_name="storageThresholds")
    def storage_thresholds(
        self,
    ) -> "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference":
        return typing.cast("GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference", jsii.get(self, "storageThresholds"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyIdInput")
    def autoscale_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoscalePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumedMemoryThresholdsInput")
    def consumed_memory_thresholds_input(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "consumedMemoryThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholdsInput")
    def cpu_thresholds_input(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "cpuThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeIdInput")
    def node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutSizeInput")
    def scale_out_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageThresholdsInput")
    def storage_thresholds_input(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], jsii.get(self, "storageThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyId")
    def autoscale_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoscalePolicyId"))

    @autoscale_policy_id.setter
    def autoscale_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee9b81d53fb2ec94991b731908a5b3f447c7d785454bde65b552cd99e62c239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afa66ffb35a21a6288b2051e922ecaa4d9409a03414a7f5b77a234435df4139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOutSize")
    def scale_out_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOutSize"))

    @scale_out_size.setter
    def scale_out_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040cf80df205bdd5280a4a754a0ab9596f1cee910fdaeb4327c7ad300ac7b26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOutSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ff80a89059ee2a1041db96fa49f5b6aa4c37e05adc0f46b82bf54fd777ee4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145f032542fac82f2ef24d2e63533e346a6819717bd20b9f1b481b220c14d86d)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_in GoogleVmwareenginePrivateCloud#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#scale_out GoogleVmwareenginePrivateCloud#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9822458ec058af42ab37d94710683b4a4dcad1d4568b5025a7e50c467dbb5ada)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scaleInInput")
    def scale_in_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutInput")
    def scale_out_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleIn")
    def scale_in(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleIn"))

    @scale_in.setter
    def scale_in(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d9f94c6e76b8737ffbe4a85d9d46cc82743e07494ca3f656960e44f7bc5796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb4f7bde2dbee75a6ebc1b60cc3d83c09b9e561a84fb310e1db4f841b534d642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f4d00cafd1ea3bd81ced043855bea7b975d313e77aaf36b921cc5454ef27a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53ced6e7e4c38c8abac3675e826d3a93567d9e528c74a9af5a2c327f65abd392)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingPolicies")
    def put_autoscaling_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbf61360b0e9e9a8a8acf5cd5b41c41fcafa461b37b6e50128ccaa1f64bb030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutoscalingPolicies", [value]))

    @jsii.member(jsii_name="resetCoolDownPeriod")
    def reset_cool_down_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownPeriod", []))

    @jsii.member(jsii_name="resetMaxClusterNodeCount")
    def reset_max_cluster_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxClusterNodeCount", []))

    @jsii.member(jsii_name="resetMinClusterNodeCount")
    def reset_min_cluster_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinClusterNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicies")
    def autoscaling_policies(
        self,
    ) -> GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList:
        return typing.cast(GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList, jsii.get(self, "autoscalingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPoliciesInput")
    def autoscaling_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "autoscalingPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriodInput")
    def cool_down_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coolDownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClusterNodeCountInput")
    def max_cluster_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClusterNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minClusterNodeCountInput")
    def min_cluster_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minClusterNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriod")
    def cool_down_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coolDownPeriod"))

    @cool_down_period.setter
    def cool_down_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffb4e4c0e08ebf6996019c1f3ddca4feeda0dad906ce227df5a844cf0097fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxClusterNodeCount")
    def max_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClusterNodeCount"))

    @max_cluster_node_count.setter
    def max_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd73e9427208596f2866dc311800fb5dac4fcde93c702bb5ff29f4883e91142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minClusterNodeCount")
    def min_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minClusterNodeCount"))

    @min_cluster_node_count.setter
    def min_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874e479b380c5838be5b4875c4c1da7ede63345a12e3e19adba231027e05aa53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459b2df5bf8b1aa3988677f68d30c3043e2cfacab58648705d96ce1024266e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "node_count": "nodeCount",
        "node_type_id": "nodeTypeId",
        "custom_core_count": "customCoreCount",
    },
)
class GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs:
    def __init__(
        self,
        *,
        node_count: jsii.Number,
        node_type_id: builtins.str,
        custom_core_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_count: The number of nodes of this type in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_count GoogleVmwareenginePrivateCloud#node_count}
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_id GoogleVmwareenginePrivateCloud#node_type_id}.
        :param custom_core_count: Customized number of cores available to each node of the type. This number must always be one of 'nodeType.availableCustomCoreCounts'. If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used. This cannot be changed once the PrivateCloud is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#custom_core_count GoogleVmwareenginePrivateCloud#custom_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0300e7c0a678665cfd0aebef0705209edf46d9207a44b95dd7ddf37e8abf5c37)
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument custom_core_count", value=custom_core_count, expected_type=type_hints["custom_core_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_count": node_count,
            "node_type_id": node_type_id,
        }
        if custom_core_count is not None:
            self._values["custom_core_count"] = custom_core_count

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''The number of nodes of this type in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_count GoogleVmwareenginePrivateCloud#node_count}
        '''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#node_type_id GoogleVmwareenginePrivateCloud#node_type_id}.'''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_core_count(self) -> typing.Optional[jsii.Number]:
        '''Customized number of cores available to each node of the type.

        This number must always be one of 'nodeType.availableCustomCoreCounts'.
        If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used.
        This cannot be changed once the PrivateCloud is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#custom_core_count GoogleVmwareenginePrivateCloud#custom_core_count}
        '''
        result = self._values.get("custom_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae4c5406d23fe812378df8f095d432e86127b17327d91a83212c75d4fcd6e30f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7efe88ecc601d12dd2589bc4b698dcee3e363b1aabdea9a6bd0fc8329756d41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52cba1ce66e4da55544869556e159f0e1d6e183ab7117c6e20c4ac7ba1883bce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__171d80d508234ca536e27cd09e3b8812d14ba6e3e689a9b838faec74ccde82ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efdc002752a1db33a163a1e238259595ab76054a90e95af4e7fea5e20d3c87b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f39adcb360b4f0c7a1609fa21f7c5b42985c71296318c98d7a818c2dbb0d154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26383fd20b1581b43d8bb47f18c677387b6090daa9ccd7495a55d7c8db337401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCustomCoreCount")
    def reset_custom_core_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCoreCount", []))

    @builtins.property
    @jsii.member(jsii_name="customCoreCountInput")
    def custom_core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customCoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeIdInput")
    def node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customCoreCount")
    def custom_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customCoreCount"))

    @custom_core_count.setter
    def custom_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5f3e330bcba04cc9f3dc89e85ea6a5185f0e06ae66c7f170f767145e9ef703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635a9a0c7934efad777f78470b434980a6dc684335d5e922f9c11be6d09ee779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47d84d3cce947d11b4c574ab52b383ec27b1c214f64e90a0610417ba8fc00ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422175898176aef65e380c3faed00dae7b46d9325b6c8d27411a4ec4925532a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudManagementClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__448068074398fced790b91e0563a0aa48c5f2e86e67fa5ad97afc83f89146b4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingSettings")
    def put_autoscaling_settings(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#autoscaling_policies GoogleVmwareenginePrivateCloud#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#cool_down_period GoogleVmwareenginePrivateCloud#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#max_cluster_node_count GoogleVmwareenginePrivateCloud#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#min_cluster_node_count GoogleVmwareenginePrivateCloud#min_cluster_node_count}
        '''
        value = GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings(
            autoscaling_policies=autoscaling_policies,
            cool_down_period=cool_down_period,
            max_cluster_node_count=max_cluster_node_count,
            min_cluster_node_count=min_cluster_node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingSettings", [value]))

    @jsii.member(jsii_name="putNodeTypeConfigs")
    def put_node_type_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95151649bab7aa0a4a5e2b8df1f12df1491cd8833cd08f199e4ee049e72a490f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeTypeConfigs", [value]))

    @jsii.member(jsii_name="putStretchedClusterConfig")
    def put_stretched_cluster_config(
        self,
        *,
        preferred_location: typing.Optional[builtins.str] = None,
        secondary_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preferred_location: Zone that will remain operational when connection between the two zones is lost. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#preferred_location GoogleVmwareenginePrivateCloud#preferred_location}
        :param secondary_location: Additional zone for a higher level of availability and load balancing. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#secondary_location GoogleVmwareenginePrivateCloud#secondary_location}
        '''
        value = GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig(
            preferred_location=preferred_location,
            secondary_location=secondary_location,
        )

        return typing.cast(None, jsii.invoke(self, "putStretchedClusterConfig", [value]))

    @jsii.member(jsii_name="resetAutoscalingSettings")
    def reset_autoscaling_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingSettings", []))

    @jsii.member(jsii_name="resetNodeTypeConfigs")
    def reset_node_type_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypeConfigs", []))

    @jsii.member(jsii_name="resetStretchedClusterConfig")
    def reset_stretched_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStretchedClusterConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingSettings")
    def autoscaling_settings(
        self,
    ) -> GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference:
        return typing.cast(GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference, jsii.get(self, "autoscalingSettings"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigs")
    def node_type_configs(
        self,
    ) -> GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsList:
        return typing.cast(GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsList, jsii.get(self, "nodeTypeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="stretchedClusterConfig")
    def stretched_cluster_config(
        self,
    ) -> "GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference":
        return typing.cast("GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference", jsii.get(self, "stretchedClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingSettingsInput")
    def autoscaling_settings_input(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings], jsii.get(self, "autoscalingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigsInput")
    def node_type_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]], jsii.get(self, "nodeTypeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="stretchedClusterConfigInput")
    def stretched_cluster_config_input(
        self,
    ) -> typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig"]:
        return typing.cast(typing.Optional["GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig"], jsii.get(self, "stretchedClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fabc95fc8a3866e793a904d77cff798d0d248438aced739a1ddbfef0906a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementCluster]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudManagementCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c44981b1eb824091605d0c6b70494f0688b3dcb744a959e74e97e01d0bceda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "preferred_location": "preferredLocation",
        "secondary_location": "secondaryLocation",
    },
)
class GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig:
    def __init__(
        self,
        *,
        preferred_location: typing.Optional[builtins.str] = None,
        secondary_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preferred_location: Zone that will remain operational when connection between the two zones is lost. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#preferred_location GoogleVmwareenginePrivateCloud#preferred_location}
        :param secondary_location: Additional zone for a higher level of availability and load balancing. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#secondary_location GoogleVmwareenginePrivateCloud#secondary_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4043d55e193b1d729c4e9e2319d65bf043013ccdebd5736e43828d8413573bf1)
            check_type(argname="argument preferred_location", value=preferred_location, expected_type=type_hints["preferred_location"])
            check_type(argname="argument secondary_location", value=secondary_location, expected_type=type_hints["secondary_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preferred_location is not None:
            self._values["preferred_location"] = preferred_location
        if secondary_location is not None:
            self._values["secondary_location"] = secondary_location

    @builtins.property
    def preferred_location(self) -> typing.Optional[builtins.str]:
        '''Zone that will remain operational when connection between the two zones is lost.

        Specify the zone in the following format: projects/{project}/locations/{location}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#preferred_location GoogleVmwareenginePrivateCloud#preferred_location}
        '''
        result = self._values.get("preferred_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_location(self) -> typing.Optional[builtins.str]:
        '''Additional zone for a higher level of availability and load balancing. Specify the zone in the following format: projects/{project}/locations/{location}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#secondary_location GoogleVmwareenginePrivateCloud#secondary_location}
        '''
        result = self._values.get("secondary_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ba74d91bc9f07353b7e9f9f9991b36bde1089f2ccf7fea42ba7652a87f1d605)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPreferredLocation")
    def reset_preferred_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredLocation", []))

    @jsii.member(jsii_name="resetSecondaryLocation")
    def reset_secondary_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryLocation", []))

    @builtins.property
    @jsii.member(jsii_name="preferredLocationInput")
    def preferred_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryLocationInput")
    def secondary_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredLocation")
    def preferred_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredLocation"))

    @preferred_location.setter
    def preferred_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78729a182f7a4899e1cc9bd811a224c1e19a5fdf6ffb22b9532e44d58781f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryLocation")
    def secondary_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryLocation"))

    @secondary_location.setter
    def secondary_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77166c290ba33f0a67a69072d47d39d379b9e6e5917e26f67f5dc0df4a92ffd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03074f06f6ea24839b560150ad054d455cd8d6357349e2dc5349d5de65a805d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "management_cidr": "managementCidr",
        "vmware_engine_network": "vmwareEngineNetwork",
    },
)
class GoogleVmwareenginePrivateCloudNetworkConfig:
    def __init__(
        self,
        *,
        management_cidr: builtins.str,
        vmware_engine_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param management_cidr: Management CIDR used by VMware management appliances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#management_cidr GoogleVmwareenginePrivateCloud#management_cidr}
        :param vmware_engine_network: The relative resource name of the VMware Engine network attached to the private cloud. Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project} can either be a project number or a project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#vmware_engine_network GoogleVmwareenginePrivateCloud#vmware_engine_network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4fb001508bd40e0ec2f2fda9a6691c319e9c3c1adabf634e709ca3fd191739a)
            check_type(argname="argument management_cidr", value=management_cidr, expected_type=type_hints["management_cidr"])
            check_type(argname="argument vmware_engine_network", value=vmware_engine_network, expected_type=type_hints["vmware_engine_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "management_cidr": management_cidr,
        }
        if vmware_engine_network is not None:
            self._values["vmware_engine_network"] = vmware_engine_network

    @builtins.property
    def management_cidr(self) -> builtins.str:
        '''Management CIDR used by VMware management appliances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#management_cidr GoogleVmwareenginePrivateCloud#management_cidr}
        '''
        result = self._values.get("management_cidr")
        assert result is not None, "Required property 'management_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vmware_engine_network(self) -> typing.Optional[builtins.str]:
        '''The relative resource name of the VMware Engine network attached to the private cloud.

        Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId}
        where {project} can either be a project number or a project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#vmware_engine_network GoogleVmwareenginePrivateCloud#vmware_engine_network}
        '''
        result = self._values.get("vmware_engine_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf3af6a5950720cbc0dd70e80f95941afd80bdb6247133df1a08043525bb28a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVmwareEngineNetwork")
    def reset_vmware_engine_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmwareEngineNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="dnsServerIp")
    def dns_server_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsServerIp"))

    @builtins.property
    @jsii.member(jsii_name="managementIpAddressLayoutVersion")
    def management_ip_address_layout_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "managementIpAddressLayoutVersion"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetworkCanonical")
    def vmware_engine_network_canonical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmwareEngineNetworkCanonical"))

    @builtins.property
    @jsii.member(jsii_name="managementCidrInput")
    def management_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetworkInput")
    def vmware_engine_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmwareEngineNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="managementCidr")
    def management_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementCidr"))

    @management_cidr.setter
    def management_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0bf640e92a454bcd80a98be45a11642f2ebe141af318d29400ae5428d6391a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetwork")
    def vmware_engine_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmwareEngineNetwork"))

    @vmware_engine_network.setter
    def vmware_engine_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd34c419cdb261e28aae7352a07c5127f47c40bc30aaba817e55f57b0047069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmwareEngineNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareenginePrivateCloudNetworkConfig]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28482401484d31f27f66ea095549f131d657057d4ad8c72ca60432f9f71c6f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudNsx",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVmwareenginePrivateCloudNsx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudNsx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudNsxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudNsxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21d53b8f6d0f7d2ff446a968bbd6631d672ffe11831829789ab58ab581573f8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareenginePrivateCloudNsxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145044289888325922f6ed51a8e4430239e447b186764062d347590ae1269262)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareenginePrivateCloudNsxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8269c90a867126f0f7d41a0ccf0146bd5132140dc0ae88afd7a3ebb41667e9c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4f0381382598480b6275ba8e414200bf5bfa8ede18b55fd1955e933c52826f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43a842ef525fae368964fd422530593bf4012eb67453b751b3dd1aaf0f1e0ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudNsxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudNsxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3421330a2d796cf216d55612cb63f792362731b7b4e00468f7c15d8a24473b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIp"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleVmwareenginePrivateCloudNsx]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudNsx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudNsx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca1b0633dad6c0054608f590bd034c3e40228b35ead27ffa40680c5953b6dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVmwareenginePrivateCloudTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#create GoogleVmwareenginePrivateCloud#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#delete GoogleVmwareenginePrivateCloud#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#update GoogleVmwareenginePrivateCloud#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457980453ff982703f4d6d5c3ab877b63bbfb8451e9611ef4dc417937e16bd99)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#create GoogleVmwareenginePrivateCloud#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#delete GoogleVmwareenginePrivateCloud#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_private_cloud#update GoogleVmwareenginePrivateCloud#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a30416e8276427d739ed90d0b7f1aea31ea477187e26a595f95b6986df41968)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8590b3fad8108cb6621815f05aacc1fd0e0c8cb3a540e6a47a7515fb2247d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed692bc75c292fa47049e22cbe4cfacc59a2fa0080ac5b6d076012c1ff99104c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73825afe66fc611748ea9d8810820ed990cfdb5b3253dd3c15b39b9037b41671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f94db99731cf080eff81c34977f01afe0f62aae1690876b7b3db9a8872666b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudVcenter",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVmwareenginePrivateCloudVcenter:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareenginePrivateCloudVcenter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareenginePrivateCloudVcenterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudVcenterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00fe1fd58ee2156e2dbcd958d731a7d16d3455dd41cfea130b98b26f198c32cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareenginePrivateCloudVcenterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebfaaa16aef5fde82b59bfddbd56ac468264c8dc35a2207f0d5b7a50277544e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareenginePrivateCloudVcenterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ee3657c0ac3197824f1d5e85aa3b768969de737cea8e9261855ba0213a031c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a47a31ab5aa44b47e8b9c3645e6eb437e5d682fa7304a6d86d8e458cd3e01491)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8343497478e191db5b169506db7c05a8917a7c5659552685794682d76d338a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareenginePrivateCloudVcenterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareenginePrivateCloud.GoogleVmwareenginePrivateCloudVcenterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda99815049c5707234833a32e95cfdc38dba37d516568154a0bed2ac9c7daa6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIp"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleVmwareenginePrivateCloudVcenter]:
        return typing.cast(typing.Optional[GoogleVmwareenginePrivateCloudVcenter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareenginePrivateCloudVcenter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9327e0dde23675412d0a8a28e88587cee54d3e8aea50189d750508dfc74ad8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVmwareenginePrivateCloud",
    "GoogleVmwareenginePrivateCloudConfig",
    "GoogleVmwareenginePrivateCloudHcx",
    "GoogleVmwareenginePrivateCloudHcxList",
    "GoogleVmwareenginePrivateCloudHcxOutputReference",
    "GoogleVmwareenginePrivateCloudManagementCluster",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs",
    "GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsList",
    "GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterOutputReference",
    "GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig",
    "GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference",
    "GoogleVmwareenginePrivateCloudNetworkConfig",
    "GoogleVmwareenginePrivateCloudNetworkConfigOutputReference",
    "GoogleVmwareenginePrivateCloudNsx",
    "GoogleVmwareenginePrivateCloudNsxList",
    "GoogleVmwareenginePrivateCloudNsxOutputReference",
    "GoogleVmwareenginePrivateCloudTimeouts",
    "GoogleVmwareenginePrivateCloudTimeoutsOutputReference",
    "GoogleVmwareenginePrivateCloudVcenter",
    "GoogleVmwareenginePrivateCloudVcenterList",
    "GoogleVmwareenginePrivateCloudVcenterOutputReference",
]

publication.publish()

def _typecheckingstub__2287f49ce23cb9e9f7fd9e71ba0958498a7a3a038f9a562a2e2ab8c1f1dc1b91(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    management_cluster: typing.Union[GoogleVmwareenginePrivateCloudManagementCluster, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network_config: typing.Union[GoogleVmwareenginePrivateCloudNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    deletion_delay_hours: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__910220e86cd9a900908b6737633546cb90495f61e97451b5b1d22d912995c209(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937e524e72079a0eb41caa308d0f75c9d1e717096de9fc9ffdedf7bc0d9b794c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbd7d68e5c7a125688bfc70fd1da8441d21e2268810242b98f387872dd1c9f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a5a3d3761e2dd32dd8f35ee8eb4710363ea304f0f7b4ef5e3832676d6347f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308486ad451c55c9de138b8d8e4caa5b8edc1cfdcb1b5bf40fa0fb77153e994f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc590156adb7194209cd440fcdfbc115e8a677c2cad769df9eaca03349fa748(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46655afdb8710738741e2eed232ffd6a45d95e79f2f90845b8f48371cf5121ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb72ee018f368e73db8f086831f7dec093a56af202ae007d4e507c665c6fc5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252778e8d77f9b6452a3cc3ae3562b92cfd8ad8768668e214eb6ed9653f7201e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee04f524d445b6ab7bdee68ea828f764b44a923d807e33c72303595c1591d8db(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    management_cluster: typing.Union[GoogleVmwareenginePrivateCloudManagementCluster, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network_config: typing.Union[GoogleVmwareenginePrivateCloudNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    deletion_delay_hours: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9f4963ee8c8c8303ebc305db70bc319f560592b1dfd14eb3b9ea1225879b27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0793e598b9a4da069d35bec797ec093ded7cc43a599ce26d35ee5df5eb66339b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ff6819d693a95083fd25b31dcfbfb1ec2580709563b18cfac39cc5d848d813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631f81888e2b0a89922eb7831561c7d6fcbe6e1fad08ba5084ad477b6960a646(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b05c8fbdaff024324cf447bcfe3201f3c09a38a0a379c3a2a57f5a22e91bad9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414eea0a77380e0c4550f6f60d3ae011cfd3ffc2d40a2ef8cacc70fb099aa314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46545b1925e4fd790a8ab4a0980ff6b413b5cf0d98abdb58cbebcf4f87362b78(
    value: typing.Optional[GoogleVmwareenginePrivateCloudHcx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e429c4e7e31683f4a5b31ee9177b744c7256d97166f7ad87745b03b65b50b8(
    *,
    cluster_id: builtins.str,
    autoscaling_settings: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stretched_cluster_config: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8963e4446786394ff545264986547c697c6cfbe2034fb99b41bf62c5ab894d58(
    *,
    autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    cool_down_period: typing.Optional[builtins.str] = None,
    max_cluster_node_count: typing.Optional[jsii.Number] = None,
    min_cluster_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74cf810b094bf65720a0391e159748545b2b153cd8fff851fdff76c1e4e5460(
    *,
    autoscale_policy_id: builtins.str,
    node_type_id: builtins.str,
    scale_out_size: jsii.Number,
    consumed_memory_thresholds: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    cpu_thresholds: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_thresholds: typing.Optional[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dcf218e7876dffaea41e514eea0ee6948c8dc9a00760d63073444da1a37388(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952f919a02f40f8ce4f75f2522efca98739bfe2c413d741bae84a1c3fc5afdfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85774d575e59337c878a4c9fb3961cc9194e822b5a081349998681182ae98b77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cdc92f5c135bde64b7b36aa8ac72fc49fced3d80398d72ca6efc7a6487981b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db72429117c8c026b466579a74c6b257473e16949924784eed29b36c93da2cf2(
    value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0877b57acc44c5e8127a53a1fcb52da6014c5f23f877c0a2b46caf5e4a4b522f(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e444a1865f764ec618de11acb35e6758f8d4d0365a017da9f8b462265fcb2b0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6021a92e11546e6a8fe7be2f18bc860ba9d64aaf1808095f0aaa91995f3eab8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829726644e865122d8aab2f302ae9eadeaf9091e8fb0acfc28f88229729f2333(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6172358596b4295c68e19b58c71af39d482311af28586c1be908dca3dd6e0b(
    value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64aae60108c227542f677d943ce72761968f7309c800bf4f37f0c12e6c95f75a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5a07548e6df3583957723cc46c3c32539cc01e34816e6f367364735714882b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc59b33375088d50f35d4404b9ec33d15915496fccce4e9231250658b36dd2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e426e4c11d85a5b10ede648a5b4d2b822fa7b93f2289878dd009b36db92dad8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82db595cd7f9be191cfc9be141912b2fabdaabddca70f0d038c822a7489de392(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b434e8e09b2e591c8906143cde0cfc7fa4a2538353f3e76285290f8b093ff71e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefa5d34a739ed38c5fbfcd4ffecc99f9aa6f4bbd852b716270b8c8b97583859(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee9b81d53fb2ec94991b731908a5b3f447c7d785454bde65b552cd99e62c239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afa66ffb35a21a6288b2051e922ecaa4d9409a03414a7f5b77a234435df4139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040cf80df205bdd5280a4a754a0ab9596f1cee910fdaeb4327c7ad300ac7b26e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ff80a89059ee2a1041db96fa49f5b6aa4c37e05adc0f46b82bf54fd777ee4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145f032542fac82f2ef24d2e63533e346a6819717bd20b9f1b481b220c14d86d(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9822458ec058af42ab37d94710683b4a4dcad1d4568b5025a7e50c467dbb5ada(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d9f94c6e76b8737ffbe4a85d9d46cc82743e07494ca3f656960e44f7bc5796(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4f7bde2dbee75a6ebc1b60cc3d83c09b9e561a84fb310e1db4f841b534d642(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f4d00cafd1ea3bd81ced043855bea7b975d313e77aaf36b921cc5454ef27a0(
    value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ced6e7e4c38c8abac3675e826d3a93567d9e528c74a9af5a2c327f65abd392(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbf61360b0e9e9a8a8acf5cd5b41c41fcafa461b37b6e50128ccaa1f64bb030(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffb4e4c0e08ebf6996019c1f3ddca4feeda0dad906ce227df5a844cf0097fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd73e9427208596f2866dc311800fb5dac4fcde93c702bb5ff29f4883e91142(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874e479b380c5838be5b4875c4c1da7ede63345a12e3e19adba231027e05aa53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459b2df5bf8b1aa3988677f68d30c3043e2cfacab58648705d96ce1024266e19(
    value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterAutoscalingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0300e7c0a678665cfd0aebef0705209edf46d9207a44b95dd7ddf37e8abf5c37(
    *,
    node_count: jsii.Number,
    node_type_id: builtins.str,
    custom_core_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4c5406d23fe812378df8f095d432e86127b17327d91a83212c75d4fcd6e30f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7efe88ecc601d12dd2589bc4b698dcee3e363b1aabdea9a6bd0fc8329756d41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cba1ce66e4da55544869556e159f0e1d6e183ab7117c6e20c4ac7ba1883bce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171d80d508234ca536e27cd09e3b8812d14ba6e3e689a9b838faec74ccde82ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdc002752a1db33a163a1e238259595ab76054a90e95af4e7fea5e20d3c87b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f39adcb360b4f0c7a1609fa21f7c5b42985c71296318c98d7a818c2dbb0d154(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26383fd20b1581b43d8bb47f18c677387b6090daa9ccd7495a55d7c8db337401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5f3e330bcba04cc9f3dc89e85ea6a5185f0e06ae66c7f170f767145e9ef703(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635a9a0c7934efad777f78470b434980a6dc684335d5e922f9c11be6d09ee779(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47d84d3cce947d11b4c574ab52b383ec27b1c214f64e90a0610417ba8fc00ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422175898176aef65e380c3faed00dae7b46d9325b6c8d27411a4ec4925532a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448068074398fced790b91e0563a0aa48c5f2e86e67fa5ad97afc83f89146b4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95151649bab7aa0a4a5e2b8df1f12df1491cd8833cd08f199e4ee049e72a490f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareenginePrivateCloudManagementClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fabc95fc8a3866e793a904d77cff798d0d248438aced739a1ddbfef0906a21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c44981b1eb824091605d0c6b70494f0688b3dcb744a959e74e97e01d0bceda6(
    value: typing.Optional[GoogleVmwareenginePrivateCloudManagementCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4043d55e193b1d729c4e9e2319d65bf043013ccdebd5736e43828d8413573bf1(
    *,
    preferred_location: typing.Optional[builtins.str] = None,
    secondary_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba74d91bc9f07353b7e9f9f9991b36bde1089f2ccf7fea42ba7652a87f1d605(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78729a182f7a4899e1cc9bd811a224c1e19a5fdf6ffb22b9532e44d58781f30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77166c290ba33f0a67a69072d47d39d379b9e6e5917e26f67f5dc0df4a92ffd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03074f06f6ea24839b560150ad054d455cd8d6357349e2dc5349d5de65a805d8(
    value: typing.Optional[GoogleVmwareenginePrivateCloudManagementClusterStretchedClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fb001508bd40e0ec2f2fda9a6691c319e9c3c1adabf634e709ca3fd191739a(
    *,
    management_cidr: builtins.str,
    vmware_engine_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf3af6a5950720cbc0dd70e80f95941afd80bdb6247133df1a08043525bb28a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0bf640e92a454bcd80a98be45a11642f2ebe141af318d29400ae5428d6391a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd34c419cdb261e28aae7352a07c5127f47c40bc30aaba817e55f57b0047069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28482401484d31f27f66ea095549f131d657057d4ad8c72ca60432f9f71c6f6f(
    value: typing.Optional[GoogleVmwareenginePrivateCloudNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d53b8f6d0f7d2ff446a968bbd6631d672ffe11831829789ab58ab581573f8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145044289888325922f6ed51a8e4430239e447b186764062d347590ae1269262(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8269c90a867126f0f7d41a0ccf0146bd5132140dc0ae88afd7a3ebb41667e9c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4f0381382598480b6275ba8e414200bf5bfa8ede18b55fd1955e933c52826f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a842ef525fae368964fd422530593bf4012eb67453b751b3dd1aaf0f1e0ae0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3421330a2d796cf216d55612cb63f792362731b7b4e00468f7c15d8a24473b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca1b0633dad6c0054608f590bd034c3e40228b35ead27ffa40680c5953b6dd5(
    value: typing.Optional[GoogleVmwareenginePrivateCloudNsx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457980453ff982703f4d6d5c3ab877b63bbfb8451e9611ef4dc417937e16bd99(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a30416e8276427d739ed90d0b7f1aea31ea477187e26a595f95b6986df41968(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8590b3fad8108cb6621815f05aacc1fd0e0c8cb3a540e6a47a7515fb2247d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed692bc75c292fa47049e22cbe4cfacc59a2fa0080ac5b6d076012c1ff99104c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73825afe66fc611748ea9d8810820ed990cfdb5b3253dd3c15b39b9037b41671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f94db99731cf080eff81c34977f01afe0f62aae1690876b7b3db9a8872666b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareenginePrivateCloudTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fe1fd58ee2156e2dbcd958d731a7d16d3455dd41cfea130b98b26f198c32cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebfaaa16aef5fde82b59bfddbd56ac468264c8dc35a2207f0d5b7a50277544e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ee3657c0ac3197824f1d5e85aa3b768969de737cea8e9261855ba0213a031c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47a31ab5aa44b47e8b9c3645e6eb437e5d682fa7304a6d86d8e458cd3e01491(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8343497478e191db5b169506db7c05a8917a7c5659552685794682d76d338a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda99815049c5707234833a32e95cfdc38dba37d516568154a0bed2ac9c7daa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9327e0dde23675412d0a8a28e88587cee54d3e8aea50189d750508dfc74ad8eb(
    value: typing.Optional[GoogleVmwareenginePrivateCloudVcenter],
) -> None:
    """Type checking stubs"""
    pass
