r'''
# `google_access_context_manager_service_perimeter`

Refer to the Terraform Registry for docs: [`google_access_context_manager_service_perimeter`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter).
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


class AccessContextManagerServicePerimeter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeter",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter google_access_context_manager_service_perimeter}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        title: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        perimeter_type: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimeterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter google_access_context_manager_service_perimeter} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Resource name for the ServicePerimeter. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/servicePerimeters/{short_name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#name AccessContextManagerServicePerimeter#name}
        :param parent: The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#parent AccessContextManagerServicePerimeter#parent}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        :param description: Description of the ServicePerimeter and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#description AccessContextManagerServicePerimeter#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#id AccessContextManagerServicePerimeter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param perimeter_type: Specifies the type of the Perimeter. There are two types: regular and bridge. Regular Service Perimeter contains resources, access levels, and restricted services. Every resource can be in at most ONE regular Service Perimeter. In addition to being in a regular service perimeter, a resource can also be in zero or more perimeter bridges. A perimeter bridge only contains resources. Cross project operations are permitted if all effected resources share some perimeter (whether bridge or regular). Perimeter Bridge does not contain access levels or services: those are governed entirely by the regular perimeter that resource is in. Perimeter Bridges are typically useful when building more complex topologies with many independent perimeters that need to share some data with a common perimeter, but should not be able to share data among themselves. Default value: "PERIMETER_TYPE_REGULAR" Possible values: ["PERIMETER_TYPE_REGULAR", "PERIMETER_TYPE_BRIDGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#perimeter_type AccessContextManagerServicePerimeter#perimeter_type}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#spec AccessContextManagerServicePerimeter#spec}
        :param status: status block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#status AccessContextManagerServicePerimeter#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#timeouts AccessContextManagerServicePerimeter#timeouts}
        :param use_explicit_dry_run_spec: Use explicit dry run spec flag. Ordinarily, a dry-run spec implicitly exists for all Service Perimeters, and that spec is identical to the status for those Service Perimeters. When this flag is set, it inhibits the generation of the implicit spec, thereby allowing the user to explicitly provide a configuration ("spec") to use in a dry-run version of the Service Perimeter. This allows the user to test changes to the enforced config ("status") without actually enforcing them. This testing is done through analyzing the differences between currently enforced and suggested restrictions. useExplicitDryRunSpec must bet set to True if any of the fields in the spec are set to non-default values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#use_explicit_dry_run_spec AccessContextManagerServicePerimeter#use_explicit_dry_run_spec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea01145565edb1cf7cef28821509525f981c6e49c3f70708f7d46bf57acaecb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerServicePerimeterConfig(
            name=name,
            parent=parent,
            title=title,
            description=description,
            id=id,
            perimeter_type=perimeter_type,
            spec=spec,
            status=status,
            timeouts=timeouts,
            use_explicit_dry_run_spec=use_explicit_dry_run_spec,
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
        '''Generates CDKTF code for importing a AccessContextManagerServicePerimeter resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerServicePerimeter to import.
        :param import_from_id: The id of the existing AccessContextManagerServicePerimeter that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerServicePerimeter to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc975870545842087dd78f7185128a29d51c8a67f29dc02a5c062e1065af4196)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpecVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_levels AccessContextManagerServicePerimeter#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_policies AccessContextManagerServicePerimeter#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_policies AccessContextManagerServicePerimeter#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#restricted_services AccessContextManagerServicePerimeter#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#vpc_accessible_services AccessContextManagerServicePerimeter#vpc_accessible_services}
        '''
        value = AccessContextManagerServicePerimeterSpec(
            access_levels=access_levels,
            egress_policies=egress_policies,
            ingress_policies=ingress_policies,
            resources=resources,
            restricted_services=restricted_services,
            vpc_accessible_services=vpc_accessible_services,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putStatus")
    def put_status(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatusVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_levels AccessContextManagerServicePerimeter#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_policies AccessContextManagerServicePerimeter#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_policies AccessContextManagerServicePerimeter#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#restricted_services AccessContextManagerServicePerimeter#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#vpc_accessible_services AccessContextManagerServicePerimeter#vpc_accessible_services}
        '''
        value = AccessContextManagerServicePerimeterStatus(
            access_levels=access_levels,
            egress_policies=egress_policies,
            ingress_policies=ingress_policies,
            resources=resources,
            restricted_services=restricted_services,
            vpc_accessible_services=vpc_accessible_services,
        )

        return typing.cast(None, jsii.invoke(self, "putStatus", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#create AccessContextManagerServicePerimeter#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#delete AccessContextManagerServicePerimeter#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#update AccessContextManagerServicePerimeter#update}.
        '''
        value = AccessContextManagerServicePerimeterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPerimeterType")
    def reset_perimeter_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerimeterType", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUseExplicitDryRunSpec")
    def reset_use_explicit_dry_run_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseExplicitDryRunSpec", []))

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
    @jsii.member(jsii_name="spec")
    def spec(self) -> "AccessContextManagerServicePerimeterSpecOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "AccessContextManagerServicePerimeterStatusOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterStatusOutputReference", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AccessContextManagerServicePerimeterTimeoutsOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

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
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="perimeterTypeInput")
    def perimeter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perimeterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["AccessContextManagerServicePerimeterSpec"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatus"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatus"], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimeterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimeterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="useExplicitDryRunSpecInput")
    def use_explicit_dry_run_spec_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useExplicitDryRunSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ff62d8ccb2f9925c4fabfa43c73c62bb68bbbc560d04bc8a2bcae74b6eb55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc49484ff5f3db1a8f90e05ca861c999b7c599ee9e6e75a22ea4ce25278e0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4b3015bd9df41435cb61fcbe1e128f1cbe9c652647f538c6d1668131827870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ef923f14bf5565ad71c041a6bb663c9949a437eb36268d1b3e4828384257cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perimeterType")
    def perimeter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perimeterType"))

    @perimeter_type.setter
    def perimeter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204854beabc352119ed07145b447b7e20415095be1abd7e22a1e2184fd17f34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perimeterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd6079920771427c53dd30b747e39d0f8d87a04bdb08fa877ed35fedd14cb51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExplicitDryRunSpec")
    def use_explicit_dry_run_spec(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useExplicitDryRunSpec"))

    @use_explicit_dry_run_spec.setter
    def use_explicit_dry_run_spec(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c31e65d024d5f6b9a3cc4b3c23544eedc4574e320badaa30bd1dc46e50c409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExplicitDryRunSpec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterConfig",
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
        "parent": "parent",
        "title": "title",
        "description": "description",
        "id": "id",
        "perimeter_type": "perimeterType",
        "spec": "spec",
        "status": "status",
        "timeouts": "timeouts",
        "use_explicit_dry_run_spec": "useExplicitDryRunSpec",
    },
)
class AccessContextManagerServicePerimeterConfig(
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
        parent: builtins.str,
        title: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        perimeter_type: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimeterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Resource name for the ServicePerimeter. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/servicePerimeters/{short_name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#name AccessContextManagerServicePerimeter#name}
        :param parent: The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#parent AccessContextManagerServicePerimeter#parent}
        :param title: Human readable title. Must be unique within the Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        :param description: Description of the ServicePerimeter and its use. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#description AccessContextManagerServicePerimeter#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#id AccessContextManagerServicePerimeter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param perimeter_type: Specifies the type of the Perimeter. There are two types: regular and bridge. Regular Service Perimeter contains resources, access levels, and restricted services. Every resource can be in at most ONE regular Service Perimeter. In addition to being in a regular service perimeter, a resource can also be in zero or more perimeter bridges. A perimeter bridge only contains resources. Cross project operations are permitted if all effected resources share some perimeter (whether bridge or regular). Perimeter Bridge does not contain access levels or services: those are governed entirely by the regular perimeter that resource is in. Perimeter Bridges are typically useful when building more complex topologies with many independent perimeters that need to share some data with a common perimeter, but should not be able to share data among themselves. Default value: "PERIMETER_TYPE_REGULAR" Possible values: ["PERIMETER_TYPE_REGULAR", "PERIMETER_TYPE_BRIDGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#perimeter_type AccessContextManagerServicePerimeter#perimeter_type}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#spec AccessContextManagerServicePerimeter#spec}
        :param status: status block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#status AccessContextManagerServicePerimeter#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#timeouts AccessContextManagerServicePerimeter#timeouts}
        :param use_explicit_dry_run_spec: Use explicit dry run spec flag. Ordinarily, a dry-run spec implicitly exists for all Service Perimeters, and that spec is identical to the status for those Service Perimeters. When this flag is set, it inhibits the generation of the implicit spec, thereby allowing the user to explicitly provide a configuration ("spec") to use in a dry-run version of the Service Perimeter. This allows the user to test changes to the enforced config ("status") without actually enforcing them. This testing is done through analyzing the differences between currently enforced and suggested restrictions. useExplicitDryRunSpec must bet set to True if any of the fields in the spec are set to non-default values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#use_explicit_dry_run_spec AccessContextManagerServicePerimeter#use_explicit_dry_run_spec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(spec, dict):
            spec = AccessContextManagerServicePerimeterSpec(**spec)
        if isinstance(status, dict):
            status = AccessContextManagerServicePerimeterStatus(**status)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerServicePerimeterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9501e26546981e0c8095e545bc58731b632287571708642f5c6cdd9a35e41fb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument perimeter_type", value=perimeter_type, expected_type=type_hints["perimeter_type"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument use_explicit_dry_run_spec", value=use_explicit_dry_run_spec, expected_type=type_hints["use_explicit_dry_run_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parent": parent,
            "title": title,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if perimeter_type is not None:
            self._values["perimeter_type"] = perimeter_type
        if spec is not None:
            self._values["spec"] = spec
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if use_explicit_dry_run_spec is not None:
            self._values["use_explicit_dry_run_spec"] = use_explicit_dry_run_spec

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
        '''Resource name for the ServicePerimeter. The short_name component must begin with a letter and only include alphanumeric and '_'. Format: accessPolicies/{policy_id}/servicePerimeters/{short_name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#name AccessContextManagerServicePerimeter#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The AccessPolicy this ServicePerimeter lives in. Format: accessPolicies/{policy_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#parent AccessContextManagerServicePerimeter#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Human readable title. Must be unique within the Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the ServicePerimeter and its use. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#description AccessContextManagerServicePerimeter#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#id AccessContextManagerServicePerimeter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def perimeter_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of the Perimeter.

        There are two types: regular and
        bridge. Regular Service Perimeter contains resources, access levels,
        and restricted services. Every resource can be in at most
        ONE regular Service Perimeter.

        In addition to being in a regular service perimeter, a resource can also
        be in zero or more perimeter bridges. A perimeter bridge only contains
        resources. Cross project operations are permitted if all effected
        resources share some perimeter (whether bridge or regular). Perimeter
        Bridge does not contain access levels or services: those are governed
        entirely by the regular perimeter that resource is in.

        Perimeter Bridges are typically useful when building more complex
        topologies with many independent perimeters that need to share some data
        with a common perimeter, but should not be able to share data among
        themselves. Default value: "PERIMETER_TYPE_REGULAR" Possible values: ["PERIMETER_TYPE_REGULAR", "PERIMETER_TYPE_BRIDGE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#perimeter_type AccessContextManagerServicePerimeter#perimeter_type}
        '''
        result = self._values.get("perimeter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["AccessContextManagerServicePerimeterSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#spec AccessContextManagerServicePerimeter#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpec"], result)

    @builtins.property
    def status(self) -> typing.Optional["AccessContextManagerServicePerimeterStatus"]:
        '''status block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#status AccessContextManagerServicePerimeter#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatus"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#timeouts AccessContextManagerServicePerimeter#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterTimeouts"], result)

    @builtins.property
    def use_explicit_dry_run_spec(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use explicit dry run spec flag.

        Ordinarily, a dry-run spec implicitly exists
        for all Service Perimeters, and that spec is identical to the status for those
        Service Perimeters. When this flag is set, it inhibits the generation of the
        implicit spec, thereby allowing the user to explicitly provide a
        configuration ("spec") to use in a dry-run version of the Service Perimeter.
        This allows the user to test changes to the enforced config ("status") without
        actually enforcing them. This testing is done through analyzing the differences
        between currently enforced and suggested restrictions. useExplicitDryRunSpec must
        bet set to True if any of the fields in the spec are set to non-default values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#use_explicit_dry_run_spec AccessContextManagerServicePerimeter#use_explicit_dry_run_spec}
        '''
        result = self._values.get("use_explicit_dry_run_spec")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpec",
    jsii_struct_bases=[],
    name_mapping={
        "access_levels": "accessLevels",
        "egress_policies": "egressPolicies",
        "ingress_policies": "ingressPolicies",
        "resources": "resources",
        "restricted_services": "restrictedServices",
        "vpc_accessible_services": "vpcAccessibleServices",
    },
)
class AccessContextManagerServicePerimeterSpec:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpecVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_levels AccessContextManagerServicePerimeter#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_policies AccessContextManagerServicePerimeter#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_policies AccessContextManagerServicePerimeter#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#restricted_services AccessContextManagerServicePerimeter#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#vpc_accessible_services AccessContextManagerServicePerimeter#vpc_accessible_services}
        '''
        if isinstance(vpc_accessible_services, dict):
            vpc_accessible_services = AccessContextManagerServicePerimeterSpecVpcAccessibleServices(**vpc_accessible_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dcee124c0487559970302b3886915da65d488359296c9b4cc282d9e8a5e0bf)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument egress_policies", value=egress_policies, expected_type=type_hints["egress_policies"])
            check_type(argname="argument ingress_policies", value=ingress_policies, expected_type=type_hints["ingress_policies"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument restricted_services", value=restricted_services, expected_type=type_hints["restricted_services"])
            check_type(argname="argument vpc_accessible_services", value=vpc_accessible_services, expected_type=type_hints["vpc_accessible_services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels
        if egress_policies is not None:
            self._values["egress_policies"] = egress_policies
        if ingress_policies is not None:
            self._values["ingress_policies"] = ingress_policies
        if resources is not None:
            self._values["resources"] = resources
        if restricted_services is not None:
            self._values["restricted_services"] = restricted_services
        if vpc_accessible_services is not None:
            self._values["vpc_accessible_services"] = vpc_accessible_services

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet.

        AccessLevels listed must be in the same policy as this
        ServicePerimeter. Referencing a nonexistent AccessLevel is a
        syntax error. If no AccessLevel names are listed, resources within
        the perimeter can only be accessed via GCP calls with request
        origins within the perimeter. For Service Perimeter Bridge, must
        be empty.

        Format: accessPolicies/{policy_id}/accessLevels/{access_level_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_levels AccessContextManagerServicePerimeter#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def egress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPolicies"]]]:
        '''egress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_policies AccessContextManagerServicePerimeter#egress_policies}
        '''
        result = self._values.get("egress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPolicies"]]], result)

    @builtins.property
    def ingress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPolicies"]]]:
        '''ingress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_policies AccessContextManagerServicePerimeter#ingress_policies}
        '''
        result = self._values.get("ingress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPolicies"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def restricted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''GCP services that are subject to the Service Perimeter restrictions.

        Must contain a list of services. For example, if
        'storage.googleapis.com' is specified, access to the storage
        buckets inside the perimeter must meet the perimeter's access
        restrictions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#restricted_services AccessContextManagerServicePerimeter#restricted_services}
        '''
        result = self._values.get("restricted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_accessible_services(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterSpecVpcAccessibleServices"]:
        '''vpc_accessible_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#vpc_accessible_services AccessContextManagerServicePerimeter#vpc_accessible_services}
        '''
        result = self._values.get("vpc_accessible_services")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpecVpcAccessibleServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimeterSpecEgressPolicies:
    def __init__(
        self,
        *,
        egress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_from AccessContextManagerServicePerimeter#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_to AccessContextManagerServicePerimeter#egress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        if isinstance(egress_from, dict):
            egress_from = AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo(**egress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cd08dbab1e8fcba9ce01590ce54655d5f0efe35bf8413a4f546858a219a694)
            check_type(argname="argument egress_from", value=egress_from, expected_type=type_hints["egress_from"])
            check_type(argname="argument egress_to", value=egress_to, expected_type=type_hints["egress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_from is not None:
            self._values["egress_from"] = egress_from
        if egress_to is not None:
            self._values["egress_to"] = egress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def egress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_from AccessContextManagerServicePerimeter#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_to AccessContextManagerServicePerimeter#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecEgressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this 'EgressPolicy'. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#source_restriction AccessContextManagerServicePerimeter#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01856b80585f3d86dbdab3a2a879267b7c6c51940c8ebe4685b67c7ad9c42e25)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument source_restriction", value=source_restriction, expected_type=type_hints["source_restriction"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if source_restriction is not None:
            self._values["source_restriction"] = source_restriction
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identities that are allowed access through this 'EgressPolicy'.

        Should be in the format of email address. The email address should
        represent individual user or service account only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#source_restriction AccessContextManagerServicePerimeter#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41aa72aa08518c0b83ca635d1949ad314ccde7cae8468e65c08037d497f9598d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1397dfd3aa5139f3c87318758680a1d3a413e0b61cc5ff48e33c9dbd8f7adab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSourceRestriction")
    def reset_source_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRestriction", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRestrictionInput")
    def source_restriction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113f0440eff061f45d89ff445025f95b247f44cd0a1344cdaca1b819a39b5e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828a0e744b8dc69e3d9cbd12514052e4564228904e264d4545a7d7a4b8d6ca61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8116b8bd5a73c5ec855d1e82d7dd57f6806fde6104845533313ef868514d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1984209bc4de2295c76faf8558a92c9ddafa5279b8022f2e2f26b87399dcd60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa26cc085910f903beb3bb44cf266086b29e9eeda011949221a7be4e7aae37c3)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to egress the perimeter.

        Requests from these resources are allowed to access data outside the perimeter.
        Currently only projects are allowed. Project format: 'projects/{project_number}'.
        The resource may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the
        case of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc1d0a974c1145143e749afaf5996b21b40cc421013daf25f9e0f368e1933ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e299e6627016a327342b1d9a72f1495185eb893a2be42e7a9bad379ddf0603)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c66204a1e26fb1820b08e1ec04cec4f2ad1a529a2070b589229fdc5f5ebddbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bea4a2c74452fe9162797ed6e9693bb02e3d2aaa0681aee3a6b76368d59eab26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d665bdd1a1ad47651825284a085179c970da3828d4f5598ddf46419d6405d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149c81a4f55f758749bbed5050b844bcdb47698e4a79371542c3838476df55f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebdeda582db5019109b7002a4313b6e4f040f456dea536b32373959f0628be9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23be8ed6d9f24098cdcbb6a654d188a93f80fe3f0e2bbd45ceb660a24e9446cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe097cb2ca51f23b468436f104fedf1223596f54461c9ec1736b44abe926398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3773165bf6113693a92d5197d087f98d6ef603275d1314c62efb7505c8d83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#external_resources AccessContextManagerServicePerimeter#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541126ea0257c464b21c268c55cc07c4361a88042d327c8513f816c3d6dd6bc2)
            check_type(argname="argument external_resources", value=external_resources, expected_type=type_hints["external_resources"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_resources is not None:
            self._values["external_resources"] = external_resources
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def external_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of external resources that are allowed to be accessed.

        A request
        matches if it contains an external resource in this list (Example:
        s3://bucket/path). Currently '*' is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#external_resources AccessContextManagerServicePerimeter#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636af21a70c56163b684852bbfdf6da5bdf18f074200901ee891e50c8c9cadc6)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3282dd35af911df00fb73f16446cb8e50a1c8a388b0a8090f1523ae90b18e7ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab5c7a0448a951fc7b544961658e6b20ff790ed0fe079b5abb45b9a812b53d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4641ffbd318378d6ddf76503459bc703a5470e83e043fbdd33e1b7a6502b450)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17b3dd5b8439e6814e0f3acd41f20eeab65f07505909e4891ecebcfd29b75352)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2f8220ab35e8e79aba7c0b5901a5d234e615e8647b0153aef8d98a87b155cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631e1f435eb358e00b7be26d8c905e35876484b2137911f7ce80b8d95e9173ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24611fb0eba9b08d77efd0f0d9da091ed90b1a57db8a57e5b5c04b8b7a943194)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'.

        If '*' used as value for method,
        then ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1cf32c3dbd4e6295e51bbe11a9555ebd265f3091875e0e2605f6a76d80ef68a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db3bc51b8e1d30af4fca5ff8c8c4796d37efdb721e7729341f5ae124c5fa8d19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f1d2b4a73691c11411c3209708970bb37c6631a3005714a5b6769e1617190e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40e03135d3f10b6f2ce0c6c2c9d4cb8c012a8f1e26fc3247424581f79630489d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a121a196f056b482bc9d9c827102243f8eda81956ec7fc1904ac4b8a8feb0d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f59b8bbf7a703cdaa0c78f21356a8dd4f8a965c99764c719d18e8aa5885543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85612b55c2cb2dbe3bafa1d9c5004d580e234d05b2f45f4cc2dffc9c0122e662)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e82eaa02f39a4ac4d963421a499283fdb47455545a21145c615cbdecf48dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17cddbc04b3d955027da19181344f6eeaa3325e1a20d47341def9ceb84e5bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321a6f0d39afa385e6db2ae292e69cfb86fae8dfce2cf1324bd59425bd05084b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0dfa698d0237b4533c2282557bfacde372f230921d0c6e7a0ee5ee2ac9c5148)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60fdb5b34b39f19239f097d1a811477b39581efef1bd4b22e76353f4fb570787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4dcaefe537a6c725f71e2789bd527641db751c2203d85ca80445df089538b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edd393da598c2f5d3773403f4233a26cf8b3a69bd0044bb666105763e955ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff964c23590031cae0cb373814039103fac9418592171926f58ea589d171104)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efac8381b967ff001d53fdf72d6c246db6ce9047168421413d7258d0c33a2ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetExternalResources")
    def reset_external_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalResources", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="externalResources")
    def external_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalResources"))

    @external_resources.setter
    def external_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d076fe8375c87958e5842490300576274a9730ae8b17c3f7bc8efe128fe9b3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0bd89635100a38a5d2c45057a86a4ee1612fe5137e0b240272ceffe2b4a41b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a801f18baac9c11d677750c6484fbc4f9c27396689f737628ad6d57f468eac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d740b328c7277f689dbb4e0d72f641c8a8ec5e00a5d2b8993924b8a615b155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecEgressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65763458290c7fd51d78c10301a6c451fa539e3d95de8a954fd939af1aa960f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecEgressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe0da00cf3098b0529fd399b272aa8fcfd3c86b5e73514bebf375469b867daf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecEgressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a402e72d1aee53658fdad33135401b5b7e12d826e114e49f3e674db4fc77354)
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
            type_hints = typing.get_type_hints(_typecheckingstub__518e40d902b832d9835d10cec207a925eceb045b93736babee9b840be15c70e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d54bc3594028b0a4694a66455d5d1adcbc73c867b6983124eaa246c5afc779a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f620a051c49e76ef68e526a05adea8e16c7aa3361afe3f1d3250a25aae035e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecEgressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecEgressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e61a49e9f552c9944b63d0b596195d0828027acf8411b1ddc69dc92f907bb5d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEgressFrom")
    def put_egress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this 'EgressPolicy'. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#source_restriction AccessContextManagerServicePerimeter#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        value = AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom(
            identities=identities,
            identity_type=identity_type,
            source_restriction=source_restriction,
            sources=sources,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressFrom", [value]))

    @jsii.member(jsii_name="putEgressTo")
    def put_egress_to(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#external_resources AccessContextManagerServicePerimeter#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        value = AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo(
            external_resources=external_resources,
            operations=operations,
            resources=resources,
            roles=roles,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressTo", [value]))

    @jsii.member(jsii_name="resetEgressFrom")
    def reset_egress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressFrom", []))

    @jsii.member(jsii_name="resetEgressTo")
    def reset_egress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="egressFrom")
    def egress_from(
        self,
    ) -> AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromOutputReference, jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOutputReference, jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo], jsii.get(self, "egressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da56decedc44ef15f7be524d67fad750e1cac580f91576960df7932ae530a830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad692999ace735f2eac12f699add7b1de8b976d4d7392013a2c43019938dae5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimeterSpecIngressPolicies:
    def __init__(
        self,
        *,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_from AccessContextManagerServicePerimeter#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_to AccessContextManagerServicePerimeter#ingress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        if isinstance(ingress_from, dict):
            ingress_from = AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo(**ingress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae5923c3d496f1aece930f3c8d17008e45f76785287c61132594bc22b259cef)
            check_type(argname="argument ingress_from", value=ingress_from, expected_type=type_hints["ingress_from"])
            check_type(argname="argument ingress_to", value=ingress_to, expected_type=type_hints["ingress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress_from is not None:
            self._values["ingress_from"] = ingress_from
        if ingress_to is not None:
            self._values["ingress_to"] = ingress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def ingress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_from AccessContextManagerServicePerimeter#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_to AccessContextManagerServicePerimeter#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecIngressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b391cd53f0929ca560b732b04572a7574f6ef832f4571fec124ec89cafc286)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of identities that are allowed access through this ingress policy.

        Should be in the format of email address. The email address should represent
        individual user or service account only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9b895a23f69d2089d11c140cffb3c7fc507afcca922ebd09144144b866a43c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7570fbe45b16027d090d1ec8093fd890f38c6d8d190ad144890a4f79e446cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e86e023eb35fba1a8cab478f2076fb4277bfc73f3cc6315444eb59699a8a021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cab6562b2b2d140557b046733a5017f54ef3a41e6701808ebc34a93b670ee02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc797c76eac65d09584003a61e4568b402a59f1341b42229b9d917ab035d208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects are allowed. Format 'projects/{project_number}' The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b609967725522f6dfdd65b6f5409a9b5804c581151bf4c21cd8aeb614ea42d)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet.

        'AccessLevels' listed
        must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent
        'AccessLevel' will cause an error. If no 'AccessLevel' names are listed,
        resources within the perimeter can only be accessed via Google Cloud calls
        with request origins within the perimeter.
        Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.'
        If * is specified, then all IngressSources will be allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to ingress the perimeter.

        Requests from these resources will be allowed to access perimeter data.
        Currently only projects are allowed. Format 'projects/{project_number}'
        The project may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the case
        of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ca50b64266d6de0d7e883209f3d6057ba5bbf82641cd24db2e8afdb94221e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7cdb64219d20d8d6a45fc853171adffe24f2b2dd440bd3c965784b3f6c15213)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ceb718f71d8e0b6338cfae159e368089379920f301efb61542ca4db3d51bb12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__016356fadcf2f7854cc030020e18b94037d7258f6fbcc4ad1dbe42abde0072cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3416dd475a176e38c68f514e5433965a0c8efac7dddaaa345f399a73b5119031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7baf3d560146799a0e0052d277ec939b7037eb8c2c691c5e5a920c7bf41626cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__794f41f2538a577aa9a69a7b174d49f95122edfe846a3569818fa036c64c9822)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c258e99769e498a136664bf8526943a64c43250779bbcb2201ae6254a181fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248d1d02097e31266e0a6975fa328ddbbc4e084e957dc6395d68300cab8b3cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79a4661326d6494ec24d796f954d2f351c5b70946d2abfa6babdfc32079ab9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419e2e89f6261ad1087b5407797ff772ca5e8cd537c3b1db285b278060777cf1)
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d719f428c353427537c2c50e940b5472a9718d79a0960ebea2107ec02d6c7437)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4716ddce89a62754f2724d2fe053ec2c44c90ef4e98a000ec53ede1a74bce22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701ed09ee82fb5f74ecbfad32ee9d1f8d0cdb38b9eb7b99dc7ab7161fc0db253)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb08c74274e12cbd2152e070474884bab6a65832fd902b7a495b0cfc2199c15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34df57b028c1266f4849940979b5cad2102aee6e3763636c7667e50b8e81b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72d0c8a4e769d561f87613376d35884ae52704e4afb96d65b97e8dddc546f35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491e38d70156691cec2fddb50d589fb1a035f99050cfe045a80a975a4fec56d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5ec22892bb476eca65d6d1526c32f5f44a37c0dcdc2ec82f978f10a6bb16c1)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'.

        If '*' used as value for 'method', then
        ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__516794f95060636a7e2c5aaf74ad13b6d97f8d2e0065e28dd0156c023d8fd4d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bc2ac12b49b00f510357f049de275713de878ec6c95440c3f77e6e84853eff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d5a775eec1dd155931e9b9421849d33f9dd4e5da56a3b29cb78c5406e2558f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e1b02156e41df68db3addd5bedbc0755400957eefaf8055be883c1d5cf78e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__242c9516bd3bee910488ea702b9eda597b9b403881f99ac4868f8def8712b221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45feeddb7feb12e47fb7933dd07f4969c1305a1c964104bcb13aaf43c5c1a67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfd9f12efa9942d7fa00a42616325c5e194f5a855d8f57bcc95edff5f59ca227)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af002925224676a80c487f07e09f437e20ab3c7b5bfec3d965402f31bf110ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cc6513cc6c0ebee35447e5a356c7669dcfa11be995e4d71e3aac801682e43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360beae8fff61bfbeeea18a65a2d98df01f0b31018d4bbdeef858cf75c4f9e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a6a45691ae606ebb63fdaa359a2e2c7e0de9f1b253ce29134837ef46235ee1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225c11c1dbf49449b152a28cf28e111343df4ab63a4332f706faadf7252fd52b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce9a807889bf348da0be849fa4d5872366c0372f22aaaa6ca7884827ac4e04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c1ddba2273e19649d403e6ee693a1e1c6bdb54ea687ebf833d904e0eb38561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51d75d3a6f2c0c8c754fafc07a79fba1413651f0440b775334a660fcc57ced14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ded0a54aae7aaa9b54b7eefb6f886a0570e7bd7c6edcd77695ab17ff55526c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e06486f0df20351ab5530117638d914e8e73761f959cd7d15c4a5a686c6918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f456606f65603da1b9d4662883165db0447d0b16710d99f87f38b496bd22fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a401cbfcef63bd5408833a1511e5e39823c8af21ccd733d9efee33d5a03cbffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecIngressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5e67a73acd6e9cc46b4ded158b6487c254cab4a775ea8ded011bc82056410e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterSpecIngressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839cc41d969379a9bff8ba9901a9ffbdbecc71eb01d8d8d06e46da310ad0753e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterSpecIngressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9068247c974c3c8ec75d409370a4aa350a22c04b753cbdc64846b2ecccf9ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a8fdfa147724382c84f9765d97bf794ed724c54b5e2aee870f490ea81fd6b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47b396f53d8903490479f86a98d3df314e98574c63837d976353558ce745fdb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b147d7fc224da20f5d0b03ce6c15262d2e837a7461e7c1362c68a64a61b49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecIngressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecIngressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec8f836fa92693e7ba5ee5ba8c1d4b02559c1a8d2197614b20d3d4a41b0e552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIngressFrom")
    def put_ingress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: A list of identities that are allowed access through this ingress policy. Should be in the format of email address. The email address should represent individual user or service account only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        value = AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        value = AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo(
            operations=operations, resources=resources, roles=roles
        )

        return typing.cast(None, jsii.invoke(self, "putIngressTo", [value]))

    @jsii.member(jsii_name="resetIngressFrom")
    def reset_ingress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressFrom", []))

    @jsii.member(jsii_name="resetIngressTo")
    def reset_ingress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="ingressFrom")
    def ingress_from(
        self,
    ) -> AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromOutputReference, jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOutputReference, jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo], jsii.get(self, "ingressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee71f15124fc516a8bc73af2e0566257834da3b64f11d2867379013efa2acd9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69dfa31127877b443652ef97354e354a140eec34bc35e06d9260ac6bc10cf540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81d6e2aad54e9d3263a35181f96eb888b3d345ea3006d91aa53edac90ebda25d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressPolicies")
    def put_egress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12c3bf0daa6ff526e922a21081354862e4ddbb7f5d8f2c9df65aa3239232d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEgressPolicies", [value]))

    @jsii.member(jsii_name="putIngressPolicies")
    def put_ingress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31aa3b68643b256303848652eabdbaeac14b4038d26edf1a3484353a7b6a069a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngressPolicies", [value]))

    @jsii.member(jsii_name="putVpcAccessibleServices")
    def put_vpc_accessible_services(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#allowed_services AccessContextManagerServicePerimeter#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#enable_restriction AccessContextManagerServicePerimeter#enable_restriction}
        '''
        value = AccessContextManagerServicePerimeterSpecVpcAccessibleServices(
            allowed_services=allowed_services, enable_restriction=enable_restriction
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccessibleServices", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @jsii.member(jsii_name="resetEgressPolicies")
    def reset_egress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressPolicies", []))

    @jsii.member(jsii_name="resetIngressPolicies")
    def reset_ingress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressPolicies", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRestrictedServices")
    def reset_restricted_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedServices", []))

    @jsii.member(jsii_name="resetVpcAccessibleServices")
    def reset_vpc_accessible_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccessibleServices", []))

    @builtins.property
    @jsii.member(jsii_name="egressPolicies")
    def egress_policies(
        self,
    ) -> AccessContextManagerServicePerimeterSpecEgressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimeterSpecEgressPoliciesList, jsii.get(self, "egressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="ingressPolicies")
    def ingress_policies(
        self,
    ) -> AccessContextManagerServicePerimeterSpecIngressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimeterSpecIngressPoliciesList, jsii.get(self, "ingressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServices")
    def vpc_accessible_services(
        self,
    ) -> "AccessContextManagerServicePerimeterSpecVpcAccessibleServicesOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterSpecVpcAccessibleServicesOutputReference", jsii.get(self, "vpcAccessibleServices"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="egressPoliciesInput")
    def egress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPolicies]]], jsii.get(self, "egressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressPoliciesInput")
    def ingress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPolicies]]], jsii.get(self, "ingressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedServicesInput")
    def restricted_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServicesInput")
    def vpc_accessible_services_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterSpecVpcAccessibleServices"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterSpecVpcAccessibleServices"], jsii.get(self, "vpcAccessibleServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d4c4b869d5dea24b5905fbd48d7c8fb3df138c2fb13b897ef046f7814cda00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fb7dc58251ba310f7fd951890bfc2cec43d9dd1adfa878a545562493371f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedServices")
    def restricted_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedServices"))

    @restricted_services.setter
    def restricted_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828381e00b333973d5eeab0b56d06b333b38688f6ef84d94573ed0fd432f6896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpec]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bb9cf0f38ae0c1f1e7a812873ccddaad1f9dc76539fe860a7f0461027583b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecVpcAccessibleServices",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services": "allowedServices",
        "enable_restriction": "enableRestriction",
    },
)
class AccessContextManagerServicePerimeterSpecVpcAccessibleServices:
    def __init__(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#allowed_services AccessContextManagerServicePerimeter#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#enable_restriction AccessContextManagerServicePerimeter#enable_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243d35481fc3586171d6a3d7c330efcaae9a2e737e0e7e65854337ae08e6b386)
            check_type(argname="argument allowed_services", value=allowed_services, expected_type=type_hints["allowed_services"])
            check_type(argname="argument enable_restriction", value=enable_restriction, expected_type=type_hints["enable_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_services is not None:
            self._values["allowed_services"] = allowed_services
        if enable_restriction is not None:
            self._values["enable_restriction"] = enable_restriction

    @builtins.property
    def allowed_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#allowed_services AccessContextManagerServicePerimeter#allowed_services}
        '''
        result = self._values.get("allowed_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#enable_restriction AccessContextManagerServicePerimeter#enable_restriction}
        '''
        result = self._values.get("enable_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterSpecVpcAccessibleServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterSpecVpcAccessibleServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterSpecVpcAccessibleServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7617b1fb4017955f97539a1062112a3699a28bdf0acd18c3d5627402db5e285)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedServices")
    def reset_allowed_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedServices", []))

    @jsii.member(jsii_name="resetEnableRestriction")
    def reset_enable_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="allowedServicesInput")
    def allowed_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRestrictionInput")
    def enable_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedServices")
    def allowed_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedServices"))

    @allowed_services.setter
    def allowed_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5696246d94640583a5f6082fc375289e6d53c715c66b246c5eb67fb94b0bc31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRestriction")
    def enable_restriction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRestriction"))

    @enable_restriction.setter
    def enable_restriction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9b1167bc0ff963b2576f7db8faf9022c2232c1fba31673098df93951e77328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterSpecVpcAccessibleServices]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterSpecVpcAccessibleServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterSpecVpcAccessibleServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e8a87127a332a3f7ab0002ac473c4ab6d27c597766518b5b2a8b5ef8a387e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatus",
    jsii_struct_bases=[],
    name_mapping={
        "access_levels": "accessLevels",
        "egress_policies": "egressPolicies",
        "ingress_policies": "ingressPolicies",
        "resources": "resources",
        "restricted_services": "restrictedServices",
        "vpc_accessible_services": "vpcAccessibleServices",
    },
)
class AccessContextManagerServicePerimeterStatus:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusEgressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusIngressPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_accessible_services: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatusVpcAccessibleServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet. AccessLevels listed must be in the same policy as this ServicePerimeter. Referencing a nonexistent AccessLevel is a syntax error. If no AccessLevel names are listed, resources within the perimeter can only be accessed via GCP calls with request origins within the perimeter. For Service Perimeter Bridge, must be empty. Format: accessPolicies/{policy_id}/accessLevels/{access_level_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_levels AccessContextManagerServicePerimeter#access_levels}
        :param egress_policies: egress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_policies AccessContextManagerServicePerimeter#egress_policies}
        :param ingress_policies: ingress_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_policies AccessContextManagerServicePerimeter#ingress_policies}
        :param resources: A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param restricted_services: GCP services that are subject to the Service Perimeter restrictions. Must contain a list of services. For example, if 'storage.googleapis.com' is specified, access to the storage buckets inside the perimeter must meet the perimeter's access restrictions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#restricted_services AccessContextManagerServicePerimeter#restricted_services}
        :param vpc_accessible_services: vpc_accessible_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#vpc_accessible_services AccessContextManagerServicePerimeter#vpc_accessible_services}
        '''
        if isinstance(vpc_accessible_services, dict):
            vpc_accessible_services = AccessContextManagerServicePerimeterStatusVpcAccessibleServices(**vpc_accessible_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e710c7f9b0f668fb3ad6e29a864c23f099c1d928518abe7305c31947a846193)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument egress_policies", value=egress_policies, expected_type=type_hints["egress_policies"])
            check_type(argname="argument ingress_policies", value=ingress_policies, expected_type=type_hints["ingress_policies"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument restricted_services", value=restricted_services, expected_type=type_hints["restricted_services"])
            check_type(argname="argument vpc_accessible_services", value=vpc_accessible_services, expected_type=type_hints["vpc_accessible_services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels
        if egress_policies is not None:
            self._values["egress_policies"] = egress_policies
        if ingress_policies is not None:
            self._values["ingress_policies"] = ingress_policies
        if resources is not None:
            self._values["resources"] = resources
        if restricted_services is not None:
            self._values["restricted_services"] = restricted_services
        if vpc_accessible_services is not None:
            self._values["vpc_accessible_services"] = vpc_accessible_services

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of AccessLevel resource names that allow resources within the ServicePerimeter to be accessed from the internet.

        AccessLevels listed must be in the same policy as this
        ServicePerimeter. Referencing a nonexistent AccessLevel is a
        syntax error. If no AccessLevel names are listed, resources within
        the perimeter can only be accessed via GCP calls with request
        origins within the perimeter. For Service Perimeter Bridge, must
        be empty.

        Format: accessPolicies/{policy_id}/accessLevels/{access_level_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_levels AccessContextManagerServicePerimeter#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def egress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPolicies"]]]:
        '''egress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_policies AccessContextManagerServicePerimeter#egress_policies}
        '''
        result = self._values.get("egress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPolicies"]]], result)

    @builtins.property
    def ingress_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPolicies"]]]:
        '''ingress_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_policies AccessContextManagerServicePerimeter#ingress_policies}
        '''
        result = self._values.get("ingress_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPolicies"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of GCP resources that are inside of the service perimeter. Currently only projects are allowed. Format: projects/{project_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def restricted_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''GCP services that are subject to the Service Perimeter restrictions.

        Must contain a list of services. For example, if
        'storage.googleapis.com' is specified, access to the storage
        buckets inside the perimeter must meet the perimeter's access
        restrictions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#restricted_services AccessContextManagerServicePerimeter#restricted_services}
        '''
        result = self._values.get("restricted_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_accessible_services(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatusVpcAccessibleServices"]:
        '''vpc_accessible_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#vpc_accessible_services AccessContextManagerServicePerimeter#vpc_accessible_services}
        '''
        result = self._values.get("vpc_accessible_services")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatusVpcAccessibleServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "egress_from": "egressFrom",
        "egress_to": "egressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimeterStatusEgressPolicies:
    def __init__(
        self,
        *,
        egress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        egress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param egress_from: egress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_from AccessContextManagerServicePerimeter#egress_from}
        :param egress_to: egress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_to AccessContextManagerServicePerimeter#egress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        if isinstance(egress_from, dict):
            egress_from = AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom(**egress_from)
        if isinstance(egress_to, dict):
            egress_to = AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo(**egress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418335c724bc5f81a9054297a41894d473415f08dbf7ef6e2b94ee233c01ad22)
            check_type(argname="argument egress_from", value=egress_from, expected_type=type_hints["egress_from"])
            check_type(argname="argument egress_to", value=egress_to, expected_type=type_hints["egress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_from is not None:
            self._values["egress_from"] = egress_from
        if egress_to is not None:
            self._values["egress_to"] = egress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def egress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom"]:
        '''egress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_from AccessContextManagerServicePerimeter#egress_from}
        '''
        result = self._values.get("egress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom"], result)

    @builtins.property
    def egress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo"]:
        '''egress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#egress_to AccessContextManagerServicePerimeter#egress_to}
        '''
        result = self._values.get("egress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusEgressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "source_restriction": "sourceRestriction",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#source_restriction AccessContextManagerServicePerimeter#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3fe2bfb4154bed2543e03041f47edf8a1b4c550a29f2e11c726983ffc6cf22)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument source_restriction", value=source_restriction, expected_type=type_hints["source_restriction"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if source_restriction is not None:
            self._values["source_restriction"] = source_restriction
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identities can be an individual user, service account, Google group, or third-party identity.

        For third-party identity, only single identities
        are supported and other identity types are not supported.The v1 identities
        that have the prefix user, group and serviceAccount in
        https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access to outside the perimeter.

        If left unspecified, then members of 'identities' field will
        be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_restriction(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce traffic restrictions based on 'sources' field.

        If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#source_restriction AccessContextManagerServicePerimeter#source_restriction}
        '''
        result = self._values.get("source_restriction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d90efa0b2fdee4b54f0cac1a88a77a06079d63005d7b329e5ce1d0c5ff13bfe8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731970046315edd734f3d8f6e4475de69e9cf183969436d44af5b7f7bf1f8a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSourceRestriction")
    def reset_source_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRestriction", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRestrictionInput")
    def source_restriction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1be10957878a39648a9c55af8cd52d9a4a5a036d370148f41de16855733363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77bc627559e4031b3680c703c8df6e4e5b576f3b31be3bbc16a58d78dd4b4dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRestriction")
    def source_restriction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceRestriction"))

    @source_restriction.setter
    def source_restriction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d8dc67f330384e76a5893159dd8097725775afe56bd58fdfb32b783bc400a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7324f5953916f9c906f3e1ffff498277469b04af0095722a17e924a4a7629a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        :param resource: A Google Cloud resource that is allowed to egress the perimeter. Requests from these resources are allowed to access data outside the perimeter. Currently only projects are allowed. Project format: 'projects/{project_number}'. The resource may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b4ee509236eb10b9d75d17ee5291407e1cf03937f3c414ea0b4ee9dcd2157d)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An AccessLevel resource name that allows resources outside the ServicePerimeter to be accessed from the inside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to egress the perimeter.

        Requests from these resources are allowed to access data outside the perimeter.
        Currently only projects are allowed. Project format: 'projects/{project_number}'.
        The resource may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the
        case of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d0d18a814468c9c680a76c2bf32ad098fa553e16d9e2d5881aa98354d08206)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5594b5006ffb1cf6159b036242e96fcf6cd43929667dd4026040495316b277cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce58700dcf04ae2fb998ae02e385b3699eac648c4af224b9955d07e36c25868b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d077c146ea9a9a0aec19675f5385edfbb40178075552f499bf5a85f44bdf96a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ea7dbd04ee9b917790755db7a642ebcf1eaecefe9fa4be2b7f03ef9edea4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9e4e3570eacaf56e2409b86271114cc5997f9740aa2da640450817401db76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e315cb4496647a95786c60e8604357dda948ba19e47997041dbcd03e92714bb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ef32740b88b6adc072ce9a811bf72664b34b423d0e89c3e8a521be6a0be372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__890064ff0dcdf1adfc8bc9c1da731d72f3ded92cea6cb0cfdfce46ba858d24e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd351eee02292ada2eb61597b35b11b8e5de4e1d704cb369e99373cc79f4cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo",
    jsii_struct_bases=[],
    name_mapping={
        "external_resources": "externalResources",
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo:
    def __init__(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#external_resources AccessContextManagerServicePerimeter#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b49c7b4d2022c68f7f485bbbc9861816826b6038f59d76e9bf5738b6f1bf46)
            check_type(argname="argument external_resources", value=external_resources, expected_type=type_hints["external_resources"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_resources is not None:
            self._values["external_resources"] = external_resources
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def external_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of external resources that are allowed to be accessed.

        A request
        matches if it contains an external resource in this list (Example:
        s3://bucket/path). Currently '*' is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#external_resources AccessContextManagerServicePerimeter#external_resources}
        '''
        result = self._values.get("external_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', that match this to stanza.

        A request matches
        if it contains a resource in this list. If * is specified for resources,
        then this 'EgressTo' rule will authorize access to all resources outside
        the perimeter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with serviceName field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9c01750a336673514456d0e2b05c52c53dc53e2e052d5804851eed2e199667)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with serviceName
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcd5d5f046fced630086ad798e169306cf5f63174fa5f1101cbb9c1be0a6d6de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50dc49621967d1249d00921148224fd71c23717e0f90ee9e761cc21b6295ed4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebbbc3746542d480c226da2a18190e3243aa44e3669d9eb42391b0cc2e6af60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ece7635def0a742b51e81f2f64fd7359f93a1134721110fd24f323229ff564d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b1634e1d81c1137ee316a7d69ac7a2b788b808af71a0f615fc7e97518d61493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b01d0933441d6f4bef22560e8dfc25351bc65689ff8752ebb0a91874789b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'. If '*' used as value for method, then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91af1cf29d9bbb59bf9aba64ea221da51467216b82937b00d21cbde3ac7e549f)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for 'method' should be a valid method name for the corresponding 'serviceName' in 'ApiOperation'.

        If '*' used as value for method,
        then ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__081c69117797858fdc2dd743e9bf0b69d03f553a55a699358d33dc018210b924)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74e808c9da1c8cf91915b82e87c4ea5314609a590c69a76c42d83d3d5782577)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aaf369971724b7926db099e7f5083d27eb5f54a834198d8b8ff5e6125dd6157)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d13d88ee0cc15ca4aaddb871c15c775bf2c057dabb98e61c6b7f8bc8a9987455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2c9681acb1a9de35e9e621c9a188712795634b57fd3ed87f72534bd98d393dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b26d59aebae12eb676fb8872f86ef574e1dc5d1b2380244cd7a1f072cc33ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d4040df566447ffa71b855bf8529169f6d161a3b83d0e57d5f3d44ad2798882)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8785dbbc6619b98cef49d5c073a1adbc83351a7fdfde770499922634191bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d9ad4d4b50ea84dbb98b8af90e46c6fd680677984cf348332e9c8a5a7339ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2957fd906f60dcf6df0878f88b835f883c31e286f37464defdebdfe543113dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c19120269a3bf2e7847b7b4d70ba777d32a65c04d3c72aa29477344cd3502cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ec81719b039165d5d92783e0c9df8424ead3ab2fc95f11d07a68a0c0718024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3a70c450484f780a6dd1a2bc31b677321cab3cf5db14d9038301eb307b30a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c843e7486d0cef334001c3c7c291de21b8ab1fee300adc6d7130f77f3edea913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced33bf37637c8a4906c1457e241b280eada42a8cd71bc82ef95c3632abb9120)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d88f58d2ae4cfe820a25962b0ed4bab90f0bf09fc3a996ddfa56e427186b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetExternalResources")
    def reset_external_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalResources", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="externalResourcesInput")
    def external_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="externalResources")
    def external_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalResources"))

    @external_resources.setter
    def external_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6946d22714ab6cdf73f6cb5c0be85bd42571141106720b7010e574d3b31885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22a067f86a42904a8f7ccf8b18c6fd09d74475a14ebe8a1bd1532fa698beb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7bb7feaedc860e684f8bf1721bf78071549c80a54f62960d868d7cd68124a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7821e77b22b236d3b245413693f7da342320a9941f825219bd0a0d70a9e17956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusEgressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c840bc45c98bef4bb144b148a36b74acc2ea14872f411887d8432038ac743d24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusEgressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47c10f93a3ed6181a0fe028008c6d74913e1a4ff1071aac822718e263f30166)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusEgressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c8192b01d747b3d308d26f9ff080bc7e372572330d98aec8071baa50f8d411)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2259c1ebba862af0a064f7c2ebb21da686358250f7b60e98e9c551efd8d64e74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3f5f3c98c04dfe34b722398c8d3df798a2be2c2741ef091e92459cd753d9404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3630e7a49f7136f9325a103557911cde41f764e62e30abb40554f029ee13fde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusEgressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusEgressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7252fc15aa3b622149c7f9f0f4fbc47d6ed131470695a209d777fef1064fda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEgressFrom")
    def put_egress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        source_restriction: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access to outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param source_restriction: Whether to enforce traffic restrictions based on 'sources' field. If the 'sources' field is non-empty, then this field must be set to 'SOURCE_RESTRICTION_ENABLED'. Possible values: ["SOURCE_RESTRICTION_UNSPECIFIED", "SOURCE_RESTRICTION_ENABLED", "SOURCE_RESTRICTION_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#source_restriction AccessContextManagerServicePerimeter#source_restriction}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        value = AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom(
            identities=identities,
            identity_type=identity_type,
            source_restriction=source_restriction,
            sources=sources,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressFrom", [value]))

    @jsii.member(jsii_name="putEgressTo")
    def put_egress_to(
        self,
        *,
        external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_resources: A list of external resources that are allowed to be accessed. A request matches if it contains an external resource in this list (Example: s3://bucket/path). Currently '*' is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#external_resources AccessContextManagerServicePerimeter#external_resources}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', that match this to stanza. A request matches if it contains a resource in this list. If * is specified for resources, then this 'EgressTo' rule will authorize access to all resources outside the perimeter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'EgressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        value = AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo(
            external_resources=external_resources,
            operations=operations,
            resources=resources,
            roles=roles,
        )

        return typing.cast(None, jsii.invoke(self, "putEgressTo", [value]))

    @jsii.member(jsii_name="resetEgressFrom")
    def reset_egress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressFrom", []))

    @jsii.member(jsii_name="resetEgressTo")
    def reset_egress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="egressFrom")
    def egress_from(
        self,
    ) -> AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromOutputReference, jsii.get(self, "egressFrom"))

    @builtins.property
    @jsii.member(jsii_name="egressTo")
    def egress_to(
        self,
    ) -> AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOutputReference, jsii.get(self, "egressTo"))

    @builtins.property
    @jsii.member(jsii_name="egressFromInput")
    def egress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom], jsii.get(self, "egressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="egressToInput")
    def egress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo], jsii.get(self, "egressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a888e349cfa2b81807a9af13b4ca258e71b4a15d298937503218c0d181d1ed39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baf093f99b4d89fbda1e6020984f830f867245490d0da34362c3b8af1e6f717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_from": "ingressFrom",
        "ingress_to": "ingressTo",
        "title": "title",
    },
)
class AccessContextManagerServicePerimeterStatusIngressPolicies:
    def __init__(
        self,
        *,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_from AccessContextManagerServicePerimeter#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_to AccessContextManagerServicePerimeter#ingress_to}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        if isinstance(ingress_from, dict):
            ingress_from = AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo(**ingress_to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ad73b043a0499d8b280956e2b6450f3f8be794207a02fb3f288c2a99f2eda4)
            check_type(argname="argument ingress_from", value=ingress_from, expected_type=type_hints["ingress_from"])
            check_type(argname="argument ingress_to", value=ingress_to, expected_type=type_hints["ingress_to"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress_from is not None:
            self._values["ingress_from"] = ingress_from
        if ingress_to is not None:
            self._values["ingress_to"] = ingress_to
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def ingress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_from AccessContextManagerServicePerimeter#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#ingress_to AccessContextManagerServicePerimeter#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#title AccessContextManagerServicePerimeter#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusIngressPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af02ca031f5ea96206826b4404cd731bd36fe006560e1f015a2b6e1b432b31b)
            check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identities is not None:
            self._values["identities"] = identities
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identities can be an individual user, service account, Google group, or third-party identity.

        For third-party identity, only single identities
        are supported and other identity types are not supported.The v1 identities
        that have the prefix user, group and serviceAccount in
        https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e74874b8f63bb994bd194611065d95eb5fe6522bacc4501915c950f4e71b299)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a1e520b2e734a53eb94aab03e064d91bb3d5ade8c89db89ca68dca48e6ac1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetIdentities")
    def reset_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentities", []))

    @jsii.member(jsii_name="resetIdentityType")
    def reset_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityType", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="identitiesInput")
    def identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTypeInput")
    def identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82788d45b9b5240ce4aa95536ec0a3dda2fbcb7c94907453e6dcf39c5c1d2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ede02bc67716ddfacbfba46cc8aca9a201cee718956c4f061600a26cc62a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574abe8097c2879a3fea8ee1430c3f8f305d28a91c93b261eabb80b573ab78dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects and VPCs are allowed. Project format: 'projects/{projectNumber}' VPC network format: '//compute.googleapis.com/projects/{PROJECT_ID}/global/networks/{NAME}'. The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c572f46a2f083bdf8c3f591a12e62070bd94855a44fc0e2343fffeb08685a44e)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet.

        'AccessLevels' listed
        must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent
        'AccessLevel' will cause an error. If no 'AccessLevel' names are listed,
        resources within the perimeter can only be accessed via Google Cloud calls
        with request origins within the perimeter.
        Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.'
        If * is specified, then all IngressSources will be allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#access_level AccessContextManagerServicePerimeter#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to ingress the perimeter.

        Requests from these resources will be allowed to access perimeter data.
        Currently only projects and VPCs are allowed.
        Project format: 'projects/{projectNumber}'
        VPC network format:
        '//compute.googleapis.com/projects/{PROJECT_ID}/global/networks/{NAME}'.
        The project may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the case
        of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resource AccessContextManagerServicePerimeter#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc9ecdd6b944f2316f1dd8dbabcb5556af10bc83ee9031f5226dcf5921949eb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90b93ac7602bad82e55e5ad53ec94e374640bc5782a38d0c4c77b43c03c9b17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ae409e9398358a0e4b997942e04cc8cb5d497e43b6c1253c4aa19911770e4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a215f33e715fa4ed5ec063689fa6a997dc527884b20e4af6bdac4a3650ac67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3022719aa7d2af56b0588001fef847dd0fe3f87bdc857154e531bc4c703e0b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da5e551dcbe73958445f3f74da9647ee7845182abf97ef06d6802c9aad91609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61f748de49af8152090c5d499e40e1a1f497b7982429e8531870fb177c2b49d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessLevel")
    def reset_access_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevel", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30855ef542d9334259418553b858b8a66308c23bfe2b12983735b5a5e43e5e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b120282c0ad3314250843588865d7e2b057213e12959866e9474cb5ec3c0fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dc7bd23b5d51ee88c0250f72d4238a3f748c3805a267157642d9c27bc8e6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b01ab7c9ca598c5bc6ef8a7ac9498cd7282af4c1400527f15338962b8a6c0e)
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operations is not None:
            self._values["operations"] = operations
        if resources is not None:
            self._values["resources"] = resources
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6531bef9e053aef21f3770c48766a2124a89b8a8862b97652c0e944117d82753)
            check_type(argname="argument method_selectors", value=method_selectors, expected_type=type_hints["method_selectors"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method_selectors is not None:
            self._values["method_selectors"] = method_selectors
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def method_selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method_selectors AccessContextManagerServicePerimeter#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#service_name AccessContextManagerServicePerimeter#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcae72b2c4f19f99fe6a3e4da7b8e711dbb0da49fd28bd0b4dbbb03d589a2069)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18853425a13068374c1730d9dd18300b51d80de1c764d6aa0ef508edc532d4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c286bded7bf85a220e4bc0cc581b50272f95621d5778a4d3c55a03b6955f1bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f11bbc8d2bb42404af44723e28d7aa3fb66ab7d15135d72f4d7f30c89ba6f3fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af4778699274154f20dcf86e27081c9fe24bbb1f30b8975b19d8332e108ea1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fd11b1158be93a32060f60d6ced414895f47debc3692cb623968694100dcfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f38c40b18451f31b2b30896f8189d63d36a0fb4fff4f4d8a1cbefdc7eb735b)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'.

        If '*' used as value for 'method', then
        ALL methods and permissions are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#method AccessContextManagerServicePerimeter#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#permission AccessContextManagerServicePerimeter#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__582f75356a392236bf48e868a1f2ecc4309dfee12045b22acad93592f479b578)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002ec570d04afa65cf87e29b46b4c1f4cc39f4813c0ab09d1e08229e94373ad0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9061d5fa9428c8eb305f9ed45932315a761158cd0a3c5d674d74280298f8223)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf85af8e33a2ac27246761e7e3b22105d0b955e373f21d7082a4d885732163a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c14b10b515ff7ecf4fe58ddb0e57c6e8fe99d392b2ad977c624e8baea129b809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8515b1348af0d957161d7effc10456f7657b2127685264bc66b57e9a6e5dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1b83e54e16a92eb449b02e44e15e0714b05ffe7356bad2f92c43bf26c22ca9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7eba791a4c77d3f1f1f674098b0a8334b8111dfda59d6b0a2921a2d063645d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87f6019fc253dd11f3d3e63fd88a116792f6cb7db9697ea9641295982210575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2adaa319aa74d6e6058648f2d2695ff647c4872c05e55e8a95cf66db9b35bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66dc9877f26c928d678641d38c28fdb797b8b8edca090af813423b5a02ae6fb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92dd14df5b0e1013e001f0c8b257896a67af83412543901347d29ac5be018fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMethodSelectors", [value]))

    @jsii.member(jsii_name="resetMethodSelectors")
    def reset_method_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethodSelectors", []))

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="methodSelectors")
    def method_selectors(
        self,
    ) -> AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a30c2f56563f22fe5d73f74d6d4b00c775e1e497f3a38eedae94721848b1153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35b3fd481d9569619070395cfb4c0fea2ea254cf2a0c9577176ffcad648fd2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4614193489258897b600c6b7cd4f4773efb0dceda8d5ebd1cab7991ea5cd2b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4e0be24dafd50b8f14e0566847d2d934464651f6d77d1b19f7ff66586589a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b59597c03c727be9922349cd84ca5393e8ff8c44cfff8a08056c667a8e98ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea8202edac34f72424ce91799335939c96775303c893ff7791a565ecee1945f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7f859106c8ba2ba2f045ade20cc37b23420fd9c70b7b16ef6d501e21cb66f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusIngressPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2501c7e3dc5ca190cf4b8d8abce2c973071c981e0fd2ad1d6989294202e483c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterStatusIngressPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87aa5bbe828a4c4b0a03ef56ff614a38417741c76faf0a120ec67d21a048c67f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterStatusIngressPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e87bd31d4d37a39740bb9515a8be18c60d2fd96ffbb0315ec6a52cb91e92fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db2fa02ea57aa4111413869c1928b4a8a8c44eda01f2710974454b2eab18378c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d2e9e87587265efb0842af3a157e55a71a700316eccbcee1a006587efe36a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410a576672d151a8c7aab37c38f4c2e587b9318b58667fc6bdfb1e9ac537468d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusIngressPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusIngressPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef7f7f5b5ca027e96acbd3795d89475bdfa1fdcece6403855249857415bbaae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIngressFrom")
    def put_ingress_from(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identities AccessContextManagerServicePerimeter#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["IDENTITY_TYPE_UNSPECIFIED", "ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#identity_type AccessContextManagerServicePerimeter#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#sources AccessContextManagerServicePerimeter#sources}
        '''
        value = AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#operations AccessContextManagerServicePerimeter#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#resources AccessContextManagerServicePerimeter#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#roles AccessContextManagerServicePerimeter#roles}
        '''
        value = AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo(
            operations=operations, resources=resources, roles=roles
        )

        return typing.cast(None, jsii.invoke(self, "putIngressTo", [value]))

    @jsii.member(jsii_name="resetIngressFrom")
    def reset_ingress_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressFrom", []))

    @jsii.member(jsii_name="resetIngressTo")
    def reset_ingress_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressTo", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="ingressFrom")
    def ingress_from(
        self,
    ) -> AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromOutputReference, jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOutputReference:
        return typing.cast(AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOutputReference, jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo], jsii.get(self, "ingressToInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8e48a40faa555d64175203c2099496c24f43f4a6615fa74eb166a611de4a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fda671bdc942aace02e4989b2c3fdc0c9472453eeb7a2cf27b8c9fe5510a5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__134037e4bb108e575fee1834a14243a78fe237a03bd40582afaf685f7b6412e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEgressPolicies")
    def put_egress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fbf1f79e498af59a234f5904ad2b98a0a5978e2489ff89c7b9882d94cbec07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEgressPolicies", [value]))

    @jsii.member(jsii_name="putIngressPolicies")
    def put_ingress_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1756886d26b0124930a0a2a9f5771ec31d3aeafca86007008cf7ed2d16c500bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngressPolicies", [value]))

    @jsii.member(jsii_name="putVpcAccessibleServices")
    def put_vpc_accessible_services(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#allowed_services AccessContextManagerServicePerimeter#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#enable_restriction AccessContextManagerServicePerimeter#enable_restriction}
        '''
        value = AccessContextManagerServicePerimeterStatusVpcAccessibleServices(
            allowed_services=allowed_services, enable_restriction=enable_restriction
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccessibleServices", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @jsii.member(jsii_name="resetEgressPolicies")
    def reset_egress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressPolicies", []))

    @jsii.member(jsii_name="resetIngressPolicies")
    def reset_ingress_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressPolicies", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRestrictedServices")
    def reset_restricted_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedServices", []))

    @jsii.member(jsii_name="resetVpcAccessibleServices")
    def reset_vpc_accessible_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccessibleServices", []))

    @builtins.property
    @jsii.member(jsii_name="egressPolicies")
    def egress_policies(
        self,
    ) -> AccessContextManagerServicePerimeterStatusEgressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimeterStatusEgressPoliciesList, jsii.get(self, "egressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="ingressPolicies")
    def ingress_policies(
        self,
    ) -> AccessContextManagerServicePerimeterStatusIngressPoliciesList:
        return typing.cast(AccessContextManagerServicePerimeterStatusIngressPoliciesList, jsii.get(self, "ingressPolicies"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServices")
    def vpc_accessible_services(
        self,
    ) -> "AccessContextManagerServicePerimeterStatusVpcAccessibleServicesOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterStatusVpcAccessibleServicesOutputReference", jsii.get(self, "vpcAccessibleServices"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="egressPoliciesInput")
    def egress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPolicies]]], jsii.get(self, "egressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressPoliciesInput")
    def ingress_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPolicies]]], jsii.get(self, "ingressPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedServicesInput")
    def restricted_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessibleServicesInput")
    def vpc_accessible_services_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterStatusVpcAccessibleServices"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterStatusVpcAccessibleServices"], jsii.get(self, "vpcAccessibleServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010339e8069f2ed1aca77ebdfaf9e07344e904a8a06a7edfa6af3dd3c98562d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e758551c6f4154e748deb2404aa4d49fc4de3b6bf495839259c96d1305b77d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedServices")
    def restricted_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedServices"))

    @restricted_services.setter
    def restricted_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f9f25fee5f5c19211644c56c0bf3094d3fdd15d76e02353492608a98eb3ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatus]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eee72a789c07ee750025f77fd4d8a9e221dd01534a4fa13dd8a7bb879bcb102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusVpcAccessibleServices",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services": "allowedServices",
        "enable_restriction": "enableRestriction",
    },
)
class AccessContextManagerServicePerimeterStatusVpcAccessibleServices:
    def __init__(
        self,
        *,
        allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_services: The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#allowed_services AccessContextManagerServicePerimeter#allowed_services}
        :param enable_restriction: Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#enable_restriction AccessContextManagerServicePerimeter#enable_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7dfe3d3ce3cb07e026a5735721e05874a62c125b6a67bfb2159734b76de384)
            check_type(argname="argument allowed_services", value=allowed_services, expected_type=type_hints["allowed_services"])
            check_type(argname="argument enable_restriction", value=enable_restriction, expected_type=type_hints["enable_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_services is not None:
            self._values["allowed_services"] = allowed_services
        if enable_restriction is not None:
            self._values["enable_restriction"] = enable_restriction

    @builtins.property
    def allowed_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of APIs usable within the Service Perimeter. Must be empty unless 'enableRestriction' is True.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#allowed_services AccessContextManagerServicePerimeter#allowed_services}
        '''
        result = self._values.get("allowed_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to restrict API calls within the Service Perimeter to the list of APIs specified in 'allowedServices'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#enable_restriction AccessContextManagerServicePerimeter#enable_restriction}
        '''
        result = self._values.get("enable_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterStatusVpcAccessibleServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterStatusVpcAccessibleServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterStatusVpcAccessibleServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a60811128264e4d003ecfb06487a700845d26c50beb1166812f571dbc2343415)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedServices")
    def reset_allowed_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedServices", []))

    @jsii.member(jsii_name="resetEnableRestriction")
    def reset_enable_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="allowedServicesInput")
    def allowed_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRestrictionInput")
    def enable_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedServices")
    def allowed_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedServices"))

    @allowed_services.setter
    def allowed_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04cfa4984509485c79a980ff7e55ca6e2928eec4034ce802f3d3253fc9d54431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRestriction")
    def enable_restriction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRestriction"))

    @enable_restriction.setter
    def enable_restriction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b76d50a03455e1f4d892c756e2112dccb33002e4d7a9dc4dd1ba484a5c7d64b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterStatusVpcAccessibleServices]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterStatusVpcAccessibleServices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterStatusVpcAccessibleServices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d33540d39f117db63b09a40d05899a8376d4a9ea4ecbe8e0754c79cfd427a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessContextManagerServicePerimeterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#create AccessContextManagerServicePerimeter#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#delete AccessContextManagerServicePerimeter#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#update AccessContextManagerServicePerimeter#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31dfdcb9a79df16e72d15c6b4b7b1f7c2eb6783d3a5d2a225917f08b4c97e42)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#create AccessContextManagerServicePerimeter#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#delete AccessContextManagerServicePerimeter#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter#update AccessContextManagerServicePerimeter#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeter.AccessContextManagerServicePerimeterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1fadcfab5628f9bdae10b4b7e11b5a3aec83ec1bb86a325382b874b41d6d9cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfb5496d28498e537fde845d54119188718eb7bedaa9a1cba14e688a4ffcab3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d435048fad717a368b45489f1d40150c8305c8addda8945365bb6cb5a398f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd723a2cc90848cb02f54079fac907c9dea3f899e2f53e13e292ed8c2631e913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe766da0e5cb887bd6f06724365c4dbd96a782068c701a3deeccc99263858fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerServicePerimeter",
    "AccessContextManagerServicePerimeterConfig",
    "AccessContextManagerServicePerimeterSpec",
    "AccessContextManagerServicePerimeterSpecEgressPolicies",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromOutputReference",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesList",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSourcesOutputReference",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsList",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsOutputReference",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOutputReference",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesList",
    "AccessContextManagerServicePerimeterSpecEgressPoliciesOutputReference",
    "AccessContextManagerServicePerimeterSpecIngressPolicies",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromOutputReference",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesList",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSourcesOutputReference",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsList",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsOutputReference",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOutputReference",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesList",
    "AccessContextManagerServicePerimeterSpecIngressPoliciesOutputReference",
    "AccessContextManagerServicePerimeterSpecOutputReference",
    "AccessContextManagerServicePerimeterSpecVpcAccessibleServices",
    "AccessContextManagerServicePerimeterSpecVpcAccessibleServicesOutputReference",
    "AccessContextManagerServicePerimeterStatus",
    "AccessContextManagerServicePerimeterStatusEgressPolicies",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromOutputReference",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesList",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSourcesOutputReference",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsList",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsOutputReference",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOutputReference",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesList",
    "AccessContextManagerServicePerimeterStatusEgressPoliciesOutputReference",
    "AccessContextManagerServicePerimeterStatusIngressPolicies",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromOutputReference",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesList",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSourcesOutputReference",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsList",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsOutputReference",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOutputReference",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesList",
    "AccessContextManagerServicePerimeterStatusIngressPoliciesOutputReference",
    "AccessContextManagerServicePerimeterStatusOutputReference",
    "AccessContextManagerServicePerimeterStatusVpcAccessibleServices",
    "AccessContextManagerServicePerimeterStatusVpcAccessibleServicesOutputReference",
    "AccessContextManagerServicePerimeterTimeouts",
    "AccessContextManagerServicePerimeterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2ea01145565edb1cf7cef28821509525f981c6e49c3f70708f7d46bf57acaecb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    title: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    perimeter_type: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimeterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__dc975870545842087dd78f7185128a29d51c8a67f29dc02a5c062e1065af4196(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ff62d8ccb2f9925c4fabfa43c73c62bb68bbbc560d04bc8a2bcae74b6eb55f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc49484ff5f3db1a8f90e05ca861c999b7c599ee9e6e75a22ea4ce25278e0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4b3015bd9df41435cb61fcbe1e128f1cbe9c652647f538c6d1668131827870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ef923f14bf5565ad71c041a6bb663c9949a437eb36268d1b3e4828384257cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204854beabc352119ed07145b447b7e20415095be1abd7e22a1e2184fd17f34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd6079920771427c53dd30b747e39d0f8d87a04bdb08fa877ed35fedd14cb51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c31e65d024d5f6b9a3cc4b3c23544eedc4574e320badaa30bd1dc46e50c409(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9501e26546981e0c8095e545bc58731b632287571708642f5c6cdd9a35e41fb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    parent: builtins.str,
    title: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    perimeter_type: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimeterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_explicit_dry_run_spec: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dcee124c0487559970302b3886915da65d488359296c9b4cc282d9e8a5e0bf(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_accessible_services: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpecVpcAccessibleServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cd08dbab1e8fcba9ce01590ce54655d5f0efe35bf8413a4f546858a219a694(
    *,
    egress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01856b80585f3d86dbdab3a2a879267b7c6c51940c8ebe4685b67c7ad9c42e25(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41aa72aa08518c0b83ca635d1949ad314ccde7cae8468e65c08037d497f9598d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1397dfd3aa5139f3c87318758680a1d3a413e0b61cc5ff48e33c9dbd8f7adab9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113f0440eff061f45d89ff445025f95b247f44cd0a1344cdaca1b819a39b5e58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828a0e744b8dc69e3d9cbd12514052e4564228904e264d4545a7d7a4b8d6ca61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8116b8bd5a73c5ec855d1e82d7dd57f6806fde6104845533313ef868514d1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1984209bc4de2295c76faf8558a92c9ddafa5279b8022f2e2f26b87399dcd60(
    value: typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa26cc085910f903beb3bb44cf266086b29e9eeda011949221a7be4e7aae37c3(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc1d0a974c1145143e749afaf5996b21b40cc421013daf25f9e0f368e1933ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e299e6627016a327342b1d9a72f1495185eb893a2be42e7a9bad379ddf0603(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c66204a1e26fb1820b08e1ec04cec4f2ad1a529a2070b589229fdc5f5ebddbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea4a2c74452fe9162797ed6e9693bb02e3d2aaa0681aee3a6b76368d59eab26(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d665bdd1a1ad47651825284a085179c970da3828d4f5598ddf46419d6405d72(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149c81a4f55f758749bbed5050b844bcdb47698e4a79371542c3838476df55f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdeda582db5019109b7002a4313b6e4f040f456dea536b32373959f0628be9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23be8ed6d9f24098cdcbb6a654d188a93f80fe3f0e2bbd45ceb660a24e9446cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe097cb2ca51f23b468436f104fedf1223596f54461c9ec1736b44abe926398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3773165bf6113693a92d5197d087f98d6ef603275d1314c62efb7505c8d83e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541126ea0257c464b21c268c55cc07c4361a88042d327c8513f816c3d6dd6bc2(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636af21a70c56163b684852bbfdf6da5bdf18f074200901ee891e50c8c9cadc6(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3282dd35af911df00fb73f16446cb8e50a1c8a388b0a8090f1523ae90b18e7ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab5c7a0448a951fc7b544961658e6b20ff790ed0fe079b5abb45b9a812b53d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4641ffbd318378d6ddf76503459bc703a5470e83e043fbdd33e1b7a6502b450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b3dd5b8439e6814e0f3acd41f20eeab65f07505909e4891ecebcfd29b75352(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f8220ab35e8e79aba7c0b5901a5d234e615e8647b0153aef8d98a87b155cbb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631e1f435eb358e00b7be26d8c905e35876484b2137911f7ce80b8d95e9173ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24611fb0eba9b08d77efd0f0d9da091ed90b1a57db8a57e5b5c04b8b7a943194(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cf32c3dbd4e6295e51bbe11a9555ebd265f3091875e0e2605f6a76d80ef68a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3bc51b8e1d30af4fca5ff8c8c4796d37efdb721e7729341f5ae124c5fa8d19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f1d2b4a73691c11411c3209708970bb37c6631a3005714a5b6769e1617190e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e03135d3f10b6f2ce0c6c2c9d4cb8c012a8f1e26fc3247424581f79630489d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a121a196f056b482bc9d9c827102243f8eda81956ec7fc1904ac4b8a8feb0d28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f59b8bbf7a703cdaa0c78f21356a8dd4f8a965c99764c719d18e8aa5885543(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85612b55c2cb2dbe3bafa1d9c5004d580e234d05b2f45f4cc2dffc9c0122e662(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e82eaa02f39a4ac4d963421a499283fdb47455545a21145c615cbdecf48dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17cddbc04b3d955027da19181344f6eeaa3325e1a20d47341def9ceb84e5bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321a6f0d39afa385e6db2ae292e69cfb86fae8dfce2cf1324bd59425bd05084b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dfa698d0237b4533c2282557bfacde372f230921d0c6e7a0ee5ee2ac9c5148(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fdb5b34b39f19239f097d1a811477b39581efef1bd4b22e76353f4fb570787(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4dcaefe537a6c725f71e2789bd527641db751c2203d85ca80445df089538b2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edd393da598c2f5d3773403f4233a26cf8b3a69bd0044bb666105763e955ffb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff964c23590031cae0cb373814039103fac9418592171926f58ea589d171104(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efac8381b967ff001d53fdf72d6c246db6ce9047168421413d7258d0c33a2ec2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d076fe8375c87958e5842490300576274a9730ae8b17c3f7bc8efe128fe9b3e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0bd89635100a38a5d2c45057a86a4ee1612fe5137e0b240272ceffe2b4a41b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a801f18baac9c11d677750c6484fbc4f9c27396689f737628ad6d57f468eac6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d740b328c7277f689dbb4e0d72f641c8a8ec5e00a5d2b8993924b8a615b155(
    value: typing.Optional[AccessContextManagerServicePerimeterSpecEgressPoliciesEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65763458290c7fd51d78c10301a6c451fa539e3d95de8a954fd939af1aa960f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe0da00cf3098b0529fd399b272aa8fcfd3c86b5e73514bebf375469b867daf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a402e72d1aee53658fdad33135401b5b7e12d826e114e49f3e674db4fc77354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518e40d902b832d9835d10cec207a925eceb045b93736babee9b840be15c70e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d54bc3594028b0a4694a66455d5d1adcbc73c867b6983124eaa246c5afc779a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f620a051c49e76ef68e526a05adea8e16c7aa3361afe3f1d3250a25aae035e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecEgressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61a49e9f552c9944b63d0b596195d0828027acf8411b1ddc69dc92f907bb5d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da56decedc44ef15f7be524d67fad750e1cac580f91576960df7932ae530a830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad692999ace735f2eac12f699add7b1de8b976d4d7392013a2c43019938dae5b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecEgressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae5923c3d496f1aece930f3c8d17008e45f76785287c61132594bc22b259cef(
    *,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b391cd53f0929ca560b732b04572a7574f6ef832f4571fec124ec89cafc286(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b895a23f69d2089d11c140cffb3c7fc507afcca922ebd09144144b866a43c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7570fbe45b16027d090d1ec8093fd890f38c6d8d190ad144890a4f79e446cc7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e86e023eb35fba1a8cab478f2076fb4277bfc73f3cc6315444eb59699a8a021(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cab6562b2b2d140557b046733a5017f54ef3a41e6701808ebc34a93b670ee02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc797c76eac65d09584003a61e4568b402a59f1341b42229b9d917ab035d208(
    value: typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b609967725522f6dfdd65b6f5409a9b5804c581151bf4c21cd8aeb614ea42d(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ca50b64266d6de0d7e883209f3d6057ba5bbf82641cd24db2e8afdb94221e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cdb64219d20d8d6a45fc853171adffe24f2b2dd440bd3c965784b3f6c15213(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ceb718f71d8e0b6338cfae159e368089379920f301efb61542ca4db3d51bb12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016356fadcf2f7854cc030020e18b94037d7258f6fbcc4ad1dbe42abde0072cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3416dd475a176e38c68f514e5433965a0c8efac7dddaaa345f399a73b5119031(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7baf3d560146799a0e0052d277ec939b7037eb8c2c691c5e5a920c7bf41626cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794f41f2538a577aa9a69a7b174d49f95122edfe846a3569818fa036c64c9822(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c258e99769e498a136664bf8526943a64c43250779bbcb2201ae6254a181fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248d1d02097e31266e0a6975fa328ddbbc4e084e957dc6395d68300cab8b3cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79a4661326d6494ec24d796f954d2f351c5b70946d2abfa6babdfc32079ab9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419e2e89f6261ad1087b5407797ff772ca5e8cd537c3b1db285b278060777cf1(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d719f428c353427537c2c50e940b5472a9718d79a0960ebea2107ec02d6c7437(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4716ddce89a62754f2724d2fe053ec2c44c90ef4e98a000ec53ede1a74bce22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701ed09ee82fb5f74ecbfad32ee9d1f8d0cdb38b9eb7b99dc7ab7161fc0db253(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb08c74274e12cbd2152e070474884bab6a65832fd902b7a495b0cfc2199c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34df57b028c1266f4849940979b5cad2102aee6e3763636c7667e50b8e81b58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d0c8a4e769d561f87613376d35884ae52704e4afb96d65b97e8dddc546f35f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491e38d70156691cec2fddb50d589fb1a035f99050cfe045a80a975a4fec56d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5ec22892bb476eca65d6d1526c32f5f44a37c0dcdc2ec82f978f10a6bb16c1(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516794f95060636a7e2c5aaf74ad13b6d97f8d2e0065e28dd0156c023d8fd4d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bc2ac12b49b00f510357f049de275713de878ec6c95440c3f77e6e84853eff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d5a775eec1dd155931e9b9421849d33f9dd4e5da56a3b29cb78c5406e2558f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e1b02156e41df68db3addd5bedbc0755400957eefaf8055be883c1d5cf78e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242c9516bd3bee910488ea702b9eda597b9b403881f99ac4868f8def8712b221(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45feeddb7feb12e47fb7933dd07f4969c1305a1c964104bcb13aaf43c5c1a67e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd9f12efa9942d7fa00a42616325c5e194f5a855d8f57bcc95edff5f59ca227(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af002925224676a80c487f07e09f437e20ab3c7b5bfec3d965402f31bf110ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cc6513cc6c0ebee35447e5a356c7669dcfa11be995e4d71e3aac801682e43e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360beae8fff61bfbeeea18a65a2d98df01f0b31018d4bbdeef858cf75c4f9e1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6a45691ae606ebb63fdaa359a2e2c7e0de9f1b253ce29134837ef46235ee1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225c11c1dbf49449b152a28cf28e111343df4ab63a4332f706faadf7252fd52b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce9a807889bf348da0be849fa4d5872366c0372f22aaaa6ca7884827ac4e04b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c1ddba2273e19649d403e6ee693a1e1c6bdb54ea687ebf833d904e0eb38561(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d75d3a6f2c0c8c754fafc07a79fba1413651f0440b775334a660fcc57ced14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ded0a54aae7aaa9b54b7eefb6f886a0570e7bd7c6edcd77695ab17ff55526c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e06486f0df20351ab5530117638d914e8e73761f959cd7d15c4a5a686c6918(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f456606f65603da1b9d4662883165db0447d0b16710d99f87f38b496bd22fe6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a401cbfcef63bd5408833a1511e5e39823c8af21ccd733d9efee33d5a03cbffa(
    value: typing.Optional[AccessContextManagerServicePerimeterSpecIngressPoliciesIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5e67a73acd6e9cc46b4ded158b6487c254cab4a775ea8ded011bc82056410e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839cc41d969379a9bff8ba9901a9ffbdbecc71eb01d8d8d06e46da310ad0753e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9068247c974c3c8ec75d409370a4aa350a22c04b753cbdc64846b2ecccf9ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a8fdfa147724382c84f9765d97bf794ed724c54b5e2aee870f490ea81fd6b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b396f53d8903490479f86a98d3df314e98574c63837d976353558ce745fdb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b147d7fc224da20f5d0b03ce6c15262d2e837a7461e7c1362c68a64a61b49c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterSpecIngressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec8f836fa92693e7ba5ee5ba8c1d4b02559c1a8d2197614b20d3d4a41b0e552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee71f15124fc516a8bc73af2e0566257834da3b64f11d2867379013efa2acd9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69dfa31127877b443652ef97354e354a140eec34bc35e06d9260ac6bc10cf540(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterSpecIngressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d6e2aad54e9d3263a35181f96eb888b3d345ea3006d91aa53edac90ebda25d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12c3bf0daa6ff526e922a21081354862e4ddbb7f5d8f2c9df65aa3239232d37(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aa3b68643b256303848652eabdbaeac14b4038d26edf1a3484353a7b6a069a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterSpecIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d4c4b869d5dea24b5905fbd48d7c8fb3df138c2fb13b897ef046f7814cda00(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fb7dc58251ba310f7fd951890bfc2cec43d9dd1adfa878a545562493371f35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828381e00b333973d5eeab0b56d06b333b38688f6ef84d94573ed0fd432f6896(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bb9cf0f38ae0c1f1e7a812873ccddaad1f9dc76539fe860a7f0461027583b3(
    value: typing.Optional[AccessContextManagerServicePerimeterSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243d35481fc3586171d6a3d7c330efcaae9a2e737e0e7e65854337ae08e6b386(
    *,
    allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7617b1fb4017955f97539a1062112a3699a28bdf0acd18c3d5627402db5e285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5696246d94640583a5f6082fc375289e6d53c715c66b246c5eb67fb94b0bc31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9b1167bc0ff963b2576f7db8faf9022c2232c1fba31673098df93951e77328(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e8a87127a332a3f7ab0002ac473c4ab6d27c597766518b5b2a8b5ef8a387e9(
    value: typing.Optional[AccessContextManagerServicePerimeterSpecVpcAccessibleServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e710c7f9b0f668fb3ad6e29a864c23f099c1d928518abe7305c31947a846193(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    egress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ingress_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    restricted_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_accessible_services: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatusVpcAccessibleServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418335c724bc5f81a9054297a41894d473415f08dbf7ef6e2b94ee233c01ad22(
    *,
    egress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    egress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3fe2bfb4154bed2543e03041f47edf8a1b4c550a29f2e11c726983ffc6cf22(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    source_restriction: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90efa0b2fdee4b54f0cac1a88a77a06079d63005d7b329e5ce1d0c5ff13bfe8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731970046315edd734f3d8f6e4475de69e9cf183969436d44af5b7f7bf1f8a4c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1be10957878a39648a9c55af8cd52d9a4a5a036d370148f41de16855733363(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77bc627559e4031b3680c703c8df6e4e5b576f3b31be3bbc16a58d78dd4b4dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d8dc67f330384e76a5893159dd8097725775afe56bd58fdfb32b783bc400a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7324f5953916f9c906f3e1ffff498277469b04af0095722a17e924a4a7629a79(
    value: typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b4ee509236eb10b9d75d17ee5291407e1cf03937f3c414ea0b4ee9dcd2157d(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d0d18a814468c9c680a76c2bf32ad098fa553e16d9e2d5881aa98354d08206(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5594b5006ffb1cf6159b036242e96fcf6cd43929667dd4026040495316b277cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce58700dcf04ae2fb998ae02e385b3699eac648c4af224b9955d07e36c25868b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d077c146ea9a9a0aec19675f5385edfbb40178075552f499bf5a85f44bdf96a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ea7dbd04ee9b917790755db7a642ebcf1eaecefe9fa4be2b7f03ef9edea4cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9e4e3570eacaf56e2409b86271114cc5997f9740aa2da640450817401db76c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e315cb4496647a95786c60e8604357dda948ba19e47997041dbcd03e92714bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ef32740b88b6adc072ce9a811bf72664b34b423d0e89c3e8a521be6a0be372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890064ff0dcdf1adfc8bc9c1da731d72f3ded92cea6cb0cfdfce46ba858d24e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd351eee02292ada2eb61597b35b11b8e5de4e1d704cb369e99373cc79f4cef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b49c7b4d2022c68f7f485bbbc9861816826b6038f59d76e9bf5738b6f1bf46(
    *,
    external_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9c01750a336673514456d0e2b05c52c53dc53e2e052d5804851eed2e199667(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd5d5f046fced630086ad798e169306cf5f63174fa5f1101cbb9c1be0a6d6de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50dc49621967d1249d00921148224fd71c23717e0f90ee9e761cc21b6295ed4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebbbc3746542d480c226da2a18190e3243aa44e3669d9eb42391b0cc2e6af60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ece7635def0a742b51e81f2f64fd7359f93a1134721110fd24f323229ff564d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1634e1d81c1137ee316a7d69ac7a2b788b808af71a0f615fc7e97518d61493(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b01d0933441d6f4bef22560e8dfc25351bc65689ff8752ebb0a91874789b08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91af1cf29d9bbb59bf9aba64ea221da51467216b82937b00d21cbde3ac7e549f(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081c69117797858fdc2dd743e9bf0b69d03f553a55a699358d33dc018210b924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74e808c9da1c8cf91915b82e87c4ea5314609a590c69a76c42d83d3d5782577(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaf369971724b7926db099e7f5083d27eb5f54a834198d8b8ff5e6125dd6157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13d88ee0cc15ca4aaddb871c15c775bf2c057dabb98e61c6b7f8bc8a9987455(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c9681acb1a9de35e9e621c9a188712795634b57fd3ed87f72534bd98d393dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b26d59aebae12eb676fb8872f86ef574e1dc5d1b2380244cd7a1f072cc33ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4040df566447ffa71b855bf8529169f6d161a3b83d0e57d5f3d44ad2798882(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8785dbbc6619b98cef49d5c073a1adbc83351a7fdfde770499922634191bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d9ad4d4b50ea84dbb98b8af90e46c6fd680677984cf348332e9c8a5a7339ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2957fd906f60dcf6df0878f88b835f883c31e286f37464defdebdfe543113dc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c19120269a3bf2e7847b7b4d70ba777d32a65c04d3c72aa29477344cd3502cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ec81719b039165d5d92783e0c9df8424ead3ab2fc95f11d07a68a0c0718024(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3a70c450484f780a6dd1a2bc31b677321cab3cf5db14d9038301eb307b30a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c843e7486d0cef334001c3c7c291de21b8ab1fee300adc6d7130f77f3edea913(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced33bf37637c8a4906c1457e241b280eada42a8cd71bc82ef95c3632abb9120(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d88f58d2ae4cfe820a25962b0ed4bab90f0bf09fc3a996ddfa56e427186b24(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6946d22714ab6cdf73f6cb5c0be85bd42571141106720b7010e574d3b31885(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22a067f86a42904a8f7ccf8b18c6fd09d74475a14ebe8a1bd1532fa698beb72(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7bb7feaedc860e684f8bf1721bf78071549c80a54f62960d868d7cd68124a9d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7821e77b22b236d3b245413693f7da342320a9941f825219bd0a0d70a9e17956(
    value: typing.Optional[AccessContextManagerServicePerimeterStatusEgressPoliciesEgressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c840bc45c98bef4bb144b148a36b74acc2ea14872f411887d8432038ac743d24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47c10f93a3ed6181a0fe028008c6d74913e1a4ff1071aac822718e263f30166(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c8192b01d747b3d308d26f9ff080bc7e372572330d98aec8071baa50f8d411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2259c1ebba862af0a064f7c2ebb21da686358250f7b60e98e9c551efd8d64e74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f5f3c98c04dfe34b722398c8d3df798a2be2c2741ef091e92459cd753d9404(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3630e7a49f7136f9325a103557911cde41f764e62e30abb40554f029ee13fde0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusEgressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7252fc15aa3b622149c7f9f0f4fbc47d6ed131470695a209d777fef1064fda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a888e349cfa2b81807a9af13b4ca258e71b4a15d298937503218c0d181d1ed39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baf093f99b4d89fbda1e6020984f830f867245490d0da34362c3b8af1e6f717(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusEgressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ad73b043a0499d8b280956e2b6450f3f8be794207a02fb3f288c2a99f2eda4(
    *,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af02ca031f5ea96206826b4404cd731bd36fe006560e1f015a2b6e1b432b31b(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e74874b8f63bb994bd194611065d95eb5fe6522bacc4501915c950f4e71b299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a1e520b2e734a53eb94aab03e064d91bb3d5ade8c89db89ca68dca48e6ac1e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82788d45b9b5240ce4aa95536ec0a3dda2fbcb7c94907453e6dcf39c5c1d2a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ede02bc67716ddfacbfba46cc8aca9a201cee718956c4f061600a26cc62a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574abe8097c2879a3fea8ee1430c3f8f305d28a91c93b261eabb80b573ab78dc(
    value: typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c572f46a2f083bdf8c3f591a12e62070bd94855a44fc0e2343fffeb08685a44e(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9ecdd6b944f2316f1dd8dbabcb5556af10bc83ee9031f5226dcf5921949eb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90b93ac7602bad82e55e5ad53ec94e374640bc5782a38d0c4c77b43c03c9b17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ae409e9398358a0e4b997942e04cc8cb5d497e43b6c1253c4aa19911770e4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a215f33e715fa4ed5ec063689fa6a997dc527884b20e4af6bdac4a3650ac67(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3022719aa7d2af56b0588001fef847dd0fe3f87bdc857154e531bc4c703e0b1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da5e551dcbe73958445f3f74da9647ee7845182abf97ef06d6802c9aad91609(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61f748de49af8152090c5d499e40e1a1f497b7982429e8531870fb177c2b49d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30855ef542d9334259418553b858b8a66308c23bfe2b12983735b5a5e43e5e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b120282c0ad3314250843588865d7e2b057213e12959866e9474cb5ec3c0fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dc7bd23b5d51ee88c0250f72d4238a3f748c3805a267157642d9c27bc8e6fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b01ab7c9ca598c5bc6ef8a7ac9498cd7282af4c1400527f15338962b8a6c0e(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6531bef9e053aef21f3770c48766a2124a89b8a8862b97652c0e944117d82753(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcae72b2c4f19f99fe6a3e4da7b8e711dbb0da49fd28bd0b4dbbb03d589a2069(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18853425a13068374c1730d9dd18300b51d80de1c764d6aa0ef508edc532d4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c286bded7bf85a220e4bc0cc581b50272f95621d5778a4d3c55a03b6955f1bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11bbc8d2bb42404af44723e28d7aa3fb66ab7d15135d72f4d7f30c89ba6f3fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af4778699274154f20dcf86e27081c9fe24bbb1f30b8975b19d8332e108ea1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fd11b1158be93a32060f60d6ced414895f47debc3692cb623968694100dcfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f38c40b18451f31b2b30896f8189d63d36a0fb4fff4f4d8a1cbefdc7eb735b(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582f75356a392236bf48e868a1f2ecc4309dfee12045b22acad93592f479b578(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002ec570d04afa65cf87e29b46b4c1f4cc39f4813c0ab09d1e08229e94373ad0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9061d5fa9428c8eb305f9ed45932315a761158cd0a3c5d674d74280298f8223(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf85af8e33a2ac27246761e7e3b22105d0b955e373f21d7082a4d885732163a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14b10b515ff7ecf4fe58ddb0e57c6e8fe99d392b2ad977c624e8baea129b809(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8515b1348af0d957161d7effc10456f7657b2127685264bc66b57e9a6e5dfc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b83e54e16a92eb449b02e44e15e0714b05ffe7356bad2f92c43bf26c22ca9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7eba791a4c77d3f1f1f674098b0a8334b8111dfda59d6b0a2921a2d063645d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87f6019fc253dd11f3d3e63fd88a116792f6cb7db9697ea9641295982210575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2adaa319aa74d6e6058648f2d2695ff647c4872c05e55e8a95cf66db9b35bda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66dc9877f26c928d678641d38c28fdb797b8b8edca090af813423b5a02ae6fb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92dd14df5b0e1013e001f0c8b257896a67af83412543901347d29ac5be018fb0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a30c2f56563f22fe5d73f74d6d4b00c775e1e497f3a38eedae94721848b1153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35b3fd481d9569619070395cfb4c0fea2ea254cf2a0c9577176ffcad648fd2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4614193489258897b600c6b7cd4f4773efb0dceda8d5ebd1cab7991ea5cd2b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4e0be24dafd50b8f14e0566847d2d934464651f6d77d1b19f7ff66586589a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b59597c03c727be9922349cd84ca5393e8ff8c44cfff8a08056c667a8e98ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea8202edac34f72424ce91799335939c96775303c893ff7791a565ecee1945f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7f859106c8ba2ba2f045ade20cc37b23420fd9c70b7b16ef6d501e21cb66f2(
    value: typing.Optional[AccessContextManagerServicePerimeterStatusIngressPoliciesIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2501c7e3dc5ca190cf4b8d8abce2c973071c981e0fd2ad1d6989294202e483c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87aa5bbe828a4c4b0a03ef56ff614a38417741c76faf0a120ec67d21a048c67f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e87bd31d4d37a39740bb9515a8be18c60d2fd96ffbb0315ec6a52cb91e92fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2fa02ea57aa4111413869c1928b4a8a8c44eda01f2710974454b2eab18378c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2e9e87587265efb0842af3a157e55a71a700316eccbcee1a006587efe36a15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410a576672d151a8c7aab37c38f4c2e587b9318b58667fc6bdfb1e9ac537468d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterStatusIngressPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef7f7f5b5ca027e96acbd3795d89475bdfa1fdcece6403855249857415bbaae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8e48a40faa555d64175203c2099496c24f43f4a6615fa74eb166a611de4a86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fda671bdc942aace02e4989b2c3fdc0c9472453eeb7a2cf27b8c9fe5510a5a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterStatusIngressPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134037e4bb108e575fee1834a14243a78fe237a03bd40582afaf685f7b6412e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fbf1f79e498af59a234f5904ad2b98a0a5978e2489ff89c7b9882d94cbec07(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusEgressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1756886d26b0124930a0a2a9f5771ec31d3aeafca86007008cf7ed2d16c500bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterStatusIngressPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010339e8069f2ed1aca77ebdfaf9e07344e904a8a06a7edfa6af3dd3c98562d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e758551c6f4154e748deb2404aa4d49fc4de3b6bf495839259c96d1305b77d0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f9f25fee5f5c19211644c56c0bf3094d3fdd15d76e02353492608a98eb3ec3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eee72a789c07ee750025f77fd4d8a9e221dd01534a4fa13dd8a7bb879bcb102(
    value: typing.Optional[AccessContextManagerServicePerimeterStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7dfe3d3ce3cb07e026a5735721e05874a62c125b6a67bfb2159734b76de384(
    *,
    allowed_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60811128264e4d003ecfb06487a700845d26c50beb1166812f571dbc2343415(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04cfa4984509485c79a980ff7e55ca6e2928eec4034ce802f3d3253fc9d54431(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b76d50a03455e1f4d892c756e2112dccb33002e4d7a9dc4dd1ba484a5c7d64b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d33540d39f117db63b09a40d05899a8376d4a9ea4ecbe8e0754c79cfd427a3(
    value: typing.Optional[AccessContextManagerServicePerimeterStatusVpcAccessibleServices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31dfdcb9a79df16e72d15c6b4b7b1f7c2eb6783d3a5d2a225917f08b4c97e42(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fadcfab5628f9bdae10b4b7e11b5a3aec83ec1bb86a325382b874b41d6d9cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb5496d28498e537fde845d54119188718eb7bedaa9a1cba14e688a4ffcab3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d435048fad717a368b45489f1d40150c8305c8addda8945365bb6cb5a398f14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd723a2cc90848cb02f54079fac907c9dea3f899e2f53e13e292ed8c2631e913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe766da0e5cb887bd6f06724365c4dbd96a782068c701a3deeccc99263858fef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
