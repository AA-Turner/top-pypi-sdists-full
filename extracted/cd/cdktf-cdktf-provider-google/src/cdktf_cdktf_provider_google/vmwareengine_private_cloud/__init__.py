r'''
# `google_vmwareengine_private_cloud`

Refer to the Terraform Registry for docs: [`google_vmwareengine_private_cloud`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud).
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


class VmwareenginePrivateCloud(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloud",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud google_vmwareengine_private_cloud}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        management_cluster: typing.Union["VmwareenginePrivateCloudManagementCluster", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network_config: typing.Union["VmwareenginePrivateCloudNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        deletion_delay_hours: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["VmwareenginePrivateCloudTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud google_vmwareengine_private_cloud} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location where the PrivateCloud should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#location VmwareenginePrivateCloud#location}
        :param management_cluster: management_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#management_cluster VmwareenginePrivateCloud#management_cluster}
        :param name: The ID of the PrivateCloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#name VmwareenginePrivateCloud#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#network_config VmwareenginePrivateCloud#network_config}
        :param deletion_delay_hours: The number of hours to delay this request. You can set this value to an hour between 0 to 8, where setting it to 0 starts the deletion request immediately. If no value is set, a default value is set at the API Level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#deletion_delay_hours VmwareenginePrivateCloud#deletion_delay_hours}
        :param description: User-provided description for this private cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#description VmwareenginePrivateCloud#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#id VmwareenginePrivateCloud#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#project VmwareenginePrivateCloud#project}.
        :param send_deletion_delay_hours_if_zero: While set true, deletion_delay_hours value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the deletion_delay_hours field. It can be used both alone and together with deletion_delay_hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#send_deletion_delay_hours_if_zero VmwareenginePrivateCloud#send_deletion_delay_hours_if_zero}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#timeouts VmwareenginePrivateCloud#timeouts}
        :param type: Initial type of the private cloud. Possible values: ["STANDARD", "TIME_LIMITED", "STRETCHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#type VmwareenginePrivateCloud#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87c842f1357aba6a1cc4d2022c79953386bc32bae1bd4a3a03e5262de1fc9c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmwareenginePrivateCloudConfig(
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
        '''Generates CDKTF code for importing a VmwareenginePrivateCloud resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmwareenginePrivateCloud to import.
        :param import_from_id: The id of the existing VmwareenginePrivateCloud that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmwareenginePrivateCloud to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051bf214c4f2cb92e218b944aaf9d7dfd2aecd020edb6bef3838690b478843bf)
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
        autoscaling_settings: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterAutoscalingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareenginePrivateCloudManagementClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stretched_cluster_config: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterStretchedClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: The user-provided identifier of the new Cluster. The identifier must meet the following requirements: - Only contains 1-63 alphanumeric characters and hyphens - Begins with an alphabetical character - Ends with a non-hyphen character - Not formatted as a UUID - Complies with RFC 1034 (https://datatracker.ietf.org/doc/html/rfc1034) (section 3.5) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cluster_id VmwareenginePrivateCloud#cluster_id}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscaling_settings VmwareenginePrivateCloud#autoscaling_settings}
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_configs VmwareenginePrivateCloud#node_type_configs}
        :param stretched_cluster_config: stretched_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#stretched_cluster_config VmwareenginePrivateCloud#stretched_cluster_config}
        '''
        value = VmwareenginePrivateCloudManagementCluster(
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
        :param management_cidr: Management CIDR used by VMware management appliances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#management_cidr VmwareenginePrivateCloud#management_cidr}
        :param vmware_engine_network: The relative resource name of the VMware Engine network attached to the private cloud. Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project} can either be a project number or a project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#vmware_engine_network VmwareenginePrivateCloud#vmware_engine_network}
        '''
        value = VmwareenginePrivateCloudNetworkConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#create VmwareenginePrivateCloud#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#delete VmwareenginePrivateCloud#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#update VmwareenginePrivateCloud#update}.
        '''
        value = VmwareenginePrivateCloudTimeouts(
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
    def hcx(self) -> "VmwareenginePrivateCloudHcxList":
        return typing.cast("VmwareenginePrivateCloudHcxList", jsii.get(self, "hcx"))

    @builtins.property
    @jsii.member(jsii_name="managementCluster")
    def management_cluster(
        self,
    ) -> "VmwareenginePrivateCloudManagementClusterOutputReference":
        return typing.cast("VmwareenginePrivateCloudManagementClusterOutputReference", jsii.get(self, "managementCluster"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "VmwareenginePrivateCloudNetworkConfigOutputReference":
        return typing.cast("VmwareenginePrivateCloudNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="nsx")
    def nsx(self) -> "VmwareenginePrivateCloudNsxList":
        return typing.cast("VmwareenginePrivateCloudNsxList", jsii.get(self, "nsx"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VmwareenginePrivateCloudTimeoutsOutputReference":
        return typing.cast("VmwareenginePrivateCloudTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="vcenter")
    def vcenter(self) -> "VmwareenginePrivateCloudVcenterList":
        return typing.cast("VmwareenginePrivateCloudVcenterList", jsii.get(self, "vcenter"))

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
    ) -> typing.Optional["VmwareenginePrivateCloudManagementCluster"]:
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementCluster"], jsii.get(self, "managementClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudNetworkConfig"]:
        return typing.cast(typing.Optional["VmwareenginePrivateCloudNetworkConfig"], jsii.get(self, "networkConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareenginePrivateCloudTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareenginePrivateCloudTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a30e8fcd7c7a5df5fdd39f0f8d1138b4fff907711f1544a1d4ca3623ce56a42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionDelayHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b00297370c38ec9083078104626de9b073c0eeeaab892e2446498b6aae51713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b2f51358b925646a0e51efc2a725fd296d637bf183eaa9dee7e7436b16e6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250fc8e8a6d74323fe284ed664a6fcd35ed667d257064cf4bb93b7fd096bbd92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b9f9cafe21c114e79cc8424c0f63de14d93ce97b9635a4735e19ba17f722e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eef2dde7a4d0f513cf0b7cd49f2dec55f36c93be31cfbca8e92f536dfefbbff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__194f142d68c2ab12e156be3d84147c746aadb37e876f8e85fdff43218113436c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendDeletionDelayHoursIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23e777583ef780ecad12831bc69cbbba01636727404688c7dcbb0e53e201b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudConfig",
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
class VmwareenginePrivateCloudConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        management_cluster: typing.Union["VmwareenginePrivateCloudManagementCluster", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network_config: typing.Union["VmwareenginePrivateCloudNetworkConfig", typing.Dict[builtins.str, typing.Any]],
        deletion_delay_hours: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["VmwareenginePrivateCloudTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param location: The location where the PrivateCloud should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#location VmwareenginePrivateCloud#location}
        :param management_cluster: management_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#management_cluster VmwareenginePrivateCloud#management_cluster}
        :param name: The ID of the PrivateCloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#name VmwareenginePrivateCloud#name}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#network_config VmwareenginePrivateCloud#network_config}
        :param deletion_delay_hours: The number of hours to delay this request. You can set this value to an hour between 0 to 8, where setting it to 0 starts the deletion request immediately. If no value is set, a default value is set at the API Level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#deletion_delay_hours VmwareenginePrivateCloud#deletion_delay_hours}
        :param description: User-provided description for this private cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#description VmwareenginePrivateCloud#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#id VmwareenginePrivateCloud#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#project VmwareenginePrivateCloud#project}.
        :param send_deletion_delay_hours_if_zero: While set true, deletion_delay_hours value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the deletion_delay_hours field. It can be used both alone and together with deletion_delay_hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#send_deletion_delay_hours_if_zero VmwareenginePrivateCloud#send_deletion_delay_hours_if_zero}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#timeouts VmwareenginePrivateCloud#timeouts}
        :param type: Initial type of the private cloud. Possible values: ["STANDARD", "TIME_LIMITED", "STRETCHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#type VmwareenginePrivateCloud#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(management_cluster, dict):
            management_cluster = VmwareenginePrivateCloudManagementCluster(**management_cluster)
        if isinstance(network_config, dict):
            network_config = VmwareenginePrivateCloudNetworkConfig(**network_config)
        if isinstance(timeouts, dict):
            timeouts = VmwareenginePrivateCloudTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630034937a2004a630023ac93ac12a73c875c8bae38630868b46a16a2225a69e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#location VmwareenginePrivateCloud#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def management_cluster(self) -> "VmwareenginePrivateCloudManagementCluster":
        '''management_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#management_cluster VmwareenginePrivateCloud#management_cluster}
        '''
        result = self._values.get("management_cluster")
        assert result is not None, "Required property 'management_cluster' is missing"
        return typing.cast("VmwareenginePrivateCloudManagementCluster", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The ID of the PrivateCloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#name VmwareenginePrivateCloud#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_config(self) -> "VmwareenginePrivateCloudNetworkConfig":
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#network_config VmwareenginePrivateCloud#network_config}
        '''
        result = self._values.get("network_config")
        assert result is not None, "Required property 'network_config' is missing"
        return typing.cast("VmwareenginePrivateCloudNetworkConfig", result)

    @builtins.property
    def deletion_delay_hours(self) -> typing.Optional[jsii.Number]:
        '''The number of hours to delay this request.

        You can set this value to an hour between 0 to 8, where setting it to 0 starts the deletion request immediately. If no value is set, a default value is set at the API Level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#deletion_delay_hours VmwareenginePrivateCloud#deletion_delay_hours}
        '''
        result = self._values.get("deletion_delay_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description for this private cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#description VmwareenginePrivateCloud#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#id VmwareenginePrivateCloud#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#project VmwareenginePrivateCloud#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_deletion_delay_hours_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, deletion_delay_hours value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the deletion_delay_hours field. It can be used both alone and together with deletion_delay_hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#send_deletion_delay_hours_if_zero VmwareenginePrivateCloud#send_deletion_delay_hours_if_zero}
        '''
        result = self._values.get("send_deletion_delay_hours_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VmwareenginePrivateCloudTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#timeouts VmwareenginePrivateCloud#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VmwareenginePrivateCloudTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Initial type of the private cloud. Possible values: ["STANDARD", "TIME_LIMITED", "STRETCHED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#type VmwareenginePrivateCloud#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudHcx",
    jsii_struct_bases=[],
    name_mapping={},
)
class VmwareenginePrivateCloudHcx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudHcx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudHcxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudHcxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd0ece81bad82146eeaea5d30ef06acca4abdf6d0d45ee6474df68cf4870b3e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmwareenginePrivateCloudHcxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07032897b9f7b642c2f7fbb5137dbc6847da42a5d2ea69201c57b360bd83b88f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareenginePrivateCloudHcxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156c4160afb2d7c0e49bffdbc5504a0f3a52c81c5179ecbf5347d9d9e1e17de6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28299492561dabd14d3c454e9fe0d68624ce322e2ba6efe88761c335eb27e25f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1687e16c6f21df25ce231cb71d8cbd9346b0395350af6890684b7e6af0cc8b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudHcxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudHcxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a69453166b37bb9f655dcf131adcb4a5a931f75005a156e2c3cb3e8b46faae1a)
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
    def internal_value(self) -> typing.Optional[VmwareenginePrivateCloudHcx]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudHcx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudHcx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94297a7ac86e476602a40ba865daaf15e85f34ebb76d60fc6c42fd9e14e23f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementCluster",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "autoscaling_settings": "autoscalingSettings",
        "node_type_configs": "nodeTypeConfigs",
        "stretched_cluster_config": "stretchedClusterConfig",
    },
)
class VmwareenginePrivateCloudManagementCluster:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        autoscaling_settings: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterAutoscalingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareenginePrivateCloudManagementClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stretched_cluster_config: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterStretchedClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: The user-provided identifier of the new Cluster. The identifier must meet the following requirements: - Only contains 1-63 alphanumeric characters and hyphens - Begins with an alphabetical character - Ends with a non-hyphen character - Not formatted as a UUID - Complies with RFC 1034 (https://datatracker.ietf.org/doc/html/rfc1034) (section 3.5) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cluster_id VmwareenginePrivateCloud#cluster_id}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscaling_settings VmwareenginePrivateCloud#autoscaling_settings}
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_configs VmwareenginePrivateCloud#node_type_configs}
        :param stretched_cluster_config: stretched_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#stretched_cluster_config VmwareenginePrivateCloud#stretched_cluster_config}
        '''
        if isinstance(autoscaling_settings, dict):
            autoscaling_settings = VmwareenginePrivateCloudManagementClusterAutoscalingSettings(**autoscaling_settings)
        if isinstance(stretched_cluster_config, dict):
            stretched_cluster_config = VmwareenginePrivateCloudManagementClusterStretchedClusterConfig(**stretched_cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231d620248693d185d81356e009e9a8a16607fcdaa3289574a25ea43d0c04e43)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cluster_id VmwareenginePrivateCloud#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_settings(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettings"]:
        '''autoscaling_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscaling_settings VmwareenginePrivateCloud#autoscaling_settings}
        '''
        result = self._values.get("autoscaling_settings")
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettings"], result)

    @builtins.property
    def node_type_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareenginePrivateCloudManagementClusterNodeTypeConfigs"]]]:
        '''node_type_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_configs VmwareenginePrivateCloud#node_type_configs}
        '''
        result = self._values.get("node_type_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareenginePrivateCloudManagementClusterNodeTypeConfigs"]]], result)

    @builtins.property
    def stretched_cluster_config(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterStretchedClusterConfig"]:
        '''stretched_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#stretched_cluster_config VmwareenginePrivateCloud#stretched_cluster_config}
        '''
        result = self._values.get("stretched_cluster_config")
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterStretchedClusterConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_policies": "autoscalingPolicies",
        "cool_down_period": "coolDownPeriod",
        "max_cluster_node_count": "maxClusterNodeCount",
        "min_cluster_node_count": "minClusterNodeCount",
    },
)
class VmwareenginePrivateCloudManagementClusterAutoscalingSettings:
    def __init__(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies", typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscaling_policies VmwareenginePrivateCloud#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cool_down_period VmwareenginePrivateCloud#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#max_cluster_node_count VmwareenginePrivateCloud#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#min_cluster_node_count VmwareenginePrivateCloud#min_cluster_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05776c5f308a98bce367a31d88ef817d98e620b33028117195567ed409a1a0c0)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies"]]:
        '''autoscaling_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscaling_policies VmwareenginePrivateCloud#autoscaling_policies}
        '''
        result = self._values.get("autoscaling_policies")
        assert result is not None, "Required property 'autoscaling_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies"]], result)

    @builtins.property
    def cool_down_period(self) -> typing.Optional[builtins.str]:
        '''The minimum duration between consecutive autoscale operations.

        It starts once addition or removal of nodes is fully completed.
        Minimum cool down period is 30m.
        Cool down period must be in whole minutes (for example, 30m, 31m, 50m).
        Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cool_down_period VmwareenginePrivateCloud#cool_down_period}
        '''
        result = self._values.get("cool_down_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#max_cluster_node_count VmwareenginePrivateCloud#max_cluster_node_count}
        '''
        result = self._values.get("max_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#min_cluster_node_count VmwareenginePrivateCloud#min_cluster_node_count}
        '''
        result = self._values.get("min_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterAutoscalingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies",
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
class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies:
    def __init__(
        self,
        *,
        autoscale_policy_id: builtins.str,
        node_type_id: builtins.str,
        scale_out_size: jsii.Number,
        consumed_memory_thresholds: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        cpu_thresholds: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_thresholds: typing.Optional[typing.Union["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscale_policy_id VmwareenginePrivateCloud#autoscale_policy_id}.
        :param node_type_id: The canonical identifier of the node type to add or remove. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_id VmwareenginePrivateCloud#node_type_id}
        :param scale_out_size: Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out_size VmwareenginePrivateCloud#scale_out_size}
        :param consumed_memory_thresholds: consumed_memory_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#consumed_memory_thresholds VmwareenginePrivateCloud#consumed_memory_thresholds}
        :param cpu_thresholds: cpu_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cpu_thresholds VmwareenginePrivateCloud#cpu_thresholds}
        :param storage_thresholds: storage_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#storage_thresholds VmwareenginePrivateCloud#storage_thresholds}
        '''
        if isinstance(consumed_memory_thresholds, dict):
            consumed_memory_thresholds = VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(**consumed_memory_thresholds)
        if isinstance(cpu_thresholds, dict):
            cpu_thresholds = VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(**cpu_thresholds)
        if isinstance(storage_thresholds, dict):
            storage_thresholds = VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(**storage_thresholds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62f45021ea28fe13293984c2d97dac6d8df85d4c4d2ad5c9dd336b533f3ded4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscale_policy_id VmwareenginePrivateCloud#autoscale_policy_id}.'''
        result = self._values.get("autoscale_policy_id")
        assert result is not None, "Required property 'autoscale_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''The canonical identifier of the node type to add or remove.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_id VmwareenginePrivateCloud#node_type_id}
        '''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_out_size(self) -> jsii.Number:
        '''Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out_size VmwareenginePrivateCloud#scale_out_size}
        '''
        result = self._values.get("scale_out_size")
        assert result is not None, "Required property 'scale_out_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def consumed_memory_thresholds(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"]:
        '''consumed_memory_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#consumed_memory_thresholds VmwareenginePrivateCloud#consumed_memory_thresholds}
        '''
        result = self._values.get("consumed_memory_thresholds")
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"], result)

    @builtins.property
    def cpu_thresholds(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"]:
        '''cpu_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cpu_thresholds VmwareenginePrivateCloud#cpu_thresholds}
        '''
        result = self._values.get("cpu_thresholds")
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"], result)

    @builtins.property
    def storage_thresholds(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        '''storage_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#storage_thresholds VmwareenginePrivateCloud#storage_thresholds}
        '''
        result = self._values.get("storage_thresholds")
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ceddf00d9a247106d433fee6eea32cbe3cc5295cd5d303978ee6d0d8f355cc)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9989ee97fee76de65e7590c67200164fbabfc143e0f744941b2da629b6407541)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e8629ec8b4e3ff6e0d67f703ffe81b8cd8103db040de8efc607edd350b74920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e233c3378a7633c068181f1bb8e177e7dd325fee646add9a6eb26b0725ab0b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8891e7d63c56f085e963b6365139b68eacf499c694744ebc929fe9b6961e2745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5017df091509d9da5ae89dc6e2aa7488205ca21a270f4153ca324275fe3f7f2)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e75f2d67513f9dd72428be4f3b86f4cd1ad7b1c75f34fdc2c4ec0d5d14cdd40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b66d0c27890ea9f0662dd44d444991eb649ad5d38b64e23a054d5de244053a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa61e41c935a8b603155ae76f238937af603700240fde8701e10657daff9c8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a6ecfe5d23421a7d6c6e101f9b5d6818a2a76c602fff9868fcba5655271e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8056e5f1baaa2a87f339a263d481ca60a03a91ef47cc077524191fd14381fdf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3648c6e6d017cf37dcd8e6ee4b1ab7d6bb55ab9bd159d33ca58282723d0572)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf231e582a5b783517032720dbab063a10633f9430aac8612627dc16d4dc213d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4337c832d676e4ceb436cd06fdb65d82fd677e0ea16f62614909f691b8b1a467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98f2a03f155867c1fca44e72d1c193e71ed7c1c6f7c335372c0ec0bc478fc832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10d8a0f4edd51f599545987ff3a509ecb3f830da187cb1437308b2211a4db49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61a4cd8f4a566d9a45a3c73ab4c27350e2a676d9aa753a4327979f9bdfc2ed04)
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
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        value = VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(
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
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        value = VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(
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
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        value = VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(
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
    ) -> VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference:
        return typing.cast(VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference, jsii.get(self, "consumedMemoryThresholds"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholds")
    def cpu_thresholds(
        self,
    ) -> VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference:
        return typing.cast(VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference, jsii.get(self, "cpuThresholds"))

    @builtins.property
    @jsii.member(jsii_name="storageThresholds")
    def storage_thresholds(
        self,
    ) -> "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference":
        return typing.cast("VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference", jsii.get(self, "storageThresholds"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyIdInput")
    def autoscale_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoscalePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumedMemoryThresholdsInput")
    def consumed_memory_thresholds_input(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "consumedMemoryThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholdsInput")
    def cpu_thresholds_input(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "cpuThresholdsInput"))

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
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], jsii.get(self, "storageThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyId")
    def autoscale_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoscalePolicyId"))

    @autoscale_policy_id.setter
    def autoscale_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbeddb1d991f7e23c11b53fb5213fff6d026f47530421aeddf29ce2773792fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c9eebf7a3a78510093aed7eb9f67d072c008cab0bc680ee0af4d7e7846a94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOutSize")
    def scale_out_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOutSize"))

    @scale_out_size.setter
    def scale_out_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d6158583bb21b950eccf84291bc4561743fbdb7e3d92925cd8622c02cc8bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOutSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3253463dfb9f450da2df0b2e4798b453c9a6cdc1fa270cf66a9a6b802d79157e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74474be72d5e0049ba9b860a1860ddf46f3118ebf28cd17ab42dd61b6a55faa1)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_in VmwareenginePrivateCloud#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#scale_out VmwareenginePrivateCloud#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__551d3494e3f8dc76718b27b7a1cc447081f687f48abbf871075ef15ab5260f27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65bf88399827b71000b4e3ed4cdcd3863c1a1862074bd62395f0e138547b7e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc1fec88b34c6a71249b88fc9c0c0951e512109d5e00d0bb6e3c9302d29ff6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068db9e49a8786f0f49e8edbec166b5e5246094d9e0565ec51ca202407fccb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf343d5ec582e6ec351bdff361d8de93b93a2743fc5c44bacfa9925f48687af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingPolicies")
    def put_autoscaling_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9606f9c0656e31ac2b0c7c1eeb5036bb34ab0d26353e5f96800e55f6f6c8c7)
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
    ) -> VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList:
        return typing.cast(VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList, jsii.get(self, "autoscalingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPoliciesInput")
    def autoscaling_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "autoscalingPoliciesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d463bb5d514763b5917a0ec24cf2281efaac0760100b54b83b32108b607f7ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxClusterNodeCount")
    def max_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClusterNodeCount"))

    @max_cluster_node_count.setter
    def max_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a05ead14844c97fe69189396771b07e7af7580ad40095d9c8c7da772c07b008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minClusterNodeCount")
    def min_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minClusterNodeCount"))

    @min_cluster_node_count.setter
    def min_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5f399cae66506a6f1ecdac102459f72edba4ca2269c8076595bb74052624a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettings]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb4d85e47cc5a23f81e78c0bda90a0186776b994977f7bbb6f8352cad2b0639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterNodeTypeConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "node_count": "nodeCount",
        "node_type_id": "nodeTypeId",
        "custom_core_count": "customCoreCount",
    },
)
class VmwareenginePrivateCloudManagementClusterNodeTypeConfigs:
    def __init__(
        self,
        *,
        node_count: jsii.Number,
        node_type_id: builtins.str,
        custom_core_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_count: The number of nodes of this type in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_count VmwareenginePrivateCloud#node_count}
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_id VmwareenginePrivateCloud#node_type_id}.
        :param custom_core_count: Customized number of cores available to each node of the type. This number must always be one of 'nodeType.availableCustomCoreCounts'. If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used. This cannot be changed once the PrivateCloud is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#custom_core_count VmwareenginePrivateCloud#custom_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04211b79009cab9a63d805ea0551e36aace9755810958b4b6b00f77626b3f2e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_count VmwareenginePrivateCloud#node_count}
        '''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#node_type_id VmwareenginePrivateCloud#node_type_id}.'''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_core_count(self) -> typing.Optional[jsii.Number]:
        '''Customized number of cores available to each node of the type.

        This number must always be one of 'nodeType.availableCustomCoreCounts'.
        If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used.
        This cannot be changed once the PrivateCloud is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#custom_core_count VmwareenginePrivateCloud#custom_core_count}
        '''
        result = self._values.get("custom_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterNodeTypeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudManagementClusterNodeTypeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterNodeTypeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d649849c2b7b9fd43f7dfb084c54c15968d47a85c8d65178a975217bfdd1f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9073b7df5e38586d85a7a6964e24a962647f5dcb33c91e5cfa40d2304d448a3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405eb33700b1d526f20c33fa9ff0663d4716313f1eb4f1516bd6afc4d2245cbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49fa9cdb6fe466aa28d4e382adeddddefad888f8d6224fc89d9d8a3ce069501d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45ddedc494708385ab8f5089bb394f7f390c448ae7f3234c36686898d2195974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b03040eb52972dea2535d117977c00199cc5e6136875048cebcb5887114a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12ebe91f335602ff7c7723ec7c0e68e94ec67711ac39cce165cd9416c03fcc87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96d7407922d697bf84a20b46733a1424894ae182cb60fe18421373fcf42d01b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ba956ca4e723a108b42eeb4c1e85044fa39b21dc2bcf527ad49b7357d8232c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9710e87117afe61a5b5388b3bba4397d67ccda4967c45bfec7ca72704ea1c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08db413d8e4f07e32529317d7c402bbe967f27ae8605640d5e952b45ea0364d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudManagementClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85897bb69f96e698b2b982d5fb00f5c01965589a9b6e2d538df353bf9dc6bbb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingSettings")
    def put_autoscaling_settings(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#autoscaling_policies VmwareenginePrivateCloud#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#cool_down_period VmwareenginePrivateCloud#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#max_cluster_node_count VmwareenginePrivateCloud#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#min_cluster_node_count VmwareenginePrivateCloud#min_cluster_node_count}
        '''
        value = VmwareenginePrivateCloudManagementClusterAutoscalingSettings(
            autoscaling_policies=autoscaling_policies,
            cool_down_period=cool_down_period,
            max_cluster_node_count=max_cluster_node_count,
            min_cluster_node_count=min_cluster_node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingSettings", [value]))

    @jsii.member(jsii_name="putNodeTypeConfigs")
    def put_node_type_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c06c97c4da03f42cf6755329abea78d37d9e34c0a26e5600daa3630d7e5e919)
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
        :param preferred_location: Zone that will remain operational when connection between the two zones is lost. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#preferred_location VmwareenginePrivateCloud#preferred_location}
        :param secondary_location: Additional zone for a higher level of availability and load balancing. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#secondary_location VmwareenginePrivateCloud#secondary_location}
        '''
        value = VmwareenginePrivateCloudManagementClusterStretchedClusterConfig(
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
    ) -> VmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference:
        return typing.cast(VmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference, jsii.get(self, "autoscalingSettings"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigs")
    def node_type_configs(
        self,
    ) -> VmwareenginePrivateCloudManagementClusterNodeTypeConfigsList:
        return typing.cast(VmwareenginePrivateCloudManagementClusterNodeTypeConfigsList, jsii.get(self, "nodeTypeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="stretchedClusterConfig")
    def stretched_cluster_config(
        self,
    ) -> "VmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference":
        return typing.cast("VmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference", jsii.get(self, "stretchedClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingSettingsInput")
    def autoscaling_settings_input(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettings]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettings], jsii.get(self, "autoscalingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigsInput")
    def node_type_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]], jsii.get(self, "nodeTypeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="stretchedClusterConfigInput")
    def stretched_cluster_config_input(
        self,
    ) -> typing.Optional["VmwareenginePrivateCloudManagementClusterStretchedClusterConfig"]:
        return typing.cast(typing.Optional["VmwareenginePrivateCloudManagementClusterStretchedClusterConfig"], jsii.get(self, "stretchedClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e185b19d12992d59a7581aaac23f90a80d8ed44842260a8850cc1ad729eab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementCluster]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudManagementCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea630273e53947a8aca0c355b30f4589a2cbe1b6fb4dad33d6041ef6712778f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterStretchedClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "preferred_location": "preferredLocation",
        "secondary_location": "secondaryLocation",
    },
)
class VmwareenginePrivateCloudManagementClusterStretchedClusterConfig:
    def __init__(
        self,
        *,
        preferred_location: typing.Optional[builtins.str] = None,
        secondary_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preferred_location: Zone that will remain operational when connection between the two zones is lost. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#preferred_location VmwareenginePrivateCloud#preferred_location}
        :param secondary_location: Additional zone for a higher level of availability and load balancing. Specify the zone in the following format: projects/{project}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#secondary_location VmwareenginePrivateCloud#secondary_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ce80536f3aba63944561791cbd71f3db4a5293571dd780c2adc03dbebd8e0b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#preferred_location VmwareenginePrivateCloud#preferred_location}
        '''
        result = self._values.get("preferred_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_location(self) -> typing.Optional[builtins.str]:
        '''Additional zone for a higher level of availability and load balancing. Specify the zone in the following format: projects/{project}/locations/{location}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#secondary_location VmwareenginePrivateCloud#secondary_location}
        '''
        result = self._values.get("secondary_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudManagementClusterStretchedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cfcec4acb9780ea26606ae9071c7246595adc279debf942c58346a271a33c46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d475a6a8c9c56439bcdf4e7f68972ca9a0f87e2b672c72d08574057d321750b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryLocation")
    def secondary_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryLocation"))

    @secondary_location.setter
    def secondary_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182ae2f7ebf8562a2a9848515bbba3be05827e0b749e633daa2e97468b3bd17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareenginePrivateCloudManagementClusterStretchedClusterConfig]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudManagementClusterStretchedClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudManagementClusterStretchedClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b45beb06be5e013ca73eb6c5bcebaa812171bcb13cc703275c4a0d59cd1725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "management_cidr": "managementCidr",
        "vmware_engine_network": "vmwareEngineNetwork",
    },
)
class VmwareenginePrivateCloudNetworkConfig:
    def __init__(
        self,
        *,
        management_cidr: builtins.str,
        vmware_engine_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param management_cidr: Management CIDR used by VMware management appliances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#management_cidr VmwareenginePrivateCloud#management_cidr}
        :param vmware_engine_network: The relative resource name of the VMware Engine network attached to the private cloud. Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project} can either be a project number or a project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#vmware_engine_network VmwareenginePrivateCloud#vmware_engine_network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0d62eadadc19565e5ad2024784b5a7baf13deb408f216641f3dd5c36730c45)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#management_cidr VmwareenginePrivateCloud#management_cidr}
        '''
        result = self._values.get("management_cidr")
        assert result is not None, "Required property 'management_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vmware_engine_network(self) -> typing.Optional[builtins.str]:
        '''The relative resource name of the VMware Engine network attached to the private cloud.

        Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId}
        where {project} can either be a project number or a project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#vmware_engine_network VmwareenginePrivateCloud#vmware_engine_network}
        '''
        result = self._values.get("vmware_engine_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b19bdf118b9b7ce5e26d3ff331be989c7291bd6c1ba5c3517a66828dabfae44f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2976dc155e650834997a63e465cb1419df41221c012200ca9fd5af4cdbbb988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetwork")
    def vmware_engine_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmwareEngineNetwork"))

    @vmware_engine_network.setter
    def vmware_engine_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732f3e46141691bb75776cb60c8852bc904f9bfccfc7601a5e2785ebc6600de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmwareEngineNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmwareenginePrivateCloudNetworkConfig]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5277957f8c8171c2747cd4f0abcda5698ab20d3eaede44095f39ae554da9a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudNsx",
    jsii_struct_bases=[],
    name_mapping={},
)
class VmwareenginePrivateCloudNsx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudNsx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudNsxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudNsxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d07266ae5a8c97a6cf978fe83bbc3549b4107d90624a81d659a1784c274803f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VmwareenginePrivateCloudNsxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8fb309b62a569e72ee8b128dd21cc3b81388e9bfd8e84bfabd7cf908998ba9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareenginePrivateCloudNsxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a42885d6c59ad89c2983698b5d14bf82767335532005bac020679bfa271cf57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f74197bbad75059f7d13e2126ef970e481e24d60399611b3b1f363cad243539c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbc7638dc53fc705d5c96f8ba61173703d24bb30521c3529b6bfd8b8177ee46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudNsxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudNsxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2127227b0d5493317d27e972994312e41e9447f69e7c4a95cd2f8acc880cb1f3)
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
    def internal_value(self) -> typing.Optional[VmwareenginePrivateCloudNsx]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudNsx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudNsx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09c952d7e86c30e7feaf835565fc0a1bcfefbd873fc5247657c8d975961b519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VmwareenginePrivateCloudTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#create VmwareenginePrivateCloud#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#delete VmwareenginePrivateCloud#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#update VmwareenginePrivateCloud#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912f9a8ebfa4a5e63b6769a9895358cced5af3c79d487a5c71d32bdd9c46bb96)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#create VmwareenginePrivateCloud#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#delete VmwareenginePrivateCloud#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_private_cloud#update VmwareenginePrivateCloud#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2aaddc006f3253c09f0a27fc9f8e9aff30f10f1277000fe1cdaaf4f7738c87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d21033d48b4d83d2ba559f7f1045be779d6bfc432a5858db00e09f7884f969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ffd554484ea628bb5d4df5f2821ff2c7d37f423c0dcecca11a705a863b6e66e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccae5d1a9abeaf914db6278e3a5fcdbb989ad34dc75920f614cbe9a5679fbefe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84194250b24fa319594913460510d447c2d5cac5cee516e05dfea71127c99eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudVcenter",
    jsii_struct_bases=[],
    name_mapping={},
)
class VmwareenginePrivateCloudVcenter:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareenginePrivateCloudVcenter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareenginePrivateCloudVcenterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudVcenterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ec7b4dcc565ca4e3a81f2fc13a31e6b850abd753b4d6b0f3ee7ac6933767d46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareenginePrivateCloudVcenterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2e13173bfdcdedeee605d34d61accde5c586a9cd65cb8b3a4f1f7af9a364f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareenginePrivateCloudVcenterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd660bb7328b145550f972886d05e607bdf2f2fc027a480d839b6ebe9c2f451)
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
            type_hints = typing.get_type_hints(_typecheckingstub__374892da07e238e520fd026f278c9455ed7f7ff78011a95812774037c3b6aac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e76e51959aa5d41ebe7ceefe39061f187959dc108fdb163f6565501d235d631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VmwareenginePrivateCloudVcenterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareenginePrivateCloud.VmwareenginePrivateCloudVcenterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bd6fdb95809056831a8a1ff689f1987547ae7ef5d03d6fcccb8d5d2d32f5c47)
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
    def internal_value(self) -> typing.Optional[VmwareenginePrivateCloudVcenter]:
        return typing.cast(typing.Optional[VmwareenginePrivateCloudVcenter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareenginePrivateCloudVcenter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f824e613390935049298a2417e2a653fb99634c2e9ac53e9cf84b3f5d6822a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VmwareenginePrivateCloud",
    "VmwareenginePrivateCloudConfig",
    "VmwareenginePrivateCloudHcx",
    "VmwareenginePrivateCloudHcxList",
    "VmwareenginePrivateCloudHcxOutputReference",
    "VmwareenginePrivateCloudManagementCluster",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettings",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesList",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
    "VmwareenginePrivateCloudManagementClusterAutoscalingSettingsOutputReference",
    "VmwareenginePrivateCloudManagementClusterNodeTypeConfigs",
    "VmwareenginePrivateCloudManagementClusterNodeTypeConfigsList",
    "VmwareenginePrivateCloudManagementClusterNodeTypeConfigsOutputReference",
    "VmwareenginePrivateCloudManagementClusterOutputReference",
    "VmwareenginePrivateCloudManagementClusterStretchedClusterConfig",
    "VmwareenginePrivateCloudManagementClusterStretchedClusterConfigOutputReference",
    "VmwareenginePrivateCloudNetworkConfig",
    "VmwareenginePrivateCloudNetworkConfigOutputReference",
    "VmwareenginePrivateCloudNsx",
    "VmwareenginePrivateCloudNsxList",
    "VmwareenginePrivateCloudNsxOutputReference",
    "VmwareenginePrivateCloudTimeouts",
    "VmwareenginePrivateCloudTimeoutsOutputReference",
    "VmwareenginePrivateCloudVcenter",
    "VmwareenginePrivateCloudVcenterList",
    "VmwareenginePrivateCloudVcenterOutputReference",
]

publication.publish()

def _typecheckingstub__c87c842f1357aba6a1cc4d2022c79953386bc32bae1bd4a3a03e5262de1fc9c3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    management_cluster: typing.Union[VmwareenginePrivateCloudManagementCluster, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network_config: typing.Union[VmwareenginePrivateCloudNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    deletion_delay_hours: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[VmwareenginePrivateCloudTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__051bf214c4f2cb92e218b944aaf9d7dfd2aecd020edb6bef3838690b478843bf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30e8fcd7c7a5df5fdd39f0f8d1138b4fff907711f1544a1d4ca3623ce56a42b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b00297370c38ec9083078104626de9b073c0eeeaab892e2446498b6aae51713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b2f51358b925646a0e51efc2a725fd296d637bf183eaa9dee7e7436b16e6bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250fc8e8a6d74323fe284ed664a6fcd35ed667d257064cf4bb93b7fd096bbd92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b9f9cafe21c114e79cc8424c0f63de14d93ce97b9635a4735e19ba17f722e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eef2dde7a4d0f513cf0b7cd49f2dec55f36c93be31cfbca8e92f536dfefbbff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194f142d68c2ab12e156be3d84147c746aadb37e876f8e85fdff43218113436c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23e777583ef780ecad12831bc69cbbba01636727404688c7dcbb0e53e201b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630034937a2004a630023ac93ac12a73c875c8bae38630868b46a16a2225a69e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    management_cluster: typing.Union[VmwareenginePrivateCloudManagementCluster, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network_config: typing.Union[VmwareenginePrivateCloudNetworkConfig, typing.Dict[builtins.str, typing.Any]],
    deletion_delay_hours: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    send_deletion_delay_hours_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[VmwareenginePrivateCloudTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0ece81bad82146eeaea5d30ef06acca4abdf6d0d45ee6474df68cf4870b3e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07032897b9f7b642c2f7fbb5137dbc6847da42a5d2ea69201c57b360bd83b88f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156c4160afb2d7c0e49bffdbc5504a0f3a52c81c5179ecbf5347d9d9e1e17de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28299492561dabd14d3c454e9fe0d68624ce322e2ba6efe88761c335eb27e25f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1687e16c6f21df25ce231cb71d8cbd9346b0395350af6890684b7e6af0cc8b72(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69453166b37bb9f655dcf131adcb4a5a931f75005a156e2c3cb3e8b46faae1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94297a7ac86e476602a40ba865daaf15e85f34ebb76d60fc6c42fd9e14e23f9b(
    value: typing.Optional[VmwareenginePrivateCloudHcx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231d620248693d185d81356e009e9a8a16607fcdaa3289574a25ea43d0c04e43(
    *,
    cluster_id: builtins.str,
    autoscaling_settings: typing.Optional[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stretched_cluster_config: typing.Optional[typing.Union[VmwareenginePrivateCloudManagementClusterStretchedClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05776c5f308a98bce367a31d88ef817d98e620b33028117195567ed409a1a0c0(
    *,
    autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    cool_down_period: typing.Optional[builtins.str] = None,
    max_cluster_node_count: typing.Optional[jsii.Number] = None,
    min_cluster_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62f45021ea28fe13293984c2d97dac6d8df85d4c4d2ad5c9dd336b533f3ded4(
    *,
    autoscale_policy_id: builtins.str,
    node_type_id: builtins.str,
    scale_out_size: jsii.Number,
    consumed_memory_thresholds: typing.Optional[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    cpu_thresholds: typing.Optional[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_thresholds: typing.Optional[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ceddf00d9a247106d433fee6eea32cbe3cc5295cd5d303978ee6d0d8f355cc(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9989ee97fee76de65e7590c67200164fbabfc143e0f744941b2da629b6407541(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8629ec8b4e3ff6e0d67f703ffe81b8cd8103db040de8efc607edd350b74920(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e233c3378a7633c068181f1bb8e177e7dd325fee646add9a6eb26b0725ab0b30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8891e7d63c56f085e963b6365139b68eacf499c694744ebc929fe9b6961e2745(
    value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5017df091509d9da5ae89dc6e2aa7488205ca21a270f4153ca324275fe3f7f2(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e75f2d67513f9dd72428be4f3b86f4cd1ad7b1c75f34fdc2c4ec0d5d14cdd40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66d0c27890ea9f0662dd44d444991eb649ad5d38b64e23a054d5de244053a7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa61e41c935a8b603155ae76f238937af603700240fde8701e10657daff9c8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a6ecfe5d23421a7d6c6e101f9b5d6818a2a76c602fff9868fcba5655271e95(
    value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8056e5f1baaa2a87f339a263d481ca60a03a91ef47cc077524191fd14381fdf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3648c6e6d017cf37dcd8e6ee4b1ab7d6bb55ab9bd159d33ca58282723d0572(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf231e582a5b783517032720dbab063a10633f9430aac8612627dc16d4dc213d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4337c832d676e4ceb436cd06fdb65d82fd677e0ea16f62614909f691b8b1a467(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f2a03f155867c1fca44e72d1c193e71ed7c1c6f7c335372c0ec0bc478fc832(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10d8a0f4edd51f599545987ff3a509ecb3f830da187cb1437308b2211a4db49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a4cd8f4a566d9a45a3c73ab4c27350e2a676d9aa753a4327979f9bdfc2ed04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbeddb1d991f7e23c11b53fb5213fff6d026f47530421aeddf29ce2773792fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c9eebf7a3a78510093aed7eb9f67d072c008cab0bc680ee0af4d7e7846a94a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d6158583bb21b950eccf84291bc4561743fbdb7e3d92925cd8622c02cc8bd9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3253463dfb9f450da2df0b2e4798b453c9a6cdc1fa270cf66a9a6b802d79157e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74474be72d5e0049ba9b860a1860ddf46f3118ebf28cd17ab42dd61b6a55faa1(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551d3494e3f8dc76718b27b7a1cc447081f687f48abbf871075ef15ab5260f27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bf88399827b71000b4e3ed4cdcd3863c1a1862074bd62395f0e138547b7e55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc1fec88b34c6a71249b88fc9c0c0951e512109d5e00d0bb6e3c9302d29ff6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068db9e49a8786f0f49e8edbec166b5e5246094d9e0565ec51ca202407fccb27(
    value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf343d5ec582e6ec351bdff361d8de93b93a2743fc5c44bacfa9925f48687af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9606f9c0656e31ac2b0c7c1eeb5036bb34ab0d26353e5f96800e55f6f6c8c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d463bb5d514763b5917a0ec24cf2281efaac0760100b54b83b32108b607f7ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a05ead14844c97fe69189396771b07e7af7580ad40095d9c8c7da772c07b008(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5f399cae66506a6f1ecdac102459f72edba4ca2269c8076595bb74052624a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb4d85e47cc5a23f81e78c0bda90a0186776b994977f7bbb6f8352cad2b0639(
    value: typing.Optional[VmwareenginePrivateCloudManagementClusterAutoscalingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04211b79009cab9a63d805ea0551e36aace9755810958b4b6b00f77626b3f2e(
    *,
    node_count: jsii.Number,
    node_type_id: builtins.str,
    custom_core_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d649849c2b7b9fd43f7dfb084c54c15968d47a85c8d65178a975217bfdd1f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9073b7df5e38586d85a7a6964e24a962647f5dcb33c91e5cfa40d2304d448a3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405eb33700b1d526f20c33fa9ff0663d4716313f1eb4f1516bd6afc4d2245cbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fa9cdb6fe466aa28d4e382adeddddefad888f8d6224fc89d9d8a3ce069501d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ddedc494708385ab8f5089bb394f7f390c448ae7f3234c36686898d2195974(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b03040eb52972dea2535d117977c00199cc5e6136875048cebcb5887114a15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ebe91f335602ff7c7723ec7c0e68e94ec67711ac39cce165cd9416c03fcc87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d7407922d697bf84a20b46733a1424894ae182cb60fe18421373fcf42d01b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ba956ca4e723a108b42eeb4c1e85044fa39b21dc2bcf527ad49b7357d8232c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9710e87117afe61a5b5388b3bba4397d67ccda4967c45bfec7ca72704ea1c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08db413d8e4f07e32529317d7c402bbe967f27ae8605640d5e952b45ea0364d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudManagementClusterNodeTypeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85897bb69f96e698b2b982d5fb00f5c01965589a9b6e2d538df353bf9dc6bbb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c06c97c4da03f42cf6755329abea78d37d9e34c0a26e5600daa3630d7e5e919(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareenginePrivateCloudManagementClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e185b19d12992d59a7581aaac23f90a80d8ed44842260a8850cc1ad729eab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea630273e53947a8aca0c355b30f4589a2cbe1b6fb4dad33d6041ef6712778f(
    value: typing.Optional[VmwareenginePrivateCloudManagementCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ce80536f3aba63944561791cbd71f3db4a5293571dd780c2adc03dbebd8e0b(
    *,
    preferred_location: typing.Optional[builtins.str] = None,
    secondary_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cfcec4acb9780ea26606ae9071c7246595adc279debf942c58346a271a33c46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d475a6a8c9c56439bcdf4e7f68972ca9a0f87e2b672c72d08574057d321750b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182ae2f7ebf8562a2a9848515bbba3be05827e0b749e633daa2e97468b3bd17d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b45beb06be5e013ca73eb6c5bcebaa812171bcb13cc703275c4a0d59cd1725(
    value: typing.Optional[VmwareenginePrivateCloudManagementClusterStretchedClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0d62eadadc19565e5ad2024784b5a7baf13deb408f216641f3dd5c36730c45(
    *,
    management_cidr: builtins.str,
    vmware_engine_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19bdf118b9b7ce5e26d3ff331be989c7291bd6c1ba5c3517a66828dabfae44f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2976dc155e650834997a63e465cb1419df41221c012200ca9fd5af4cdbbb988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732f3e46141691bb75776cb60c8852bc904f9bfccfc7601a5e2785ebc6600de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5277957f8c8171c2747cd4f0abcda5698ab20d3eaede44095f39ae554da9a61(
    value: typing.Optional[VmwareenginePrivateCloudNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d07266ae5a8c97a6cf978fe83bbc3549b4107d90624a81d659a1784c274803f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8fb309b62a569e72ee8b128dd21cc3b81388e9bfd8e84bfabd7cf908998ba9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a42885d6c59ad89c2983698b5d14bf82767335532005bac020679bfa271cf57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74197bbad75059f7d13e2126ef970e481e24d60399611b3b1f363cad243539c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc7638dc53fc705d5c96f8ba61173703d24bb30521c3529b6bfd8b8177ee46c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2127227b0d5493317d27e972994312e41e9447f69e7c4a95cd2f8acc880cb1f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09c952d7e86c30e7feaf835565fc0a1bcfefbd873fc5247657c8d975961b519(
    value: typing.Optional[VmwareenginePrivateCloudNsx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912f9a8ebfa4a5e63b6769a9895358cced5af3c79d487a5c71d32bdd9c46bb96(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2aaddc006f3253c09f0a27fc9f8e9aff30f10f1277000fe1cdaaf4f7738c87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d21033d48b4d83d2ba559f7f1045be779d6bfc432a5858db00e09f7884f969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffd554484ea628bb5d4df5f2821ff2c7d37f423c0dcecca11a705a863b6e66e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccae5d1a9abeaf914db6278e3a5fcdbb989ad34dc75920f614cbe9a5679fbefe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84194250b24fa319594913460510d447c2d5cac5cee516e05dfea71127c99eb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareenginePrivateCloudTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec7b4dcc565ca4e3a81f2fc13a31e6b850abd753b4d6b0f3ee7ac6933767d46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2e13173bfdcdedeee605d34d61accde5c586a9cd65cb8b3a4f1f7af9a364f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd660bb7328b145550f972886d05e607bdf2f2fc027a480d839b6ebe9c2f451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374892da07e238e520fd026f278c9455ed7f7ff78011a95812774037c3b6aac8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e76e51959aa5d41ebe7ceefe39061f187959dc108fdb163f6565501d235d631(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd6fdb95809056831a8a1ff689f1987547ae7ef5d03d6fcccb8d5d2d32f5c47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f824e613390935049298a2417e2a653fb99634c2e9ac53e9cf84b3f5d6822a4f(
    value: typing.Optional[VmwareenginePrivateCloudVcenter],
) -> None:
    """Type checking stubs"""
    pass
