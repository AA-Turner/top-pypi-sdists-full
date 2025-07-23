r'''
# `google_folder_organization_policy`

Refer to the Terraform Registry for docs: [`google_folder_organization_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy).
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


class FolderOrganizationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy google_folder_organization_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        constraint: builtins.str,
        folder: builtins.str,
        boolean_policy: typing.Optional[typing.Union["FolderOrganizationPolicyBooleanPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        list_policy: typing.Optional[typing.Union["FolderOrganizationPolicyListPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_policy: typing.Optional[typing.Union["FolderOrganizationPolicyRestorePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FolderOrganizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy google_folder_organization_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param constraint: The name of the Constraint the Policy is configuring, for example, serviceuser.services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#constraint FolderOrganizationPolicy#constraint}
        :param folder: The resource name of the folder to set the policy for. Its format is folders/{folder_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#folder FolderOrganizationPolicy#folder}
        :param boolean_policy: boolean_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#boolean_policy FolderOrganizationPolicy#boolean_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#id FolderOrganizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param list_policy: list_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#list_policy FolderOrganizationPolicy#list_policy}
        :param restore_policy: restore_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#restore_policy FolderOrganizationPolicy#restore_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#timeouts FolderOrganizationPolicy#timeouts}
        :param version: Version of the Policy. Default version is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#version FolderOrganizationPolicy#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699212e47b31e6fb999e66bd54be201fa74551dc3e7920704bd41cca7b36829d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FolderOrganizationPolicyConfig(
            constraint=constraint,
            folder=folder,
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
        '''Generates CDKTF code for importing a FolderOrganizationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FolderOrganizationPolicy to import.
        :param import_from_id: The id of the existing FolderOrganizationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FolderOrganizationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0069a091d18fe2d0455a2aa7c27ad06926feafcedfd7a1babc80548d71a2df3)
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
        :param enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#enforced FolderOrganizationPolicy#enforced}
        '''
        value = FolderOrganizationPolicyBooleanPolicy(enforced=enforced)

        return typing.cast(None, jsii.invoke(self, "putBooleanPolicy", [value]))

    @jsii.member(jsii_name="putListPolicy")
    def put_list_policy(
        self,
        *,
        allow: typing.Optional[typing.Union["FolderOrganizationPolicyListPolicyAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        deny: typing.Optional[typing.Union["FolderOrganizationPolicyListPolicyDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suggested_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#allow FolderOrganizationPolicy#allow}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#deny FolderOrganizationPolicy#deny}
        :param inherit_from_parent: If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#inherit_from_parent FolderOrganizationPolicy#inherit_from_parent}
        :param suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#suggested_value FolderOrganizationPolicy#suggested_value}
        '''
        value = FolderOrganizationPolicyListPolicy(
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
        :param default: May only be set to true. If set, then the default Policy is restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#default FolderOrganizationPolicy#default}
        '''
        value = FolderOrganizationPolicyRestorePolicy(default=default)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#create FolderOrganizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#delete FolderOrganizationPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#read FolderOrganizationPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#update FolderOrganizationPolicy#update}.
        '''
        value = FolderOrganizationPolicyTimeouts(
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
    def boolean_policy(self) -> "FolderOrganizationPolicyBooleanPolicyOutputReference":
        return typing.cast("FolderOrganizationPolicyBooleanPolicyOutputReference", jsii.get(self, "booleanPolicy"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="listPolicy")
    def list_policy(self) -> "FolderOrganizationPolicyListPolicyOutputReference":
        return typing.cast("FolderOrganizationPolicyListPolicyOutputReference", jsii.get(self, "listPolicy"))

    @builtins.property
    @jsii.member(jsii_name="restorePolicy")
    def restore_policy(self) -> "FolderOrganizationPolicyRestorePolicyOutputReference":
        return typing.cast("FolderOrganizationPolicyRestorePolicyOutputReference", jsii.get(self, "restorePolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FolderOrganizationPolicyTimeoutsOutputReference":
        return typing.cast("FolderOrganizationPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="booleanPolicyInput")
    def boolean_policy_input(
        self,
    ) -> typing.Optional["FolderOrganizationPolicyBooleanPolicy"]:
        return typing.cast(typing.Optional["FolderOrganizationPolicyBooleanPolicy"], jsii.get(self, "booleanPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintInput")
    def constraint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constraintInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="listPolicyInput")
    def list_policy_input(
        self,
    ) -> typing.Optional["FolderOrganizationPolicyListPolicy"]:
        return typing.cast(typing.Optional["FolderOrganizationPolicyListPolicy"], jsii.get(self, "listPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePolicyInput")
    def restore_policy_input(
        self,
    ) -> typing.Optional["FolderOrganizationPolicyRestorePolicy"]:
        return typing.cast(typing.Optional["FolderOrganizationPolicyRestorePolicy"], jsii.get(self, "restorePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FolderOrganizationPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FolderOrganizationPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__28916f9c1f59a413972d7ddd8ccf87f0d1ea298858e1b6775088acb5774bb72e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cded63dc591a1d53cc87b94b5249e2bf69a004b227e08fc6b75bd9bfa42b224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0af1c4f895317cb91db0b3e23f88bdd4cc593b902849d2fb6067c1c2f6ffb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62593e3590b73bc0005e78524cb20fa3c69d976dfa02eee066bb3c1c7663762f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyBooleanPolicy",
    jsii_struct_bases=[],
    name_mapping={"enforced": "enforced"},
)
class FolderOrganizationPolicyBooleanPolicy:
    def __init__(
        self,
        *,
        enforced: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#enforced FolderOrganizationPolicy#enforced}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c44500ccda048b03b7b9c9df7e4711e1b5ca70115fa513b015766717b6fd99a)
            check_type(argname="argument enforced", value=enforced, expected_type=type_hints["enforced"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforced": enforced,
        }

    @builtins.property
    def enforced(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, then the Policy is enforced. If false, then any configuration is acceptable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#enforced FolderOrganizationPolicy#enforced}
        '''
        result = self._values.get("enforced")
        assert result is not None, "Required property 'enforced' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyBooleanPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderOrganizationPolicyBooleanPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyBooleanPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e1f696d5728a271452248203315e3156af085ff69947f7b8bb9f5edb5db9178)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00d5c265fedec42ac3c3361492c15517c450aef9318f7215e53190afdbddf53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforced", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FolderOrganizationPolicyBooleanPolicy]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyBooleanPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FolderOrganizationPolicyBooleanPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80573c3d0fc4db33ed044092632aa1fb7eb513d73d4dee2a1f94277189da68d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyConfig",
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
        "folder": "folder",
        "boolean_policy": "booleanPolicy",
        "id": "id",
        "list_policy": "listPolicy",
        "restore_policy": "restorePolicy",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class FolderOrganizationPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        folder: builtins.str,
        boolean_policy: typing.Optional[typing.Union[FolderOrganizationPolicyBooleanPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        list_policy: typing.Optional[typing.Union["FolderOrganizationPolicyListPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_policy: typing.Optional[typing.Union["FolderOrganizationPolicyRestorePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FolderOrganizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param constraint: The name of the Constraint the Policy is configuring, for example, serviceuser.services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#constraint FolderOrganizationPolicy#constraint}
        :param folder: The resource name of the folder to set the policy for. Its format is folders/{folder_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#folder FolderOrganizationPolicy#folder}
        :param boolean_policy: boolean_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#boolean_policy FolderOrganizationPolicy#boolean_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#id FolderOrganizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param list_policy: list_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#list_policy FolderOrganizationPolicy#list_policy}
        :param restore_policy: restore_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#restore_policy FolderOrganizationPolicy#restore_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#timeouts FolderOrganizationPolicy#timeouts}
        :param version: Version of the Policy. Default version is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#version FolderOrganizationPolicy#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(boolean_policy, dict):
            boolean_policy = FolderOrganizationPolicyBooleanPolicy(**boolean_policy)
        if isinstance(list_policy, dict):
            list_policy = FolderOrganizationPolicyListPolicy(**list_policy)
        if isinstance(restore_policy, dict):
            restore_policy = FolderOrganizationPolicyRestorePolicy(**restore_policy)
        if isinstance(timeouts, dict):
            timeouts = FolderOrganizationPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a23e543fc3403e0256baa4e5e2e5783aea0655b558fa40fdb056593240f7949)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument boolean_policy", value=boolean_policy, expected_type=type_hints["boolean_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument list_policy", value=list_policy, expected_type=type_hints["list_policy"])
            check_type(argname="argument restore_policy", value=restore_policy, expected_type=type_hints["restore_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "constraint": constraint,
            "folder": folder,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#constraint FolderOrganizationPolicy#constraint}
        '''
        result = self._values.get("constraint")
        assert result is not None, "Required property 'constraint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def folder(self) -> builtins.str:
        '''The resource name of the folder to set the policy for. Its format is folders/{folder_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#folder FolderOrganizationPolicy#folder}
        '''
        result = self._values.get("folder")
        assert result is not None, "Required property 'folder' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_policy(self) -> typing.Optional[FolderOrganizationPolicyBooleanPolicy]:
        '''boolean_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#boolean_policy FolderOrganizationPolicy#boolean_policy}
        '''
        result = self._values.get("boolean_policy")
        return typing.cast(typing.Optional[FolderOrganizationPolicyBooleanPolicy], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#id FolderOrganizationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def list_policy(self) -> typing.Optional["FolderOrganizationPolicyListPolicy"]:
        '''list_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#list_policy FolderOrganizationPolicy#list_policy}
        '''
        result = self._values.get("list_policy")
        return typing.cast(typing.Optional["FolderOrganizationPolicyListPolicy"], result)

    @builtins.property
    def restore_policy(
        self,
    ) -> typing.Optional["FolderOrganizationPolicyRestorePolicy"]:
        '''restore_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#restore_policy FolderOrganizationPolicy#restore_policy}
        '''
        result = self._values.get("restore_policy")
        return typing.cast(typing.Optional["FolderOrganizationPolicyRestorePolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FolderOrganizationPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#timeouts FolderOrganizationPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FolderOrganizationPolicyTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''Version of the Policy. Default version is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#version FolderOrganizationPolicy#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyListPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allow": "allow",
        "deny": "deny",
        "inherit_from_parent": "inheritFromParent",
        "suggested_value": "suggestedValue",
    },
)
class FolderOrganizationPolicyListPolicy:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union["FolderOrganizationPolicyListPolicyAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        deny: typing.Optional[typing.Union["FolderOrganizationPolicyListPolicyDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suggested_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#allow FolderOrganizationPolicy#allow}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#deny FolderOrganizationPolicy#deny}
        :param inherit_from_parent: If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#inherit_from_parent FolderOrganizationPolicy#inherit_from_parent}
        :param suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#suggested_value FolderOrganizationPolicy#suggested_value}
        '''
        if isinstance(allow, dict):
            allow = FolderOrganizationPolicyListPolicyAllow(**allow)
        if isinstance(deny, dict):
            deny = FolderOrganizationPolicyListPolicyDeny(**deny)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae852602e07c9b301365bdcd9d8ab5b43ab994220515d68db3eb7a5a34886eef)
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
    def allow(self) -> typing.Optional["FolderOrganizationPolicyListPolicyAllow"]:
        '''allow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#allow FolderOrganizationPolicy#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional["FolderOrganizationPolicyListPolicyAllow"], result)

    @builtins.property
    def deny(self) -> typing.Optional["FolderOrganizationPolicyListPolicyDeny"]:
        '''deny block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#deny FolderOrganizationPolicy#deny}
        '''
        result = self._values.get("deny")
        return typing.cast(typing.Optional["FolderOrganizationPolicyListPolicyDeny"], result)

    @builtins.property
    def inherit_from_parent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the values from the effective Policy of the parent resource are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#inherit_from_parent FolderOrganizationPolicy#inherit_from_parent}
        '''
        result = self._values.get("inherit_from_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suggested_value(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Console will try to default to a configuration that matches the value specified in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#suggested_value FolderOrganizationPolicy#suggested_value}
        '''
        result = self._values.get("suggested_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyListPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyListPolicyAllow",
    jsii_struct_bases=[],
    name_mapping={"all": "all", "values": "values"},
)
class FolderOrganizationPolicyListPolicyAllow:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#all FolderOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#values FolderOrganizationPolicy#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a933854f63d97695aa9285e0b6b75e41d7c69cbec679bec39357040e1ce74ce)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#all FolderOrganizationPolicy#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The policy can define specific values that are allowed or denied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#values FolderOrganizationPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyListPolicyAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderOrganizationPolicyListPolicyAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyListPolicyAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eddbf768c8bb5098f0798a8c48d168402e1b617dae092b7913693cc7210d135b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b2023f106e6d7312cd71e0d0fccc0e61680eb618e5495f71f690a1240b1ad1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4e6da40523ef6942aef9e2b9cb2bae7f873eb020e45c6357ddd183871305b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FolderOrganizationPolicyListPolicyAllow]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyListPolicyAllow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FolderOrganizationPolicyListPolicyAllow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e615d28a2f1fe59e3f691a8df61da830671ffa2841a23462aebbe33e87b611fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyListPolicyDeny",
    jsii_struct_bases=[],
    name_mapping={"all": "all", "values": "values"},
)
class FolderOrganizationPolicyListPolicyDeny:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#all FolderOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#values FolderOrganizationPolicy#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbb6d198a6f09b97744fb3dbfa9e68fb13df1dc1185cbd9fdbb316972f62106)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#all FolderOrganizationPolicy#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The policy can define specific values that are allowed or denied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#values FolderOrganizationPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyListPolicyDeny(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderOrganizationPolicyListPolicyDenyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyListPolicyDenyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1e143dc0bf39d09633dea3b4af6709d4213643f84eb63a89e72826082d59952)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8f7a324a103254416e26c207cc69fda3f5dd6a1031b58b3a1a9fad251a0577d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4e480fe25e1354807b6ceb4565ec704f19abb289c57ba4bbb16ade27d40018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FolderOrganizationPolicyListPolicyDeny]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyListPolicyDeny], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FolderOrganizationPolicyListPolicyDeny],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdfd0417dde008549d06e0b4b8b50a3404f7bdf7fdf9016b8e892c122246ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FolderOrganizationPolicyListPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyListPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f577e9dea4482f69caea43155f52cb782d674df8c9d2840b8141faf2e23a29)
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
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#all FolderOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#values FolderOrganizationPolicy#values}
        '''
        value = FolderOrganizationPolicyListPolicyAllow(all=all, values=values)

        return typing.cast(None, jsii.invoke(self, "putAllow", [value]))

    @jsii.member(jsii_name="putDeny")
    def put_deny(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param all: The policy allows or denies all values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#all FolderOrganizationPolicy#all}
        :param values: The policy can define specific values that are allowed or denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#values FolderOrganizationPolicy#values}
        '''
        value = FolderOrganizationPolicyListPolicyDeny(all=all, values=values)

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
    def allow(self) -> FolderOrganizationPolicyListPolicyAllowOutputReference:
        return typing.cast(FolderOrganizationPolicyListPolicyAllowOutputReference, jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="deny")
    def deny(self) -> FolderOrganizationPolicyListPolicyDenyOutputReference:
        return typing.cast(FolderOrganizationPolicyListPolicyDenyOutputReference, jsii.get(self, "deny"))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(self) -> typing.Optional[FolderOrganizationPolicyListPolicyAllow]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyListPolicyAllow], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="denyInput")
    def deny_input(self) -> typing.Optional[FolderOrganizationPolicyListPolicyDeny]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyListPolicyDeny], jsii.get(self, "denyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__42c181862889c0bfc3221f2f42c55274ae3cdafaab87e8e1035c8558b146706d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inheritFromParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suggestedValue")
    def suggested_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suggestedValue"))

    @suggested_value.setter
    def suggested_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ba5fa77326c2d7579362a971875daade8b3d17bae409c13eefa75849ed6822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suggestedValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FolderOrganizationPolicyListPolicy]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyListPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FolderOrganizationPolicyListPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf619734fad0e22f243f4c14b32c4abf0aa03c3b149aee9183e9c264aaf923a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyRestorePolicy",
    jsii_struct_bases=[],
    name_mapping={"default": "default"},
)
class FolderOrganizationPolicyRestorePolicy:
    def __init__(
        self,
        *,
        default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param default: May only be set to true. If set, then the default Policy is restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#default FolderOrganizationPolicy#default}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ae106d22a2b106137415c0703533bd1dfc3584da9773ee4e34498114439350)
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default": default,
        }

    @builtins.property
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''May only be set to true. If set, then the default Policy is restored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#default FolderOrganizationPolicy#default}
        '''
        result = self._values.get("default")
        assert result is not None, "Required property 'default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyRestorePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderOrganizationPolicyRestorePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyRestorePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf29303ad88a6914826413700b45ba1eb446858af52497bd37e593f8fabed78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4d435239e4b1997dee6c4b9dac01ff08e16f3103f678f5c4debeb19199d4725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FolderOrganizationPolicyRestorePolicy]:
        return typing.cast(typing.Optional[FolderOrganizationPolicyRestorePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FolderOrganizationPolicyRestorePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cac3aeb4590870d9ced66d60ce2ec2c71e74e08ac774bc167b95e8b7e9d2ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class FolderOrganizationPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#create FolderOrganizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#delete FolderOrganizationPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#read FolderOrganizationPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#update FolderOrganizationPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac563215c875faeac3b2ef147e7e3b5935bf54b761dd3409a386b3f2a3277fa)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#create FolderOrganizationPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#delete FolderOrganizationPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#read FolderOrganizationPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_organization_policy#update FolderOrganizationPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderOrganizationPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderOrganizationPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderOrganizationPolicy.FolderOrganizationPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78b7aa405501f19cc29b90124c52d5cb3e32398390c41c61aa3ffcefb65d51f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2000ecfd77eac681221d9c5f5fe0e613c1c8f5c0c0564c6b025c0c98293ada9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541ba26b7b0f883aba35ceba7a460b5aae31f5eeb9811bae124ac616febe14da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93337196d0aee92d4c3a00886d894b8b6c9e17e8d9d1688289701f966018ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__870d9d11f13a53eb88bc25b913c03a91a8736196a913f1b15888962c61d34ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderOrganizationPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderOrganizationPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderOrganizationPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899ddeab12a9c2c07ce593ea23cb182929c5f3d5d7d15c081752530cb2b9318a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FolderOrganizationPolicy",
    "FolderOrganizationPolicyBooleanPolicy",
    "FolderOrganizationPolicyBooleanPolicyOutputReference",
    "FolderOrganizationPolicyConfig",
    "FolderOrganizationPolicyListPolicy",
    "FolderOrganizationPolicyListPolicyAllow",
    "FolderOrganizationPolicyListPolicyAllowOutputReference",
    "FolderOrganizationPolicyListPolicyDeny",
    "FolderOrganizationPolicyListPolicyDenyOutputReference",
    "FolderOrganizationPolicyListPolicyOutputReference",
    "FolderOrganizationPolicyRestorePolicy",
    "FolderOrganizationPolicyRestorePolicyOutputReference",
    "FolderOrganizationPolicyTimeouts",
    "FolderOrganizationPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__699212e47b31e6fb999e66bd54be201fa74551dc3e7920704bd41cca7b36829d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    constraint: builtins.str,
    folder: builtins.str,
    boolean_policy: typing.Optional[typing.Union[FolderOrganizationPolicyBooleanPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    list_policy: typing.Optional[typing.Union[FolderOrganizationPolicyListPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_policy: typing.Optional[typing.Union[FolderOrganizationPolicyRestorePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FolderOrganizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f0069a091d18fe2d0455a2aa7c27ad06926feafcedfd7a1babc80548d71a2df3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28916f9c1f59a413972d7ddd8ccf87f0d1ea298858e1b6775088acb5774bb72e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cded63dc591a1d53cc87b94b5249e2bf69a004b227e08fc6b75bd9bfa42b224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0af1c4f895317cb91db0b3e23f88bdd4cc593b902849d2fb6067c1c2f6ffb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62593e3590b73bc0005e78524cb20fa3c69d976dfa02eee066bb3c1c7663762f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c44500ccda048b03b7b9c9df7e4711e1b5ca70115fa513b015766717b6fd99a(
    *,
    enforced: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1f696d5728a271452248203315e3156af085ff69947f7b8bb9f5edb5db9178(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00d5c265fedec42ac3c3361492c15517c450aef9318f7215e53190afdbddf53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80573c3d0fc4db33ed044092632aa1fb7eb513d73d4dee2a1f94277189da68d5(
    value: typing.Optional[FolderOrganizationPolicyBooleanPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a23e543fc3403e0256baa4e5e2e5783aea0655b558fa40fdb056593240f7949(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    constraint: builtins.str,
    folder: builtins.str,
    boolean_policy: typing.Optional[typing.Union[FolderOrganizationPolicyBooleanPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    list_policy: typing.Optional[typing.Union[FolderOrganizationPolicyListPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_policy: typing.Optional[typing.Union[FolderOrganizationPolicyRestorePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FolderOrganizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae852602e07c9b301365bdcd9d8ab5b43ab994220515d68db3eb7a5a34886eef(
    *,
    allow: typing.Optional[typing.Union[FolderOrganizationPolicyListPolicyAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    deny: typing.Optional[typing.Union[FolderOrganizationPolicyListPolicyDeny, typing.Dict[builtins.str, typing.Any]]] = None,
    inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suggested_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a933854f63d97695aa9285e0b6b75e41d7c69cbec679bec39357040e1ce74ce(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddbf768c8bb5098f0798a8c48d168402e1b617dae092b7913693cc7210d135b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2023f106e6d7312cd71e0d0fccc0e61680eb618e5495f71f690a1240b1ad1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4e6da40523ef6942aef9e2b9cb2bae7f873eb020e45c6357ddd183871305b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e615d28a2f1fe59e3f691a8df61da830671ffa2841a23462aebbe33e87b611fa(
    value: typing.Optional[FolderOrganizationPolicyListPolicyAllow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbb6d198a6f09b97744fb3dbfa9e68fb13df1dc1185cbd9fdbb316972f62106(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e143dc0bf39d09633dea3b4af6709d4213643f84eb63a89e72826082d59952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f7a324a103254416e26c207cc69fda3f5dd6a1031b58b3a1a9fad251a0577d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4e480fe25e1354807b6ceb4565ec704f19abb289c57ba4bbb16ade27d40018(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdfd0417dde008549d06e0b4b8b50a3404f7bdf7fdf9016b8e892c122246ee9(
    value: typing.Optional[FolderOrganizationPolicyListPolicyDeny],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f577e9dea4482f69caea43155f52cb782d674df8c9d2840b8141faf2e23a29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c181862889c0bfc3221f2f42c55274ae3cdafaab87e8e1035c8558b146706d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ba5fa77326c2d7579362a971875daade8b3d17bae409c13eefa75849ed6822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf619734fad0e22f243f4c14b32c4abf0aa03c3b149aee9183e9c264aaf923a(
    value: typing.Optional[FolderOrganizationPolicyListPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ae106d22a2b106137415c0703533bd1dfc3584da9773ee4e34498114439350(
    *,
    default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf29303ad88a6914826413700b45ba1eb446858af52497bd37e593f8fabed78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d435239e4b1997dee6c4b9dac01ff08e16f3103f678f5c4debeb19199d4725(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cac3aeb4590870d9ced66d60ce2ec2c71e74e08ac774bc167b95e8b7e9d2ae1(
    value: typing.Optional[FolderOrganizationPolicyRestorePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac563215c875faeac3b2ef147e7e3b5935bf54b761dd3409a386b3f2a3277fa(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b7aa405501f19cc29b90124c52d5cb3e32398390c41c61aa3ffcefb65d51f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2000ecfd77eac681221d9c5f5fe0e613c1c8f5c0c0564c6b025c0c98293ada9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541ba26b7b0f883aba35ceba7a460b5aae31f5eeb9811bae124ac616febe14da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93337196d0aee92d4c3a00886d894b8b6c9e17e8d9d1688289701f966018ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870d9d11f13a53eb88bc25b913c03a91a8736196a913f1b15888962c61d34ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899ddeab12a9c2c07ce593ea23cb182929c5f3d5d7d15c081752530cb2b9318a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderOrganizationPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
