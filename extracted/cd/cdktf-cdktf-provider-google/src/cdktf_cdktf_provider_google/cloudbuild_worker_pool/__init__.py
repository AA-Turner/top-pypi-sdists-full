r'''
# `google_cloudbuild_worker_pool`

Refer to the Terraform Registry for docs: [`google_cloudbuild_worker_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool).
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


class CloudbuildWorkerPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool google_cloudbuild_worker_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["CloudbuildWorkerPoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_service_connect: typing.Optional[typing.Union["CloudbuildWorkerPoolPrivateServiceConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudbuildWorkerPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_config: typing.Optional[typing.Union["CloudbuildWorkerPoolWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool google_cloudbuild_worker_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#location CloudbuildWorkerPool#location}
        :param name: User-defined name of the ``WorkerPool``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#name CloudbuildWorkerPool#name}
        :param annotations: User specified annotations. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#annotations CloudbuildWorkerPool#annotations}
        :param display_name: A user-specified, human-readable name for the ``WorkerPool``. If provided, this value must be 1-63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#display_name CloudbuildWorkerPool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#id CloudbuildWorkerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#network_config CloudbuildWorkerPool#network_config}
        :param private_service_connect: private_service_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#private_service_connect CloudbuildWorkerPool#private_service_connect}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#project CloudbuildWorkerPool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#timeouts CloudbuildWorkerPool#timeouts}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#worker_config CloudbuildWorkerPool#worker_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201c7d8286f48139e04d96f3e235ce830338efb554675ecd917d8b58d28a8f70)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudbuildWorkerPoolConfig(
            location=location,
            name=name,
            annotations=annotations,
            display_name=display_name,
            id=id,
            network_config=network_config,
            private_service_connect=private_service_connect,
            project=project,
            timeouts=timeouts,
            worker_config=worker_config,
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
        '''Generates CDKTF code for importing a CloudbuildWorkerPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudbuildWorkerPool to import.
        :param import_from_id: The id of the existing CloudbuildWorkerPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudbuildWorkerPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4c75ebd5b51ab8e294eaf664919305e4586f2efa197fe536ac7f2066a7797d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        peered_network: builtins.str,
        peered_network_ip_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peered_network: Required. Immutable. The network definition that the workers are peered to. If this section is left empty, the workers will be peered to ``WorkerPool.project_id`` on the service producer network. Must be in the format ``projects/{project}/global/networks/{network}``, where ``{project}`` is a project number, such as ``12345``, and ``{network}`` is the name of a VPC network in the project. See `Understanding network configuration options <https://cloud.google.com/cloud-build/docs/custom-workers/set-up-custom-worker-pool-environment#understanding_the_network_configuration_options>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#peered_network CloudbuildWorkerPool#peered_network}
        :param peered_network_ip_range: Optional. Immutable. Subnet IP range within the peered network. This is specified in CIDR notation with a slash and the subnet prefix size. You can optionally specify an IP address before the subnet prefix value. e.g. ``192.168.0.0/29`` would specify an IP range starting at 192.168.0.0 with a prefix size of 29 bits. ``/16`` would specify a prefix size of 16 bits, with an automatically determined IP within the peered VPC. If unspecified, a value of ``/24`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#peered_network_ip_range CloudbuildWorkerPool#peered_network_ip_range}
        '''
        value = CloudbuildWorkerPoolNetworkConfig(
            peered_network=peered_network,
            peered_network_ip_range=peered_network_ip_range,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putPrivateServiceConnect")
    def put_private_service_connect(
        self,
        *,
        network_attachment: builtins.str,
        route_all_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param network_attachment: Required. Immutable. The network attachment that the worker network interface is connected to. Must be in the format ``projects/{project}/regions/{region}/networkAttachments/{networkAttachment}``. The region of network attachment must be the same as the worker pool. See `Network Attachments <https://cloud.google.com/vpc/docs/about-network-attachments>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#network_attachment CloudbuildWorkerPool#network_attachment}
        :param route_all_traffic: Immutable. Route all traffic through PSC interface. Enable this if you want full control of traffic in the private pool. Configure Cloud NAT for the subnet of network attachment if you need to access public Internet. If false, Only route private IPs, e.g. 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 through PSC interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#route_all_traffic CloudbuildWorkerPool#route_all_traffic}
        '''
        value = CloudbuildWorkerPoolPrivateServiceConnect(
            network_attachment=network_attachment, route_all_traffic=route_all_traffic
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateServiceConnect", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#create CloudbuildWorkerPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#delete CloudbuildWorkerPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#update CloudbuildWorkerPool#update}.
        '''
        value = CloudbuildWorkerPoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkerConfig")
    def put_worker_config(
        self,
        *,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        no_external_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disk_size_gb: Size of the disk attached to the worker, in GB. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. Specify a value of up to 1000. If ``0`` is specified, Cloud Build will use a standard disk size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#disk_size_gb CloudbuildWorkerPool#disk_size_gb}
        :param machine_type: Machine type of a worker, such as ``n1-standard-1``. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. If left blank, Cloud Build will use ``n1-standard-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#machine_type CloudbuildWorkerPool#machine_type}
        :param no_external_ip: If true, workers are created without any public address, which prevents network egress to public IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#no_external_ip CloudbuildWorkerPool#no_external_ip}
        '''
        value = CloudbuildWorkerPoolWorkerConfig(
            disk_size_gb=disk_size_gb,
            machine_type=machine_type,
            no_external_ip=no_external_ip,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfig", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetPrivateServiceConnect")
    def reset_private_service_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateServiceConnect", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkerConfig")
    def reset_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfig", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "CloudbuildWorkerPoolNetworkConfigOutputReference":
        return typing.cast("CloudbuildWorkerPoolNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnect")
    def private_service_connect(
        self,
    ) -> "CloudbuildWorkerPoolPrivateServiceConnectOutputReference":
        return typing.cast("CloudbuildWorkerPoolPrivateServiceConnectOutputReference", jsii.get(self, "privateServiceConnect"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudbuildWorkerPoolTimeoutsOutputReference":
        return typing.cast("CloudbuildWorkerPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="workerConfig")
    def worker_config(self) -> "CloudbuildWorkerPoolWorkerConfigOutputReference":
        return typing.cast("CloudbuildWorkerPoolWorkerConfigOutputReference", jsii.get(self, "workerConfig"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["CloudbuildWorkerPoolNetworkConfig"]:
        return typing.cast(typing.Optional["CloudbuildWorkerPoolNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectInput")
    def private_service_connect_input(
        self,
    ) -> typing.Optional["CloudbuildWorkerPoolPrivateServiceConnect"]:
        return typing.cast(typing.Optional["CloudbuildWorkerPoolPrivateServiceConnect"], jsii.get(self, "privateServiceConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudbuildWorkerPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudbuildWorkerPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigInput")
    def worker_config_input(
        self,
    ) -> typing.Optional["CloudbuildWorkerPoolWorkerConfig"]:
        return typing.cast(typing.Optional["CloudbuildWorkerPoolWorkerConfig"], jsii.get(self, "workerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb138eb8c2055aded512db75e499e04105b1033983d29e70b76813071f580b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40796ca422c37d35af911ee8818324cc8d49e27861df25809f289f512c9d74a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e93738fcb37a1814320481f7e11d6d9f771014f3a79ffcb1204cf773512af74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188f18724bba3437d3b05a59d7909bb1e4714932a05154b5ef29b7e81581f7c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d27cdd3f3fb19d7c72894967c5a53fe2b8672efc33890014ca7b4225a69e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02b84bc290a340cc0ea1cc2b8a48fc834be0b32a357d3756d5f69744dd7b48d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolConfig",
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
        "name": "name",
        "annotations": "annotations",
        "display_name": "displayName",
        "id": "id",
        "network_config": "networkConfig",
        "private_service_connect": "privateServiceConnect",
        "project": "project",
        "timeouts": "timeouts",
        "worker_config": "workerConfig",
    },
)
class CloudbuildWorkerPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["CloudbuildWorkerPoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_service_connect: typing.Optional[typing.Union["CloudbuildWorkerPoolPrivateServiceConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudbuildWorkerPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_config: typing.Optional[typing.Union["CloudbuildWorkerPoolWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#location CloudbuildWorkerPool#location}
        :param name: User-defined name of the ``WorkerPool``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#name CloudbuildWorkerPool#name}
        :param annotations: User specified annotations. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#annotations CloudbuildWorkerPool#annotations}
        :param display_name: A user-specified, human-readable name for the ``WorkerPool``. If provided, this value must be 1-63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#display_name CloudbuildWorkerPool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#id CloudbuildWorkerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#network_config CloudbuildWorkerPool#network_config}
        :param private_service_connect: private_service_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#private_service_connect CloudbuildWorkerPool#private_service_connect}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#project CloudbuildWorkerPool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#timeouts CloudbuildWorkerPool#timeouts}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#worker_config CloudbuildWorkerPool#worker_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_config, dict):
            network_config = CloudbuildWorkerPoolNetworkConfig(**network_config)
        if isinstance(private_service_connect, dict):
            private_service_connect = CloudbuildWorkerPoolPrivateServiceConnect(**private_service_connect)
        if isinstance(timeouts, dict):
            timeouts = CloudbuildWorkerPoolTimeouts(**timeouts)
        if isinstance(worker_config, dict):
            worker_config = CloudbuildWorkerPoolWorkerConfig(**worker_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d22a19c417701bf410ef342363d27782a963afc66cce48575d988cf97c819c4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument private_service_connect", value=private_service_connect, expected_type=type_hints["private_service_connect"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument worker_config", value=worker_config, expected_type=type_hints["worker_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if network_config is not None:
            self._values["network_config"] = network_config
        if private_service_connect is not None:
            self._values["private_service_connect"] = private_service_connect
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if worker_config is not None:
            self._values["worker_config"] = worker_config

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
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#location CloudbuildWorkerPool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''User-defined name of the ``WorkerPool``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#name CloudbuildWorkerPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User specified annotations. See https://google.aip.dev/128#annotations for more details such as format and size limitations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#annotations CloudbuildWorkerPool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-specified, human-readable name for the ``WorkerPool``. If provided, this value must be 1-63 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#display_name CloudbuildWorkerPool#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#id CloudbuildWorkerPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(self) -> typing.Optional["CloudbuildWorkerPoolNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#network_config CloudbuildWorkerPool#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["CloudbuildWorkerPoolNetworkConfig"], result)

    @builtins.property
    def private_service_connect(
        self,
    ) -> typing.Optional["CloudbuildWorkerPoolPrivateServiceConnect"]:
        '''private_service_connect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#private_service_connect CloudbuildWorkerPool#private_service_connect}
        '''
        result = self._values.get("private_service_connect")
        return typing.cast(typing.Optional["CloudbuildWorkerPoolPrivateServiceConnect"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#project CloudbuildWorkerPool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudbuildWorkerPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#timeouts CloudbuildWorkerPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudbuildWorkerPoolTimeouts"], result)

    @builtins.property
    def worker_config(self) -> typing.Optional["CloudbuildWorkerPoolWorkerConfig"]:
        '''worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#worker_config CloudbuildWorkerPool#worker_config}
        '''
        result = self._values.get("worker_config")
        return typing.cast(typing.Optional["CloudbuildWorkerPoolWorkerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildWorkerPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "peered_network": "peeredNetwork",
        "peered_network_ip_range": "peeredNetworkIpRange",
    },
)
class CloudbuildWorkerPoolNetworkConfig:
    def __init__(
        self,
        *,
        peered_network: builtins.str,
        peered_network_ip_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peered_network: Required. Immutable. The network definition that the workers are peered to. If this section is left empty, the workers will be peered to ``WorkerPool.project_id`` on the service producer network. Must be in the format ``projects/{project}/global/networks/{network}``, where ``{project}`` is a project number, such as ``12345``, and ``{network}`` is the name of a VPC network in the project. See `Understanding network configuration options <https://cloud.google.com/cloud-build/docs/custom-workers/set-up-custom-worker-pool-environment#understanding_the_network_configuration_options>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#peered_network CloudbuildWorkerPool#peered_network}
        :param peered_network_ip_range: Optional. Immutable. Subnet IP range within the peered network. This is specified in CIDR notation with a slash and the subnet prefix size. You can optionally specify an IP address before the subnet prefix value. e.g. ``192.168.0.0/29`` would specify an IP range starting at 192.168.0.0 with a prefix size of 29 bits. ``/16`` would specify a prefix size of 16 bits, with an automatically determined IP within the peered VPC. If unspecified, a value of ``/24`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#peered_network_ip_range CloudbuildWorkerPool#peered_network_ip_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07bbea2a1146933d55d04e8b9511e45649a14716a912ff78dd8996a0f3e72bb1)
            check_type(argname="argument peered_network", value=peered_network, expected_type=type_hints["peered_network"])
            check_type(argname="argument peered_network_ip_range", value=peered_network_ip_range, expected_type=type_hints["peered_network_ip_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peered_network": peered_network,
        }
        if peered_network_ip_range is not None:
            self._values["peered_network_ip_range"] = peered_network_ip_range

    @builtins.property
    def peered_network(self) -> builtins.str:
        '''Required.

        Immutable. The network definition that the workers are peered to. If this section is left empty, the workers will be peered to ``WorkerPool.project_id`` on the service producer network. Must be in the format ``projects/{project}/global/networks/{network}``, where ``{project}`` is a project number, such as ``12345``, and ``{network}`` is the name of a VPC network in the project. See `Understanding network configuration options <https://cloud.google.com/cloud-build/docs/custom-workers/set-up-custom-worker-pool-environment#understanding_the_network_configuration_options>`_

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#peered_network CloudbuildWorkerPool#peered_network}
        '''
        result = self._values.get("peered_network")
        assert result is not None, "Required property 'peered_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peered_network_ip_range(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Immutable. Subnet IP range within the peered network. This is specified in CIDR notation with a slash and the subnet prefix size. You can optionally specify an IP address before the subnet prefix value. e.g. ``192.168.0.0/29`` would specify an IP range starting at 192.168.0.0 with a prefix size of 29 bits. ``/16`` would specify a prefix size of 16 bits, with an automatically determined IP within the peered VPC. If unspecified, a value of ``/24`` will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#peered_network_ip_range CloudbuildWorkerPool#peered_network_ip_range}
        '''
        result = self._values.get("peered_network_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildWorkerPoolNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildWorkerPoolNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b059b9229893f9e196cc45a756e99d25af160ca2767771988fcc8913992a1c92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPeeredNetworkIpRange")
    def reset_peered_network_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeeredNetworkIpRange", []))

    @builtins.property
    @jsii.member(jsii_name="peeredNetworkInput")
    def peered_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeredNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="peeredNetworkIpRangeInput")
    def peered_network_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeredNetworkIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="peeredNetwork")
    def peered_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeredNetwork"))

    @peered_network.setter
    def peered_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b2843d26e517717d2310f9efa53b61364a419744b45f2ff5327b48d90c7b03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeredNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeredNetworkIpRange")
    def peered_network_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeredNetworkIpRange"))

    @peered_network_ip_range.setter
    def peered_network_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e296b3e68c134d2f977398e1a2c601a47381237c5711c6f6f058fe2b2577a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeredNetworkIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildWorkerPoolNetworkConfig]:
        return typing.cast(typing.Optional[CloudbuildWorkerPoolNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildWorkerPoolNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c92b5c93d9f70a52e7c576d5883f1c25c1b15840dbe699a0de7bcac1041c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolPrivateServiceConnect",
    jsii_struct_bases=[],
    name_mapping={
        "network_attachment": "networkAttachment",
        "route_all_traffic": "routeAllTraffic",
    },
)
class CloudbuildWorkerPoolPrivateServiceConnect:
    def __init__(
        self,
        *,
        network_attachment: builtins.str,
        route_all_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param network_attachment: Required. Immutable. The network attachment that the worker network interface is connected to. Must be in the format ``projects/{project}/regions/{region}/networkAttachments/{networkAttachment}``. The region of network attachment must be the same as the worker pool. See `Network Attachments <https://cloud.google.com/vpc/docs/about-network-attachments>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#network_attachment CloudbuildWorkerPool#network_attachment}
        :param route_all_traffic: Immutable. Route all traffic through PSC interface. Enable this if you want full control of traffic in the private pool. Configure Cloud NAT for the subnet of network attachment if you need to access public Internet. If false, Only route private IPs, e.g. 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 through PSC interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#route_all_traffic CloudbuildWorkerPool#route_all_traffic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6571e18097f084d808618de5c89e22692374dce266b755f203f55c8ec8d24661)
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
            check_type(argname="argument route_all_traffic", value=route_all_traffic, expected_type=type_hints["route_all_traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_attachment": network_attachment,
        }
        if route_all_traffic is not None:
            self._values["route_all_traffic"] = route_all_traffic

    @builtins.property
    def network_attachment(self) -> builtins.str:
        '''Required.

        Immutable. The network attachment that the worker network interface is connected to. Must be in the format ``projects/{project}/regions/{region}/networkAttachments/{networkAttachment}``. The region of network attachment must be the same as the worker pool. See `Network Attachments <https://cloud.google.com/vpc/docs/about-network-attachments>`_

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#network_attachment CloudbuildWorkerPool#network_attachment}
        '''
        result = self._values.get("network_attachment")
        assert result is not None, "Required property 'network_attachment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_all_traffic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Immutable.

        Route all traffic through PSC interface. Enable this if you want full control of traffic in the private pool. Configure Cloud NAT for the subnet of network attachment if you need to access public Internet. If false, Only route private IPs, e.g. 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 through PSC interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#route_all_traffic CloudbuildWorkerPool#route_all_traffic}
        '''
        result = self._values.get("route_all_traffic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildWorkerPoolPrivateServiceConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildWorkerPoolPrivateServiceConnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolPrivateServiceConnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c390cae84dd15bac3316270ef0016a8faa69fdcf25ad4489d6290c0271738a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRouteAllTraffic")
    def reset_route_all_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteAllTraffic", []))

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentInput")
    def network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="routeAllTrafficInput")
    def route_all_traffic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "routeAllTrafficInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd01588efde1de797f36a2fa0cbedcd3e7e163bca14cfbe9fa12f4b9ae09f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeAllTraffic")
    def route_all_traffic(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "routeAllTraffic"))

    @route_all_traffic.setter
    def route_all_traffic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7dd138774518023d7c31027718251ae7b1009e07880ee6cf3835ae8c5d377a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeAllTraffic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudbuildWorkerPoolPrivateServiceConnect]:
        return typing.cast(typing.Optional[CloudbuildWorkerPoolPrivateServiceConnect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildWorkerPoolPrivateServiceConnect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75dd598d1662406e98939c2ff31d04d342140c806f70bce1670ac4843346b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudbuildWorkerPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#create CloudbuildWorkerPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#delete CloudbuildWorkerPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#update CloudbuildWorkerPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29da07f0d0340b7b315a1268ff20f9625e3cc6ffac9aa0fa584857cb03e28a5c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#create CloudbuildWorkerPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#delete CloudbuildWorkerPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#update CloudbuildWorkerPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildWorkerPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildWorkerPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__946d9b093ed7f41b8249b61fa869fbef29c4cf15821be574ac000ae82de6f709)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b94bd3e77648546a62174ebe3d86768324be47dfd11abdf24e3209da53070f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa238f20589ba1c12b6e447061e9dbd3bc03e565bc691c7d1d7f4e5a6fd7330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8077ebe051de00c143c0dbe81f119f8c924ed36afdb6ab10cc91e7a1537aacae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildWorkerPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildWorkerPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildWorkerPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361a244304220e1433dabe5ed687209c30876e9d675870813a4362cb1f1d8952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disk_size_gb": "diskSizeGb",
        "machine_type": "machineType",
        "no_external_ip": "noExternalIp",
    },
)
class CloudbuildWorkerPoolWorkerConfig:
    def __init__(
        self,
        *,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        no_external_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disk_size_gb: Size of the disk attached to the worker, in GB. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. Specify a value of up to 1000. If ``0`` is specified, Cloud Build will use a standard disk size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#disk_size_gb CloudbuildWorkerPool#disk_size_gb}
        :param machine_type: Machine type of a worker, such as ``n1-standard-1``. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. If left blank, Cloud Build will use ``n1-standard-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#machine_type CloudbuildWorkerPool#machine_type}
        :param no_external_ip: If true, workers are created without any public address, which prevents network egress to public IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#no_external_ip CloudbuildWorkerPool#no_external_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993e3eb5532950036228b77a0b895412fbde655bf74a595490f2d37cd3bfec39)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument no_external_ip", value=no_external_ip, expected_type=type_hints["no_external_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if no_external_ip is not None:
            self._values["no_external_ip"] = no_external_ip

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the disk attached to the worker, in GB.

        See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. Specify a value of up to 1000. If ``0`` is specified, Cloud Build will use a standard disk size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#disk_size_gb CloudbuildWorkerPool#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Machine type of a worker, such as ``n1-standard-1``.

        See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. If left blank, Cloud Build will use ``n1-standard-1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#machine_type CloudbuildWorkerPool#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_external_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, workers are created without any public address, which prevents network egress to public IPs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_worker_pool#no_external_ip CloudbuildWorkerPool#no_external_ip}
        '''
        result = self._values.get("no_external_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildWorkerPoolWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildWorkerPoolWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildWorkerPool.CloudbuildWorkerPoolWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1c70cfb3defa44d4a942f96f2b9d2344d4ef3276841ef99f452b5e8e5a105f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetNoExternalIp")
    def reset_no_external_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoExternalIp", []))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="noExternalIpInput")
    def no_external_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noExternalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec06c096b22c02e586ffd37db88cc24fbc6f3addf8952ec0821caf98b672b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0d53770fd24ccbdbd304ef5169088f2b9f211500334652fa32e2992a651173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExternalIp")
    def no_external_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noExternalIp"))

    @no_external_ip.setter
    def no_external_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf05720a3235676771d0820e9f343665150fc5f811969b64baf5a8c29f464d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExternalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildWorkerPoolWorkerConfig]:
        return typing.cast(typing.Optional[CloudbuildWorkerPoolWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildWorkerPoolWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf34513527c0f8c632339a54ca14cf1247b3201693bad816a567c227ca434ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudbuildWorkerPool",
    "CloudbuildWorkerPoolConfig",
    "CloudbuildWorkerPoolNetworkConfig",
    "CloudbuildWorkerPoolNetworkConfigOutputReference",
    "CloudbuildWorkerPoolPrivateServiceConnect",
    "CloudbuildWorkerPoolPrivateServiceConnectOutputReference",
    "CloudbuildWorkerPoolTimeouts",
    "CloudbuildWorkerPoolTimeoutsOutputReference",
    "CloudbuildWorkerPoolWorkerConfig",
    "CloudbuildWorkerPoolWorkerConfigOutputReference",
]

publication.publish()

def _typecheckingstub__201c7d8286f48139e04d96f3e235ce830338efb554675ecd917d8b58d28a8f70(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[CloudbuildWorkerPoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_service_connect: typing.Optional[typing.Union[CloudbuildWorkerPoolPrivateServiceConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudbuildWorkerPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_config: typing.Optional[typing.Union[CloudbuildWorkerPoolWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2e4c75ebd5b51ab8e294eaf664919305e4586f2efa197fe536ac7f2066a7797d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb138eb8c2055aded512db75e499e04105b1033983d29e70b76813071f580b9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40796ca422c37d35af911ee8818324cc8d49e27861df25809f289f512c9d74a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e93738fcb37a1814320481f7e11d6d9f771014f3a79ffcb1204cf773512af74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188f18724bba3437d3b05a59d7909bb1e4714932a05154b5ef29b7e81581f7c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d27cdd3f3fb19d7c72894967c5a53fe2b8672efc33890014ca7b4225a69e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02b84bc290a340cc0ea1cc2b8a48fc834be0b32a357d3756d5f69744dd7b48d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d22a19c417701bf410ef342363d27782a963afc66cce48575d988cf97c819c4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[CloudbuildWorkerPoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_service_connect: typing.Optional[typing.Union[CloudbuildWorkerPoolPrivateServiceConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudbuildWorkerPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_config: typing.Optional[typing.Union[CloudbuildWorkerPoolWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07bbea2a1146933d55d04e8b9511e45649a14716a912ff78dd8996a0f3e72bb1(
    *,
    peered_network: builtins.str,
    peered_network_ip_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b059b9229893f9e196cc45a756e99d25af160ca2767771988fcc8913992a1c92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b2843d26e517717d2310f9efa53b61364a419744b45f2ff5327b48d90c7b03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e296b3e68c134d2f977398e1a2c601a47381237c5711c6f6f058fe2b2577a39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c92b5c93d9f70a52e7c576d5883f1c25c1b15840dbe699a0de7bcac1041c6c(
    value: typing.Optional[CloudbuildWorkerPoolNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6571e18097f084d808618de5c89e22692374dce266b755f203f55c8ec8d24661(
    *,
    network_attachment: builtins.str,
    route_all_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c390cae84dd15bac3316270ef0016a8faa69fdcf25ad4489d6290c0271738a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd01588efde1de797f36a2fa0cbedcd3e7e163bca14cfbe9fa12f4b9ae09f3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7dd138774518023d7c31027718251ae7b1009e07880ee6cf3835ae8c5d377a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75dd598d1662406e98939c2ff31d04d342140c806f70bce1670ac4843346b91(
    value: typing.Optional[CloudbuildWorkerPoolPrivateServiceConnect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29da07f0d0340b7b315a1268ff20f9625e3cc6ffac9aa0fa584857cb03e28a5c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946d9b093ed7f41b8249b61fa869fbef29c4cf15821be574ac000ae82de6f709(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b94bd3e77648546a62174ebe3d86768324be47dfd11abdf24e3209da53070f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa238f20589ba1c12b6e447061e9dbd3bc03e565bc691c7d1d7f4e5a6fd7330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8077ebe051de00c143c0dbe81f119f8c924ed36afdb6ab10cc91e7a1537aacae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361a244304220e1433dabe5ed687209c30876e9d675870813a4362cb1f1d8952(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildWorkerPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993e3eb5532950036228b77a0b895412fbde655bf74a595490f2d37cd3bfec39(
    *,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    machine_type: typing.Optional[builtins.str] = None,
    no_external_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c70cfb3defa44d4a942f96f2b9d2344d4ef3276841ef99f452b5e8e5a105f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec06c096b22c02e586ffd37db88cc24fbc6f3addf8952ec0821caf98b672b4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0d53770fd24ccbdbd304ef5169088f2b9f211500334652fa32e2992a651173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf05720a3235676771d0820e9f343665150fc5f811969b64baf5a8c29f464d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf34513527c0f8c632339a54ca14cf1247b3201693bad816a567c227ca434ae5(
    value: typing.Optional[CloudbuildWorkerPoolWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass
