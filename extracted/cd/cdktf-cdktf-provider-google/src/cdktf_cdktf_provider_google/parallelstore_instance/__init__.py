r'''
# `google_parallelstore_instance`

Refer to the Terraform Registry for docs: [`google_parallelstore_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance).
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


class ParallelstoreInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.parallelstoreInstance.ParallelstoreInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance google_parallelstore_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity_gib: builtins.str,
        instance_id: builtins.str,
        location: builtins.str,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        directory_stripe_level: typing.Optional[builtins.str] = None,
        file_stripe_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ParallelstoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance google_parallelstore_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_gib: Required. Immutable. Storage capacity of Parallelstore instance in Gibibytes (GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#capacity_gib ParallelstoreInstance#capacity_gib}
        :param instance_id: The logical name of the Parallelstore instance in the user project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the customer project/ location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#instance_id ParallelstoreInstance#instance_id}
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#location ParallelstoreInstance#location}
        :param deployment_type: Parallelstore Instance deployment type. Possible values: DEPLOYMENT_TYPE_UNSPECIFIED SCRATCH PERSISTENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#deployment_type ParallelstoreInstance#deployment_type}
        :param description: The description of the instance. 2048 characters or less. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#description ParallelstoreInstance#description}
        :param directory_stripe_level: Stripe level for directories. MIN when directory has a small number of files. MAX when directory has a large number of files. Possible values: DIRECTORY_STRIPE_LEVEL_UNSPECIFIED DIRECTORY_STRIPE_LEVEL_MIN DIRECTORY_STRIPE_LEVEL_BALANCED DIRECTORY_STRIPE_LEVEL_MAX Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#directory_stripe_level ParallelstoreInstance#directory_stripe_level}
        :param file_stripe_level: Stripe level for files. MIN better suited for small size files. MAX higher throughput performance for larger files. Possible values: FILE_STRIPE_LEVEL_UNSPECIFIED FILE_STRIPE_LEVEL_MIN FILE_STRIPE_LEVEL_BALANCED FILE_STRIPE_LEVEL_MAX Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#file_stripe_level ParallelstoreInstance#file_stripe_level}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#id ParallelstoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Cloud Labels are a flexible and lightweight mechanism for organizing cloud resources into groups that reflect a customer's organizational needs and deployment strategies. Cloud Labels can be used to filter collections of resources. They can be used to control how resource metrics are aggregated. And they can be used as arguments to policy management rules (e.g. route, firewall, load balancing, etc.). - Label keys must be between 1 and 63 characters long and must conform to the following regular expression: 'a-z{0,62}'. - Label values must be between 0 and 63 characters long and must conform to the regular expression '[a-z0-9_-]{0,63}'. - No more than 64 labels can be associated with a given resource. See https://goo.gl/xmQnxf for more information on and examples of labels. If you plan to use labels in your own code, please note that additional characters may be allowed in the future. Therefore, you are advised to use an internal label representation, such as JSON, which doesn't rely upon specific characters being disallowed. For example, representing labels as the string: 'name + "*" + value' would prove problematic if we were to allow '"*"' in a future release. " **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#labels ParallelstoreInstance#labels}
        :param network: Immutable. The name of the Google Compute Engine `VPC network <https://cloud.google.com/vpc/docs/vpc>`_ to which the instance is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#network ParallelstoreInstance#network}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#project ParallelstoreInstance#project}.
        :param reserved_ip_range: Immutable. Contains the id of the allocated IP address range associated with the private service access connection for example, "test-default" associated with IP range 10.0.0.0/29. If no range id is provided all ranges will be considered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#reserved_ip_range ParallelstoreInstance#reserved_ip_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#timeouts ParallelstoreInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0658fc55748f62b3a29bb33fa1b0c8f3a1ee50e22584964eaa9bd32d58437549)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ParallelstoreInstanceConfig(
            capacity_gib=capacity_gib,
            instance_id=instance_id,
            location=location,
            deployment_type=deployment_type,
            description=description,
            directory_stripe_level=directory_stripe_level,
            file_stripe_level=file_stripe_level,
            id=id,
            labels=labels,
            network=network,
            project=project,
            reserved_ip_range=reserved_ip_range,
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
        '''Generates CDKTF code for importing a ParallelstoreInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ParallelstoreInstance to import.
        :param import_from_id: The id of the existing ParallelstoreInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ParallelstoreInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6290aa74dbd502482dbfd87c0c89039460e8b881b7a4d0979da7b9e6e2bc8d7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#create ParallelstoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#delete ParallelstoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#update ParallelstoreInstance#update}.
        '''
        value = ParallelstoreInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeploymentType")
    def reset_deployment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDirectoryStripeLevel")
    def reset_directory_stripe_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryStripeLevel", []))

    @jsii.member(jsii_name="resetFileStripeLevel")
    def reset_file_stripe_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileStripeLevel", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReservedIpRange")
    def reset_reserved_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRange", []))

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
    @jsii.member(jsii_name="accessPoints")
    def access_points(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessPoints"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="daosVersion")
    def daos_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "daosVersion"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="effectiveReservedIpRange")
    def effective_reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveReservedIpRange"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ParallelstoreInstanceTimeoutsOutputReference":
        return typing.cast("ParallelstoreInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="capacityGibInput")
    def capacity_gib_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityGibInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTypeInput")
    def deployment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryStripeLevelInput")
    def directory_stripe_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryStripeLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="fileStripeLevelInput")
    def file_stripe_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileStripeLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

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
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangeInput")
    def reserved_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ParallelstoreInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ParallelstoreInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityGib")
    def capacity_gib(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityGib"))

    @capacity_gib.setter
    def capacity_gib(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffcefaece4aeb46e267e88b0da9abe201becba116f278857781202a8de1741e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0380cdd8c1a653be49b6f6fe88676e9615dd8b33d8039960ab27e39c8f7550b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c34efd6d96ab0a8199c966b29d1fdc83d54552405831189c9681be499e83c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryStripeLevel")
    def directory_stripe_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryStripeLevel"))

    @directory_stripe_level.setter
    def directory_stripe_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3ae6287b07e99b66a5188f9817d9f72c7d6158286a3200820888c7398939e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryStripeLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileStripeLevel")
    def file_stripe_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileStripeLevel"))

    @file_stripe_level.setter
    def file_stripe_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553bafb5082b0372e1b6b99e3721f1c9317002cbc714b1b66964eb74b600b078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileStripeLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df4b116728426733775bb6c4dd7fdd4e2248f7e51bcebf9219a3569858de0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8648c99fb5a4f6ba0c24e2199b656a6b23933a10d01e40919e6ffd24183d6477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fff5810a58b93df61ff334368379b7eb728c84bb808e54ed689ab9b842c256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d4297a65a67fec75946371795e01a70ad8eff473b2f455506a57530389123d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1427f19070a184d90fce7a2e7475642865689b9f20b7722a9119de2c3fb079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2038abd0ee09b9fa66430273d2301f7f7d5eda8ac2c6ab74238478b7ac476c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRange")
    def reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedIpRange"))

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efef7189d368e7aca72b183333eaebcf6f1330c43b7d70705ff04d80e06a42f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRange", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.parallelstoreInstance.ParallelstoreInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capacity_gib": "capacityGib",
        "instance_id": "instanceId",
        "location": "location",
        "deployment_type": "deploymentType",
        "description": "description",
        "directory_stripe_level": "directoryStripeLevel",
        "file_stripe_level": "fileStripeLevel",
        "id": "id",
        "labels": "labels",
        "network": "network",
        "project": "project",
        "reserved_ip_range": "reservedIpRange",
        "timeouts": "timeouts",
    },
)
class ParallelstoreInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_gib: builtins.str,
        instance_id: builtins.str,
        location: builtins.str,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        directory_stripe_level: typing.Optional[builtins.str] = None,
        file_stripe_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ParallelstoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity_gib: Required. Immutable. Storage capacity of Parallelstore instance in Gibibytes (GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#capacity_gib ParallelstoreInstance#capacity_gib}
        :param instance_id: The logical name of the Parallelstore instance in the user project with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the customer project/ location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#instance_id ParallelstoreInstance#instance_id}
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#location ParallelstoreInstance#location}
        :param deployment_type: Parallelstore Instance deployment type. Possible values: DEPLOYMENT_TYPE_UNSPECIFIED SCRATCH PERSISTENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#deployment_type ParallelstoreInstance#deployment_type}
        :param description: The description of the instance. 2048 characters or less. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#description ParallelstoreInstance#description}
        :param directory_stripe_level: Stripe level for directories. MIN when directory has a small number of files. MAX when directory has a large number of files. Possible values: DIRECTORY_STRIPE_LEVEL_UNSPECIFIED DIRECTORY_STRIPE_LEVEL_MIN DIRECTORY_STRIPE_LEVEL_BALANCED DIRECTORY_STRIPE_LEVEL_MAX Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#directory_stripe_level ParallelstoreInstance#directory_stripe_level}
        :param file_stripe_level: Stripe level for files. MIN better suited for small size files. MAX higher throughput performance for larger files. Possible values: FILE_STRIPE_LEVEL_UNSPECIFIED FILE_STRIPE_LEVEL_MIN FILE_STRIPE_LEVEL_BALANCED FILE_STRIPE_LEVEL_MAX Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#file_stripe_level ParallelstoreInstance#file_stripe_level}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#id ParallelstoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Cloud Labels are a flexible and lightweight mechanism for organizing cloud resources into groups that reflect a customer's organizational needs and deployment strategies. Cloud Labels can be used to filter collections of resources. They can be used to control how resource metrics are aggregated. And they can be used as arguments to policy management rules (e.g. route, firewall, load balancing, etc.). - Label keys must be between 1 and 63 characters long and must conform to the following regular expression: 'a-z{0,62}'. - Label values must be between 0 and 63 characters long and must conform to the regular expression '[a-z0-9_-]{0,63}'. - No more than 64 labels can be associated with a given resource. See https://goo.gl/xmQnxf for more information on and examples of labels. If you plan to use labels in your own code, please note that additional characters may be allowed in the future. Therefore, you are advised to use an internal label representation, such as JSON, which doesn't rely upon specific characters being disallowed. For example, representing labels as the string: 'name + "*" + value' would prove problematic if we were to allow '"*"' in a future release. " **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#labels ParallelstoreInstance#labels}
        :param network: Immutable. The name of the Google Compute Engine `VPC network <https://cloud.google.com/vpc/docs/vpc>`_ to which the instance is connected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#network ParallelstoreInstance#network}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#project ParallelstoreInstance#project}.
        :param reserved_ip_range: Immutable. Contains the id of the allocated IP address range associated with the private service access connection for example, "test-default" associated with IP range 10.0.0.0/29. If no range id is provided all ranges will be considered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#reserved_ip_range ParallelstoreInstance#reserved_ip_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#timeouts ParallelstoreInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ParallelstoreInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e276658afebcd45d441d7ca3abce3bca3ab78f536eb7874e61770c4e6fd37c9f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity_gib", value=capacity_gib, expected_type=type_hints["capacity_gib"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument directory_stripe_level", value=directory_stripe_level, expected_type=type_hints["directory_stripe_level"])
            check_type(argname="argument file_stripe_level", value=file_stripe_level, expected_type=type_hints["file_stripe_level"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reserved_ip_range", value=reserved_ip_range, expected_type=type_hints["reserved_ip_range"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_gib": capacity_gib,
            "instance_id": instance_id,
            "location": location,
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
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type
        if description is not None:
            self._values["description"] = description
        if directory_stripe_level is not None:
            self._values["directory_stripe_level"] = directory_stripe_level
        if file_stripe_level is not None:
            self._values["file_stripe_level"] = file_stripe_level
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if network is not None:
            self._values["network"] = network
        if project is not None:
            self._values["project"] = project
        if reserved_ip_range is not None:
            self._values["reserved_ip_range"] = reserved_ip_range
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
    def capacity_gib(self) -> builtins.str:
        '''Required. Immutable. Storage capacity of Parallelstore instance in Gibibytes (GiB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#capacity_gib ParallelstoreInstance#capacity_gib}
        '''
        result = self._values.get("capacity_gib")
        assert result is not None, "Required property 'capacity_gib' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The logical name of the Parallelstore instance in the user project with the following restrictions:   * Must contain only lowercase letters, numbers, and hyphens.

        - Must start with a letter.

          - Must be between 1-63 characters.
          - Must end with a number or a letter.
          - Must be unique within the customer project/ location

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#instance_id ParallelstoreInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Part of 'parent'. See documentation of 'projectsId'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#location ParallelstoreInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Parallelstore Instance deployment type.   Possible values:   DEPLOYMENT_TYPE_UNSPECIFIED   SCRATCH   PERSISTENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#deployment_type ParallelstoreInstance#deployment_type}
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the instance. 2048 characters or less.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#description ParallelstoreInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_stripe_level(self) -> typing.Optional[builtins.str]:
        '''Stripe level for directories.

        MIN when directory has a small number of files.
        MAX when directory has a large number of files.
        Possible values:
        DIRECTORY_STRIPE_LEVEL_UNSPECIFIED
        DIRECTORY_STRIPE_LEVEL_MIN
        DIRECTORY_STRIPE_LEVEL_BALANCED
        DIRECTORY_STRIPE_LEVEL_MAX

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#directory_stripe_level ParallelstoreInstance#directory_stripe_level}
        '''
        result = self._values.get("directory_stripe_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_stripe_level(self) -> typing.Optional[builtins.str]:
        '''Stripe level for files.

        MIN better suited for small size files.
        MAX higher throughput performance for larger files.
        Possible values:
        FILE_STRIPE_LEVEL_UNSPECIFIED
        FILE_STRIPE_LEVEL_MIN
        FILE_STRIPE_LEVEL_BALANCED
        FILE_STRIPE_LEVEL_MAX

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#file_stripe_level ParallelstoreInstance#file_stripe_level}
        '''
        result = self._values.get("file_stripe_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#id ParallelstoreInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Cloud Labels are a flexible and lightweight mechanism for organizing cloud resources into groups that reflect a customer's organizational needs and deployment strategies.

        Cloud Labels can be used to filter collections
        of resources. They can be used to control how resource metrics are aggregated.
        And they can be used as arguments to policy management rules (e.g. route, firewall,
        load balancing, etc.).

        - Label keys must be between 1 and 63 characters long and must conform to
          the following regular expression: 'a-z{0,62}'.
        - Label values must be between 0 and 63 characters long and must conform
          to the regular expression '[a-z0-9_-]{0,63}'.
        - No more than 64 labels can be associated with a given resource.

        See https://goo.gl/xmQnxf for more information on and examples of labels.

        If you plan to use labels in your own code, please note that additional
        characters may be allowed in the future. Therefore, you are advised to use
        an internal label representation, such as JSON, which doesn't rely upon
        specific characters being disallowed.  For example, representing labels
        as the string:  'name + "*" + value' would prove problematic if we were to
        allow '"*"' in a future release. "

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#labels ParallelstoreInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Immutable. The name of the Google Compute Engine `VPC network <https://cloud.google.com/vpc/docs/vpc>`_ to which the instance is connected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#network ParallelstoreInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#project ParallelstoreInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_range(self) -> typing.Optional[builtins.str]:
        '''Immutable.

        Contains the id of the allocated IP address range
        associated with the private service access connection for example, "test-default"
        associated with IP range 10.0.0.0/29. If no range id is provided all ranges will
        be considered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#reserved_ip_range ParallelstoreInstance#reserved_ip_range}
        '''
        result = self._values.get("reserved_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ParallelstoreInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#timeouts ParallelstoreInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ParallelstoreInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParallelstoreInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.parallelstoreInstance.ParallelstoreInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ParallelstoreInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#create ParallelstoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#delete ParallelstoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#update ParallelstoreInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b306f90bf29f5eddf66049963492ade1d2d60455189b08d209ae647f5654a1b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#create ParallelstoreInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#delete ParallelstoreInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/parallelstore_instance#update ParallelstoreInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParallelstoreInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ParallelstoreInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.parallelstoreInstance.ParallelstoreInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ddf80cf6bf37db96cb55668b7281d5442fd31f736de381f8ebf1cc571f86fd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480f194a70b7891d04a738f145b4128e501e85d960a1cf6de9901ebb411ee7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a816af8ba07d9b267cf91b354e38cf05c50773e9c3c877fef482f15d918ce546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9086073aed2088be34b5a6b7c8effeb24cca6bd807cd5419d6fac7146142f9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ParallelstoreInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ParallelstoreInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ParallelstoreInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4674daf02acfe39cca9626bf7532cbd50884c42b67b7d19825f311419516ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ParallelstoreInstance",
    "ParallelstoreInstanceConfig",
    "ParallelstoreInstanceTimeouts",
    "ParallelstoreInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0658fc55748f62b3a29bb33fa1b0c8f3a1ee50e22584964eaa9bd32d58437549(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_gib: builtins.str,
    instance_id: builtins.str,
    location: builtins.str,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    directory_stripe_level: typing.Optional[builtins.str] = None,
    file_stripe_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ParallelstoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6290aa74dbd502482dbfd87c0c89039460e8b881b7a4d0979da7b9e6e2bc8d7a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffcefaece4aeb46e267e88b0da9abe201becba116f278857781202a8de1741e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0380cdd8c1a653be49b6f6fe88676e9615dd8b33d8039960ab27e39c8f7550b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c34efd6d96ab0a8199c966b29d1fdc83d54552405831189c9681be499e83c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3ae6287b07e99b66a5188f9817d9f72c7d6158286a3200820888c7398939e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553bafb5082b0372e1b6b99e3721f1c9317002cbc714b1b66964eb74b600b078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df4b116728426733775bb6c4dd7fdd4e2248f7e51bcebf9219a3569858de0c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8648c99fb5a4f6ba0c24e2199b656a6b23933a10d01e40919e6ffd24183d6477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fff5810a58b93df61ff334368379b7eb728c84bb808e54ed689ab9b842c256(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d4297a65a67fec75946371795e01a70ad8eff473b2f455506a57530389123d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1427f19070a184d90fce7a2e7475642865689b9f20b7722a9119de2c3fb079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2038abd0ee09b9fa66430273d2301f7f7d5eda8ac2c6ab74238478b7ac476c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efef7189d368e7aca72b183333eaebcf6f1330c43b7d70705ff04d80e06a42f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e276658afebcd45d441d7ca3abce3bca3ab78f536eb7874e61770c4e6fd37c9f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_gib: builtins.str,
    instance_id: builtins.str,
    location: builtins.str,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    directory_stripe_level: typing.Optional[builtins.str] = None,
    file_stripe_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ParallelstoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b306f90bf29f5eddf66049963492ade1d2d60455189b08d209ae647f5654a1b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddf80cf6bf37db96cb55668b7281d5442fd31f736de381f8ebf1cc571f86fd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480f194a70b7891d04a738f145b4128e501e85d960a1cf6de9901ebb411ee7ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a816af8ba07d9b267cf91b354e38cf05c50773e9c3c877fef482f15d918ce546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9086073aed2088be34b5a6b7c8effeb24cca6bd807cd5419d6fac7146142f9de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4674daf02acfe39cca9626bf7532cbd50884c42b67b7d19825f311419516ec5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ParallelstoreInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
