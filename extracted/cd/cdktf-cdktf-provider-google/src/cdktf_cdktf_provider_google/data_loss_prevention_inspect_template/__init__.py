r'''
# `google_data_loss_prevention_inspect_template`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_inspect_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template).
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


class DataLossPreventionInspectTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template google_data_loss_prevention_inspect_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_config: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionInspectTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template google_data_loss_prevention_inspect_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of the inspect template in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#parent DataLossPreventionInspectTemplate#parent}
        :param description: A description of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#description DataLossPreventionInspectTemplate#description}
        :param display_name: User set display name of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#display_name DataLossPreventionInspectTemplate#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#id DataLossPreventionInspectTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#inspect_config DataLossPreventionInspectTemplate#inspect_config}
        :param template_id: The template id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#template_id DataLossPreventionInspectTemplate#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#timeouts DataLossPreventionInspectTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751ed60c3e9ac8e49c9da913a65e1d35c09c6efd7fe224c27bea2150814830d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLossPreventionInspectTemplateConfig(
            parent=parent,
            description=description,
            display_name=display_name,
            id=id,
            inspect_config=inspect_config,
            template_id=template_id,
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
        '''Generates CDKTF code for importing a DataLossPreventionInspectTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLossPreventionInspectTemplate to import.
        :param import_from_id: The id of the existing DataLossPreventionInspectTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLossPreventionInspectTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be4af62e01a4b1da212e2dac58d60348d0e9cc851b2bf89725f841e938b1c78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInspectConfig")
    def put_inspect_config(
        self,
        *,
        content_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param content_options: List of options defining data content to scan. If empty, text, images, and other content will be included. Possible values: ["CONTENT_TEXT", "CONTENT_IMAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#content_options DataLossPreventionInspectTemplate#content_options}
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#custom_info_types DataLossPreventionInspectTemplate#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_info_types DataLossPreventionInspectTemplate#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#include_quote DataLossPreventionInspectTemplate#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#limits DataLossPreventionInspectTemplate#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#min_likelihood DataLossPreventionInspectTemplate#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#rule_set DataLossPreventionInspectTemplate#rule_set}
        '''
        value = DataLossPreventionInspectTemplateInspectConfig(
            content_options=content_options,
            custom_info_types=custom_info_types,
            exclude_info_types=exclude_info_types,
            include_quote=include_quote,
            info_types=info_types,
            limits=limits,
            min_likelihood=min_likelihood,
            rule_set=rule_set,
        )

        return typing.cast(None, jsii.invoke(self, "putInspectConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#create DataLossPreventionInspectTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#delete DataLossPreventionInspectTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#update DataLossPreventionInspectTemplate#update}.
        '''
        value = DataLossPreventionInspectTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInspectConfig")
    def reset_inspect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectConfig", []))

    @jsii.member(jsii_name="resetTemplateId")
    def reset_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateId", []))

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
    @jsii.member(jsii_name="inspectConfig")
    def inspect_config(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigOutputReference", jsii.get(self, "inspectConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataLossPreventionInspectTemplateTimeoutsOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectConfigInput")
    def inspect_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfig"], jsii.get(self, "inspectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="templateIdInput")
    def template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionInspectTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionInspectTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee925ae3a84fae597ced7e6cf2422e862ef2ec2999b1e71230c384d3aae3738a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569e4dbd9407f86227fae11f18034fb29b50e5c0ae84e80a837f5fe3035fd76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2430f3e6f32555e1bf6f5216c33495b5e6fde7d590e11571dd2c2f43079be142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5775c405d973f7a7e68b31d960091a3629e94920bd975754747ee8ad27b8566f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc927da5c2ca8af1f187e90b286fd8059b5deb33c0abb3dc5e54752ac9e7c763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "parent": "parent",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "inspect_config": "inspectConfig",
        "template_id": "templateId",
        "timeouts": "timeouts",
    },
)
class DataLossPreventionInspectTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_config: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionInspectTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The parent of the inspect template in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#parent DataLossPreventionInspectTemplate#parent}
        :param description: A description of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#description DataLossPreventionInspectTemplate#description}
        :param display_name: User set display name of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#display_name DataLossPreventionInspectTemplate#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#id DataLossPreventionInspectTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#inspect_config DataLossPreventionInspectTemplate#inspect_config}
        :param template_id: The template id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#template_id DataLossPreventionInspectTemplate#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#timeouts DataLossPreventionInspectTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inspect_config, dict):
            inspect_config = DataLossPreventionInspectTemplateInspectConfig(**inspect_config)
        if isinstance(timeouts, dict):
            timeouts = DataLossPreventionInspectTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0732dffe09d5e0da3e53b60a9bcfb998f072502fcdb7c0ce7e70460d17f122ca)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inspect_config", value=inspect_config, expected_type=type_hints["inspect_config"])
            check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parent": parent,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if inspect_config is not None:
            self._values["inspect_config"] = inspect_config
        if template_id is not None:
            self._values["template_id"] = template_id
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
    def parent(self) -> builtins.str:
        '''The parent of the inspect template in any of the following formats:.

        - 'projects/{{project}}'
        - 'projects/{{project}}/locations/{{location}}'
        - 'organizations/{{organization_id}}'
        - 'organizations/{{organization_id}}/locations/{{location}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#parent DataLossPreventionInspectTemplate#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the inspect template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#description DataLossPreventionInspectTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the inspect template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#display_name DataLossPreventionInspectTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#id DataLossPreventionInspectTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_config(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfig"]:
        '''inspect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#inspect_config DataLossPreventionInspectTemplate#inspect_config}
        '''
        result = self._values.get("inspect_config")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfig"], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''The template id can contain uppercase and lowercase letters, numbers, and hyphens;

        that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is
        100 characters. Can be empty to allow the system to generate one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#template_id DataLossPreventionInspectTemplate#template_id}
        '''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataLossPreventionInspectTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#timeouts DataLossPreventionInspectTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "content_options": "contentOptions",
        "custom_info_types": "customInfoTypes",
        "exclude_info_types": "excludeInfoTypes",
        "include_quote": "includeQuote",
        "info_types": "infoTypes",
        "limits": "limits",
        "min_likelihood": "minLikelihood",
        "rule_set": "ruleSet",
    },
)
class DataLossPreventionInspectTemplateInspectConfig:
    def __init__(
        self,
        *,
        content_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param content_options: List of options defining data content to scan. If empty, text, images, and other content will be included. Possible values: ["CONTENT_TEXT", "CONTENT_IMAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#content_options DataLossPreventionInspectTemplate#content_options}
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#custom_info_types DataLossPreventionInspectTemplate#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_info_types DataLossPreventionInspectTemplate#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#include_quote DataLossPreventionInspectTemplate#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#limits DataLossPreventionInspectTemplate#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#min_likelihood DataLossPreventionInspectTemplate#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#rule_set DataLossPreventionInspectTemplate#rule_set}
        '''
        if isinstance(limits, dict):
            limits = DataLossPreventionInspectTemplateInspectConfigLimits(**limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb4c8d20e9e330261aaa3d87ea40faae6a9dc9b248eef125d712ffb84fb6900)
            check_type(argname="argument content_options", value=content_options, expected_type=type_hints["content_options"])
            check_type(argname="argument custom_info_types", value=custom_info_types, expected_type=type_hints["custom_info_types"])
            check_type(argname="argument exclude_info_types", value=exclude_info_types, expected_type=type_hints["exclude_info_types"])
            check_type(argname="argument include_quote", value=include_quote, expected_type=type_hints["include_quote"])
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument min_likelihood", value=min_likelihood, expected_type=type_hints["min_likelihood"])
            check_type(argname="argument rule_set", value=rule_set, expected_type=type_hints["rule_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_options is not None:
            self._values["content_options"] = content_options
        if custom_info_types is not None:
            self._values["custom_info_types"] = custom_info_types
        if exclude_info_types is not None:
            self._values["exclude_info_types"] = exclude_info_types
        if include_quote is not None:
            self._values["include_quote"] = include_quote
        if info_types is not None:
            self._values["info_types"] = info_types
        if limits is not None:
            self._values["limits"] = limits
        if min_likelihood is not None:
            self._values["min_likelihood"] = min_likelihood
        if rule_set is not None:
            self._values["rule_set"] = rule_set

    @builtins.property
    def content_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of options defining data content to scan.

        If empty, text, images, and other content will be included. Possible values: ["CONTENT_TEXT", "CONTENT_IMAGE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#content_options DataLossPreventionInspectTemplate#content_options}
        '''
        result = self._values.get("content_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes"]]]:
        '''custom_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#custom_info_types DataLossPreventionInspectTemplate#custom_info_types}
        '''
        result = self._values.get("custom_info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes"]]], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, excludes type information of the findings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_info_types DataLossPreventionInspectTemplate#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_quote(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, a contextual quote from the data that triggered a finding is included in the response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#include_quote DataLossPreventionInspectTemplate#include_quote}
        '''
        result = self._values.get("include_quote")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigInfoTypes"]]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#limits DataLossPreventionInspectTemplate#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimits"], result)

    @builtins.property
    def min_likelihood(self) -> typing.Optional[builtins.str]:
        '''Only returns findings equal or above this threshold.

        See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#min_likelihood DataLossPreventionInspectTemplate#min_likelihood}
        '''
        result = self._values.get("min_likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSet"]]]:
        '''rule_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#rule_set DataLossPreventionInspectTemplate#rule_set}
        '''
        result = self._values.get("rule_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSet"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "info_type": "infoType",
        "dictionary": "dictionary",
        "exclusion_type": "exclusionType",
        "likelihood": "likelihood",
        "regex": "regex",
        "sensitivity_score": "sensitivityScore",
        "stored_type": "storedType",
        "surrogate_type": "surrogateType",
    },
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes:
    def __init__(
        self,
        *,
        info_type: typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType", typing.Dict[builtins.str, typing.Any]],
        dictionary: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_type: typing.Optional[builtins.str] = None,
        likelihood: typing.Optional[builtins.str] = None,
        regex: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_type: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType", typing.Dict[builtins.str, typing.Any]]] = None,
        surrogate_type: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_type DataLossPreventionInspectTemplate#info_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#dictionary DataLossPreventionInspectTemplate#dictionary}
        :param exclusion_type: If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned. It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclusion_type DataLossPreventionInspectTemplate#exclusion_type}
        :param likelihood: Likelihood to return for this CustomInfoType. This base value can be altered by a detection rule if the finding meets the criteria specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#likelihood DataLossPreventionInspectTemplate#likelihood}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#regex DataLossPreventionInspectTemplate#regex}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param stored_type: stored_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#stored_type DataLossPreventionInspectTemplate#stored_type}
        :param surrogate_type: surrogate_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#surrogate_type DataLossPreventionInspectTemplate#surrogate_type}
        '''
        if isinstance(info_type, dict):
            info_type = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType(**info_type)
        if isinstance(dictionary, dict):
            dictionary = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary(**dictionary)
        if isinstance(regex, dict):
            regex = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex(**regex)
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore(**sensitivity_score)
        if isinstance(stored_type, dict):
            stored_type = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType(**stored_type)
        if isinstance(surrogate_type, dict):
            surrogate_type = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType(**surrogate_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd362e303e4f2e50e05e2f8964036c23bebf1db4b0cd2b3fff5b6dfbe279198)
            check_type(argname="argument info_type", value=info_type, expected_type=type_hints["info_type"])
            check_type(argname="argument dictionary", value=dictionary, expected_type=type_hints["dictionary"])
            check_type(argname="argument exclusion_type", value=exclusion_type, expected_type=type_hints["exclusion_type"])
            check_type(argname="argument likelihood", value=likelihood, expected_type=type_hints["likelihood"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument stored_type", value=stored_type, expected_type=type_hints["stored_type"])
            check_type(argname="argument surrogate_type", value=surrogate_type, expected_type=type_hints["surrogate_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_type": info_type,
        }
        if dictionary is not None:
            self._values["dictionary"] = dictionary
        if exclusion_type is not None:
            self._values["exclusion_type"] = exclusion_type
        if likelihood is not None:
            self._values["likelihood"] = likelihood
        if regex is not None:
            self._values["regex"] = regex
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if stored_type is not None:
            self._values["stored_type"] = stored_type
        if surrogate_type is not None:
            self._values["surrogate_type"] = surrogate_type

    @builtins.property
    def info_type(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType":
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_type DataLossPreventionInspectTemplate#info_type}
        '''
        result = self._values.get("info_type")
        assert result is not None, "Required property 'info_type' is missing"
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType", result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#dictionary DataLossPreventionInspectTemplate#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary"], result)

    @builtins.property
    def exclusion_type(self) -> typing.Optional[builtins.str]:
        '''If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned.

        It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclusion_type DataLossPreventionInspectTemplate#exclusion_type}
        '''
        result = self._values.get("exclusion_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def likelihood(self) -> typing.Optional[builtins.str]:
        '''Likelihood to return for this CustomInfoType.

        This base value can be altered by a detection rule if the finding meets the criteria
        specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#likelihood DataLossPreventionInspectTemplate#likelihood}
        '''
        result = self._values.get("likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#regex DataLossPreventionInspectTemplate#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"], result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"], result)

    @builtins.property
    def stored_type(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"]:
        '''stored_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#stored_type DataLossPreventionInspectTemplate#stored_type}
        '''
        result = self._values.get("stored_type")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"], result)

    @builtins.property
    def surrogate_type(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"]:
        '''surrogate_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#surrogate_type DataLossPreventionInspectTemplate#surrogate_type}
        '''
        result = self._values.get("surrogate_type")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#cloud_storage_path DataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#word_list DataLossPreventionInspectTemplate#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f34ead5e92a6388a7aedd41e6a7d10f33556dd5a72364edfbcf4b9c2254c86c)
            check_type(argname="argument cloud_storage_path", value=cloud_storage_path, expected_type=type_hints["cloud_storage_path"])
            check_type(argname="argument word_list", value=word_list, expected_type=type_hints["word_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_path is not None:
            self._values["cloud_storage_path"] = cloud_storage_path
        if word_list is not None:
            self._values["word_list"] = word_list

    @builtins.property
    def cloud_storage_path(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#cloud_storage_path DataLossPreventionInspectTemplate#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#word_list DataLossPreventionInspectTemplate#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#path DataLossPreventionInspectTemplate#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5437d424aa35ead230a753e46ee734de1a4ad1c4cf3d3a2de51ae04a08bf202f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#path DataLossPreventionInspectTemplate#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6197acd6b38feb38c510bb6bb0fc4a89ecb8cfad6cc81649a4c6df3d12570285)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f606ad8ff0a5c74f7d76feb03a16a0af3ec5c33a64ab94c8da0d86fc5a6b5fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ec6e021b82c80ccbce2481d232860f658cb8b4718e8b8a70f22857c2254da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbe634d4b9560ff1a9744a6c31a6850421b51c0cfd66efc96a250e4205d6f57c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#path DataLossPreventionInspectTemplate#path}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#words DataLossPreventionInspectTemplate#words}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct(
            words=words
        )

        return typing.cast(None, jsii.invoke(self, "putWordList", [value]))

    @jsii.member(jsii_name="resetCloudStoragePath")
    def reset_cloud_storage_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStoragePath", []))

    @jsii.member(jsii_name="resetWordList")
    def reset_word_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWordList", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePath")
    def cloud_storage_path(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9111c17ca5fa79a524c06482a5d839b7a5350bcb02966ccd647c75afba12eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#words DataLossPreventionInspectTemplate#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1d607b6bbb89c31a8f5f2d1333784901c23ece3a4ee23243f1045015e5b089)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#words DataLossPreventionInspectTemplate#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed70d7fe4184c402c9f284b59a54b7b801c7ca998f04c42df0fab359f1f78491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="wordsInput")
    def words_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "wordsInput"))

    @builtins.property
    @jsii.member(jsii_name="words")
    def words(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "words"))

    @words.setter
    def words(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02bd0f58dd59bd5599be4bb4ef12d222edf77575664192e9d7632a40855f074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4386a49cba662cec566cb86607cb2525d614095f5540cc3a9b5cb3bb940400be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f90572a4396be9bc60dc605de66cf543c4f1931cc6baadc77dd24188ecb9fb1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names
        listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc7be892e7947e793876f8236f7929ad46d6e6eb9df9a139a8c8c55c2ba0044d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e76fbb98ed58e96ce4706a7bd84b7159df9053d242aedfa760483e97299f7c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ae12efb4e51d07fa7ee4e65e892fd4f0e991ff00328707bb4b64bbd284b0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__886cfb74a1d5398b5bbce9e8db3a7cf00003a6610ca7fb49e19ad57fbd51fce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ec1de685ba2325bce2264342c6b5c01ec524133fd8a3b3184d7f60b2de844e)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1549beffd4f9b7ea9e737c6b3e138ccfe4202342be595fb99a43f43c6dc44d4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61be8b573f3c62071e446518372c051cf9906b2ee94ea40d58aeec5f3b359a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e3aa803e578cd32e70054c72ecf6bea2a3462aa697401a57496df298bbab36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe617e3a10aa530e169b285355280f7158714684425c3c8c93b2b42f7e4626f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89928cb95dc5c70a8a2ac0b4103f652611f3fe451bbbbc5d00010260a0adf43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d99821ff9bdc697745fae65d9155474d65aaf643047c9a7d8cd6347b28216b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6abb09b195bb5c462720e2e12298219cf5451fa307235c5b6ede3c28e2802c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ea257899793b6c13410966bf1d44f72c6cfc44ccd0705ef3e19b0ab2da53345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fc7e44f168ed2cb882bdf2a6fb92db4a8c16e045a4c85e38aa797670362244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92d7c6fd297f1446a4aac143b639574c72a8836714cb38385027fb1472b5549b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#cloud_storage_path DataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#word_list DataLossPreventionInspectTemplate#word_list}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putInfoType")
    def put_info_type(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType(
            name=name, sensitivity_score=sensitivity_score, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putInfoType", [value]))

    @jsii.member(jsii_name="putRegex")
    def put_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="putStoredType")
    def put_stored_type(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStoredType", [value]))

    @jsii.member(jsii_name="putSurrogateType")
    def put_surrogate_type(self) -> None:
        value = DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType()

        return typing.cast(None, jsii.invoke(self, "putSurrogateType", [value]))

    @jsii.member(jsii_name="resetDictionary")
    def reset_dictionary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDictionary", []))

    @jsii.member(jsii_name="resetExclusionType")
    def reset_exclusion_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionType", []))

    @jsii.member(jsii_name="resetLikelihood")
    def reset_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLikelihood", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetStoredType")
    def reset_stored_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoredType", []))

    @jsii.member(jsii_name="resetSurrogateType")
    def reset_surrogate_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurrogateType", []))

    @builtins.property
    @jsii.member(jsii_name="dictionary")
    def dictionary(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="infoType")
    def info_type(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="storedType")
    def stored_type(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference", jsii.get(self, "storedType"))

    @builtins.property
    @jsii.member(jsii_name="surrogateType")
    def surrogate_type(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference", jsii.get(self, "surrogateType"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionTypeInput")
    def exclusion_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType], jsii.get(self, "infoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodInput")
    def likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="storedTypeInput")
    def stored_type_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"], jsii.get(self, "storedTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="surrogateTypeInput")
    def surrogate_type_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"], jsii.get(self, "surrogateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionType")
    def exclusion_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclusionType"))

    @exclusion_type.setter
    def exclusion_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b309b15f56fae23d9b0360e570bf4140a0afbb70b5c4b630a5da071b0bfedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="likelihood")
    def likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "likelihood"))

    @likelihood.setter
    def likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca607fc55859d54eeba1c4581a9d4a7f5bd054a42289026c4a74238ce07f9543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "likelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd75626fde2ce954327ac2ef2bbf2090281e47c4ddc9cfc1d7c51aa1fec2c469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e19a466fd1a4fa735cd181f948c29583e1ae97e0fdaeac27a188b56604a2915)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf02f9d516402c16dd86f04f4827187cce688594a6ee64b83fa865d3e9004fac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2315463eb11f976c80f18214262cdffc2c86cfcc1f8b71bd1d8b18f216790085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52ed54bfb97f1bda5b90b97be2f2cf20e2fd6316a2f9b2331efc0028f590493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e785e1b833166806e446c977d110fb630bf60441adde1100cbffb6b76919042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feef2d5fd85ce590a807622b28fbdb11190e35998bd944d38f326c2faaadca2a)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a941ff7deb7292f13dfc3227c9d96361529bb3c8c433f29fd314aec90219ed6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfba6dc7e141cf8b49cec68ed204007e2a6ac425204917ddb27f70998cb49e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855e0acc96c860b1642baa1e99606ff3cdaef3f83825285b60ddfe9671817452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6563230bd397cd17b23b33d06951531f3ae20bf547a5cb125526d283123d4fd7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083da1a92d4f86fae012c6e33e6cd51bd7c4430bba94abed3624203045b59c92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80b95dd0dc686fee4f9b413d4f513400aafb8f82c808d4098c4767fbddd3e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210071e6c66c5d6be2c477b1c9afe0643ad962feb2ff2f44b70307a7406ec579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23308d81e6945289cbb2eba13c316c85dffd1a46e9f4b424904196e1359f0b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25535478118e2997682651f90d97c17cb477f32f2654eae7932ae88ac7b809b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionInspectTemplateInspectConfigInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6de9ca845e02e665b686cad8b559aef1357b86814d9cde9c6e4617433dd440)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d39f0bc2700c5b47037bf493030eb1b57f9203e7feffdc879eceb724d15273c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6b4df471954e5ee7f0d6345395f4532de614f51eed66f85696c70edd1adfd1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54552fbeb66f2e49a05777e2cbcd5f893edcd8cf618267e6f7299b2360d992c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a085c6bcbf0b3e0959760bc707633aef4acf5cf934e0b322bce08875b972a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__431b7eabf86f8f2ca59a2ab192c720325b189ef777a7fbf0fd91ab162c4c13e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a6e8895bed1a3c8e481d440b5a3e768e1957cd7ba775ab6950f6fdaa207a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef07639fd3a8a22ccbb74e4af04b7691bf29220de2b44eedde4dba949b057467)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07ae06c0ca6b3b8d6df6d5f70256be57e8352b70e0cdd471ad3a863a01fcd69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012803d387bf612d8b74b803a098ce84d19d3182204e033aced6d6f2a7ae79fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fdb1b3e2fb1598167dcd8ab4bb3426545e589989d63104e2837661b20baeac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7a34bb4d756deb822adbf9a9ace99bdd32ac6ecde96dc2f2b8d98d2c252c29)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b7ef1b73d3fed8c92b18d8997c0c91f0bd0d627d295cb204e9e3f8766d53ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283864c5c4ec7e42930b047fcead7df778e7d29d0beac218694aaf0fa4ef90d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f51b9460a17edb4a58a9f9baac947f7958299b316e1b41f80cb7d9ad2753dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_findings_per_item": "maxFindingsPerItem",
        "max_findings_per_request": "maxFindingsPerRequest",
        "max_findings_per_info_type": "maxFindingsPerInfoType",
    },
)
class DataLossPreventionInspectTemplateInspectConfigLimits:
    def __init__(
        self,
        *,
        max_findings_per_item: jsii.Number,
        max_findings_per_request: jsii.Number,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_item DataLossPreventionInspectTemplate#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_request DataLossPreventionInspectTemplate#max_findings_per_request}
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_info_type DataLossPreventionInspectTemplate#max_findings_per_info_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97262d7f266f5295e7210223be4bcd05bd383b801598ef57085b8a843ed3134)
            check_type(argname="argument max_findings_per_item", value=max_findings_per_item, expected_type=type_hints["max_findings_per_item"])
            check_type(argname="argument max_findings_per_request", value=max_findings_per_request, expected_type=type_hints["max_findings_per_request"])
            check_type(argname="argument max_findings_per_info_type", value=max_findings_per_info_type, expected_type=type_hints["max_findings_per_info_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_findings_per_item": max_findings_per_item,
            "max_findings_per_request": max_findings_per_request,
        }
        if max_findings_per_info_type is not None:
            self._values["max_findings_per_info_type"] = max_findings_per_info_type

    @builtins.property
    def max_findings_per_item(self) -> jsii.Number:
        '''Max number of findings that will be returned for each item scanned. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_item DataLossPreventionInspectTemplate#max_findings_per_item}
        '''
        result = self._values.get("max_findings_per_item")
        assert result is not None, "Required property 'max_findings_per_item' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_findings_per_request(self) -> jsii.Number:
        '''Max number of findings that will be returned per request/job. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_request DataLossPreventionInspectTemplate#max_findings_per_request}
        '''
        result = self._values.get("max_findings_per_request")
        assert result is not None, "Required property 'max_findings_per_request' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_findings_per_info_type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType"]]]:
        '''max_findings_per_info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_info_type DataLossPreventionInspectTemplate#max_findings_per_info_type}
        '''
        result = self._values.get("max_findings_per_info_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType",
    jsii_struct_bases=[],
    name_mapping={"max_findings": "maxFindings", "info_type": "infoType"},
)
class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType:
    def __init__(
        self,
        *,
        max_findings: jsii.Number,
        info_type: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_findings: Max findings limit for the given infoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings DataLossPreventionInspectTemplate#max_findings}
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_type DataLossPreventionInspectTemplate#info_type}
        '''
        if isinstance(info_type, dict):
            info_type = DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(**info_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb03f37ae83c1346daeb27b5cc53561923e26b18c997071bed8da108116ceb78)
            check_type(argname="argument max_findings", value=max_findings, expected_type=type_hints["max_findings"])
            check_type(argname="argument info_type", value=info_type, expected_type=type_hints["info_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_findings": max_findings,
        }
        if info_type is not None:
            self._values["info_type"] = info_type

    @builtins.property
    def max_findings(self) -> jsii.Number:
        '''Max findings limit for the given infoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings DataLossPreventionInspectTemplate#max_findings}
        '''
        result = self._values.get("max_findings")
        assert result is not None, "Required property 'max_findings' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def info_type(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"]:
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_type DataLossPreventionInspectTemplate#info_type}
        '''
        result = self._values.get("info_type")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393836c3e6da221ed789d99af87badca0e378032e350ca6a7f0a43248ad5afb3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__840c8d6b591cc943465c6f9a756bdb3848c30674a8291ef9454604ef848fd68b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c611f79d295d68840b5dcbcdb412070c540c53d900195dcecb1acdc44103eeb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad059969b308816af315aaf838b2c02c5d0f57caa26317cfeb39721ab69ca15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5a30583fc833651d65fe8207a19b48c398a209de8cf50c53302a66cf8bf96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b463934e7c7d26b9ff9f554e4f3b238bbd86c648cdee32c9f2ba860d8c7232)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2bfaeebd44c18e4ce6960ccf544d712cb76fdf98e64f3591dff9cd6f4ae8a7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ab4de7aeb407a8331e05f414603bcb02bf84bd2071d031d718212140ecb8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3a186ed7da4f63942e36e44ec5bb1747e915f2f2355708ba77cfbf9caa476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef413e1adcd5d8e3a9f03e6e57fe72495f9f205a69c5b690ab961a9d9670226f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbd88fea70929901761b2c25266c36847d45d6452059a97fc7cd9362b40eb88)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb7c23cd3fefe853ae30497e0e185605cddf3807e27798a0669474fb7d9c8d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65fb9e4e9862d907cf04d36a34b801456eec4b2bea1b4099a3d245a7a1acd52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f5d3e892eb26dddbce5c05b5e49a06fdab78604027653a8e941ddf9317d6129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7573ae9ca2c8d53868396cb389b50944ce5e9fa568d74cb5aca77b0e2263effc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77388454b6300e60a350ca904be348f1f5af23f626ae0814003a614e42cc7886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoType")
    def put_info_type(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(
            name=name, sensitivity_score=sensitivity_score, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putInfoType", [value]))

    @jsii.member(jsii_name="resetInfoType")
    def reset_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoType", []))

    @builtins.property
    @jsii.member(jsii_name="infoType")
    def info_type(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "infoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsInput")
    def max_findings_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindings")
    def max_findings(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindings"))

    @max_findings.setter
    def max_findings(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc57ac7f833fc5adea71557bf235b5aa4ea1c26cf529b5783e2de7cf56ab8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa1bf2fecef896793f6aebd4ccefa9c30e322bfe45458f52fac1c9d1b12360b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20c2e5582a939951f5408f5414d87918dcad1bb30b96f94c1d7106851a988b33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaxFindingsPerInfoType")
    def put_max_findings_per_info_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7db3c0606e036c1bfe59b0215aca20340fb7b8dbc77a7f2b66d316239d223fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaxFindingsPerInfoType", [value]))

    @jsii.member(jsii_name="resetMaxFindingsPerInfoType")
    def reset_max_findings_per_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFindingsPerInfoType", []))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoType")
    def max_findings_per_info_type(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList, jsii.get(self, "maxFindingsPerInfoType"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoTypeInput")
    def max_findings_per_info_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "maxFindingsPerInfoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerItemInput")
    def max_findings_per_item_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFindingsPerItemInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerRequestInput")
    def max_findings_per_request_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFindingsPerRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerItem")
    def max_findings_per_item(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindingsPerItem"))

    @max_findings_per_item.setter
    def max_findings_per_item(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207dbbfd9a1ad0b77869d3f8935d918a06e8d4cad8ad798e0b109a30d7458b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerItem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerRequest")
    def max_findings_per_request(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindingsPerRequest"))

    @max_findings_per_request.setter
    def max_findings_per_request(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55506b12db831b04778321ba5eeefaa1366aa3c554fe52ca4a5a271b188cff4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimits]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb96488fcf94b9c5f6e8f56e16e09b125c3eeb0391d553a98e16d5478adfd63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac60f1f2a3499af4f0ec026dd0506daab8affd8747835a287ef447675da4113)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomInfoTypes")
    def put_custom_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff7a07b83cba348df0566be3beb2826e7327ac64fd9253049c7f74a637d40af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomInfoTypes", [value]))

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed48f75ac469f26ee93f49c6c82c55a008efb39be6a83c4f06b35b14ba086df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        max_findings_per_item: jsii.Number,
        max_findings_per_request: jsii.Number,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_item DataLossPreventionInspectTemplate#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_request DataLossPreventionInspectTemplate#max_findings_per_request}
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#max_findings_per_info_type DataLossPreventionInspectTemplate#max_findings_per_info_type}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigLimits(
            max_findings_per_item=max_findings_per_item,
            max_findings_per_request=max_findings_per_request,
            max_findings_per_info_type=max_findings_per_info_type,
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putRuleSet")
    def put_rule_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c29291caae51a9786fc444e7d2a066dca305ab85bcf3da1aca0cb01713add91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuleSet", [value]))

    @jsii.member(jsii_name="resetContentOptions")
    def reset_content_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentOptions", []))

    @jsii.member(jsii_name="resetCustomInfoTypes")
    def reset_custom_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomInfoTypes", []))

    @jsii.member(jsii_name="resetExcludeInfoTypes")
    def reset_exclude_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeInfoTypes", []))

    @jsii.member(jsii_name="resetIncludeQuote")
    def reset_include_quote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeQuote", []))

    @jsii.member(jsii_name="resetInfoTypes")
    def reset_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfoTypes", []))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetMinLikelihood")
    def reset_min_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLikelihood", []))

    @jsii.member(jsii_name="resetRuleSet")
    def reset_rule_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleSet", []))

    @builtins.property
    @jsii.member(jsii_name="customInfoTypes")
    def custom_info_types(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList, jsii.get(self, "customInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(self) -> DataLossPreventionInspectTemplateInspectConfigInfoTypesList:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigLimitsOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetList":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetList", jsii.get(self, "ruleSet"))

    @builtins.property
    @jsii.member(jsii_name="contentOptionsInput")
    def content_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="customInfoTypesInput")
    def custom_info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]], jsii.get(self, "customInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypesInput")
    def exclude_info_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeQuoteInput")
    def include_quote_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeQuoteInput"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimits]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="minLikelihoodInput")
    def min_likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetInput")
    def rule_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSet"]]], jsii.get(self, "ruleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="contentOptions")
    def content_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contentOptions"))

    @content_options.setter
    def content_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c92a02c662aff1e58a1fd8208daf90d264ccd43db1af7f1398da2e68af39f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypes")
    def exclude_info_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeInfoTypes"))

    @exclude_info_types.setter
    def exclude_info_types(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02184d0b8c60b4ef53d4e8ef36b1d6b168ef72869fdba2d10f5a81f6a5227b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeInfoTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeQuote")
    def include_quote(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeQuote"))

    @include_quote.setter
    def include_quote(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e023e5296907452d03b35b324fa88f759830d2260753063bc4e5341c810dbdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQuote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLikelihood")
    def min_likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minLikelihood"))

    @min_likelihood.setter
    def min_likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c008e8e9f3f5efa30eb4ffe3a02e2fc82fa4ba495ccfd41f143974e0b9511c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfig]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe962f45fb29c0a67b4f2d99d8a487e91a4f28da01698448cfc342a1d545ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSet",
    jsii_struct_bases=[],
    name_mapping={"info_types": "infoTypes", "rules": "rules"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSet:
    def __init__(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes", typing.Dict[builtins.str, typing.Any]]]],
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#rules DataLossPreventionInspectTemplate#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d82d4ae97d18774a4f9ef8ceb59ce492167923f668d5692936b2748b0bbef08)
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_types": info_types,
            "rules": rules,
        }

    @builtins.property
    def info_types(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes"]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        '''
        result = self._values.get("info_types")
        assert result is not None, "Required property 'info_types' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes"]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#rules DataLossPreventionInspectTemplate#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc05fe18cdf80783f1b30226988861d42648c743944651570548219087d0a3a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22bef1f719935c2214e2a9cac7c6c89a0532d9af0a3ec309d5308df05109471e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac13b64a3e968ceb6cc413b1dbb44bde2e07866d16d8a84341ec7393b571a07)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e574930ec7d86fc2fad395df026e04e9ff4969a3977f9617b6721045c0df0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a28019df9c7ef1b7da50fd118d9bf597f8c04a3bca552b224934782bc1acb57f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8b54e67a3c76bfafa3c9dab19e0a5c15fd58caaec03ed1e77d4da9a6da67acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db45877870f0c0bed756b866808a4a8c9f2cc3507334f76a7c724870dcd085b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2de83aafbe238cd0494ee901440b819a704628f4d3c70e318a25e46aed695256)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63cabcce03b76f11cf6a12f6b1b1ba74f80c79d172f626cf92f29b4101eba3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28600656c416f6dff013d86cb4a24192831faaed4857d389fa57476e5476ff81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a492854e20b5027118dbecb7b11f91286d660c6dc190c2a62aff57823671b839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085ab96bd5abd38ae6220e8a736b7886d8da0fdc56085a1c34efe6351d6b43af)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46a15d0f6708ad23d3dd31080979073cc10e7bfa9c59f766ebb26af79faa21b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25601e9e0d159bc5b8fccf1900c66c9b5738fbb07b2722cb81c9f10847828285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61a1b72a94561f2f94bf3346af6a4ad305af14a9152094918a2ad71e8fde081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1998c397cd33130a87b0ad3491e4aef5eb78cc89d11a29a1c4141cf301b3507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1cc8a0fb1b39080465bb0c76ee371eeadc46d8f53ee807b41600ed715ee3250)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6518fe5c5464f708e2f1ef351a612c55de795a9cb59a5561b9d1e00df75de6a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__467c764289ca70e5b34bc9bd02dff7583bccc4d871125b582b08b95d741b2b6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f04f5c5f088ee5129c71c6cec7a048bc554c95ec1de563ca1a086aea67947d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb2f940ab5933131e917b35c3e45551f23b7d48055c9dd5e6a630af6bfb5b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37ebdf30ecb888c30f8f075099ceebc5d63b229aff0dfecc20b81de084523c6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657bfd58595fa46b2f5676a5a2692c711b2869e7eb6b92024e9df516a02a305e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae320c1cbcbe57547c0ae85d544db004967c19c8cb31197160b7f2f2474fe6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesList":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d2453ab37d0f5bd76441873bd15bfe48c572c1cdc5357463d553ecf3095471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRules",
    jsii_struct_bases=[],
    name_mapping={"exclusion_rule": "exclusionRule", "hotword_rule": "hotwordRule"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRules:
    def __init__(
        self,
        *,
        exclusion_rule: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule", typing.Dict[builtins.str, typing.Any]]] = None,
        hotword_rule: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param exclusion_rule: exclusion_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclusion_rule DataLossPreventionInspectTemplate#exclusion_rule}
        :param hotword_rule: hotword_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_rule DataLossPreventionInspectTemplate#hotword_rule}
        '''
        if isinstance(exclusion_rule, dict):
            exclusion_rule = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule(**exclusion_rule)
        if isinstance(hotword_rule, dict):
            hotword_rule = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule(**hotword_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed259ceb3f2c24aaa688a6d6c1bf5fb2ab2572685e0c8f557f93b8e1ddb94a4)
            check_type(argname="argument exclusion_rule", value=exclusion_rule, expected_type=type_hints["exclusion_rule"])
            check_type(argname="argument hotword_rule", value=hotword_rule, expected_type=type_hints["hotword_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion_rule is not None:
            self._values["exclusion_rule"] = exclusion_rule
        if hotword_rule is not None:
            self._values["hotword_rule"] = hotword_rule

    @builtins.property
    def exclusion_rule(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule"]:
        '''exclusion_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclusion_rule DataLossPreventionInspectTemplate#exclusion_rule}
        '''
        result = self._values.get("exclusion_rule")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule"], result)

    @builtins.property
    def hotword_rule(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule"]:
        '''hotword_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_rule DataLossPreventionInspectTemplate#hotword_rule}
        '''
        result = self._values.get("hotword_rule")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule",
    jsii_struct_bases=[],
    name_mapping={
        "matching_type": "matchingType",
        "dictionary": "dictionary",
        "exclude_by_hotword": "excludeByHotword",
        "exclude_info_types": "excludeInfoTypes",
        "regex": "regex",
    },
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule:
    def __init__(
        self,
        *,
        matching_type: builtins.str,
        dictionary: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#matching_type DataLossPreventionInspectTemplate#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#dictionary DataLossPreventionInspectTemplate#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_by_hotword DataLossPreventionInspectTemplate#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_info_types DataLossPreventionInspectTemplate#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#regex DataLossPreventionInspectTemplate#regex}
        '''
        if isinstance(dictionary, dict):
            dictionary = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary(**dictionary)
        if isinstance(exclude_by_hotword, dict):
            exclude_by_hotword = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(**exclude_by_hotword)
        if isinstance(exclude_info_types, dict):
            exclude_info_types = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(**exclude_info_types)
        if isinstance(regex, dict):
            regex = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex(**regex)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a4a8abfbbfe235984751cb1df4e06bc44f8d4464c3014592d880c7c1fda869)
            check_type(argname="argument matching_type", value=matching_type, expected_type=type_hints["matching_type"])
            check_type(argname="argument dictionary", value=dictionary, expected_type=type_hints["dictionary"])
            check_type(argname="argument exclude_by_hotword", value=exclude_by_hotword, expected_type=type_hints["exclude_by_hotword"])
            check_type(argname="argument exclude_info_types", value=exclude_info_types, expected_type=type_hints["exclude_info_types"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matching_type": matching_type,
        }
        if dictionary is not None:
            self._values["dictionary"] = dictionary
        if exclude_by_hotword is not None:
            self._values["exclude_by_hotword"] = exclude_by_hotword
        if exclude_info_types is not None:
            self._values["exclude_info_types"] = exclude_info_types
        if regex is not None:
            self._values["regex"] = regex

    @builtins.property
    def matching_type(self) -> builtins.str:
        '''How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#matching_type DataLossPreventionInspectTemplate#matching_type}
        '''
        result = self._values.get("matching_type")
        assert result is not None, "Required property 'matching_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#dictionary DataLossPreventionInspectTemplate#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary"], result)

    @builtins.property
    def exclude_by_hotword(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"]:
        '''exclude_by_hotword block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_by_hotword DataLossPreventionInspectTemplate#exclude_by_hotword}
        '''
        result = self._values.get("exclude_by_hotword")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"]:
        '''exclude_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_info_types DataLossPreventionInspectTemplate#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#regex DataLossPreventionInspectTemplate#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#cloud_storage_path DataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#word_list DataLossPreventionInspectTemplate#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499e40b513fcdb092d85a847585efd2e3474493a04f9547f020049e21e4d9338)
            check_type(argname="argument cloud_storage_path", value=cloud_storage_path, expected_type=type_hints["cloud_storage_path"])
            check_type(argname="argument word_list", value=word_list, expected_type=type_hints["word_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_storage_path is not None:
            self._values["cloud_storage_path"] = cloud_storage_path
        if word_list is not None:
            self._values["word_list"] = word_list

    @builtins.property
    def cloud_storage_path(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#cloud_storage_path DataLossPreventionInspectTemplate#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#word_list DataLossPreventionInspectTemplate#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#path DataLossPreventionInspectTemplate#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04bc359a7773af0202a7cc8bafbbee297265a3e328aa1215fa8f4e47e73dc3f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#path DataLossPreventionInspectTemplate#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__311fea9a69c0cfc0b5a5157a50d8c654535010fef34e7bed4e0997f1a8e8623e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3094b44160633e4cbc7c42d8d47e6a6b75747c519d3ed2a1de6dda8220e5513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0274f9381ece508aef7dbdc01b590f730237cf10f652ad9d611a5b4ebf9466a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b78ad3d8f2bca513520909cddadb36a4da889a61ded97ae149574e202fe400e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#path DataLossPreventionInspectTemplate#path}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#words DataLossPreventionInspectTemplate#words}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(
            words=words
        )

        return typing.cast(None, jsii.invoke(self, "putWordList", [value]))

    @jsii.member(jsii_name="resetCloudStoragePath")
    def reset_cloud_storage_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudStoragePath", []))

    @jsii.member(jsii_name="resetWordList")
    def reset_word_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWordList", []))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePath")
    def cloud_storage_path(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e784aa5203b8a262207021fcd2bc60ee22df6310d7144937a95ceae9c95852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#words DataLossPreventionInspectTemplate#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a75eeacd25a7c986597b4211a04b1e2ccd4f88fc8845964b5a0c121610bc648)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#words DataLossPreventionInspectTemplate#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__208972778dd14d28227d8f5ae04af40c320156bc31611d39c101eeacbcbe1399)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="wordsInput")
    def words_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "wordsInput"))

    @builtins.property
    @jsii.member(jsii_name="words")
    def words(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "words"))

    @words.setter
    def words(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccaed0f6d88661673dd9b21878a8c0311db27a0c708f6a750384146f2b84eeea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d87055d39a010b22d2999fd97b6a421463fc8f212f63aa37999fc1b67961d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    jsii_struct_bases=[],
    name_mapping={"hotword_regex": "hotwordRegex", "proximity": "proximity"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword:
    def __init__(
        self,
        *,
        hotword_regex: typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex", typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_regex DataLossPreventionInspectTemplate#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#proximity DataLossPreventionInspectTemplate#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(**hotword_regex)
        if isinstance(proximity, dict):
            proximity = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bc715ab0e31bd10954d8df09f0806eff4cd9f81209893703a9a1594ad78173)
            check_type(argname="argument hotword_regex", value=hotword_regex, expected_type=type_hints["hotword_regex"])
            check_type(argname="argument proximity", value=proximity, expected_type=type_hints["proximity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hotword_regex": hotword_regex,
            "proximity": proximity,
        }

    @builtins.property
    def hotword_regex(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex":
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_regex DataLossPreventionInspectTemplate#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        assert result is not None, "Required property 'hotword_regex' is missing"
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex", result)

    @builtins.property
    def proximity(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity":
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#proximity DataLossPreventionInspectTemplate#proximity}
        '''
        result = self._values.get("proximity")
        assert result is not None, "Required property 'proximity' is missing"
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398b33a52a65c13850d746f7a1659eef1fe401aa4214406a1081d0e15a7ad436)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified,
        the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09e487e17834a1f715eeef3fd371c3b064ade21c07eb7cdcfd2f22df3df02b37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0bea6946f5de9ae0c10cb2518bc3a4840d8d6dc6fbc6b64bf897081e8b900d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163f0c60604145b51de2b11dd5b954e6e73074a0d87fd716f24a3a9443964c4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7c4bc439cb033c0112e8ea2adb0c5a8cec46230ce00fb5166c7c76686213f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18bca36e530588358b00ab45c52f7ff3565de9032dc87b270a978ebae01a4afb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHotwordRegex")
    def put_hotword_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putHotwordRegex", [value]))

    @jsii.member(jsii_name="putProximity")
    def put_proximity(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_after DataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_before DataLossPreventionInspectTemplate#window_before}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(
            window_after=window_after, window_before=window_before
        )

        return typing.cast(None, jsii.invoke(self, "putProximity", [value]))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegex")
    def hotword_regex(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a592c488b49e4f2432d3c8b896e206f5599f2f3efe68b83314e2e6b046797f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_after DataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_before DataLossPreventionInspectTemplate#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f306ea74c4bedf4880aa5ebc1638db706296e6cdbca7d9e97d21429580440b)
            check_type(argname="argument window_after", value=window_after, expected_type=type_hints["window_after"])
            check_type(argname="argument window_before", value=window_before, expected_type=type_hints["window_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if window_after is not None:
            self._values["window_after"] = window_after
        if window_before is not None:
            self._values["window_before"] = window_before

    @builtins.property
    def window_after(self) -> typing.Optional[jsii.Number]:
        '''Number of characters after the finding to consider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_after DataLossPreventionInspectTemplate#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_before DataLossPreventionInspectTemplate#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32ecb2fa01782c94efffa22e0bfa60df1e47834d2724eb024a3ca5b122899bf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWindowAfter")
    def reset_window_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowAfter", []))

    @jsii.member(jsii_name="resetWindowBefore")
    def reset_window_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowBefore", []))

    @builtins.property
    @jsii.member(jsii_name="windowAfterInput")
    def window_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="windowBeforeInput")
    def window_before_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowAfter")
    def window_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowAfter"))

    @window_after.setter
    def window_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02828e9798a0f09078117a08abc7f47059d0e90c169e56db58e6a45ac1c5eb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf0887d45804ed2c5b39a9b2ee973bc88301d903f7f7f7c6169cafbc03c36a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a9ff0287a0a07c37156e392aaf18ba9e6c81fb7e39ef0b307db5d6448087ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    jsii_struct_bases=[],
    name_mapping={"info_types": "infoTypes"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes:
    def __init__(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eea1f4c158818d6adcf8bc9084720a8b79cbe9c1b9aa8e2359a0a2e6653458e)
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_types": info_types,
        }

    @builtins.property
    def info_types(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        '''
        result = self._values.get("info_types")
        assert result is not None, "Required property 'info_types' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca9c1cbd205a4e5d27a91f4f755ba5abe75dcdb02847fbd284b1fe71994e3bc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity_score", value=sensitivity_score, expected_type=type_hints["sensitivity_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sensitivity_score is not None:
            self._values["sensitivity_score"] = sensitivity_score
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the information type.

        Either a name of your choosing when creating a CustomInfoType, or one of the names listed
        at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#name DataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#sensitivity_score DataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#version DataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7abc63f8c814620d93c7c629862cdcf5ce0bfcb26faf18f4c608af60cf428ca6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2834a2a6f2ad6965ba4624033af37ea34f01627ea49d60c3524b9dfdd1b2c7f8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ba6da80be58fb905cb0cf928a37bc3331dfb771f096c7263ce2fe003d1de2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd93988a7d7fcc2205f77a5a20681754b75fdb47c15a364125f50ede92f18eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__324665677272191a373e6d90d41f84183807f181043199741d9119852077027f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0022e96fdef86cd086faa5a982f440f799eec30716b51867c25905642bb473ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0ab814a6e7fac7ac1f0e5a97d1cc57970439740a68a9fc4f33b7cbf35ee49b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="resetSensitivityScore")
    def reset_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivityScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee05558cf12912b913581c4de9084fec4865ae6cfd829bf26446f46d9a22d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ac818cd63c04d4d065573bd567eb18a16170c11596c02848d7870b50c8c575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17cbcc36812567205dcb13cb1182efcd7b88fb164092ed6c744724e1089d1a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da6c1e6d7c5a86c7cb6682654243e6b68e7ab3cd6165a84c8d84d162924d168)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#score DataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b61d1ce569927f4a96768ec883a44bad287b4b270c5124ad743837ee8a7ac294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "score"))

    @score.setter
    def score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f01a9e91ef4f36a3ce8b604d08a565fc83e5197633013f2917c492156ca0732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5750e0b750a48cd7651b1bce0c33803d3e3d731c6b42ce98f30c63472a60f740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e771c09aef6ef4dcf8bd92430a3925acca1e72b60a8e10bf88eeeebed893a062)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4b73fd73919879ea9a5d11c15fd035e04acc11ada309c72e7b7c9eeb829c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e217a6cbfd7d81342924c72a6e23e354b6437d26986dc9debc6600778adf0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e87097870f553831681464d74f3698a3593ac6d9d72c53e664ba0928df496241)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#cloud_storage_path DataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#word_list DataLossPreventionInspectTemplate#word_list}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putExcludeByHotword")
    def put_exclude_by_hotword(
        self,
        *,
        hotword_regex: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_regex DataLossPreventionInspectTemplate#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#proximity DataLossPreventionInspectTemplate#proximity}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(
            hotword_regex=hotword_regex, proximity=proximity
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeByHotword", [value]))

    @jsii.member(jsii_name="putExcludeInfoTypes")
    def put_exclude_info_types(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#info_types DataLossPreventionInspectTemplate#info_types}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(
            info_types=info_types
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeInfoTypes", [value]))

    @jsii.member(jsii_name="putRegex")
    def put_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="resetDictionary")
    def reset_dictionary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDictionary", []))

    @jsii.member(jsii_name="resetExcludeByHotword")
    def reset_exclude_by_hotword(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeByHotword", []))

    @jsii.member(jsii_name="resetExcludeInfoTypes")
    def reset_exclude_info_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeInfoTypes", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @builtins.property
    @jsii.member(jsii_name="dictionary")
    def dictionary(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotword")
    def exclude_by_hotword(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference, jsii.get(self, "excludeByHotword"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypes")
    def exclude_info_types(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference, jsii.get(self, "excludeInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotwordInput")
    def exclude_by_hotword_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "excludeByHotwordInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypesInput")
    def exclude_info_types_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "excludeInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingTypeInput")
    def matching_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingType")
    def matching_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchingType"))

    @matching_type.setter
    def matching_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a4363b4939b8e582a518ecda9e5ba85a4dd9e1411992eb56256dc98dbb9161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f8dab11ececc83a3b520d40031547feedc69343ead0ee386f231b299386389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889493a2bd31552349a16a8a08d6558efef5e4fa0a1cc659f69b0d9599a408a9)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__004e596c6b985979339cabc72c39d394cf1afa7f41771a2706eb21378579a118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7ca089a8f454f31364f09b128b273d957ed6880ddd9d4b349766805b20ffb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7119d951d90e7c7c09e49dbd249e3ee3a821d69e760ed221959c67978c3acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e855d75aa8139b78c81794c7346b3a6597288a2b32ec8982f170530d09b97d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule",
    jsii_struct_bases=[],
    name_mapping={
        "hotword_regex": "hotwordRegex",
        "likelihood_adjustment": "likelihoodAdjustment",
        "proximity": "proximity",
    },
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule:
    def __init__(
        self,
        *,
        hotword_regex: typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex", typing.Dict[builtins.str, typing.Any]],
        likelihood_adjustment: typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment", typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_regex DataLossPreventionInspectTemplate#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#likelihood_adjustment DataLossPreventionInspectTemplate#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#proximity DataLossPreventionInspectTemplate#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex(**hotword_regex)
        if isinstance(likelihood_adjustment, dict):
            likelihood_adjustment = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(**likelihood_adjustment)
        if isinstance(proximity, dict):
            proximity = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11473eb59a7785ac7acbb3a04aaf494ccfebdc168cd97976d565f49acd33a206)
            check_type(argname="argument hotword_regex", value=hotword_regex, expected_type=type_hints["hotword_regex"])
            check_type(argname="argument likelihood_adjustment", value=likelihood_adjustment, expected_type=type_hints["likelihood_adjustment"])
            check_type(argname="argument proximity", value=proximity, expected_type=type_hints["proximity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hotword_regex": hotword_regex,
            "likelihood_adjustment": likelihood_adjustment,
            "proximity": proximity,
        }

    @builtins.property
    def hotword_regex(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex":
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_regex DataLossPreventionInspectTemplate#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        assert result is not None, "Required property 'hotword_regex' is missing"
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex", result)

    @builtins.property
    def likelihood_adjustment(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment":
        '''likelihood_adjustment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#likelihood_adjustment DataLossPreventionInspectTemplate#likelihood_adjustment}
        '''
        result = self._values.get("likelihood_adjustment")
        assert result is not None, "Required property 'likelihood_adjustment' is missing"
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment", result)

    @builtins.property
    def proximity(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity":
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#proximity DataLossPreventionInspectTemplate#proximity}
        '''
        result = self._values.get("proximity")
        assert result is not None, "Required property 'proximity' is missing"
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e97d0c4e64cddce4ad0dd8a30469462e1b9ed95e37142e970e9c375a4851d9)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument group_indexes", value=group_indexes, expected_type=type_hints["group_indexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }
        if group_indexes is not None:
            self._values["group_indexes"] = group_indexes

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified,
        the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__015059fcd5ec63c3e18ab7a6c7f53007b53b0f88fd3c54207b9fbbce6bb4fcc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupIndexes")
    def reset_group_indexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupIndexes", []))

    @builtins.property
    @jsii.member(jsii_name="groupIndexesInput")
    def group_indexes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "groupIndexesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIndexes")
    def group_indexes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "groupIndexes"))

    @group_indexes.setter
    def group_indexes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8285eee697ad809a5cc748d1699f0fc5a133f041d1415ca3fbd99ef47d34880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6410512f7766e7e3d09f80f83374e9b17576d5983374fc2eb093a4c85d1ba318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615521a4799e6c3d5c771d64f5e50fcb9dc3f79365ef1ebdf886cef039a15e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_likelihood": "fixedLikelihood",
        "relative_likelihood": "relativeLikelihood",
    },
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment:
    def __init__(
        self,
        *,
        fixed_likelihood: typing.Optional[builtins.str] = None,
        relative_likelihood: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#fixed_likelihood DataLossPreventionInspectTemplate#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#relative_likelihood DataLossPreventionInspectTemplate#relative_likelihood}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0b3556e8297f50ddcfeb7ba60de332d0a98f3ae456d008685e37f5f39732ad)
            check_type(argname="argument fixed_likelihood", value=fixed_likelihood, expected_type=type_hints["fixed_likelihood"])
            check_type(argname="argument relative_likelihood", value=relative_likelihood, expected_type=type_hints["relative_likelihood"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed_likelihood is not None:
            self._values["fixed_likelihood"] = fixed_likelihood
        if relative_likelihood is not None:
            self._values["relative_likelihood"] = relative_likelihood

    @builtins.property
    def fixed_likelihood(self) -> typing.Optional[builtins.str]:
        '''Set the likelihood of a finding to a fixed value.

        Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#fixed_likelihood DataLossPreventionInspectTemplate#fixed_likelihood}
        '''
        result = self._values.get("fixed_likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relative_likelihood(self) -> typing.Optional[jsii.Number]:
        '''Increase or decrease the likelihood by the specified number of levels.

        For example,
        if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1,
        then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY.
        Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an
        adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY
        will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#relative_likelihood DataLossPreventionInspectTemplate#relative_likelihood}
        '''
        result = self._values.get("relative_likelihood")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__510dfea293c60d9482a5dfb214e198236201849b0cc4f6356b3f0291efb15a2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixedLikelihood")
    def reset_fixed_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedLikelihood", []))

    @jsii.member(jsii_name="resetRelativeLikelihood")
    def reset_relative_likelihood(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelativeLikelihood", []))

    @builtins.property
    @jsii.member(jsii_name="fixedLikelihoodInput")
    def fixed_likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeLikelihoodInput")
    def relative_likelihood_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "relativeLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedLikelihood")
    def fixed_likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedLikelihood"))

    @fixed_likelihood.setter
    def fixed_likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb3729cfc5c736b521c6945f3da80fb4fda1891a072648751c32ae6b93d2b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeLikelihood")
    def relative_likelihood(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "relativeLikelihood"))

    @relative_likelihood.setter
    def relative_likelihood(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706ae74182882511516723138af3696f0dcc1607cb5f47de480fd58ac376508d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3d4ee14738ac453d0921f7d3975c8c18fdb4a47e36a945454f33449f4c8832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__146db9609811b079fe13c9a8d8efd0e6e49a6dc119fc24cf0bd50fd4ad57990a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHotwordRegex")
    def put_hotword_regex(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#pattern DataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#group_indexes DataLossPreventionInspectTemplate#group_indexes}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putHotwordRegex", [value]))

    @jsii.member(jsii_name="putLikelihoodAdjustment")
    def put_likelihood_adjustment(
        self,
        *,
        fixed_likelihood: typing.Optional[builtins.str] = None,
        relative_likelihood: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#fixed_likelihood DataLossPreventionInspectTemplate#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#relative_likelihood DataLossPreventionInspectTemplate#relative_likelihood}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(
            fixed_likelihood=fixed_likelihood, relative_likelihood=relative_likelihood
        )

        return typing.cast(None, jsii.invoke(self, "putLikelihoodAdjustment", [value]))

    @jsii.member(jsii_name="putProximity")
    def put_proximity(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_after DataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_before DataLossPreventionInspectTemplate#window_before}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity(
            window_after=window_after, window_before=window_before
        )

        return typing.cast(None, jsii.invoke(self, "putProximity", [value]))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegex")
    def hotword_regex(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustment")
    def likelihood_adjustment(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference, jsii.get(self, "likelihoodAdjustment"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference":
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustmentInput")
    def likelihood_adjustment_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "likelihoodAdjustmentInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity"]:
        return typing.cast(typing.Optional["DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1485c1ada54090d64c75d2d7de7a1cad38ce1bfcc1f6b3ea51b6fd292a5777c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_after DataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_before DataLossPreventionInspectTemplate#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d481d3b2a51bdf294317f1608c37d999160adf3950fdaee8724355321dc03a72)
            check_type(argname="argument window_after", value=window_after, expected_type=type_hints["window_after"])
            check_type(argname="argument window_before", value=window_before, expected_type=type_hints["window_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if window_after is not None:
            self._values["window_after"] = window_after
        if window_before is not None:
            self._values["window_before"] = window_before

    @builtins.property
    def window_after(self) -> typing.Optional[jsii.Number]:
        '''Number of characters after the finding to consider. Either this or window_before must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_after DataLossPreventionInspectTemplate#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider. Either this or window_after must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#window_before DataLossPreventionInspectTemplate#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__281c873e7e7ada34b49128530c9c2347d969afadf6264d67daaf4f64eb69003f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWindowAfter")
    def reset_window_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowAfter", []))

    @jsii.member(jsii_name="resetWindowBefore")
    def reset_window_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowBefore", []))

    @builtins.property
    @jsii.member(jsii_name="windowAfterInput")
    def window_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="windowBeforeInput")
    def window_before_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "windowBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowAfter")
    def window_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowAfter"))

    @window_after.setter
    def window_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc8400052407de28548088a470679818738682ec3ab8692690a2278ef12e4e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bcd79e5662e6312163f90177513f221b1d7394d374c17f8d136ec0a4aefbb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3f68594df3a27bfc97d69be64d1d8bda2952feb9ef6fdeeb689196e689ca03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__103389ff987dee163d228169428e07d820a4121912d9dd2400f41adcd11d2190)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67be153bbac1736d95f55f7fb4d5695616a7b00713788912e8991e589173ba3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281651188aea017c0d87c46df8556490376cb08eaec68fb1bb8667d84b69bf7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57dd84ecafde223420ffaeb3e86ef7c77c84331ab44a0cad318c36d161d2e7c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb49a33193cf6e5e1a429c3a3ce936869f6310ef6718b3f1a7a6f8ec13aa4fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c398adc945a18df7ca8d30329a86ea39fa92182c9de590c79878c977717fffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c6163fe5d2649d113d427632cc52179c30493aefc12f051f70de4e1c66c4d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExclusionRule")
    def put_exclusion_rule(
        self,
        *,
        matching_type: builtins.str,
        dictionary: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#matching_type DataLossPreventionInspectTemplate#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#dictionary DataLossPreventionInspectTemplate#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_by_hotword DataLossPreventionInspectTemplate#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#exclude_info_types DataLossPreventionInspectTemplate#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#regex DataLossPreventionInspectTemplate#regex}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule(
            matching_type=matching_type,
            dictionary=dictionary,
            exclude_by_hotword=exclude_by_hotword,
            exclude_info_types=exclude_info_types,
            regex=regex,
        )

        return typing.cast(None, jsii.invoke(self, "putExclusionRule", [value]))

    @jsii.member(jsii_name="putHotwordRule")
    def put_hotword_rule(
        self,
        *,
        hotword_regex: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]],
        likelihood_adjustment: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#hotword_regex DataLossPreventionInspectTemplate#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#likelihood_adjustment DataLossPreventionInspectTemplate#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#proximity DataLossPreventionInspectTemplate#proximity}
        '''
        value = DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule(
            hotword_regex=hotword_regex,
            likelihood_adjustment=likelihood_adjustment,
            proximity=proximity,
        )

        return typing.cast(None, jsii.invoke(self, "putHotwordRule", [value]))

    @jsii.member(jsii_name="resetExclusionRule")
    def reset_exclusion_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionRule", []))

    @jsii.member(jsii_name="resetHotwordRule")
    def reset_hotword_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotwordRule", []))

    @builtins.property
    @jsii.member(jsii_name="exclusionRule")
    def exclusion_rule(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference, jsii.get(self, "exclusionRule"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRule")
    def hotword_rule(
        self,
    ) -> DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference:
        return typing.cast(DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference, jsii.get(self, "hotwordRule"))

    @builtins.property
    @jsii.member(jsii_name="exclusionRuleInput")
    def exclusion_rule_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "exclusionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRuleInput")
    def hotword_rule_input(
        self,
    ) -> typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "hotwordRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e41ccda1770722cb6761a5cf5400950b61e150ca0392e825fc5f78ff72c6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataLossPreventionInspectTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#create DataLossPreventionInspectTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#delete DataLossPreventionInspectTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#update DataLossPreventionInspectTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11bd95d1b00ce1e94d41ec6f50062e56599e50e30397f4f2ba62dacfcb505c64)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#create DataLossPreventionInspectTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#delete DataLossPreventionInspectTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_loss_prevention_inspect_template#update DataLossPreventionInspectTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionInspectTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionInspectTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionInspectTemplate.DataLossPreventionInspectTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3cbbd9ba28f574763adbf0ff08c643d82361431a1eb64342247b27bad00fda7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b4f389d708bb5a89e81a312039d762ef89aa17ad18f9fcf08506ae7ad18a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ea6c5d869df30d696b554037482bcd21887dede47864692355b9b1c8a53631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a936f1db07a4b3eae65cbd2f39cf6e3611d69881346ad41f3d6b04bc401a287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2368bff4d13cd126763f1859a3cda2cae8f94a742e1847d832a8c2a085f6b43b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataLossPreventionInspectTemplate",
    "DataLossPreventionInspectTemplateConfig",
    "DataLossPreventionInspectTemplateInspectConfig",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType",
    "DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigInfoTypes",
    "DataLossPreventionInspectTemplateInspectConfigInfoTypesList",
    "DataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore",
    "DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigLimits",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList",
    "DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigLimitsOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSet",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetList",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRules",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesList",
    "DataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference",
    "DataLossPreventionInspectTemplateTimeouts",
    "DataLossPreventionInspectTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__751ed60c3e9ac8e49c9da913a65e1d35c09c6efd7fe224c27bea2150814830d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_config: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionInspectTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8be4af62e01a4b1da212e2dac58d60348d0e9cc851b2bf89725f841e938b1c78(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee925ae3a84fae597ced7e6cf2422e862ef2ec2999b1e71230c384d3aae3738a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569e4dbd9407f86227fae11f18034fb29b50e5c0ae84e80a837f5fe3035fd76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2430f3e6f32555e1bf6f5216c33495b5e6fde7d590e11571dd2c2f43079be142(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5775c405d973f7a7e68b31d960091a3629e94920bd975754747ee8ad27b8566f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc927da5c2ca8af1f187e90b286fd8059b5deb33c0abb3dc5e54752ac9e7c763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0732dffe09d5e0da3e53b60a9bcfb998f072502fcdb7c0ce7e70460d17f122ca(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_config: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionInspectTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb4c8d20e9e330261aaa3d87ea40faae6a9dc9b248eef125d712ffb84fb6900(
    *,
    content_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    limits: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    min_likelihood: typing.Optional[builtins.str] = None,
    rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd362e303e4f2e50e05e2f8964036c23bebf1db4b0cd2b3fff5b6dfbe279198(
    *,
    info_type: typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType, typing.Dict[builtins.str, typing.Any]],
    dictionary: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusion_type: typing.Optional[builtins.str] = None,
    likelihood: typing.Optional[builtins.str] = None,
    regex: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_type: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType, typing.Dict[builtins.str, typing.Any]]] = None,
    surrogate_type: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f34ead5e92a6388a7aedd41e6a7d10f33556dd5a72364edfbcf4b9c2254c86c(
    *,
    cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5437d424aa35ead230a753e46ee734de1a4ad1c4cf3d3a2de51ae04a08bf202f(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6197acd6b38feb38c510bb6bb0fc4a89ecb8cfad6cc81649a4c6df3d12570285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f606ad8ff0a5c74f7d76feb03a16a0af3ec5c33a64ab94c8da0d86fc5a6b5fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ec6e021b82c80ccbce2481d232860f658cb8b4718e8b8a70f22857c2254da6(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe634d4b9560ff1a9744a6c31a6850421b51c0cfd66efc96a250e4205d6f57c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9111c17ca5fa79a524c06482a5d839b7a5350bcb02966ccd647c75afba12eff(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1d607b6bbb89c31a8f5f2d1333784901c23ece3a4ee23243f1045015e5b089(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed70d7fe4184c402c9f284b59a54b7b801c7ca998f04c42df0fab359f1f78491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02bd0f58dd59bd5599be4bb4ef12d222edf77575664192e9d7632a40855f074(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4386a49cba662cec566cb86607cb2525d614095f5540cc3a9b5cb3bb940400be(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f90572a4396be9bc60dc605de66cf543c4f1931cc6baadc77dd24188ecb9fb1(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7be892e7947e793876f8236f7929ad46d6e6eb9df9a139a8c8c55c2ba0044d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e76fbb98ed58e96ce4706a7bd84b7159df9053d242aedfa760483e97299f7c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ae12efb4e51d07fa7ee4e65e892fd4f0e991ff00328707bb4b64bbd284b0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886cfb74a1d5398b5bbce9e8db3a7cf00003a6610ca7fb49e19ad57fbd51fce9(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ec1de685ba2325bce2264342c6b5c01ec524133fd8a3b3184d7f60b2de844e(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1549beffd4f9b7ea9e737c6b3e138ccfe4202342be595fb99a43f43c6dc44d4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61be8b573f3c62071e446518372c051cf9906b2ee94ea40d58aeec5f3b359a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e3aa803e578cd32e70054c72ecf6bea2a3462aa697401a57496df298bbab36(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe617e3a10aa530e169b285355280f7158714684425c3c8c93b2b42f7e4626f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89928cb95dc5c70a8a2ac0b4103f652611f3fe451bbbbc5d00010260a0adf43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d99821ff9bdc697745fae65d9155474d65aaf643047c9a7d8cd6347b28216b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6abb09b195bb5c462720e2e12298219cf5451fa307235c5b6ede3c28e2802c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea257899793b6c13410966bf1d44f72c6cfc44ccd0705ef3e19b0ab2da53345(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fc7e44f168ed2cb882bdf2a6fb92db4a8c16e045a4c85e38aa797670362244(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d7c6fd297f1446a4aac143b639574c72a8836714cb38385027fb1472b5549b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b309b15f56fae23d9b0360e570bf4140a0afbb70b5c4b630a5da071b0bfedc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca607fc55859d54eeba1c4581a9d4a7f5bd054a42289026c4a74238ce07f9543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd75626fde2ce954327ac2ef2bbf2090281e47c4ddc9cfc1d7c51aa1fec2c469(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e19a466fd1a4fa735cd181f948c29583e1ae97e0fdaeac27a188b56604a2915(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf02f9d516402c16dd86f04f4827187cce688594a6ee64b83fa865d3e9004fac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2315463eb11f976c80f18214262cdffc2c86cfcc1f8b71bd1d8b18f216790085(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52ed54bfb97f1bda5b90b97be2f2cf20e2fd6316a2f9b2331efc0028f590493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e785e1b833166806e446c977d110fb630bf60441adde1100cbffb6b76919042(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feef2d5fd85ce590a807622b28fbdb11190e35998bd944d38f326c2faaadca2a(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a941ff7deb7292f13dfc3227c9d96361529bb3c8c433f29fd314aec90219ed6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfba6dc7e141cf8b49cec68ed204007e2a6ac425204917ddb27f70998cb49e1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855e0acc96c860b1642baa1e99606ff3cdaef3f83825285b60ddfe9671817452(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6563230bd397cd17b23b33d06951531f3ae20bf547a5cb125526d283123d4fd7(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083da1a92d4f86fae012c6e33e6cd51bd7c4430bba94abed3624203045b59c92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80b95dd0dc686fee4f9b413d4f513400aafb8f82c808d4098c4767fbddd3e50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210071e6c66c5d6be2c477b1c9afe0643ad962feb2ff2f44b70307a7406ec579(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23308d81e6945289cbb2eba13c316c85dffd1a46e9f4b424904196e1359f0b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25535478118e2997682651f90d97c17cb477f32f2654eae7932ae88ac7b809b(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6de9ca845e02e665b686cad8b559aef1357b86814d9cde9c6e4617433dd440(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d39f0bc2700c5b47037bf493030eb1b57f9203e7feffdc879eceb724d15273c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6b4df471954e5ee7f0d6345395f4532de614f51eed66f85696c70edd1adfd1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54552fbeb66f2e49a05777e2cbcd5f893edcd8cf618267e6f7299b2360d992c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a085c6bcbf0b3e0959760bc707633aef4acf5cf934e0b322bce08875b972a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431b7eabf86f8f2ca59a2ab192c720325b189ef777a7fbf0fd91ab162c4c13e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a6e8895bed1a3c8e481d440b5a3e768e1957cd7ba775ab6950f6fdaa207a53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef07639fd3a8a22ccbb74e4af04b7691bf29220de2b44eedde4dba949b057467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07ae06c0ca6b3b8d6df6d5f70256be57e8352b70e0cdd471ad3a863a01fcd69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012803d387bf612d8b74b803a098ce84d19d3182204e033aced6d6f2a7ae79fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fdb1b3e2fb1598167dcd8ab4bb3426545e589989d63104e2837661b20baeac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7a34bb4d756deb822adbf9a9ace99bdd32ac6ecde96dc2f2b8d98d2c252c29(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b7ef1b73d3fed8c92b18d8997c0c91f0bd0d627d295cb204e9e3f8766d53ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283864c5c4ec7e42930b047fcead7df778e7d29d0beac218694aaf0fa4ef90d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f51b9460a17edb4a58a9f9baac947f7958299b316e1b41f80cb7d9ad2753dca(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97262d7f266f5295e7210223be4bcd05bd383b801598ef57085b8a843ed3134(
    *,
    max_findings_per_item: jsii.Number,
    max_findings_per_request: jsii.Number,
    max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb03f37ae83c1346daeb27b5cc53561923e26b18c997071bed8da108116ceb78(
    *,
    max_findings: jsii.Number,
    info_type: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393836c3e6da221ed789d99af87badca0e378032e350ca6a7f0a43248ad5afb3(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840c8d6b591cc943465c6f9a756bdb3848c30674a8291ef9454604ef848fd68b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c611f79d295d68840b5dcbcdb412070c540c53d900195dcecb1acdc44103eeb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad059969b308816af315aaf838b2c02c5d0f57caa26317cfeb39721ab69ca15f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5a30583fc833651d65fe8207a19b48c398a209de8cf50c53302a66cf8bf96f(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b463934e7c7d26b9ff9f554e4f3b238bbd86c648cdee32c9f2ba860d8c7232(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bfaeebd44c18e4ce6960ccf544d712cb76fdf98e64f3591dff9cd6f4ae8a7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ab4de7aeb407a8331e05f414603bcb02bf84bd2071d031d718212140ecb8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3a186ed7da4f63942e36e44ec5bb1747e915f2f2355708ba77cfbf9caa476e(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef413e1adcd5d8e3a9f03e6e57fe72495f9f205a69c5b690ab961a9d9670226f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbd88fea70929901761b2c25266c36847d45d6452059a97fc7cd9362b40eb88(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb7c23cd3fefe853ae30497e0e185605cddf3807e27798a0669474fb7d9c8d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65fb9e4e9862d907cf04d36a34b801456eec4b2bea1b4099a3d245a7a1acd52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5d3e892eb26dddbce5c05b5e49a06fdab78604027653a8e941ddf9317d6129(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7573ae9ca2c8d53868396cb389b50944ce5e9fa568d74cb5aca77b0e2263effc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77388454b6300e60a350ca904be348f1f5af23f626ae0814003a614e42cc7886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc57ac7f833fc5adea71557bf235b5aa4ea1c26cf529b5783e2de7cf56ab8ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa1bf2fecef896793f6aebd4ccefa9c30e322bfe45458f52fac1c9d1b12360b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c2e5582a939951f5408f5414d87918dcad1bb30b96f94c1d7106851a988b33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7db3c0606e036c1bfe59b0215aca20340fb7b8dbc77a7f2b66d316239d223fb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207dbbfd9a1ad0b77869d3f8935d918a06e8d4cad8ad798e0b109a30d7458b43(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55506b12db831b04778321ba5eeefaa1366aa3c554fe52ca4a5a271b188cff4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb96488fcf94b9c5f6e8f56e16e09b125c3eeb0391d553a98e16d5478adfd63(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac60f1f2a3499af4f0ec026dd0506daab8affd8747835a287ef447675da4113(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff7a07b83cba348df0566be3beb2826e7327ac64fd9253049c7f74a637d40af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed48f75ac469f26ee93f49c6c82c55a008efb39be6a83c4f06b35b14ba086df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c29291caae51a9786fc444e7d2a066dca305ab85bcf3da1aca0cb01713add91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c92a02c662aff1e58a1fd8208daf90d264ccd43db1af7f1398da2e68af39f94(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02184d0b8c60b4ef53d4e8ef36b1d6b168ef72869fdba2d10f5a81f6a5227b07(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e023e5296907452d03b35b324fa88f759830d2260753063bc4e5341c810dbdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c008e8e9f3f5efa30eb4ffe3a02e2fc82fa4ba495ccfd41f143974e0b9511c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe962f45fb29c0a67b4f2d99d8a487e91a4f28da01698448cfc342a1d545ef3(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d82d4ae97d18774a4f9ef8ceb59ce492167923f668d5692936b2748b0bbef08(
    *,
    info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc05fe18cdf80783f1b30226988861d42648c743944651570548219087d0a3a(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bef1f719935c2214e2a9cac7c6c89a0532d9af0a3ec309d5308df05109471e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac13b64a3e968ceb6cc413b1dbb44bde2e07866d16d8a84341ec7393b571a07(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e574930ec7d86fc2fad395df026e04e9ff4969a3977f9617b6721045c0df0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28019df9c7ef1b7da50fd118d9bf597f8c04a3bca552b224934782bc1acb57f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b54e67a3c76bfafa3c9dab19e0a5c15fd58caaec03ed1e77d4da9a6da67acb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db45877870f0c0bed756b866808a4a8c9f2cc3507334f76a7c724870dcd085b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de83aafbe238cd0494ee901440b819a704628f4d3c70e318a25e46aed695256(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63cabcce03b76f11cf6a12f6b1b1ba74f80c79d172f626cf92f29b4101eba3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28600656c416f6dff013d86cb4a24192831faaed4857d389fa57476e5476ff81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a492854e20b5027118dbecb7b11f91286d660c6dc190c2a62aff57823671b839(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085ab96bd5abd38ae6220e8a736b7886d8da0fdc56085a1c34efe6351d6b43af(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a15d0f6708ad23d3dd31080979073cc10e7bfa9c59f766ebb26af79faa21b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25601e9e0d159bc5b8fccf1900c66c9b5738fbb07b2722cb81c9f10847828285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61a1b72a94561f2f94bf3346af6a4ad305af14a9152094918a2ad71e8fde081(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1998c397cd33130a87b0ad3491e4aef5eb78cc89d11a29a1c4141cf301b3507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1cc8a0fb1b39080465bb0c76ee371eeadc46d8f53ee807b41600ed715ee3250(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6518fe5c5464f708e2f1ef351a612c55de795a9cb59a5561b9d1e00df75de6a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467c764289ca70e5b34bc9bd02dff7583bccc4d871125b582b08b95d741b2b6e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f04f5c5f088ee5129c71c6cec7a048bc554c95ec1de563ca1a086aea67947d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb2f940ab5933131e917b35c3e45551f23b7d48055c9dd5e6a630af6bfb5b2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ebdf30ecb888c30f8f075099ceebc5d63b229aff0dfecc20b81de084523c6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657bfd58595fa46b2f5676a5a2692c711b2869e7eb6b92024e9df516a02a305e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae320c1cbcbe57547c0ae85d544db004967c19c8cb31197160b7f2f2474fe6bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d2453ab37d0f5bd76441873bd15bfe48c572c1cdc5357463d553ecf3095471(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed259ceb3f2c24aaa688a6d6c1bf5fb2ab2572685e0c8f557f93b8e1ddb94a4(
    *,
    exclusion_rule: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule, typing.Dict[builtins.str, typing.Any]]] = None,
    hotword_rule: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a4a8abfbbfe235984751cb1df4e06bc44f8d4464c3014592d880c7c1fda869(
    *,
    matching_type: builtins.str,
    dictionary: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_by_hotword: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_info_types: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499e40b513fcdb092d85a847585efd2e3474493a04f9547f020049e21e4d9338(
    *,
    cloud_storage_path: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04bc359a7773af0202a7cc8bafbbee297265a3e328aa1215fa8f4e47e73dc3f(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311fea9a69c0cfc0b5a5157a50d8c654535010fef34e7bed4e0997f1a8e8623e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3094b44160633e4cbc7c42d8d47e6a6b75747c519d3ed2a1de6dda8220e5513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0274f9381ece508aef7dbdc01b590f730237cf10f652ad9d611a5b4ebf9466a6(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78ad3d8f2bca513520909cddadb36a4da889a61ded97ae149574e202fe400e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e784aa5203b8a262207021fcd2bc60ee22df6310d7144937a95ceae9c95852(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a75eeacd25a7c986597b4211a04b1e2ccd4f88fc8845964b5a0c121610bc648(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208972778dd14d28227d8f5ae04af40c320156bc31611d39c101eeacbcbe1399(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccaed0f6d88661673dd9b21878a8c0311db27a0c708f6a750384146f2b84eeea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d87055d39a010b22d2999fd97b6a421463fc8f212f63aa37999fc1b67961d91(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bc715ab0e31bd10954d8df09f0806eff4cd9f81209893703a9a1594ad78173(
    *,
    hotword_regex: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]],
    proximity: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398b33a52a65c13850d746f7a1659eef1fe401aa4214406a1081d0e15a7ad436(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e487e17834a1f715eeef3fd371c3b064ade21c07eb7cdcfd2f22df3df02b37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bea6946f5de9ae0c10cb2518bc3a4840d8d6dc6fbc6b64bf897081e8b900d6(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163f0c60604145b51de2b11dd5b954e6e73074a0d87fd716f24a3a9443964c4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7c4bc439cb033c0112e8ea2adb0c5a8cec46230ce00fb5166c7c76686213f0(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bca36e530588358b00ab45c52f7ff3565de9032dc87b270a978ebae01a4afb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a592c488b49e4f2432d3c8b896e206f5599f2f3efe68b83314e2e6b046797f(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f306ea74c4bedf4880aa5ebc1638db706296e6cdbca7d9e97d21429580440b(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ecb2fa01782c94efffa22e0bfa60df1e47834d2724eb024a3ca5b122899bf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02828e9798a0f09078117a08abc7f47059d0e90c169e56db58e6a45ac1c5eb2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf0887d45804ed2c5b39a9b2ee973bc88301d903f7f7f7c6169cafbc03c36a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a9ff0287a0a07c37156e392aaf18ba9e6c81fb7e39ef0b307db5d6448087ba(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eea1f4c158818d6adcf8bc9084720a8b79cbe9c1b9aa8e2359a0a2e6653458e(
    *,
    info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca9c1cbd205a4e5d27a91f4f755ba5abe75dcdb02847fbd284b1fe71994e3bc(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abc63f8c814620d93c7c629862cdcf5ce0bfcb26faf18f4c608af60cf428ca6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2834a2a6f2ad6965ba4624033af37ea34f01627ea49d60c3524b9dfdd1b2c7f8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ba6da80be58fb905cb0cf928a37bc3331dfb771f096c7263ce2fe003d1de2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd93988a7d7fcc2205f77a5a20681754b75fdb47c15a364125f50ede92f18eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324665677272191a373e6d90d41f84183807f181043199741d9119852077027f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0022e96fdef86cd086faa5a982f440f799eec30716b51867c25905642bb473ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ab814a6e7fac7ac1f0e5a97d1cc57970439740a68a9fc4f33b7cbf35ee49b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee05558cf12912b913581c4de9084fec4865ae6cfd829bf26446f46d9a22d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ac818cd63c04d4d065573bd567eb18a16170c11596c02848d7870b50c8c575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17cbcc36812567205dcb13cb1182efcd7b88fb164092ed6c744724e1089d1a73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da6c1e6d7c5a86c7cb6682654243e6b68e7ab3cd6165a84c8d84d162924d168(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61d1ce569927f4a96768ec883a44bad287b4b270c5124ad743837ee8a7ac294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f01a9e91ef4f36a3ce8b604d08a565fc83e5197633013f2917c492156ca0732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5750e0b750a48cd7651b1bce0c33803d3e3d731c6b42ce98f30c63472a60f740(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e771c09aef6ef4dcf8bd92430a3925acca1e72b60a8e10bf88eeeebed893a062(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4b73fd73919879ea9a5d11c15fd035e04acc11ada309c72e7b7c9eeb829c61(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e217a6cbfd7d81342924c72a6e23e354b6437d26986dc9debc6600778adf0af(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87097870f553831681464d74f3698a3593ac6d9d72c53e664ba0928df496241(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a4363b4939b8e582a518ecda9e5ba85a4dd9e1411992eb56256dc98dbb9161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f8dab11ececc83a3b520d40031547feedc69343ead0ee386f231b299386389(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889493a2bd31552349a16a8a08d6558efef5e4fa0a1cc659f69b0d9599a408a9(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004e596c6b985979339cabc72c39d394cf1afa7f41771a2706eb21378579a118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7ca089a8f454f31364f09b128b273d957ed6880ddd9d4b349766805b20ffb2(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7119d951d90e7c7c09e49dbd249e3ee3a821d69e760ed221959c67978c3acd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e855d75aa8139b78c81794c7346b3a6597288a2b32ec8982f170530d09b97d0b(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11473eb59a7785ac7acbb3a04aaf494ccfebdc168cd97976d565f49acd33a206(
    *,
    hotword_regex: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]],
    likelihood_adjustment: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]],
    proximity: typing.Union[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e97d0c4e64cddce4ad0dd8a30469462e1b9ed95e37142e970e9c375a4851d9(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015059fcd5ec63c3e18ab7a6c7f53007b53b0f88fd3c54207b9fbbce6bb4fcc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8285eee697ad809a5cc748d1699f0fc5a133f041d1415ca3fbd99ef47d34880(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6410512f7766e7e3d09f80f83374e9b17576d5983374fc2eb093a4c85d1ba318(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615521a4799e6c3d5c771d64f5e50fcb9dc3f79365ef1ebdf886cef039a15e29(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0b3556e8297f50ddcfeb7ba60de332d0a98f3ae456d008685e37f5f39732ad(
    *,
    fixed_likelihood: typing.Optional[builtins.str] = None,
    relative_likelihood: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510dfea293c60d9482a5dfb214e198236201849b0cc4f6356b3f0291efb15a2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb3729cfc5c736b521c6945f3da80fb4fda1891a072648751c32ae6b93d2b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706ae74182882511516723138af3696f0dcc1607cb5f47de480fd58ac376508d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3d4ee14738ac453d0921f7d3975c8c18fdb4a47e36a945454f33449f4c8832(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146db9609811b079fe13c9a8d8efd0e6e49a6dc119fc24cf0bd50fd4ad57990a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1485c1ada54090d64c75d2d7de7a1cad38ce1bfcc1f6b3ea51b6fd292a5777c8(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d481d3b2a51bdf294317f1608c37d999160adf3950fdaee8724355321dc03a72(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281c873e7e7ada34b49128530c9c2347d969afadf6264d67daaf4f64eb69003f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc8400052407de28548088a470679818738682ec3ab8692690a2278ef12e4e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bcd79e5662e6312163f90177513f221b1d7394d374c17f8d136ec0a4aefbb7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3f68594df3a27bfc97d69be64d1d8bda2952feb9ef6fdeeb689196e689ca03(
    value: typing.Optional[DataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103389ff987dee163d228169428e07d820a4121912d9dd2400f41adcd11d2190(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67be153bbac1736d95f55f7fb4d5695616a7b00713788912e8991e589173ba3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281651188aea017c0d87c46df8556490376cb08eaec68fb1bb8667d84b69bf7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57dd84ecafde223420ffaeb3e86ef7c77c84331ab44a0cad318c36d161d2e7c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb49a33193cf6e5e1a429c3a3ce936869f6310ef6718b3f1a7a6f8ec13aa4fcd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c398adc945a18df7ca8d30329a86ea39fa92182c9de590c79878c977717fffa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionInspectTemplateInspectConfigRuleSetRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c6163fe5d2649d113d427632cc52179c30493aefc12f051f70de4e1c66c4d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e41ccda1770722cb6761a5cf5400950b61e150ca0392e825fc5f78ff72c6e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateInspectConfigRuleSetRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bd95d1b00ce1e94d41ec6f50062e56599e50e30397f4f2ba62dacfcb505c64(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cbbd9ba28f574763adbf0ff08c643d82361431a1eb64342247b27bad00fda7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b4f389d708bb5a89e81a312039d762ef89aa17ad18f9fcf08506ae7ad18a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ea6c5d869df30d696b554037482bcd21887dede47864692355b9b1c8a53631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a936f1db07a4b3eae65cbd2f39cf6e3611d69881346ad41f3d6b04bc401a287(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2368bff4d13cd126763f1859a3cda2cae8f94a742e1847d832a8c2a085f6b43b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionInspectTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
