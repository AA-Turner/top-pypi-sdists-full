r'''
# `google_cloudbuild_worker_pool`

Refer to the Terraform Registry for docs: [`google_cloudbuild_worker_pool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool).
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


class GoogleCloudbuildWorkerPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool google_cloudbuild_worker_pool}.'''

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
        network_config: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_service_connect: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolPrivateServiceConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_config: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool google_cloudbuild_worker_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#location GoogleCloudbuildWorkerPool#location}
        :param name: User-defined name of the ``WorkerPool``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#name GoogleCloudbuildWorkerPool#name}
        :param annotations: User specified annotations. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#annotations GoogleCloudbuildWorkerPool#annotations}
        :param display_name: A user-specified, human-readable name for the ``WorkerPool``. If provided, this value must be 1-63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#display_name GoogleCloudbuildWorkerPool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#id GoogleCloudbuildWorkerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#network_config GoogleCloudbuildWorkerPool#network_config}
        :param private_service_connect: private_service_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#private_service_connect GoogleCloudbuildWorkerPool#private_service_connect}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#project GoogleCloudbuildWorkerPool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#timeouts GoogleCloudbuildWorkerPool#timeouts}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#worker_config GoogleCloudbuildWorkerPool#worker_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9366ea34785f78792e9638151e5d824de55cf900bdd1bd51c832bf4f04a82176)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudbuildWorkerPoolConfig(
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
        '''Generates CDKTF code for importing a GoogleCloudbuildWorkerPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudbuildWorkerPool to import.
        :param import_from_id: The id of the existing GoogleCloudbuildWorkerPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudbuildWorkerPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c27451dfaa2abba79334fa6cd5959b7995befd4c7c5cb9d625e42a2e36e9471)
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
        :param peered_network: Required. Immutable. The network definition that the workers are peered to. If this section is left empty, the workers will be peered to ``WorkerPool.project_id`` on the service producer network. Must be in the format ``projects/{project}/global/networks/{network}``, where ``{project}`` is a project number, such as ``12345``, and ``{network}`` is the name of a VPC network in the project. See `Understanding network configuration options <https://cloud.google.com/cloud-build/docs/custom-workers/set-up-custom-worker-pool-environment#understanding_the_network_configuration_options>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#peered_network GoogleCloudbuildWorkerPool#peered_network}
        :param peered_network_ip_range: Optional. Immutable. Subnet IP range within the peered network. This is specified in CIDR notation with a slash and the subnet prefix size. You can optionally specify an IP address before the subnet prefix value. e.g. ``192.168.0.0/29`` would specify an IP range starting at 192.168.0.0 with a prefix size of 29 bits. ``/16`` would specify a prefix size of 16 bits, with an automatically determined IP within the peered VPC. If unspecified, a value of ``/24`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#peered_network_ip_range GoogleCloudbuildWorkerPool#peered_network_ip_range}
        '''
        value = GoogleCloudbuildWorkerPoolNetworkConfig(
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
        :param network_attachment: Required. Immutable. The network attachment that the worker network interface is connected to. Must be in the format ``projects/{project}/regions/{region}/networkAttachments/{networkAttachment}``. The region of network attachment must be the same as the worker pool. See `Network Attachments <https://cloud.google.com/vpc/docs/about-network-attachments>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#network_attachment GoogleCloudbuildWorkerPool#network_attachment}
        :param route_all_traffic: Immutable. Route all traffic through PSC interface. Enable this if you want full control of traffic in the private pool. Configure Cloud NAT for the subnet of network attachment if you need to access public Internet. If false, Only route private IPs, e.g. 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 through PSC interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#route_all_traffic GoogleCloudbuildWorkerPool#route_all_traffic}
        '''
        value = GoogleCloudbuildWorkerPoolPrivateServiceConnect(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#create GoogleCloudbuildWorkerPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#delete GoogleCloudbuildWorkerPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#update GoogleCloudbuildWorkerPool#update}.
        '''
        value = GoogleCloudbuildWorkerPoolTimeouts(
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
        :param disk_size_gb: Size of the disk attached to the worker, in GB. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. Specify a value of up to 1000. If ``0`` is specified, Cloud Build will use a standard disk size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#disk_size_gb GoogleCloudbuildWorkerPool#disk_size_gb}
        :param machine_type: Machine type of a worker, such as ``n1-standard-1``. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. If left blank, Cloud Build will use ``n1-standard-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#machine_type GoogleCloudbuildWorkerPool#machine_type}
        :param no_external_ip: If true, workers are created without any public address, which prevents network egress to public IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#no_external_ip GoogleCloudbuildWorkerPool#no_external_ip}
        '''
        value = GoogleCloudbuildWorkerPoolWorkerConfig(
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
    def network_config(
        self,
    ) -> "GoogleCloudbuildWorkerPoolNetworkConfigOutputReference":
        return typing.cast("GoogleCloudbuildWorkerPoolNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnect")
    def private_service_connect(
        self,
    ) -> "GoogleCloudbuildWorkerPoolPrivateServiceConnectOutputReference":
        return typing.cast("GoogleCloudbuildWorkerPoolPrivateServiceConnectOutputReference", jsii.get(self, "privateServiceConnect"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudbuildWorkerPoolTimeoutsOutputReference":
        return typing.cast("GoogleCloudbuildWorkerPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def worker_config(self) -> "GoogleCloudbuildWorkerPoolWorkerConfigOutputReference":
        return typing.cast("GoogleCloudbuildWorkerPoolWorkerConfigOutputReference", jsii.get(self, "workerConfig"))

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
    ) -> typing.Optional["GoogleCloudbuildWorkerPoolNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectInput")
    def private_service_connect_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildWorkerPoolPrivateServiceConnect"]:
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolPrivateServiceConnect"], jsii.get(self, "privateServiceConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildWorkerPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildWorkerPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigInput")
    def worker_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildWorkerPoolWorkerConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolWorkerConfig"], jsii.get(self, "workerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ace7b7da8788e814b643e052f9c6988953ce095c9717572e6c266dc365c1b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02541a250723c780bab205ea4a9fed793ad4cad7dd087677159c9eb060104463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f954feceea24bfa09f40088fc575377ee15a0dc4894be8efab04d8d88943bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0657a99d6184f4e0ff66ff4261a5e776b13e8ffe0c358395e21cac61f42b7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7642be85d0f15f2804daa285dab88fab79cfb07034185d20512a0add4bda377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73628f9449661e4f9c929e6c66dce1595490b88ad33061d53fc0d702271b94f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolConfig",
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
class GoogleCloudbuildWorkerPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network_config: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_service_connect: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolPrivateServiceConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_config: typing.Optional[typing.Union["GoogleCloudbuildWorkerPoolWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#location GoogleCloudbuildWorkerPool#location}
        :param name: User-defined name of the ``WorkerPool``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#name GoogleCloudbuildWorkerPool#name}
        :param annotations: User specified annotations. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#annotations GoogleCloudbuildWorkerPool#annotations}
        :param display_name: A user-specified, human-readable name for the ``WorkerPool``. If provided, this value must be 1-63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#display_name GoogleCloudbuildWorkerPool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#id GoogleCloudbuildWorkerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#network_config GoogleCloudbuildWorkerPool#network_config}
        :param private_service_connect: private_service_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#private_service_connect GoogleCloudbuildWorkerPool#private_service_connect}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#project GoogleCloudbuildWorkerPool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#timeouts GoogleCloudbuildWorkerPool#timeouts}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#worker_config GoogleCloudbuildWorkerPool#worker_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_config, dict):
            network_config = GoogleCloudbuildWorkerPoolNetworkConfig(**network_config)
        if isinstance(private_service_connect, dict):
            private_service_connect = GoogleCloudbuildWorkerPoolPrivateServiceConnect(**private_service_connect)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudbuildWorkerPoolTimeouts(**timeouts)
        if isinstance(worker_config, dict):
            worker_config = GoogleCloudbuildWorkerPoolWorkerConfig(**worker_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe4c7520556f59ba99c89b5c96c398c2a026423062ac115e95f97c9ff7e598d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#location GoogleCloudbuildWorkerPool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''User-defined name of the ``WorkerPool``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#name GoogleCloudbuildWorkerPool#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#annotations GoogleCloudbuildWorkerPool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-specified, human-readable name for the ``WorkerPool``. If provided, this value must be 1-63 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#display_name GoogleCloudbuildWorkerPool#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#id GoogleCloudbuildWorkerPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildWorkerPoolNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#network_config GoogleCloudbuildWorkerPool#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolNetworkConfig"], result)

    @builtins.property
    def private_service_connect(
        self,
    ) -> typing.Optional["GoogleCloudbuildWorkerPoolPrivateServiceConnect"]:
        '''private_service_connect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#private_service_connect GoogleCloudbuildWorkerPool#private_service_connect}
        '''
        result = self._values.get("private_service_connect")
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolPrivateServiceConnect"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#project GoogleCloudbuildWorkerPool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudbuildWorkerPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#timeouts GoogleCloudbuildWorkerPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolTimeouts"], result)

    @builtins.property
    def worker_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildWorkerPoolWorkerConfig"]:
        '''worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#worker_config GoogleCloudbuildWorkerPool#worker_config}
        '''
        result = self._values.get("worker_config")
        return typing.cast(typing.Optional["GoogleCloudbuildWorkerPoolWorkerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildWorkerPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "peered_network": "peeredNetwork",
        "peered_network_ip_range": "peeredNetworkIpRange",
    },
)
class GoogleCloudbuildWorkerPoolNetworkConfig:
    def __init__(
        self,
        *,
        peered_network: builtins.str,
        peered_network_ip_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peered_network: Required. Immutable. The network definition that the workers are peered to. If this section is left empty, the workers will be peered to ``WorkerPool.project_id`` on the service producer network. Must be in the format ``projects/{project}/global/networks/{network}``, where ``{project}`` is a project number, such as ``12345``, and ``{network}`` is the name of a VPC network in the project. See `Understanding network configuration options <https://cloud.google.com/cloud-build/docs/custom-workers/set-up-custom-worker-pool-environment#understanding_the_network_configuration_options>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#peered_network GoogleCloudbuildWorkerPool#peered_network}
        :param peered_network_ip_range: Optional. Immutable. Subnet IP range within the peered network. This is specified in CIDR notation with a slash and the subnet prefix size. You can optionally specify an IP address before the subnet prefix value. e.g. ``192.168.0.0/29`` would specify an IP range starting at 192.168.0.0 with a prefix size of 29 bits. ``/16`` would specify a prefix size of 16 bits, with an automatically determined IP within the peered VPC. If unspecified, a value of ``/24`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#peered_network_ip_range GoogleCloudbuildWorkerPool#peered_network_ip_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1779f83c427fcfeb7666a2a6630099a36e671b89eb276428e85e421a5f642a0e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#peered_network GoogleCloudbuildWorkerPool#peered_network}
        '''
        result = self._values.get("peered_network")
        assert result is not None, "Required property 'peered_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peered_network_ip_range(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Immutable. Subnet IP range within the peered network. This is specified in CIDR notation with a slash and the subnet prefix size. You can optionally specify an IP address before the subnet prefix value. e.g. ``192.168.0.0/29`` would specify an IP range starting at 192.168.0.0 with a prefix size of 29 bits. ``/16`` would specify a prefix size of 16 bits, with an automatically determined IP within the peered VPC. If unspecified, a value of ``/24`` will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#peered_network_ip_range GoogleCloudbuildWorkerPool#peered_network_ip_range}
        '''
        result = self._values.get("peered_network_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildWorkerPoolNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildWorkerPoolNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__103ae614c4f9bcd34ad409b5a00967063491790e30bae3c0d8ce4e3eacf6f67a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e52b807f9f3bf3d3aa1986d43a509887b1e6d78f3b563379c9b36a0a2c438abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeredNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeredNetworkIpRange")
    def peered_network_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeredNetworkIpRange"))

    @peered_network_ip_range.setter
    def peered_network_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47b5eee55341ec4e77802a7c35e020a3dc17b94f6b3093c05640732e29d023c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeredNetworkIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildWorkerPoolNetworkConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildWorkerPoolNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildWorkerPoolNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e698547656f101169a0ff892325c88b114f00c03e64e6f2d6d1db893ea0126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolPrivateServiceConnect",
    jsii_struct_bases=[],
    name_mapping={
        "network_attachment": "networkAttachment",
        "route_all_traffic": "routeAllTraffic",
    },
)
class GoogleCloudbuildWorkerPoolPrivateServiceConnect:
    def __init__(
        self,
        *,
        network_attachment: builtins.str,
        route_all_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param network_attachment: Required. Immutable. The network attachment that the worker network interface is connected to. Must be in the format ``projects/{project}/regions/{region}/networkAttachments/{networkAttachment}``. The region of network attachment must be the same as the worker pool. See `Network Attachments <https://cloud.google.com/vpc/docs/about-network-attachments>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#network_attachment GoogleCloudbuildWorkerPool#network_attachment}
        :param route_all_traffic: Immutable. Route all traffic through PSC interface. Enable this if you want full control of traffic in the private pool. Configure Cloud NAT for the subnet of network attachment if you need to access public Internet. If false, Only route private IPs, e.g. 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 through PSC interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#route_all_traffic GoogleCloudbuildWorkerPool#route_all_traffic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490ff7cbd7d4fd73ccc570ac1b1a293a90ea7429ce10f2b3c8d5def5ce2e2cd9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#network_attachment GoogleCloudbuildWorkerPool#network_attachment}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#route_all_traffic GoogleCloudbuildWorkerPool#route_all_traffic}
        '''
        result = self._values.get("route_all_traffic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildWorkerPoolPrivateServiceConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildWorkerPoolPrivateServiceConnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolPrivateServiceConnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7453a3885818d4ee9634091cb089676361f375e2ea2d4ecb00951f20221ae289)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15df171b17e707ab1a22c29dcfe5adbc9773a3499ed5ee741b81e9f44d0aa26f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da79e91b89df74c0c7a3826cf66d3f389aaef5f161b2c3ea2f2781a054055ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeAllTraffic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildWorkerPoolPrivateServiceConnect]:
        return typing.cast(typing.Optional[GoogleCloudbuildWorkerPoolPrivateServiceConnect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildWorkerPoolPrivateServiceConnect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669cdd0e42882bfcadbf10f41ec2284ee03cd577e1793981ac7af4d16b245c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudbuildWorkerPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#create GoogleCloudbuildWorkerPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#delete GoogleCloudbuildWorkerPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#update GoogleCloudbuildWorkerPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46bcd2423c8edabac62a935a3ba76d9ed8aa0e99212a7a32bfb5ccbe0ac8a1a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#create GoogleCloudbuildWorkerPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#delete GoogleCloudbuildWorkerPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#update GoogleCloudbuildWorkerPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildWorkerPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildWorkerPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18b04cc05e4200baa25fd258ee0a06dda8858077b4d7d5add26580e31b71a90d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8904d5d54ac89b966ded3f3592aa38a5097989ac861671e8856ea5485fc3c55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df9fa8c5fe1f224ef5c4152d18d626e58a5607528c5729ceb4e26c9740e2ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7aa35dec93669c7f87ac0923cebdca043a16bfc2f94f894e546719f8647429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildWorkerPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildWorkerPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildWorkerPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef93b181f3f003f10016697552b830c9c4e55fba924f87d5c4da17de6f54c8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disk_size_gb": "diskSizeGb",
        "machine_type": "machineType",
        "no_external_ip": "noExternalIp",
    },
)
class GoogleCloudbuildWorkerPoolWorkerConfig:
    def __init__(
        self,
        *,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        no_external_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disk_size_gb: Size of the disk attached to the worker, in GB. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. Specify a value of up to 1000. If ``0`` is specified, Cloud Build will use a standard disk size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#disk_size_gb GoogleCloudbuildWorkerPool#disk_size_gb}
        :param machine_type: Machine type of a worker, such as ``n1-standard-1``. See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. If left blank, Cloud Build will use ``n1-standard-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#machine_type GoogleCloudbuildWorkerPool#machine_type}
        :param no_external_ip: If true, workers are created without any public address, which prevents network egress to public IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#no_external_ip GoogleCloudbuildWorkerPool#no_external_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678dbca53b2acc71b837fb0c62da6014479945238390e7d3a5ff25872546f4f4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#disk_size_gb GoogleCloudbuildWorkerPool#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Machine type of a worker, such as ``n1-standard-1``.

        See `Worker pool config file <https://cloud.google.com/cloud-build/docs/custom-workers/worker-pool-config-file>`_. If left blank, Cloud Build will use ``n1-standard-1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#machine_type GoogleCloudbuildWorkerPool#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_external_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, workers are created without any public address, which prevents network egress to public IPs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_worker_pool#no_external_ip GoogleCloudbuildWorkerPool#no_external_ip}
        '''
        result = self._values.get("no_external_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildWorkerPoolWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildWorkerPoolWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildWorkerPool.GoogleCloudbuildWorkerPoolWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc8a793781315fb214a27fb20285d350555052c374f13cc3bb5e92bcbf709f6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d3e8909ea5def261e90bed5217aa21b783bb78f4ef80d1a5704ab46748bc1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f6f8a620502a8e2a97d936b110cf95c25ffbd23faf382a794324dc9e592710)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23f3e0372707522d85817d741e85f6f4eb4eab46fefb2f4aac3d372ef56c4ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExternalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudbuildWorkerPoolWorkerConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildWorkerPoolWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildWorkerPoolWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5153418febf952541a0a3cb571629b9d52348ae4b84a2dc2260ebfdf8edfd05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudbuildWorkerPool",
    "GoogleCloudbuildWorkerPoolConfig",
    "GoogleCloudbuildWorkerPoolNetworkConfig",
    "GoogleCloudbuildWorkerPoolNetworkConfigOutputReference",
    "GoogleCloudbuildWorkerPoolPrivateServiceConnect",
    "GoogleCloudbuildWorkerPoolPrivateServiceConnectOutputReference",
    "GoogleCloudbuildWorkerPoolTimeouts",
    "GoogleCloudbuildWorkerPoolTimeoutsOutputReference",
    "GoogleCloudbuildWorkerPoolWorkerConfig",
    "GoogleCloudbuildWorkerPoolWorkerConfigOutputReference",
]

publication.publish()

def _typecheckingstub__9366ea34785f78792e9638151e5d824de55cf900bdd1bd51c832bf4f04a82176(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_service_connect: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolPrivateServiceConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_config: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8c27451dfaa2abba79334fa6cd5959b7995befd4c7c5cb9d625e42a2e36e9471(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ace7b7da8788e814b643e052f9c6988953ce095c9717572e6c266dc365c1b5a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02541a250723c780bab205ea4a9fed793ad4cad7dd087677159c9eb060104463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f954feceea24bfa09f40088fc575377ee15a0dc4894be8efab04d8d88943bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0657a99d6184f4e0ff66ff4261a5e776b13e8ffe0c358395e21cac61f42b7d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7642be85d0f15f2804daa285dab88fab79cfb07034185d20512a0add4bda377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73628f9449661e4f9c929e6c66dce1595490b88ad33061d53fc0d702271b94f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe4c7520556f59ba99c89b5c96c398c2a026423062ac115e95f97c9ff7e598d(
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
    network_config: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_service_connect: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolPrivateServiceConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_config: typing.Optional[typing.Union[GoogleCloudbuildWorkerPoolWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1779f83c427fcfeb7666a2a6630099a36e671b89eb276428e85e421a5f642a0e(
    *,
    peered_network: builtins.str,
    peered_network_ip_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103ae614c4f9bcd34ad409b5a00967063491790e30bae3c0d8ce4e3eacf6f67a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52b807f9f3bf3d3aa1986d43a509887b1e6d78f3b563379c9b36a0a2c438abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47b5eee55341ec4e77802a7c35e020a3dc17b94f6b3093c05640732e29d023c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e698547656f101169a0ff892325c88b114f00c03e64e6f2d6d1db893ea0126(
    value: typing.Optional[GoogleCloudbuildWorkerPoolNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490ff7cbd7d4fd73ccc570ac1b1a293a90ea7429ce10f2b3c8d5def5ce2e2cd9(
    *,
    network_attachment: builtins.str,
    route_all_traffic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7453a3885818d4ee9634091cb089676361f375e2ea2d4ecb00951f20221ae289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15df171b17e707ab1a22c29dcfe5adbc9773a3499ed5ee741b81e9f44d0aa26f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da79e91b89df74c0c7a3826cf66d3f389aaef5f161b2c3ea2f2781a054055ce5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669cdd0e42882bfcadbf10f41ec2284ee03cd577e1793981ac7af4d16b245c00(
    value: typing.Optional[GoogleCloudbuildWorkerPoolPrivateServiceConnect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46bcd2423c8edabac62a935a3ba76d9ed8aa0e99212a7a32bfb5ccbe0ac8a1a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b04cc05e4200baa25fd258ee0a06dda8858077b4d7d5add26580e31b71a90d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8904d5d54ac89b966ded3f3592aa38a5097989ac861671e8856ea5485fc3c55f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df9fa8c5fe1f224ef5c4152d18d626e58a5607528c5729ceb4e26c9740e2ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7aa35dec93669c7f87ac0923cebdca043a16bfc2f94f894e546719f8647429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef93b181f3f003f10016697552b830c9c4e55fba924f87d5c4da17de6f54c8ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildWorkerPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678dbca53b2acc71b837fb0c62da6014479945238390e7d3a5ff25872546f4f4(
    *,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    machine_type: typing.Optional[builtins.str] = None,
    no_external_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8a793781315fb214a27fb20285d350555052c374f13cc3bb5e92bcbf709f6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3e8909ea5def261e90bed5217aa21b783bb78f4ef80d1a5704ab46748bc1c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f6f8a620502a8e2a97d936b110cf95c25ffbd23faf382a794324dc9e592710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f3e0372707522d85817d741e85f6f4eb4eab46fefb2f4aac3d372ef56c4ff2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5153418febf952541a0a3cb571629b9d52348ae4b84a2dc2260ebfdf8edfd05(
    value: typing.Optional[GoogleCloudbuildWorkerPoolWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass
