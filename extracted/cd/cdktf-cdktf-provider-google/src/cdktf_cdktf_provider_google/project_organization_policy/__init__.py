r'''
# `google_project_organization_policy`

Refer to the Terraform Registry for docs: [`google_project_organization_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy).
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


class ProjectOrganizationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy google_project_organization_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        constraint: builtins.str,
        project: builtins.str,
        boolean_policy: typing.Optional[typing.Union["ProjectOrganizationPolicyBooleanPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        list_policy: typing.Optional[typing.Union["ProjectOrganizationPolicyListPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_policy: typing.Optional[typing.Union["ProjectOrganizationPolicyRestorePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ProjectOrganizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy google_project_organization_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param constraint: The name of the Constraint the Policy is configuring, for example, serviceuser.services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#constraint ProjectOrganizationPolicy#constraint}
        :param project: The project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#project ProjectOrganizationPolicy#project}
        :param boolean_policy: boolean_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#boolean_policy ProjectOrganizationPolicy#boolean_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#id ProjectOrganizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param list_policy: list_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#list_policy ProjectOrganizationPolicy#list_policy}
        :param restore_policy: restore_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#restore_policy ProjectOrganizationPolicy#restore_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#timeouts ProjectOrganizationPolicy#timeouts}
        :param version: Version of the Policy. Default version is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#version ProjectOrganizationPolicy#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead685c93b5f9fd800098f3d13722956bef913a44836f8c94d0cfe57ff00e613)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectOrganizationPolicyConfig(
            constraint=constraint,
            project=project,
            boolean_policy=boolean_policy,
            id=id,
            list_policy=list_policy,
            restore_policy=restore_policy,
            timeouts=timeouts,
            version=version,
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
        '''Generates CDKTF code for importing a ProjectOrganizationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProjectOrganizationPolicy to import.
        :param import_from_id: The id of the existing ProjectOrganizationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProjectOrganizationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24a4eabc939bdf6ed28735d93f451a3492fc60dfceecffe7b8658eb78332f6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBooleanPolicy")
    def put_boolean_policy(
        self,
        *,
        enforced: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#enforced ProjectOrganizationPolicy#enforced}
        '''
        value = ProjectOrganizationPolicyBooleanPolicy(enforced=enforced)

        return typing.cast(None, jsii.invoke(self, "putBooleanPolicy", [value]))

    @jsii.member(jsii_name="putListPolicy")
    def put_list_policy(
        self,
        *,
        allow: typing.Optional[typing.Union["ProjectOrganizationPolicyListPolicyAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        deny: typing.Optional[typing.Union["ProjectOrganizationPolicyListPolicyDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suggested_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#allow ProjectOrganizationPolicy#allow}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#deny ProjectOrganizationPolicy#deny}
        :param inherit_from_parent: If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#inherit_from_parent ProjectOrganizationPolicy#inherit_from_parent}
        :param suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#suggested_value ProjectOrganizationPolicy#suggested_value}
        '''
        value = ProjectOrganizationPolicyListPolicy(
            allow=allow,
            deny=deny,
            inherit_from_parent=inherit_from_parent,
            suggested_value=suggested_value,
        )

        return typing.cast(None, jsii.invoke(self, "putListPolicy", [value]))

    @jsii.member(jsii_name="putRestorePolicy")
    def put_restore_policy(
        self,
        *,
        default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param default: May only be set to true. If set, then the default Policy is restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#default ProjectOrganizationPolicy#default}
        '''
        value = ProjectOrganizationPolicyRestorePolicy(default=default)

        return typing.cast(None, jsii.invoke(self, "putRestorePolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#create ProjectOrganizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#delete ProjectOrganizationPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#read ProjectOrganizationPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#update ProjectOrganizationPolicy#update}.
        '''
        value = ProjectOrganizationPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBooleanPolicy")
    def reset_boolean_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetListPolicy")
    def reset_list_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListPolicy", []))

    @jsii.member(jsii_name="resetRestorePolicy")
    def reset_restore_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="booleanPolicy")
    def boolean_policy(self) -> "ProjectOrganizationPolicyBooleanPolicyOutputReference":
        return typing.cast("ProjectOrganizationPolicyBooleanPolicyOutputReference", jsii.get(self, "booleanPolicy"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="listPolicy")
    def list_policy(self) -> "ProjectOrganizationPolicyListPolicyOutputReference":
        return typing.cast("ProjectOrganizationPolicyListPolicyOutputReference", jsii.get(self, "listPolicy"))

    @builtins.property
    @jsii.member(jsii_name="restorePolicy")
    def restore_policy(self) -> "ProjectOrganizationPolicyRestorePolicyOutputReference":
        return typing.cast("ProjectOrganizationPolicyRestorePolicyOutputReference", jsii.get(self, "restorePolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ProjectOrganizationPolicyTimeoutsOutputReference":
        return typing.cast("ProjectOrganizationPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="booleanPolicyInput")
    def boolean_policy_input(
        self,
    ) -> typing.Optional["ProjectOrganizationPolicyBooleanPolicy"]:
        return typing.cast(typing.Optional["ProjectOrganizationPolicyBooleanPolicy"], jsii.get(self, "booleanPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintInput")
    def constraint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constraintInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="listPolicyInput")
    def list_policy_input(
        self,
    ) -> typing.Optional["ProjectOrganizationPolicyListPolicy"]:
        return typing.cast(typing.Optional["ProjectOrganizationPolicyListPolicy"], jsii.get(self, "listPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePolicyInput")
    def restore_policy_input(
        self,
    ) -> typing.Optional["ProjectOrganizationPolicyRestorePolicy"]:
        return typing.cast(typing.Optional["ProjectOrganizationPolicyRestorePolicy"], jsii.get(self, "restorePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ProjectOrganizationPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ProjectOrganizationPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="constraint")
    def constraint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "constraint"))

    @constraint.setter
    def constraint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e56fd6ecef72d29ff94086eb985fcb06d7496b51c288f6e6e613d1e829436d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb264e9d786766dc70625455db8bb2196d166612771cbc08613e9a4fc86003f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f9ec9b3bfaa923c87346a24b9993918c18e18068c0e200d514196b5eb952a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6543ffb48b93646baea4a79983c23382b2e8a0cc7f9adabb03fe560bf08666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyBooleanPolicy",
    jsii_struct_bases=[],
    name_mapping={"enforced": "enforced"},
)
class ProjectOrganizationPolicyBooleanPolicy:
    def __init__(
        self,
        *,
        enforced: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#enforced ProjectOrganizationPolicy#enforced}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8e14179c3b709235b61cd20d104eb4ffdb0f528a8d68f941dcbfcc2b6cbc5c)
            check_type(argname="argument enforced", value=enforced, expected_type=type_hints["enforced"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforced": enforced,
        }

    @builtins.property
    def enforced(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, then the Policy is enforced. If false, then any configuration is acceptable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#enforced ProjectOrganizationPolicy#enforced}
        '''
        result = self._values.get("enforced")
        assert result is not None, "Required property 'enforced' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyBooleanPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectOrganizationPolicyBooleanPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyBooleanPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c205335fa4b5350a5d2b0f64bf057c54c5cfda098c4f6058f44012a0f37da8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enforcedInput")
    def enforced_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforcedInput"))

    @builtins.property
    @jsii.member(jsii_name="enforced")
    def enforced(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforced"))

    @enforced.setter
    def enforced(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44d9cd343f98448f322a17418e6b3959040d32017706225f894a8202c2cc1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforced", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProjectOrganizationPolicyBooleanPolicy]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyBooleanPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectOrganizationPolicyBooleanPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff67821a904fc744f2b2b2aeab7e012edba50d33088a3209df601953769f3d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "constraint": "constraint",
        "project": "project",
        "boolean_policy": "booleanPolicy",
        "id": "id",
        "list_policy": "listPolicy",
        "restore_policy": "restorePolicy",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class ProjectOrganizationPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        constraint: builtins.str,
        project: builtins.str,
        boolean_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyBooleanPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        list_policy: typing.Optional[typing.Union["ProjectOrganizationPolicyListPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_policy: typing.Optional[typing.Union["ProjectOrganizationPolicyRestorePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ProjectOrganizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param constraint: The name of the Constraint the Policy is configuring, for example, serviceuser.services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#constraint ProjectOrganizationPolicy#constraint}
        :param project: The project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#project ProjectOrganizationPolicy#project}
        :param boolean_policy: boolean_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#boolean_policy ProjectOrganizationPolicy#boolean_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#id ProjectOrganizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param list_policy: list_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#list_policy ProjectOrganizationPolicy#list_policy}
        :param restore_policy: restore_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#restore_policy ProjectOrganizationPolicy#restore_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#timeouts ProjectOrganizationPolicy#timeouts}
        :param version: Version of the Policy. Default version is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#version ProjectOrganizationPolicy#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(boolean_policy, dict):
            boolean_policy = ProjectOrganizationPolicyBooleanPolicy(**boolean_policy)
        if isinstance(list_policy, dict):
            list_policy = ProjectOrganizationPolicyListPolicy(**list_policy)
        if isinstance(restore_policy, dict):
            restore_policy = ProjectOrganizationPolicyRestorePolicy(**restore_policy)
        if isinstance(timeouts, dict):
            timeouts = ProjectOrganizationPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee98a612bea32de7ddf02da21861127e668d453ee7343be0cb110e225846b41)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument boolean_policy", value=boolean_policy, expected_type=type_hints["boolean_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument list_policy", value=list_policy, expected_type=type_hints["list_policy"])
            check_type(argname="argument restore_policy", value=restore_policy, expected_type=type_hints["restore_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "constraint": constraint,
            "project": project,
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
        if boolean_policy is not None:
            self._values["boolean_policy"] = boolean_policy
        if id is not None:
            self._values["id"] = id
        if list_policy is not None:
            self._values["list_policy"] = list_policy
        if restore_policy is not None:
            self._values["restore_policy"] = restore_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version

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
    def constraint(self) -> builtins.str:
        '''The name of the Constraint the Policy is configuring, for example, serviceuser.services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#constraint ProjectOrganizationPolicy#constraint}
        '''
        result = self._values.get("constraint")
        assert result is not None, "Required property 'constraint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#project ProjectOrganizationPolicy#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_policy(self) -> typing.Optional[ProjectOrganizationPolicyBooleanPolicy]:
        '''boolean_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#boolean_policy ProjectOrganizationPolicy#boolean_policy}
        '''
        result = self._values.get("boolean_policy")
        return typing.cast(typing.Optional[ProjectOrganizationPolicyBooleanPolicy], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#id ProjectOrganizationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def list_policy(self) -> typing.Optional["ProjectOrganizationPolicyListPolicy"]:
        '''list_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#list_policy ProjectOrganizationPolicy#list_policy}
        '''
        result = self._values.get("list_policy")
        return typing.cast(typing.Optional["ProjectOrganizationPolicyListPolicy"], result)

    @builtins.property
    def restore_policy(
        self,
    ) -> typing.Optional["ProjectOrganizationPolicyRestorePolicy"]:
        '''restore_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#restore_policy ProjectOrganizationPolicy#restore_policy}
        '''
        result = self._values.get("restore_policy")
        return typing.cast(typing.Optional["ProjectOrganizationPolicyRestorePolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ProjectOrganizationPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#timeouts ProjectOrganizationPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ProjectOrganizationPolicyTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''Version of the Policy. Default version is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#version ProjectOrganizationPolicy#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyListPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allow": "allow",
        "deny": "deny",
        "inherit_from_parent": "inheritFromParent",
        "suggested_value": "suggestedValue",
    },
)
class ProjectOrganizationPolicyListPolicy:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union["ProjectOrganizationPolicyListPolicyAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        deny: typing.Optional[typing.Union["ProjectOrganizationPolicyListPolicyDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suggested_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#allow ProjectOrganizationPolicy#allow}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#deny ProjectOrganizationPolicy#deny}
        :param inherit_from_parent: If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#inherit_from_parent ProjectOrganizationPolicy#inherit_from_parent}
        :param suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#suggested_value ProjectOrganizationPolicy#suggested_value}
        '''
        if isinstance(allow, dict):
            allow = ProjectOrganizationPolicyListPolicyAllow(**allow)
        if isinstance(deny, dict):
            deny = ProjectOrganizationPolicyListPolicyDeny(**deny)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e8169c070429bb55db0e008f78bd6e03712a33a65a46d21ed2131b1b0014de)
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument deny", value=deny, expected_type=type_hints["deny"])
            check_type(argname="argument inherit_from_parent", value=inherit_from_parent, expected_type=type_hints["inherit_from_parent"])
            check_type(argname="argument suggested_value", value=suggested_value, expected_type=type_hints["suggested_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow is not None:
            self._values["allow"] = allow
        if deny is not None:
            self._values["deny"] = deny
        if inherit_from_parent is not None:
            self._values["inherit_from_parent"] = inherit_from_parent
        if suggested_value is not None:
            self._values["suggested_value"] = suggested_value

    @builtins.property
    def allow(self) -> typing.Optional["ProjectOrganizationPolicyListPolicyAllow"]:
        '''allow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#allow ProjectOrganizationPolicy#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional["ProjectOrganizationPolicyListPolicyAllow"], result)

    @builtins.property
    def deny(self) -> typing.Optional["ProjectOrganizationPolicyListPolicyDeny"]:
        '''deny block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#deny ProjectOrganizationPolicy#deny}
        '''
        result = self._values.get("deny")
        return typing.cast(typing.Optional["ProjectOrganizationPolicyListPolicyDeny"], result)

    @builtins.property
    def inherit_from_parent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#inherit_from_parent ProjectOrganizationPolicy#inherit_from_parent}
        '''
        result = self._values.get("inherit_from_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suggested_value(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Console will try to default to a configuration that matches the value specified in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#suggested_value ProjectOrganizationPolicy#suggested_value}
        '''
        result = self._values.get("suggested_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyListPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyListPolicyAllow",
    jsii_struct_bases=[],
    name_mapping={"all": "all", "values": "values"},
)
class ProjectOrganizationPolicyListPolicyAllow:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#all ProjectOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#values ProjectOrganizationPolicy#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca79c8fd6c476de555a43b27d97fe60a230b9b7d2cae184259cc2cf1ab6975c7)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The policy allows or denies all values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#all ProjectOrganizationPolicy#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The policy can define specific values that are allowed or denied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#values ProjectOrganizationPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyListPolicyAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectOrganizationPolicyListPolicyAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyListPolicyAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b5215d0f57e6a52bcc438f9a262951162dd782a94eba3ab0c5943e3b54aae7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAll")
    def reset_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAll", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "all"))

    @all.setter
    def all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7642684342bd7f488f4d71ff85ed03641d551aa79a785f689a785370b3c635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcb0e2bb42e16aff793ba0b4432c2371ff7148279309576b0c0306adeb82b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ProjectOrganizationPolicyListPolicyAllow]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyListPolicyAllow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectOrganizationPolicyListPolicyAllow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dade005ad6ea058024103166969c681828f59dc0d0214ddc8f64a8073d99dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyListPolicyDeny",
    jsii_struct_bases=[],
    name_mapping={"all": "all", "values": "values"},
)
class ProjectOrganizationPolicyListPolicyDeny:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#all ProjectOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#values ProjectOrganizationPolicy#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdf71e9e2bfc06d9eefa8b77efef7961763ac226274627e65f3b46871606ff9)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The policy allows or denies all values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#all ProjectOrganizationPolicy#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The policy can define specific values that are allowed or denied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#values ProjectOrganizationPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyListPolicyDeny(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectOrganizationPolicyListPolicyDenyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyListPolicyDenyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__492a33c791f5605c7885a9c7752cb5ce80d48f24a0fd3bce90025f594cdfd2af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAll")
    def reset_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAll", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "all"))

    @all.setter
    def all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078de0e22ea207b4b269c0ce2d1a694e2b631e6ab0eb14d40858a68224a16a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b126cbc37a38fe583f9799332f55444946bdc57058a9d127e0097199d1edee32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ProjectOrganizationPolicyListPolicyDeny]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyListPolicyDeny], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectOrganizationPolicyListPolicyDeny],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c9c9535d38a42eec7d017a00b93be33051f144f918439ea6e6be6c7a7e3ccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectOrganizationPolicyListPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyListPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d55d0d8fa63c6a4bbeaf59907466eca378c7c0b5dd7f72d3a6857b2c862d1ab3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllow")
    def put_allow(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#all ProjectOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#values ProjectOrganizationPolicy#values}
        '''
        value = ProjectOrganizationPolicyListPolicyAllow(all=all, values=values)

        return typing.cast(None, jsii.invoke(self, "putAllow", [value]))

    @jsii.member(jsii_name="putDeny")
    def put_deny(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#all ProjectOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#values ProjectOrganizationPolicy#values}
        '''
        value = ProjectOrganizationPolicyListPolicyDeny(all=all, values=values)

        return typing.cast(None, jsii.invoke(self, "putDeny", [value]))

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetDeny")
    def reset_deny(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeny", []))

    @jsii.member(jsii_name="resetInheritFromParent")
    def reset_inherit_from_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInheritFromParent", []))

    @jsii.member(jsii_name="resetSuggestedValue")
    def reset_suggested_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestedValue", []))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> ProjectOrganizationPolicyListPolicyAllowOutputReference:
        return typing.cast(ProjectOrganizationPolicyListPolicyAllowOutputReference, jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="deny")
    def deny(self) -> ProjectOrganizationPolicyListPolicyDenyOutputReference:
        return typing.cast(ProjectOrganizationPolicyListPolicyDenyOutputReference, jsii.get(self, "deny"))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(self) -> typing.Optional[ProjectOrganizationPolicyListPolicyAllow]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyListPolicyAllow], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="denyInput")
    def deny_input(self) -> typing.Optional[ProjectOrganizationPolicyListPolicyDeny]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyListPolicyDeny], jsii.get(self, "denyInput"))

    @builtins.property
    @jsii.member(jsii_name="inheritFromParentInput")
    def inherit_from_parent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inheritFromParentInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestedValueInput")
    def suggested_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suggestedValueInput"))

    @builtins.property
    @jsii.member(jsii_name="inheritFromParent")
    def inherit_from_parent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inheritFromParent"))

    @inherit_from_parent.setter
    def inherit_from_parent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4879fec1b983be06e0f80af38edd86127a0938004e89ab0471d00a1d93f60a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inheritFromParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suggestedValue")
    def suggested_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suggestedValue"))

    @suggested_value.setter
    def suggested_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98593fa45f33d9047594eb3c84070d422ce990d5970b2130ce26b496a0a81362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suggestedValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProjectOrganizationPolicyListPolicy]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyListPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectOrganizationPolicyListPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e7e957bdfce5ebcfcd3b895e7df64cc9f48224080528f0e09af72494e7a18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyRestorePolicy",
    jsii_struct_bases=[],
    name_mapping={"default": "default"},
)
class ProjectOrganizationPolicyRestorePolicy:
    def __init__(
        self,
        *,
        default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param default: May only be set to true. If set, then the default Policy is restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#default ProjectOrganizationPolicy#default}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3e4024243ef98df577b9d8c70388391a09b9eb8ec05724ef84da8664def5a5)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default": default,
        }

    @builtins.property
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''May only be set to true. If set, then the default Policy is restored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#default ProjectOrganizationPolicy#default}
        '''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyRestorePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectOrganizationPolicyRestorePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyRestorePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66b09d11313eb19cab9d1f3807ff82d0be08e64e77f9710a2532c04b62ae45db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81cf7e985397f885d6373ea2e2ad55d02ef67ce667c1a82558fe4868c5c87d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProjectOrganizationPolicyRestorePolicy]:
        return typing.cast(typing.Optional[ProjectOrganizationPolicyRestorePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProjectOrganizationPolicyRestorePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3756d49134c6d6631cdf823e364ec84e5ffff148be7c15bc1c790ba6028e4cbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ProjectOrganizationPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#create ProjectOrganizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#delete ProjectOrganizationPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#read ProjectOrganizationPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#update ProjectOrganizationPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff78cd702054b9d2d8088193ff645aabaa6e145daa2e7d07cbea7f882e1aac09)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#create ProjectOrganizationPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#delete ProjectOrganizationPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#read ProjectOrganizationPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_organization_policy#update ProjectOrganizationPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOrganizationPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectOrganizationPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectOrganizationPolicy.ProjectOrganizationPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd7d72ea2caeb9080cd6259c5608b59b4507aecffa0ec0cb7e5867187a32c71a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6902623fb5a2e58e42b8b623bc891d6c5b148b25b656bb3fe376695972a18717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6fcff43f183ab8b2a1068f5c9d8de6cd18b293ece6500de3559f2697bdb869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6058f7bdccdda7e2126f21ee73ec44f34a18214c5d12766c64b0704f013ec604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3763752cb5eeb87265538aa546e8b207acba21808b96bbcdf3202d9be6354b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectOrganizationPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectOrganizationPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectOrganizationPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5fb4af164fa2614cc181ccb07f20e970dbeefeb9bb347ee70642ab647248ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ProjectOrganizationPolicy",
    "ProjectOrganizationPolicyBooleanPolicy",
    "ProjectOrganizationPolicyBooleanPolicyOutputReference",
    "ProjectOrganizationPolicyConfig",
    "ProjectOrganizationPolicyListPolicy",
    "ProjectOrganizationPolicyListPolicyAllow",
    "ProjectOrganizationPolicyListPolicyAllowOutputReference",
    "ProjectOrganizationPolicyListPolicyDeny",
    "ProjectOrganizationPolicyListPolicyDenyOutputReference",
    "ProjectOrganizationPolicyListPolicyOutputReference",
    "ProjectOrganizationPolicyRestorePolicy",
    "ProjectOrganizationPolicyRestorePolicyOutputReference",
    "ProjectOrganizationPolicyTimeouts",
    "ProjectOrganizationPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ead685c93b5f9fd800098f3d13722956bef913a44836f8c94d0cfe57ff00e613(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    constraint: builtins.str,
    project: builtins.str,
    boolean_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyBooleanPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    list_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyListPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyRestorePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ProjectOrganizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__a24a4eabc939bdf6ed28735d93f451a3492fc60dfceecffe7b8658eb78332f6f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e56fd6ecef72d29ff94086eb985fcb06d7496b51c288f6e6e613d1e829436d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb264e9d786766dc70625455db8bb2196d166612771cbc08613e9a4fc86003f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f9ec9b3bfaa923c87346a24b9993918c18e18068c0e200d514196b5eb952a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6543ffb48b93646baea4a79983c23382b2e8a0cc7f9adabb03fe560bf08666(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8e14179c3b709235b61cd20d104eb4ffdb0f528a8d68f941dcbfcc2b6cbc5c(
    *,
    enforced: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c205335fa4b5350a5d2b0f64bf057c54c5cfda098c4f6058f44012a0f37da8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44d9cd343f98448f322a17418e6b3959040d32017706225f894a8202c2cc1c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff67821a904fc744f2b2b2aeab7e012edba50d33088a3209df601953769f3d75(
    value: typing.Optional[ProjectOrganizationPolicyBooleanPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee98a612bea32de7ddf02da21861127e668d453ee7343be0cb110e225846b41(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    constraint: builtins.str,
    project: builtins.str,
    boolean_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyBooleanPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    list_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyListPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_policy: typing.Optional[typing.Union[ProjectOrganizationPolicyRestorePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ProjectOrganizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e8169c070429bb55db0e008f78bd6e03712a33a65a46d21ed2131b1b0014de(
    *,
    allow: typing.Optional[typing.Union[ProjectOrganizationPolicyListPolicyAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    deny: typing.Optional[typing.Union[ProjectOrganizationPolicyListPolicyDeny, typing.Dict[builtins.str, typing.Any]]] = None,
    inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suggested_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca79c8fd6c476de555a43b27d97fe60a230b9b7d2cae184259cc2cf1ab6975c7(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b5215d0f57e6a52bcc438f9a262951162dd782a94eba3ab0c5943e3b54aae7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7642684342bd7f488f4d71ff85ed03641d551aa79a785f689a785370b3c635(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcb0e2bb42e16aff793ba0b4432c2371ff7148279309576b0c0306adeb82b35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dade005ad6ea058024103166969c681828f59dc0d0214ddc8f64a8073d99dcd(
    value: typing.Optional[ProjectOrganizationPolicyListPolicyAllow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdf71e9e2bfc06d9eefa8b77efef7961763ac226274627e65f3b46871606ff9(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492a33c791f5605c7885a9c7752cb5ce80d48f24a0fd3bce90025f594cdfd2af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078de0e22ea207b4b269c0ce2d1a694e2b631e6ab0eb14d40858a68224a16a3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b126cbc37a38fe583f9799332f55444946bdc57058a9d127e0097199d1edee32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c9c9535d38a42eec7d017a00b93be33051f144f918439ea6e6be6c7a7e3ccb(
    value: typing.Optional[ProjectOrganizationPolicyListPolicyDeny],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55d0d8fa63c6a4bbeaf59907466eca378c7c0b5dd7f72d3a6857b2c862d1ab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4879fec1b983be06e0f80af38edd86127a0938004e89ab0471d00a1d93f60a11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98593fa45f33d9047594eb3c84070d422ce990d5970b2130ce26b496a0a81362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e7e957bdfce5ebcfcd3b895e7df64cc9f48224080528f0e09af72494e7a18d(
    value: typing.Optional[ProjectOrganizationPolicyListPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3e4024243ef98df577b9d8c70388391a09b9eb8ec05724ef84da8664def5a5(
    *,
    default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b09d11313eb19cab9d1f3807ff82d0be08e64e77f9710a2532c04b62ae45db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81cf7e985397f885d6373ea2e2ad55d02ef67ce667c1a82558fe4868c5c87d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3756d49134c6d6631cdf823e364ec84e5ffff148be7c15bc1c790ba6028e4cbf(
    value: typing.Optional[ProjectOrganizationPolicyRestorePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff78cd702054b9d2d8088193ff645aabaa6e145daa2e7d07cbea7f882e1aac09(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7d72ea2caeb9080cd6259c5608b59b4507aecffa0ec0cb7e5867187a32c71a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6902623fb5a2e58e42b8b623bc891d6c5b148b25b656bb3fe376695972a18717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6fcff43f183ab8b2a1068f5c9d8de6cd18b293ece6500de3559f2697bdb869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6058f7bdccdda7e2126f21ee73ec44f34a18214c5d12766c64b0704f013ec604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3763752cb5eeb87265538aa546e8b207acba21808b96bbcdf3202d9be6354b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5fb4af164fa2614cc181ccb07f20e970dbeefeb9bb347ee70642ab647248ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectOrganizationPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
