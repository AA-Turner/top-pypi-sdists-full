r'''
# `google_bigtable_app_profile`

Refer to the Terraform Registry for docs: [`google_bigtable_app_profile`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile).
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


class GoogleBigtableAppProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile google_bigtable_app_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_profile_id: builtins.str,
        data_boost_isolation_read_only: typing.Optional[typing.Union["GoogleBigtableAppProfileDataBoostIsolationReadOnly", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instance: typing.Optional[builtins.str] = None,
        multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        row_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        single_cluster_routing: typing.Optional[typing.Union["GoogleBigtableAppProfileSingleClusterRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        standard_isolation: typing.Optional[typing.Union["GoogleBigtableAppProfileStandardIsolation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigtableAppProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile google_bigtable_app_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_profile_id: The unique name of the app profile in the form '[*a-zA-Z0-9][-*.a-zA-Z0-9]*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#app_profile_id GoogleBigtableAppProfile#app_profile_id}
        :param data_boost_isolation_read_only: data_boost_isolation_read_only block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#data_boost_isolation_read_only GoogleBigtableAppProfile#data_boost_isolation_read_only}
        :param description: Long form description of the use case for this app profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#description GoogleBigtableAppProfile#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#id GoogleBigtableAppProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_warnings: If true, ignore safety checks when deleting/updating the app profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#ignore_warnings GoogleBigtableAppProfile#ignore_warnings}
        :param instance: The name of the instance to create the app profile within. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#instance GoogleBigtableAppProfile#instance}
        :param multi_cluster_routing_cluster_ids: The set of clusters to route to. The order is ignored; clusters will be tried in order of distance. If left empty, all clusters are eligible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#multi_cluster_routing_cluster_ids GoogleBigtableAppProfile#multi_cluster_routing_cluster_ids}
        :param multi_cluster_routing_use_any: If true, read/write requests are routed to the nearest cluster in the instance, and will fail over to the nearest cluster that is available in the event of transient errors or delays. Clusters in a region are considered equidistant. Choosing this option sacrifices read-your-writes consistency to improve availability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#multi_cluster_routing_use_any GoogleBigtableAppProfile#multi_cluster_routing_use_any}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#project GoogleBigtableAppProfile#project}.
        :param row_affinity: Must be used with multi-cluster routing. If true, then this app profile will use row affinity sticky routing. With row affinity, Bigtable will route single row key requests based on the row key, rather than randomly. Instead, each row key will be assigned to a cluster by Cloud Bigtable, and will stick to that cluster. Choosing this option improves read-your-writes consistency for most requests under most circumstances, without sacrificing availability. Consistency is not guaranteed, as requests may still fail over between clusters in the event of errors or latency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#row_affinity GoogleBigtableAppProfile#row_affinity}
        :param single_cluster_routing: single_cluster_routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#single_cluster_routing GoogleBigtableAppProfile#single_cluster_routing}
        :param standard_isolation: standard_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#standard_isolation GoogleBigtableAppProfile#standard_isolation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#timeouts GoogleBigtableAppProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31e6c1dd88227c70950c77c8b7b4d37ad39018aeb3010f1110a948debec6497)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigtableAppProfileConfig(
            app_profile_id=app_profile_id,
            data_boost_isolation_read_only=data_boost_isolation_read_only,
            description=description,
            id=id,
            ignore_warnings=ignore_warnings,
            instance=instance,
            multi_cluster_routing_cluster_ids=multi_cluster_routing_cluster_ids,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            project=project,
            row_affinity=row_affinity,
            single_cluster_routing=single_cluster_routing,
            standard_isolation=standard_isolation,
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
        '''Generates CDKTF code for importing a GoogleBigtableAppProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBigtableAppProfile to import.
        :param import_from_id: The id of the existing GoogleBigtableAppProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBigtableAppProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9cf0d8ddcf46a2342c6589d011e91f16328b884f5a1d6cf394d3b74e4bed22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataBoostIsolationReadOnly")
    def put_data_boost_isolation_read_only(
        self,
        *,
        compute_billing_owner: builtins.str,
    ) -> None:
        '''
        :param compute_billing_owner: The Compute Billing Owner for this Data Boost App Profile. Possible values: ["HOST_PAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#compute_billing_owner GoogleBigtableAppProfile#compute_billing_owner}
        '''
        value = GoogleBigtableAppProfileDataBoostIsolationReadOnly(
            compute_billing_owner=compute_billing_owner
        )

        return typing.cast(None, jsii.invoke(self, "putDataBoostIsolationReadOnly", [value]))

    @jsii.member(jsii_name="putSingleClusterRouting")
    def put_single_cluster_routing(
        self,
        *,
        cluster_id: builtins.str,
        allow_transactional_writes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_id: The cluster to which read/write requests should be routed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#cluster_id GoogleBigtableAppProfile#cluster_id}
        :param allow_transactional_writes: If true, CheckAndMutateRow and ReadModifyWriteRow requests are allowed by this app profile. It is unsafe to send these requests to the same table/row/column in multiple clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#allow_transactional_writes GoogleBigtableAppProfile#allow_transactional_writes}
        '''
        value = GoogleBigtableAppProfileSingleClusterRouting(
            cluster_id=cluster_id,
            allow_transactional_writes=allow_transactional_writes,
        )

        return typing.cast(None, jsii.invoke(self, "putSingleClusterRouting", [value]))

    @jsii.member(jsii_name="putStandardIsolation")
    def put_standard_isolation(self, *, priority: builtins.str) -> None:
        '''
        :param priority: The priority of requests sent using this app profile. Possible values: ["PRIORITY_LOW", "PRIORITY_MEDIUM", "PRIORITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#priority GoogleBigtableAppProfile#priority}
        '''
        value = GoogleBigtableAppProfileStandardIsolation(priority=priority)

        return typing.cast(None, jsii.invoke(self, "putStandardIsolation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#create GoogleBigtableAppProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#delete GoogleBigtableAppProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#update GoogleBigtableAppProfile#update}.
        '''
        value = GoogleBigtableAppProfileTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataBoostIsolationReadOnly")
    def reset_data_boost_isolation_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataBoostIsolationReadOnly", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreWarnings")
    def reset_ignore_warnings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreWarnings", []))

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetMultiClusterRoutingClusterIds")
    def reset_multi_cluster_routing_cluster_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiClusterRoutingClusterIds", []))

    @jsii.member(jsii_name="resetMultiClusterRoutingUseAny")
    def reset_multi_cluster_routing_use_any(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiClusterRoutingUseAny", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRowAffinity")
    def reset_row_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowAffinity", []))

    @jsii.member(jsii_name="resetSingleClusterRouting")
    def reset_single_cluster_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleClusterRouting", []))

    @jsii.member(jsii_name="resetStandardIsolation")
    def reset_standard_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandardIsolation", []))

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
    @jsii.member(jsii_name="dataBoostIsolationReadOnly")
    def data_boost_isolation_read_only(
        self,
    ) -> "GoogleBigtableAppProfileDataBoostIsolationReadOnlyOutputReference":
        return typing.cast("GoogleBigtableAppProfileDataBoostIsolationReadOnlyOutputReference", jsii.get(self, "dataBoostIsolationReadOnly"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="singleClusterRouting")
    def single_cluster_routing(
        self,
    ) -> "GoogleBigtableAppProfileSingleClusterRoutingOutputReference":
        return typing.cast("GoogleBigtableAppProfileSingleClusterRoutingOutputReference", jsii.get(self, "singleClusterRouting"))

    @builtins.property
    @jsii.member(jsii_name="standardIsolation")
    def standard_isolation(
        self,
    ) -> "GoogleBigtableAppProfileStandardIsolationOutputReference":
        return typing.cast("GoogleBigtableAppProfileStandardIsolationOutputReference", jsii.get(self, "standardIsolation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBigtableAppProfileTimeoutsOutputReference":
        return typing.cast("GoogleBigtableAppProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appProfileIdInput")
    def app_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataBoostIsolationReadOnlyInput")
    def data_boost_isolation_read_only_input(
        self,
    ) -> typing.Optional["GoogleBigtableAppProfileDataBoostIsolationReadOnly"]:
        return typing.cast(typing.Optional["GoogleBigtableAppProfileDataBoostIsolationReadOnly"], jsii.get(self, "dataBoostIsolationReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreWarningsInput")
    def ignore_warnings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreWarningsInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingClusterIdsInput")
    def multi_cluster_routing_cluster_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "multiClusterRoutingClusterIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingUseAnyInput")
    def multi_cluster_routing_use_any_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multiClusterRoutingUseAnyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rowAffinityInput")
    def row_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rowAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="singleClusterRoutingInput")
    def single_cluster_routing_input(
        self,
    ) -> typing.Optional["GoogleBigtableAppProfileSingleClusterRouting"]:
        return typing.cast(typing.Optional["GoogleBigtableAppProfileSingleClusterRouting"], jsii.get(self, "singleClusterRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="standardIsolationInput")
    def standard_isolation_input(
        self,
    ) -> typing.Optional["GoogleBigtableAppProfileStandardIsolation"]:
        return typing.cast(typing.Optional["GoogleBigtableAppProfileStandardIsolation"], jsii.get(self, "standardIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigtableAppProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigtableAppProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="appProfileId")
    def app_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appProfileId"))

    @app_profile_id.setter
    def app_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f775aa0ca76fbec02fb44439bc22597388f9b4884b410dce1a87582b31fedd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec2acaa024e5191886ae9c1ab708c072a8392879d4d9b55e771da088ba006ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8209646eef9c21964a23992dd2ecc4d01bb29d70b1de081c63120e90b54b26f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreWarnings")
    def ignore_warnings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreWarnings"))

    @ignore_warnings.setter
    def ignore_warnings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19ef89c2d24ff513193d7ecbd4fbfb3bff73acbb2057d33834474350131695c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreWarnings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c150bf18c198baa068b62297f4d590330167331f6fb44dbbdb5e1e6f3a8a4f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingClusterIds")
    def multi_cluster_routing_cluster_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "multiClusterRoutingClusterIds"))

    @multi_cluster_routing_cluster_ids.setter
    def multi_cluster_routing_cluster_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55faf66e1ffc5f74cd61d90eee62d1de71170516d01225aadfd26c0df095d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiClusterRoutingClusterIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingUseAny")
    def multi_cluster_routing_use_any(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multiClusterRoutingUseAny"))

    @multi_cluster_routing_use_any.setter
    def multi_cluster_routing_use_any(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5a9be0fdee18b7e32825a2ee83e61c47d7e8e98a5eb1b37ed6d25d55376194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiClusterRoutingUseAny", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd7b1ed3bc918ec1389b6357ab7af84322741c894061b01ef7224aa90a2b7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowAffinity")
    def row_affinity(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rowAffinity"))

    @row_affinity.setter
    def row_affinity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9996fbcd5540c8bb650c14ec53546c95858e31b5b259f7c0a9079a3a2620540b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowAffinity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_profile_id": "appProfileId",
        "data_boost_isolation_read_only": "dataBoostIsolationReadOnly",
        "description": "description",
        "id": "id",
        "ignore_warnings": "ignoreWarnings",
        "instance": "instance",
        "multi_cluster_routing_cluster_ids": "multiClusterRoutingClusterIds",
        "multi_cluster_routing_use_any": "multiClusterRoutingUseAny",
        "project": "project",
        "row_affinity": "rowAffinity",
        "single_cluster_routing": "singleClusterRouting",
        "standard_isolation": "standardIsolation",
        "timeouts": "timeouts",
    },
)
class GoogleBigtableAppProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_profile_id: builtins.str,
        data_boost_isolation_read_only: typing.Optional[typing.Union["GoogleBigtableAppProfileDataBoostIsolationReadOnly", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instance: typing.Optional[builtins.str] = None,
        multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        row_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        single_cluster_routing: typing.Optional[typing.Union["GoogleBigtableAppProfileSingleClusterRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        standard_isolation: typing.Optional[typing.Union["GoogleBigtableAppProfileStandardIsolation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigtableAppProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_profile_id: The unique name of the app profile in the form '[*a-zA-Z0-9][-*.a-zA-Z0-9]*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#app_profile_id GoogleBigtableAppProfile#app_profile_id}
        :param data_boost_isolation_read_only: data_boost_isolation_read_only block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#data_boost_isolation_read_only GoogleBigtableAppProfile#data_boost_isolation_read_only}
        :param description: Long form description of the use case for this app profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#description GoogleBigtableAppProfile#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#id GoogleBigtableAppProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_warnings: If true, ignore safety checks when deleting/updating the app profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#ignore_warnings GoogleBigtableAppProfile#ignore_warnings}
        :param instance: The name of the instance to create the app profile within. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#instance GoogleBigtableAppProfile#instance}
        :param multi_cluster_routing_cluster_ids: The set of clusters to route to. The order is ignored; clusters will be tried in order of distance. If left empty, all clusters are eligible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#multi_cluster_routing_cluster_ids GoogleBigtableAppProfile#multi_cluster_routing_cluster_ids}
        :param multi_cluster_routing_use_any: If true, read/write requests are routed to the nearest cluster in the instance, and will fail over to the nearest cluster that is available in the event of transient errors or delays. Clusters in a region are considered equidistant. Choosing this option sacrifices read-your-writes consistency to improve availability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#multi_cluster_routing_use_any GoogleBigtableAppProfile#multi_cluster_routing_use_any}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#project GoogleBigtableAppProfile#project}.
        :param row_affinity: Must be used with multi-cluster routing. If true, then this app profile will use row affinity sticky routing. With row affinity, Bigtable will route single row key requests based on the row key, rather than randomly. Instead, each row key will be assigned to a cluster by Cloud Bigtable, and will stick to that cluster. Choosing this option improves read-your-writes consistency for most requests under most circumstances, without sacrificing availability. Consistency is not guaranteed, as requests may still fail over between clusters in the event of errors or latency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#row_affinity GoogleBigtableAppProfile#row_affinity}
        :param single_cluster_routing: single_cluster_routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#single_cluster_routing GoogleBigtableAppProfile#single_cluster_routing}
        :param standard_isolation: standard_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#standard_isolation GoogleBigtableAppProfile#standard_isolation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#timeouts GoogleBigtableAppProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_boost_isolation_read_only, dict):
            data_boost_isolation_read_only = GoogleBigtableAppProfileDataBoostIsolationReadOnly(**data_boost_isolation_read_only)
        if isinstance(single_cluster_routing, dict):
            single_cluster_routing = GoogleBigtableAppProfileSingleClusterRouting(**single_cluster_routing)
        if isinstance(standard_isolation, dict):
            standard_isolation = GoogleBigtableAppProfileStandardIsolation(**standard_isolation)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigtableAppProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0bdfbaf6a42f9ac97174ff7d1dc90b995082735c90e8996f76f95889d43761)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_profile_id", value=app_profile_id, expected_type=type_hints["app_profile_id"])
            check_type(argname="argument data_boost_isolation_read_only", value=data_boost_isolation_read_only, expected_type=type_hints["data_boost_isolation_read_only"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_warnings", value=ignore_warnings, expected_type=type_hints["ignore_warnings"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument multi_cluster_routing_cluster_ids", value=multi_cluster_routing_cluster_ids, expected_type=type_hints["multi_cluster_routing_cluster_ids"])
            check_type(argname="argument multi_cluster_routing_use_any", value=multi_cluster_routing_use_any, expected_type=type_hints["multi_cluster_routing_use_any"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument row_affinity", value=row_affinity, expected_type=type_hints["row_affinity"])
            check_type(argname="argument single_cluster_routing", value=single_cluster_routing, expected_type=type_hints["single_cluster_routing"])
            check_type(argname="argument standard_isolation", value=standard_isolation, expected_type=type_hints["standard_isolation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_profile_id": app_profile_id,
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
        if data_boost_isolation_read_only is not None:
            self._values["data_boost_isolation_read_only"] = data_boost_isolation_read_only
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ignore_warnings is not None:
            self._values["ignore_warnings"] = ignore_warnings
        if instance is not None:
            self._values["instance"] = instance
        if multi_cluster_routing_cluster_ids is not None:
            self._values["multi_cluster_routing_cluster_ids"] = multi_cluster_routing_cluster_ids
        if multi_cluster_routing_use_any is not None:
            self._values["multi_cluster_routing_use_any"] = multi_cluster_routing_use_any
        if project is not None:
            self._values["project"] = project
        if row_affinity is not None:
            self._values["row_affinity"] = row_affinity
        if single_cluster_routing is not None:
            self._values["single_cluster_routing"] = single_cluster_routing
        if standard_isolation is not None:
            self._values["standard_isolation"] = standard_isolation
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
    def app_profile_id(self) -> builtins.str:
        '''The unique name of the app profile in the form '[*a-zA-Z0-9][-*.a-zA-Z0-9]*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#app_profile_id GoogleBigtableAppProfile#app_profile_id}
        '''
        result = self._values.get("app_profile_id")
        assert result is not None, "Required property 'app_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_boost_isolation_read_only(
        self,
    ) -> typing.Optional["GoogleBigtableAppProfileDataBoostIsolationReadOnly"]:
        '''data_boost_isolation_read_only block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#data_boost_isolation_read_only GoogleBigtableAppProfile#data_boost_isolation_read_only}
        '''
        result = self._values.get("data_boost_isolation_read_only")
        return typing.cast(typing.Optional["GoogleBigtableAppProfileDataBoostIsolationReadOnly"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Long form description of the use case for this app profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#description GoogleBigtableAppProfile#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#id GoogleBigtableAppProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, ignore safety checks when deleting/updating the app profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#ignore_warnings GoogleBigtableAppProfile#ignore_warnings}
        '''
        result = self._values.get("ignore_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''The name of the instance to create the app profile within.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#instance GoogleBigtableAppProfile#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_cluster_routing_cluster_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of clusters to route to.

        The order is ignored; clusters will be tried in order of distance. If left empty, all clusters are eligible.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#multi_cluster_routing_cluster_ids GoogleBigtableAppProfile#multi_cluster_routing_cluster_ids}
        '''
        result = self._values.get("multi_cluster_routing_cluster_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def multi_cluster_routing_use_any(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, read/write requests are routed to the nearest cluster in the instance, and will fail over to the nearest cluster that is available in the event of transient errors or delays.

        Clusters in a region are considered equidistant. Choosing this option sacrifices read-your-writes
        consistency to improve availability.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#multi_cluster_routing_use_any GoogleBigtableAppProfile#multi_cluster_routing_use_any}
        '''
        result = self._values.get("multi_cluster_routing_use_any")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#project GoogleBigtableAppProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def row_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Must be used with multi-cluster routing.

        If true, then this app profile will use row affinity sticky routing. With row affinity, Bigtable will route single row key requests based on the row key, rather than randomly. Instead, each row key will be assigned to a cluster by Cloud Bigtable, and will stick to that cluster. Choosing this option improves read-your-writes consistency for most requests under most circumstances, without sacrificing availability. Consistency is not guaranteed, as requests may still fail over between clusters in the event of errors or latency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#row_affinity GoogleBigtableAppProfile#row_affinity}
        '''
        result = self._values.get("row_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def single_cluster_routing(
        self,
    ) -> typing.Optional["GoogleBigtableAppProfileSingleClusterRouting"]:
        '''single_cluster_routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#single_cluster_routing GoogleBigtableAppProfile#single_cluster_routing}
        '''
        result = self._values.get("single_cluster_routing")
        return typing.cast(typing.Optional["GoogleBigtableAppProfileSingleClusterRouting"], result)

    @builtins.property
    def standard_isolation(
        self,
    ) -> typing.Optional["GoogleBigtableAppProfileStandardIsolation"]:
        '''standard_isolation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#standard_isolation GoogleBigtableAppProfile#standard_isolation}
        '''
        result = self._values.get("standard_isolation")
        return typing.cast(typing.Optional["GoogleBigtableAppProfileStandardIsolation"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBigtableAppProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#timeouts GoogleBigtableAppProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigtableAppProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigtableAppProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileDataBoostIsolationReadOnly",
    jsii_struct_bases=[],
    name_mapping={"compute_billing_owner": "computeBillingOwner"},
)
class GoogleBigtableAppProfileDataBoostIsolationReadOnly:
    def __init__(self, *, compute_billing_owner: builtins.str) -> None:
        '''
        :param compute_billing_owner: The Compute Billing Owner for this Data Boost App Profile. Possible values: ["HOST_PAYS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#compute_billing_owner GoogleBigtableAppProfile#compute_billing_owner}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418322c1c34c2fc277cc127e42a9bfd67e1a12cfc845d809b3bd27217a04e1de)
            check_type(argname="argument compute_billing_owner", value=compute_billing_owner, expected_type=type_hints["compute_billing_owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_billing_owner": compute_billing_owner,
        }

    @builtins.property
    def compute_billing_owner(self) -> builtins.str:
        '''The Compute Billing Owner for this Data Boost App Profile. Possible values: ["HOST_PAYS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#compute_billing_owner GoogleBigtableAppProfile#compute_billing_owner}
        '''
        result = self._values.get("compute_billing_owner")
        assert result is not None, "Required property 'compute_billing_owner' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigtableAppProfileDataBoostIsolationReadOnly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigtableAppProfileDataBoostIsolationReadOnlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileDataBoostIsolationReadOnlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__408bcb7b20ea0a88ee9e14c09d2f51114e5636990101efc733f2821b97864110)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="computeBillingOwnerInput")
    def compute_billing_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeBillingOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="computeBillingOwner")
    def compute_billing_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeBillingOwner"))

    @compute_billing_owner.setter
    def compute_billing_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfbcf751bc5e98463c89fa71616e1e4c79f942d5c3cc23cb5b1911730995f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeBillingOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigtableAppProfileDataBoostIsolationReadOnly]:
        return typing.cast(typing.Optional[GoogleBigtableAppProfileDataBoostIsolationReadOnly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigtableAppProfileDataBoostIsolationReadOnly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1750c3b3312d1c48f097659826cc720eaf65197adb1dc28f7cc9e5ec4a0d151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileSingleClusterRouting",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "allow_transactional_writes": "allowTransactionalWrites",
    },
)
class GoogleBigtableAppProfileSingleClusterRouting:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        allow_transactional_writes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_id: The cluster to which read/write requests should be routed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#cluster_id GoogleBigtableAppProfile#cluster_id}
        :param allow_transactional_writes: If true, CheckAndMutateRow and ReadModifyWriteRow requests are allowed by this app profile. It is unsafe to send these requests to the same table/row/column in multiple clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#allow_transactional_writes GoogleBigtableAppProfile#allow_transactional_writes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175fbc581b1575a24ae3ed426a9d1f193a62894d9a938256d88bf0ae9647cbed)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument allow_transactional_writes", value=allow_transactional_writes, expected_type=type_hints["allow_transactional_writes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
        }
        if allow_transactional_writes is not None:
            self._values["allow_transactional_writes"] = allow_transactional_writes

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''The cluster to which read/write requests should be routed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#cluster_id GoogleBigtableAppProfile#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_transactional_writes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, CheckAndMutateRow and ReadModifyWriteRow requests are allowed by this app profile.

        It is unsafe to send these requests to the same table/row/column in multiple clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#allow_transactional_writes GoogleBigtableAppProfile#allow_transactional_writes}
        '''
        result = self._values.get("allow_transactional_writes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigtableAppProfileSingleClusterRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigtableAppProfileSingleClusterRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileSingleClusterRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcbdb15965dde492535df7a40b009acf278aeb68fdfa53225bd89bbea711041e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowTransactionalWrites")
    def reset_allow_transactional_writes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowTransactionalWrites", []))

    @builtins.property
    @jsii.member(jsii_name="allowTransactionalWritesInput")
    def allow_transactional_writes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowTransactionalWritesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowTransactionalWrites")
    def allow_transactional_writes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowTransactionalWrites"))

    @allow_transactional_writes.setter
    def allow_transactional_writes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623ac6eed873deef818cd8d7820f90970b75b9674e8a6c38f894e88ef09ba9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowTransactionalWrites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9f809445990e766bbb6fa6348ed764ee85030b11a903e9b8f76b706a0f6a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigtableAppProfileSingleClusterRouting]:
        return typing.cast(typing.Optional[GoogleBigtableAppProfileSingleClusterRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigtableAppProfileSingleClusterRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8915b41ebc0623377fce976e6aea70bd283c58df906b9c8100bdf73917f2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileStandardIsolation",
    jsii_struct_bases=[],
    name_mapping={"priority": "priority"},
)
class GoogleBigtableAppProfileStandardIsolation:
    def __init__(self, *, priority: builtins.str) -> None:
        '''
        :param priority: The priority of requests sent using this app profile. Possible values: ["PRIORITY_LOW", "PRIORITY_MEDIUM", "PRIORITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#priority GoogleBigtableAppProfile#priority}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241aedc96f1c0bf5a1f8519ca84f7b77d39ef2754eb4757bf2c8dc6ef31d0a20)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
        }

    @builtins.property
    def priority(self) -> builtins.str:
        '''The priority of requests sent using this app profile. Possible values: ["PRIORITY_LOW", "PRIORITY_MEDIUM", "PRIORITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#priority GoogleBigtableAppProfile#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigtableAppProfileStandardIsolation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigtableAppProfileStandardIsolationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileStandardIsolationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8dfe5b851e88b790fbd728eded2675ffce781686c304225c16c882aed0fd0c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2c07d3d7626bc93809819ad5211b99b775f8debf2d272995e0fd4104ef3b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigtableAppProfileStandardIsolation]:
        return typing.cast(typing.Optional[GoogleBigtableAppProfileStandardIsolation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigtableAppProfileStandardIsolation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d8584152c22fea5a2060b8a6e29f92ddc466786def30a63dbad6b4c83e059e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigtableAppProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#create GoogleBigtableAppProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#delete GoogleBigtableAppProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#update GoogleBigtableAppProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377ba4c6fcbaf9972350853ada5ed5dc5a6452c2a28efc638d3aca74823f99f2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#create GoogleBigtableAppProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#delete GoogleBigtableAppProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigtable_app_profile#update GoogleBigtableAppProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigtableAppProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigtableAppProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigtableAppProfile.GoogleBigtableAppProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f29f23feef4189add7be4dc0c61567944f5b5d50e78b49677ff96deb3dea49e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09025e1d91616b5a3c30e7df8d6e916251ad67f67af12217211d2e59c3cf52fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbfbe7247b09601c4345930f2ac6ac571baf3bde0ffa3a65add82de7c20c683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057b0c270cda0a86ba0cf0b5226660fedafcfc5ceb5eb2d23f8502d1bea42d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigtableAppProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigtableAppProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigtableAppProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ea97ed89eb264e2d29792018d426c14a9da76ea248b8e5bfbb116897cf3dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBigtableAppProfile",
    "GoogleBigtableAppProfileConfig",
    "GoogleBigtableAppProfileDataBoostIsolationReadOnly",
    "GoogleBigtableAppProfileDataBoostIsolationReadOnlyOutputReference",
    "GoogleBigtableAppProfileSingleClusterRouting",
    "GoogleBigtableAppProfileSingleClusterRoutingOutputReference",
    "GoogleBigtableAppProfileStandardIsolation",
    "GoogleBigtableAppProfileStandardIsolationOutputReference",
    "GoogleBigtableAppProfileTimeouts",
    "GoogleBigtableAppProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a31e6c1dd88227c70950c77c8b7b4d37ad39018aeb3010f1110a948debec6497(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_profile_id: builtins.str,
    data_boost_isolation_read_only: typing.Optional[typing.Union[GoogleBigtableAppProfileDataBoostIsolationReadOnly, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instance: typing.Optional[builtins.str] = None,
    multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    row_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    single_cluster_routing: typing.Optional[typing.Union[GoogleBigtableAppProfileSingleClusterRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    standard_isolation: typing.Optional[typing.Union[GoogleBigtableAppProfileStandardIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigtableAppProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ca9cf0d8ddcf46a2342c6589d011e91f16328b884f5a1d6cf394d3b74e4bed22(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f775aa0ca76fbec02fb44439bc22597388f9b4884b410dce1a87582b31fedd0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec2acaa024e5191886ae9c1ab708c072a8392879d4d9b55e771da088ba006ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8209646eef9c21964a23992dd2ecc4d01bb29d70b1de081c63120e90b54b26f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19ef89c2d24ff513193d7ecbd4fbfb3bff73acbb2057d33834474350131695c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c150bf18c198baa068b62297f4d590330167331f6fb44dbbdb5e1e6f3a8a4f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55faf66e1ffc5f74cd61d90eee62d1de71170516d01225aadfd26c0df095d6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5a9be0fdee18b7e32825a2ee83e61c47d7e8e98a5eb1b37ed6d25d55376194(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd7b1ed3bc918ec1389b6357ab7af84322741c894061b01ef7224aa90a2b7a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9996fbcd5540c8bb650c14ec53546c95858e31b5b259f7c0a9079a3a2620540b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0bdfbaf6a42f9ac97174ff7d1dc90b995082735c90e8996f76f95889d43761(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_profile_id: builtins.str,
    data_boost_isolation_read_only: typing.Optional[typing.Union[GoogleBigtableAppProfileDataBoostIsolationReadOnly, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instance: typing.Optional[builtins.str] = None,
    multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    row_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    single_cluster_routing: typing.Optional[typing.Union[GoogleBigtableAppProfileSingleClusterRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    standard_isolation: typing.Optional[typing.Union[GoogleBigtableAppProfileStandardIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigtableAppProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418322c1c34c2fc277cc127e42a9bfd67e1a12cfc845d809b3bd27217a04e1de(
    *,
    compute_billing_owner: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408bcb7b20ea0a88ee9e14c09d2f51114e5636990101efc733f2821b97864110(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfbcf751bc5e98463c89fa71616e1e4c79f942d5c3cc23cb5b1911730995f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1750c3b3312d1c48f097659826cc720eaf65197adb1dc28f7cc9e5ec4a0d151(
    value: typing.Optional[GoogleBigtableAppProfileDataBoostIsolationReadOnly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175fbc581b1575a24ae3ed426a9d1f193a62894d9a938256d88bf0ae9647cbed(
    *,
    cluster_id: builtins.str,
    allow_transactional_writes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbdb15965dde492535df7a40b009acf278aeb68fdfa53225bd89bbea711041e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623ac6eed873deef818cd8d7820f90970b75b9674e8a6c38f894e88ef09ba9b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9f809445990e766bbb6fa6348ed764ee85030b11a903e9b8f76b706a0f6a31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8915b41ebc0623377fce976e6aea70bd283c58df906b9c8100bdf73917f2bf(
    value: typing.Optional[GoogleBigtableAppProfileSingleClusterRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241aedc96f1c0bf5a1f8519ca84f7b77d39ef2754eb4757bf2c8dc6ef31d0a20(
    *,
    priority: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8dfe5b851e88b790fbd728eded2675ffce781686c304225c16c882aed0fd0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2c07d3d7626bc93809819ad5211b99b775f8debf2d272995e0fd4104ef3b67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d8584152c22fea5a2060b8a6e29f92ddc466786def30a63dbad6b4c83e059e(
    value: typing.Optional[GoogleBigtableAppProfileStandardIsolation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377ba4c6fcbaf9972350853ada5ed5dc5a6452c2a28efc638d3aca74823f99f2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29f23feef4189add7be4dc0c61567944f5b5d50e78b49677ff96deb3dea49e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09025e1d91616b5a3c30e7df8d6e916251ad67f67af12217211d2e59c3cf52fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbfbe7247b09601c4345930f2ac6ac571baf3bde0ffa3a65add82de7c20c683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057b0c270cda0a86ba0cf0b5226660fedafcfc5ceb5eb2d23f8502d1bea42d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ea97ed89eb264e2d29792018d426c14a9da76ea248b8e5bfbb116897cf3dc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigtableAppProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
