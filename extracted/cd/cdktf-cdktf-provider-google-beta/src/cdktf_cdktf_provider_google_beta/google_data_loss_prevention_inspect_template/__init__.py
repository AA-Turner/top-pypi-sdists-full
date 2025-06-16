r'''
# `google_data_loss_prevention_inspect_template`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_inspect_template`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template).
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


class GoogleDataLossPreventionInspectTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template google_data_loss_prevention_inspect_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_config: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template google_data_loss_prevention_inspect_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param parent: The parent of the inspect template in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#parent GoogleDataLossPreventionInspectTemplate#parent}
        :param description: A description of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#description GoogleDataLossPreventionInspectTemplate#description}
        :param display_name: User set display name of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#display_name GoogleDataLossPreventionInspectTemplate#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#id GoogleDataLossPreventionInspectTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#inspect_config GoogleDataLossPreventionInspectTemplate#inspect_config}
        :param template_id: The template id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#template_id GoogleDataLossPreventionInspectTemplate#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#timeouts GoogleDataLossPreventionInspectTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f103ff1da08637f8d6abc72f77463ec9bdbe67f5e109e8d39056406159a47ea8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataLossPreventionInspectTemplateConfig(
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
        '''Generates CDKTF code for importing a GoogleDataLossPreventionInspectTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataLossPreventionInspectTemplate to import.
        :param import_from_id: The id of the existing GoogleDataLossPreventionInspectTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataLossPreventionInspectTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79da7c3860b6a60bbfb3f096f310fd2739d0c21b1cebbdf417d1500184ec24aa)
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
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param content_options: List of options defining data content to scan. If empty, text, images, and other content will be included. Possible values: ["CONTENT_TEXT", "CONTENT_IMAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#content_options GoogleDataLossPreventionInspectTemplate#content_options}
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#custom_info_types GoogleDataLossPreventionInspectTemplate#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_info_types GoogleDataLossPreventionInspectTemplate#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#include_quote GoogleDataLossPreventionInspectTemplate#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#limits GoogleDataLossPreventionInspectTemplate#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#min_likelihood GoogleDataLossPreventionInspectTemplate#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#rule_set GoogleDataLossPreventionInspectTemplate#rule_set}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#create GoogleDataLossPreventionInspectTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#delete GoogleDataLossPreventionInspectTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#update GoogleDataLossPreventionInspectTemplate#update}.
        '''
        value = GoogleDataLossPreventionInspectTemplateTimeouts(
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigOutputReference", jsii.get(self, "inspectConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateTimeoutsOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfig"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfig"], jsii.get(self, "inspectConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionInspectTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataLossPreventionInspectTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e034cd9368bd1b9bd7e3a0236694a1a57b923826e8a1635a73e23678da1af57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04db4281e862d05f52816629fd234c67a00782feecc15ab41ba465330190a6b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb748014957aa2b65a4131b30f67417a49ff5dfa80bb208b1c1affceec22c05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a176a5358f5f1ea9eca2f3359b571501257e73c88912881851518e2cd969be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98362cce9d1c1c21b14f59a81373318bc70a1fad52f6efb7cdce865cc171cd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateConfig",
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
class GoogleDataLossPreventionInspectTemplateConfig(
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
        parent: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_config: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param parent: The parent of the inspect template in any of the following formats:. - 'projects/{{project}}' - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#parent GoogleDataLossPreventionInspectTemplate#parent}
        :param description: A description of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#description GoogleDataLossPreventionInspectTemplate#description}
        :param display_name: User set display name of the inspect template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#display_name GoogleDataLossPreventionInspectTemplate#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#id GoogleDataLossPreventionInspectTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_config: inspect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#inspect_config GoogleDataLossPreventionInspectTemplate#inspect_config}
        :param template_id: The template id can contain uppercase and lowercase letters, numbers, and hyphens; that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is 100 characters. Can be empty to allow the system to generate one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#template_id GoogleDataLossPreventionInspectTemplate#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#timeouts GoogleDataLossPreventionInspectTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inspect_config, dict):
            inspect_config = GoogleDataLossPreventionInspectTemplateInspectConfig(**inspect_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataLossPreventionInspectTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde1ba894bdafec5d7af05c5048d8e78a5a63d88d2117910f1920e01cc1815b8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#parent GoogleDataLossPreventionInspectTemplate#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the inspect template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#description GoogleDataLossPreventionInspectTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User set display name of the inspect template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#display_name GoogleDataLossPreventionInspectTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#id GoogleDataLossPreventionInspectTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_config(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfig"]:
        '''inspect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#inspect_config GoogleDataLossPreventionInspectTemplate#inspect_config}
        '''
        result = self._values.get("inspect_config")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfig"], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''The template id can contain uppercase and lowercase letters, numbers, and hyphens;

        that is, it must match the regular expression: [a-zA-Z\\d-_]+. The maximum length is
        100 characters. Can be empty to allow the system to generate one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#template_id GoogleDataLossPreventionInspectTemplate#template_id}
        '''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#timeouts GoogleDataLossPreventionInspectTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfig",
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
class GoogleDataLossPreventionInspectTemplateInspectConfig:
    def __init__(
        self,
        *,
        content_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        limits: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        min_likelihood: typing.Optional[builtins.str] = None,
        rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param content_options: List of options defining data content to scan. If empty, text, images, and other content will be included. Possible values: ["CONTENT_TEXT", "CONTENT_IMAGE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#content_options GoogleDataLossPreventionInspectTemplate#content_options}
        :param custom_info_types: custom_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#custom_info_types GoogleDataLossPreventionInspectTemplate#custom_info_types}
        :param exclude_info_types: When true, excludes type information of the findings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_info_types GoogleDataLossPreventionInspectTemplate#exclude_info_types}
        :param include_quote: When true, a contextual quote from the data that triggered a finding is included in the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#include_quote GoogleDataLossPreventionInspectTemplate#include_quote}
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#limits GoogleDataLossPreventionInspectTemplate#limits}
        :param min_likelihood: Only returns findings equal or above this threshold. See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#min_likelihood GoogleDataLossPreventionInspectTemplate#min_likelihood}
        :param rule_set: rule_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#rule_set GoogleDataLossPreventionInspectTemplate#rule_set}
        '''
        if isinstance(limits, dict):
            limits = GoogleDataLossPreventionInspectTemplateInspectConfigLimits(**limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b30d67ddebcffc9eafb240b2e8b6585ada3edf1e4a116ee70c8d8425cb50523)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#content_options GoogleDataLossPreventionInspectTemplate#content_options}
        '''
        result = self._values.get("content_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes"]]]:
        '''custom_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#custom_info_types GoogleDataLossPreventionInspectTemplate#custom_info_types}
        '''
        result = self._values.get("custom_info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes"]]], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, excludes type information of the findings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_info_types GoogleDataLossPreventionInspectTemplate#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_quote(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, a contextual quote from the data that triggered a finding is included in the response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#include_quote GoogleDataLossPreventionInspectTemplate#include_quote}
        '''
        result = self._values.get("include_quote")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def info_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes"]]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        '''
        result = self._values.get("info_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes"]]], result)

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#limits GoogleDataLossPreventionInspectTemplate#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimits"], result)

    @builtins.property
    def min_likelihood(self) -> typing.Optional[builtins.str]:
        '''Only returns findings equal or above this threshold.

        See https://cloud.google.com/dlp/docs/likelihood for more info Default value: "POSSIBLE" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#min_likelihood GoogleDataLossPreventionInspectTemplate#min_likelihood}
        '''
        result = self._values.get("min_likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet"]]]:
        '''rule_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#rule_set GoogleDataLossPreventionInspectTemplate#rule_set}
        '''
        result = self._values.get("rule_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes",
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
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes:
    def __init__(
        self,
        *,
        info_type: typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType", typing.Dict[builtins.str, typing.Any]],
        dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_type: typing.Optional[builtins.str] = None,
        likelihood: typing.Optional[builtins.str] = None,
        regex: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        stored_type: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType", typing.Dict[builtins.str, typing.Any]]] = None,
        surrogate_type: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_type GoogleDataLossPreventionInspectTemplate#info_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#dictionary GoogleDataLossPreventionInspectTemplate#dictionary}
        :param exclusion_type: If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned. It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclusion_type GoogleDataLossPreventionInspectTemplate#exclusion_type}
        :param likelihood: Likelihood to return for this CustomInfoType. This base value can be altered by a detection rule if the finding meets the criteria specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#likelihood GoogleDataLossPreventionInspectTemplate#likelihood}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#regex GoogleDataLossPreventionInspectTemplate#regex}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param stored_type: stored_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#stored_type GoogleDataLossPreventionInspectTemplate#stored_type}
        :param surrogate_type: surrogate_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#surrogate_type GoogleDataLossPreventionInspectTemplate#surrogate_type}
        '''
        if isinstance(info_type, dict):
            info_type = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType(**info_type)
        if isinstance(dictionary, dict):
            dictionary = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary(**dictionary)
        if isinstance(regex, dict):
            regex = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex(**regex)
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore(**sensitivity_score)
        if isinstance(stored_type, dict):
            stored_type = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType(**stored_type)
        if isinstance(surrogate_type, dict):
            surrogate_type = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType(**surrogate_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34c7a831c8a87f1a8632320b2834be3d9b6ddeb2d3d8df48bcae90dba37c63c)
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType":
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_type GoogleDataLossPreventionInspectTemplate#info_type}
        '''
        result = self._values.get("info_type")
        assert result is not None, "Required property 'info_type' is missing"
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType", result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#dictionary GoogleDataLossPreventionInspectTemplate#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary"], result)

    @builtins.property
    def exclusion_type(self) -> typing.Optional[builtins.str]:
        '''If set to EXCLUSION_TYPE_EXCLUDE this infoType will not cause a finding to be returned.

        It still can be used for rules matching. Possible values: ["EXCLUSION_TYPE_EXCLUDE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclusion_type GoogleDataLossPreventionInspectTemplate#exclusion_type}
        '''
        result = self._values.get("exclusion_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def likelihood(self) -> typing.Optional[builtins.str]:
        '''Likelihood to return for this CustomInfoType.

        This base value can be altered by a detection rule if the finding meets the criteria
        specified by the rule. Default value: "VERY_LIKELY" Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#likelihood GoogleDataLossPreventionInspectTemplate#likelihood}
        '''
        result = self._values.get("likelihood")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#regex GoogleDataLossPreventionInspectTemplate#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"], result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"], result)

    @builtins.property
    def stored_type(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"]:
        '''stored_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#stored_type GoogleDataLossPreventionInspectTemplate#stored_type}
        '''
        result = self._values.get("stored_type")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"], result)

    @builtins.property
    def surrogate_type(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"]:
        '''surrogate_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#surrogate_type GoogleDataLossPreventionInspectTemplate#surrogate_type}
        '''
        result = self._values.get("surrogate_type")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#cloud_storage_path GoogleDataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#word_list GoogleDataLossPreventionInspectTemplate#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299e2956b8e644a0ab7b6f26ccede6a33075fcc39e0060455834d6d778ed79c3)
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
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#cloud_storage_path GoogleDataLossPreventionInspectTemplate#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#word_list GoogleDataLossPreventionInspectTemplate#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#path GoogleDataLossPreventionInspectTemplate#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a70d5ef26e6232c8ad21104e5ad44cd259e807bc102bb9b49c03e54046969ad)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#path GoogleDataLossPreventionInspectTemplate#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9af5c9e706d23acc11be7e7dedbaad913ef46731b7ceaf35eac4271f9886e133)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75f4597e4f1ffe74757bfe970b9ba8674a479e1c5a5d80e7be04dd703d9080d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54a2de392e03b4a1858e0c48d23360cf5d8deb76b1caabcaa24340e5b933d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a47acfa5a98caee273c31b4d4a9204c931a5ede0ab1d1bc4ccedf5987d49a269)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#path GoogleDataLossPreventionInspectTemplate#path}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#words GoogleDataLossPreventionInspectTemplate#words}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct(
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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a660e3cf26ed9c95aa86d5ef1c456eebc3f644b08c9812caa54d451e1b2992af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#words GoogleDataLossPreventionInspectTemplate#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c0a0e591e9c95e06cc45b747c533e2ae19d2cb27347a3e46bd37aba1565602)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#words GoogleDataLossPreventionInspectTemplate#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed638c796c36da19ba9dc59ea0327599563c1d73128af83c85c0401d5f4873e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4147c2dbe1c106dbfad6fd0599b78a42ae769e9eb628f2ffa9342aab845fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b425f3b7d42d86e44090d4ba0f02cf948ed925f601241bcd294d20d12ba2dcb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cf3d914f580f4a4f848afbea2aea8e693112841bd728f894dfcb2d6344f412)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8199e84718ddb44e5fd6a3caab314c56e7dee5f909681491128735299af3046)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore(
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__46b0c414a08f22f81140cccff0c8d60d9c4bc0eb8235155d420a97e2980a3ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ae97dc661cf6c0bcdf1cb54d3e05c264b90904bbd3a3c4d57bf7fecb9a7439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002a5cc78cd417577c78104588cdd5d61571f55bb50f9f109753eb4146d734b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9a29adec81866e519f63acf59c9fbad30581ff4d4a34594018abea57cd8830)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__094a4ad7c696eae1635efe5b3da61f87c026df5f435a519eab11c501a7734ed5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10351dadb08f5387affd2dde963ba64489d01299d972ba7250bd273f0b14dc41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e99a1ffa752688c0aee86144dbce5602f81804e8ae3b41530e0b8eb2c3d6685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a3668a1f935ebd13d4c77caaeffdcae7bb79b73dc31fb76c0105001db18ef1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667b60cfd414a96b206d5d3571ca6492c91f90d1d5477578769099ae75556353)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce52076390cca56712418f765c838a84d600743401f4e4ec5fa7070780736ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b7622286a587b434c5f05247a3f7e3f8c8c245eb429ad9bd780915c0a0763e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2a7d6a2e54fe6bc1ef7abe099b61cc8a99f06193697a0405d5261c15c8bde96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10a0ba8d65be39c6d304779202f18496c4f80699b7eb3c7b5fd1ae982840e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d161556534e0cd2b3d7e08cca4f470d76baf11a44dc163d4782a093a2a7900a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#cloud_storage_path GoogleDataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#word_list GoogleDataLossPreventionInspectTemplate#word_list}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putInfoType")
    def put_info_type(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType(
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex(
            pattern=pattern, group_indexes=group_indexes
        )

        return typing.cast(None, jsii.invoke(self, "putRegex", [value]))

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore(
            score=score
        )

        return typing.cast(None, jsii.invoke(self, "putSensitivityScore", [value]))

    @jsii.member(jsii_name="putStoredType")
    def put_stored_type(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStoredType", [value]))

    @jsii.member(jsii_name="putSurrogateType")
    def put_surrogate_type(self) -> None:
        value = GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType()

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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="infoType")
    def info_type(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScore")
    def sensitivity_score(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="storedType")
    def stored_type(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference", jsii.get(self, "storedType"))

    @builtins.property
    @jsii.member(jsii_name="surrogateType")
    def surrogate_type(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference", jsii.get(self, "surrogateType"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionTypeInput")
    def exclusion_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType], jsii.get(self, "infoTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodInput")
    def likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="storedTypeInput")
    def stored_type_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType"], jsii.get(self, "storedTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="surrogateTypeInput")
    def surrogate_type_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType"], jsii.get(self, "surrogateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionType")
    def exclusion_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclusionType"))

    @exclusion_type.setter
    def exclusion_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3878f229ccab3210a36465096046d389b4a164e5fa935424493abbbe3c760290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="likelihood")
    def likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "likelihood"))

    @likelihood.setter
    def likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b9502d61ee092e4c4a0e4fd530b5121046c7cfd2d0ad7f40f2cacbf77bef54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "likelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd2a1cd49fb4d7f8940a81bdae26b4b900c517e169c93c8e4b73ddca9d3cc66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4894c147dc86ff480ad2bd62bca1ee95d19eca1402871baf8f31d6b9d1482248)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__876c7db9ffb2d024ffbc11e81a8e64e8312a6c0af74e15d374e7b0a5248725b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23ee53832a565e9369f186acac91f2f459c7d5095857d187373ca46d63146f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7741e0194865f01e1570db9a0e9e70e90e63aa38e0c2c5675b9df6a3dd7827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8758bd0d973fb82dfd9ef60446bd75e81d9184c1afa38ef2f35abc2bdd41bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87926d915ce9debde35f422d3ed902cbd3b8795d2e3ab4a2598eca9fdf926840)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1be7111e40f72d36596dd4fe423f1c3f6824511176522c1a5a63df8c776637e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe00eb5f931fb4d73fa4e60faa1bb56fd64d57d605c7dedd796d0bf2227a5ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea1e5cd724b2e93a2a6ccb27fc08b25db4da2ede925612e95c196f501afd234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc6f531e5c1e01afdc8cd12c636607b7f25ddddb1b1d6da4791a7fac01efa4a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name of the requested StoredInfoType, for example 'organizations/433245324/storedInfoTypes/432452342' or 'projects/project-id/storedInfoTypes/432452342'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf625be13b9547b2eb59f8c7d4bfd954558951b269afec16128e1fd9f17ca25d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f2825fa45c36854d42d71b537ada89c88e5709d3034453057fee51ca5b72029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c3607998f34e23f9a4e84276e5499132e4a1b585b4c76adcd2ed43873d476a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f1f391ce948157c3934b1c19689cca7ec6ac4a6e5ee19c3e364129b0b96499)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8001317d9b1e46e1f1d66dd9bd1cc5052dd52138477a09a0de91f0e6682d1721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version of the information type to use. By default, the version is set to stable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80876e69afce67e2b81400902ce097a6e5164f567b1e13907b36932df3cb8153)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the information type to use. By default, the version is set to stable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9af8c32a23340e360b71b7f8b72f5386a95de4b544809642d88b37dadbe71a44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc8a4e4b36aeb221987e0b67058fe21ef00637434b34d744802d9cd457a15ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f132b3e05286b45e26708e10a51e8ea2f08b562622ad77ac7bbf0cf6de9759d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__089eec203433153cc62c2da77aeb7bb82698f581a2ddda0c4b82972d506a73a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2e159f0d426fd76ff5b1691540f997ff34248c6de80fa2660b52c4663f59b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53cef9bdc8196094a533e5c46244bb3f3e2691e6415e968602381ebbe9734dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1a512209ad6f4a7d5e1ad083160081b59e8559f366e784d1f09cc48016ecad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore(
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__56b44130b60166b4fbc241b3c578a74fab9a58e5577ebc4fb4787aeca9c43ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f0bc1da658f2677e5ead39955741d6632b937fe8e7c831c4563fa802c95712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4547c5e00926d020efdd37e1889c056943e6300f56ed3c431be2e64a4bbc98ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d682b62351799823072a04f32c1e9d128aa3887385b8c78860389e896334cb)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2bae2159dc60c5ff51532d9feb21ee50204c2879faa925412445b7fa00bfee3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e4a37ed74fb4cea304d5e407792fa32a7c9caefe72f4aa93b22857a01be0b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152d608c6bffa6d3e8d13b6435bc34af671c58247adc75b94589d891f18d53ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimits",
    jsii_struct_bases=[],
    name_mapping={
        "max_findings_per_item": "maxFindingsPerItem",
        "max_findings_per_request": "maxFindingsPerRequest",
        "max_findings_per_info_type": "maxFindingsPerInfoType",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigLimits:
    def __init__(
        self,
        *,
        max_findings_per_item: jsii.Number,
        max_findings_per_request: jsii.Number,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_item GoogleDataLossPreventionInspectTemplate#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_request GoogleDataLossPreventionInspectTemplate#max_findings_per_request}
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_info_type GoogleDataLossPreventionInspectTemplate#max_findings_per_info_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae35a08bf43e661488872419108aef12c60065d808475d46cd3fa9bff6216a0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_item GoogleDataLossPreventionInspectTemplate#max_findings_per_item}
        '''
        result = self._values.get("max_findings_per_item")
        assert result is not None, "Required property 'max_findings_per_item' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_findings_per_request(self) -> jsii.Number:
        '''Max number of findings that will be returned per request/job. The maximum returned is 2000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_request GoogleDataLossPreventionInspectTemplate#max_findings_per_request}
        '''
        result = self._values.get("max_findings_per_request")
        assert result is not None, "Required property 'max_findings_per_request' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_findings_per_info_type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType"]]]:
        '''max_findings_per_info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_info_type GoogleDataLossPreventionInspectTemplate#max_findings_per_info_type}
        '''
        result = self._values.get("max_findings_per_info_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType",
    jsii_struct_bases=[],
    name_mapping={"max_findings": "maxFindings", "info_type": "infoType"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType:
    def __init__(
        self,
        *,
        max_findings: jsii.Number,
        info_type: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_findings: Max findings limit for the given infoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings GoogleDataLossPreventionInspectTemplate#max_findings}
        :param info_type: info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_type GoogleDataLossPreventionInspectTemplate#info_type}
        '''
        if isinstance(info_type, dict):
            info_type = GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(**info_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c755349974c88eb9a95cd625d1ede517e764e6792dcbfb47a7b40206d0aa9b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings GoogleDataLossPreventionInspectTemplate#max_findings}
        '''
        result = self._values.get("max_findings")
        assert result is not None, "Required property 'max_findings' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def info_type(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"]:
        '''info_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_type GoogleDataLossPreventionInspectTemplate#info_type}
        '''
        result = self._values.get("info_type")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1995751165870ce1327f2de7b36e181543b451b54d23792cdf1dd292ce6e1bc2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c92271261ba9ae1c9ab3166ae85c287b00f1a8c0d261b6289b1fe711608fb369)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__76d1c65fbaeaf8b2fd77baca44ddd031ad508859bfdc87c0cdf90deeebe6e6b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6280c262dd50098956cb54908d1ca7b7879e701c93c78ee275f256332ecb9138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace4b2b8e8b19c499954ac6b361edf210982e9c16d16fd3739e5b8af6c68dc58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5cfb64d21349863129abd0a424e5a9b6828443d1864f5d250621b94e6488098)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68497e04a820a94dd1759552a8fc933d873d34b845320e0cdbfa909b05cf8115)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb2ba04ce5d4c82d07fa933bc6110cbfbf647edc26e48326a2259f3a0282949f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916fd644c44eabe4d35fd171f250bb8469305d47b056af07249d00ea9a6bea3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c23d26c7d587e1df40d968b947290a2ef1291dc27121fd8dc9e742b9bd665c66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4853b86f310f478ba4d52b907401848735bdfa581763dac4a845579aec0ecbdd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96146dc81d9d590267f86ef1490b57f8e2a8012f7186cd4141a78c5f3ee5f51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5d40475013a56fe1b7cf2c8e03288b8e6de4f7a8be1e5c12a9c7b2fa232003c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c0d2c0b2d96676ce193851fdd55ac025642a972d280e0273b07fb1031cd1236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8d9f2f797283762dacb2493d7ece4cc7ac079a22044f2e541990e954724a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4f8afb4049e0af57c4187c1733743438e64d6a47e16a3398b92e447664f9aea)
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
        sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType(
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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference, jsii.get(self, "infoType"))

    @builtins.property
    @jsii.member(jsii_name="infoTypeInput")
    def info_type_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType], jsii.get(self, "infoTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e7453a2d98f077ba146fcaa17282fd3d2b400ddd101120570ab984daa67fcc5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a470ae69007aceae01c76b33d8b2c436ad4c9cdae7ef2fedb3a61d7573621ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a9c8351d95ce45f348a488ed21757a57ef9e0720c52f82604ed5dcc52820d2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaxFindingsPerInfoType")
    def put_max_findings_per_info_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35577bd101cd2e1a094035bed8df61a164820cff148dc6644497e37ecfde9475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaxFindingsPerInfoType", [value]))

    @jsii.member(jsii_name="resetMaxFindingsPerInfoType")
    def reset_max_findings_per_info_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFindingsPerInfoType", []))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoType")
    def max_findings_per_info_type(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList, jsii.get(self, "maxFindingsPerInfoType"))

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerInfoTypeInput")
    def max_findings_per_info_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]], jsii.get(self, "maxFindingsPerInfoTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e2e5fed614bfd3213cdd36a61a19ab858fdbdc62640202d74a7005e92be73e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerItem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFindingsPerRequest")
    def max_findings_per_request(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFindingsPerRequest"))

    @max_findings_per_request.setter
    def max_findings_per_request(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559a3bb6d67fe57c8baec6b46854a3f3436eae90c62dbf7760c1074ab7714d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFindingsPerRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimits]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7f95ecace248275c27d675fe333c712414e2ac4f866e742e0f90b16783b442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5502e30675e4fd6457cdb00656f89d678257f665f296cd7c884ce41130adc91a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomInfoTypes")
    def put_custom_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6dd62ac71d32f7ea6f1cf4f13e18a4e41eb5d8cf0381de7ea39af9c4e92a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomInfoTypes", [value]))

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab72fa6b96375ace8044969c32b815930a6d10d2eee58505439e5448e31a3be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        max_findings_per_item: jsii.Number,
        max_findings_per_request: jsii.Number,
        max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_findings_per_item: Max number of findings that will be returned for each item scanned. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_item GoogleDataLossPreventionInspectTemplate#max_findings_per_item}
        :param max_findings_per_request: Max number of findings that will be returned per request/job. The maximum returned is 2000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_request GoogleDataLossPreventionInspectTemplate#max_findings_per_request}
        :param max_findings_per_info_type: max_findings_per_info_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#max_findings_per_info_type GoogleDataLossPreventionInspectTemplate#max_findings_per_info_type}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigLimits(
            max_findings_per_item=max_findings_per_item,
            max_findings_per_request=max_findings_per_request,
            max_findings_per_info_type=max_findings_per_info_type,
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putRuleSet")
    def put_rule_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd059197f974ca3661f8a53def8286a4c4896001595b279fa5375ba79fe5a4a7)
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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList, jsii.get(self, "customInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesList:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigLimitsOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="ruleSet")
    def rule_set(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetList":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetList", jsii.get(self, "ruleSet"))

    @builtins.property
    @jsii.member(jsii_name="contentOptionsInput")
    def content_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="customInfoTypesInput")
    def custom_info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]], jsii.get(self, "customInfoTypesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimits]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="minLikelihoodInput")
    def min_likelihood_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minLikelihoodInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetInput")
    def rule_set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet"]]], jsii.get(self, "ruleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="contentOptions")
    def content_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contentOptions"))

    @content_options.setter
    def content_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da4ba5b0143e08b6e4a698eab79a1e5287bf57e108ba629e94262890fec8160)
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
            type_hints = typing.get_type_hints(_typecheckingstub__754c47a7e03de9190fe9f19ac8f3a4e7ff55b518475471e377741a769141caf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7391521a2b12154db3c7b29d465212a54fb63dc3e2cc6ba3f0a1ed480ce9c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQuote", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLikelihood")
    def min_likelihood(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minLikelihood"))

    @min_likelihood.setter
    def min_likelihood(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f73244c1a07b164b4bedea21f4ad6a3bab66c940d1431f6bc16cd9f37d6fcc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfig]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3f42b6601e7199030ca725dee2bcc752024dc797a910be436a8d687f283141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet",
    jsii_struct_bases=[],
    name_mapping={"info_types": "infoTypes", "rules": "rules"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet:
    def __init__(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes", typing.Dict[builtins.str, typing.Any]]]],
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#rules GoogleDataLossPreventionInspectTemplate#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb3c687005bb10f66ff50506ac419646ebb4d45e7205f4549a3732832cbe97e)
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_types": info_types,
            "rules": rules,
        }

    @builtins.property
    def info_types(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes"]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        '''
        result = self._values.get("info_types")
        assert result is not None, "Required property 'info_types' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes"]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#rules GoogleDataLossPreventionInspectTemplate#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400e1a0875546fe13e8c9a780a5c22fa4cbb979327c9906b98d7cf924d3001ac)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf57a2458c1d21131caa614ad96ae3972f24144198c0003e0ae8dae8506d0c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603d943a111b0584a0426a0a3348c9415dea2e45bfdca7fb68419d16d827661b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e44c7fd3c5fbf805d098dae05c0a49c95f1c00048d195b89880af05d544808)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0718a4bedcd69b9dd97a2ac785530355d0ae2d1a0d57384fc98253dcba81a4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__467535a21ad5bfe8274a82128b62343bd334b7c0f8ef62326fd7df5c780b8d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e98cc0fa0f7c8d0627d053b035363bcfbbd7f567e3c8e9e1df9334cf0abc94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c3920f871e64bac413ecf1ad1bfa5c31f537a8e0ca2003a370360468d3a8e8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore(
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a131d4fd4118f8be1d0cb2671421a3938461afa474e8f6068ccf0385ef99a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37b7f2a5ab798d3b57bb65761e2d348915cc32dbb0021015282c86f75545922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfad68b0cce1f1e4b3bdd80951cb73ca71b30d9fc10d53fa56fee767487f61c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e23879830054712b8f2b6d3e444b09e7f92343a36d94064701bba5260b8ebc)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd9326031683ac929345b475db3e509defd3d3243fa0975ce1e25349f1468a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34c1011d8122ef0da7046d4ed9d613944fa04176ce98a9b24630f89398ab52a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27cc69f82a271fe9b27c75d592258439cdcb690779e00e45ff6dd9ce2d512bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__230ed78ce11f6241cb2b25ad4e3eb77d14274680c871a97debde3bdb84a9bbc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2720b4d68c5c6a9cb497cac6bf138c95c3f48bb3ed901c2fbee80fae6b764f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ebb399cad614a176b0036a33d19681e62dda3bcf727f627659089239d7235f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69b42b2da088a5ce6c30bdc6070e069a7249926504c0ca1de48a51f218fa5795)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7082ee3d7398ccd3cf365c3ec204402c75c062812affe9252e3ec8a8f60b9032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7149e419365fcbe3995c09df8f4380d5c1b6081d8fc26a09449877844db680bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__514223bdbfe46449a92ab11d727b374e362208ea990e9a49bf1cdcb9df88b9c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7408fa50875835e4332ecb87c7e62f96bd2f7ecc55700869a1e1029d3d4638b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0ab6ed16a84f7522e208ef02e4bbcb79931101e5dbe10913226630b2620a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesList":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09104965804ecad9058d105e3e48eebe4d0efa9be9948792e5784514d0bf3c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules",
    jsii_struct_bases=[],
    name_mapping={"exclusion_rule": "exclusionRule", "hotword_rule": "hotwordRule"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules:
    def __init__(
        self,
        *,
        exclusion_rule: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule", typing.Dict[builtins.str, typing.Any]]] = None,
        hotword_rule: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param exclusion_rule: exclusion_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclusion_rule GoogleDataLossPreventionInspectTemplate#exclusion_rule}
        :param hotword_rule: hotword_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_rule GoogleDataLossPreventionInspectTemplate#hotword_rule}
        '''
        if isinstance(exclusion_rule, dict):
            exclusion_rule = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule(**exclusion_rule)
        if isinstance(hotword_rule, dict):
            hotword_rule = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule(**hotword_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1db436982dbcee610d573bffda97a7e59697e8d4ee3ffd28f1d73eff48e803b)
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
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule"]:
        '''exclusion_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclusion_rule GoogleDataLossPreventionInspectTemplate#exclusion_rule}
        '''
        result = self._values.get("exclusion_rule")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule"], result)

    @builtins.property
    def hotword_rule(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule"]:
        '''hotword_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_rule GoogleDataLossPreventionInspectTemplate#hotword_rule}
        '''
        result = self._values.get("hotword_rule")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule",
    jsii_struct_bases=[],
    name_mapping={
        "matching_type": "matchingType",
        "dictionary": "dictionary",
        "exclude_by_hotword": "excludeByHotword",
        "exclude_info_types": "excludeInfoTypes",
        "regex": "regex",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule:
    def __init__(
        self,
        *,
        matching_type: builtins.str,
        dictionary: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#matching_type GoogleDataLossPreventionInspectTemplate#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#dictionary GoogleDataLossPreventionInspectTemplate#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_by_hotword GoogleDataLossPreventionInspectTemplate#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_info_types GoogleDataLossPreventionInspectTemplate#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#regex GoogleDataLossPreventionInspectTemplate#regex}
        '''
        if isinstance(dictionary, dict):
            dictionary = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary(**dictionary)
        if isinstance(exclude_by_hotword, dict):
            exclude_by_hotword = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(**exclude_by_hotword)
        if isinstance(exclude_info_types, dict):
            exclude_info_types = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(**exclude_info_types)
        if isinstance(regex, dict):
            regex = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex(**regex)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd9debc19fc9db273f102b3f78500057157450a0f98174fb3d8e75dae6d9bf2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#matching_type GoogleDataLossPreventionInspectTemplate#matching_type}
        '''
        result = self._values.get("matching_type")
        assert result is not None, "Required property 'matching_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dictionary(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary"]:
        '''dictionary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#dictionary GoogleDataLossPreventionInspectTemplate#dictionary}
        '''
        result = self._values.get("dictionary")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary"], result)

    @builtins.property
    def exclude_by_hotword(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"]:
        '''exclude_by_hotword block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_by_hotword GoogleDataLossPreventionInspectTemplate#exclude_by_hotword}
        '''
        result = self._values.get("exclude_by_hotword")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword"], result)

    @builtins.property
    def exclude_info_types(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"]:
        '''exclude_info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_info_types GoogleDataLossPreventionInspectTemplate#exclude_info_types}
        '''
        result = self._values.get("exclude_info_types")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes"], result)

    @builtins.property
    def regex(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"]:
        '''regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#regex GoogleDataLossPreventionInspectTemplate#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary",
    jsii_struct_bases=[],
    name_mapping={"cloud_storage_path": "cloudStoragePath", "word_list": "wordList"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary:
    def __init__(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath", typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#cloud_storage_path GoogleDataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#word_list GoogleDataLossPreventionInspectTemplate#word_list}
        '''
        if isinstance(cloud_storage_path, dict):
            cloud_storage_path = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(**cloud_storage_path)
        if isinstance(word_list, dict):
            word_list = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(**word_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec69c27be9fbe51fd80ed1a114ceb48e2675d2b2f5db9d251696519567a4c796)
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
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"]:
        '''cloud_storage_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#cloud_storage_path GoogleDataLossPreventionInspectTemplate#cloud_storage_path}
        '''
        result = self._values.get("cloud_storage_path")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath"], result)

    @builtins.property
    def word_list(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        '''word_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#word_list GoogleDataLossPreventionInspectTemplate#word_list}
        '''
        result = self._values.get("word_list")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#path GoogleDataLossPreventionInspectTemplate#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02891eb911cf9f87710b71866865bbac4b6846aabfa5055bbb2a5427e81b79fe)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#path GoogleDataLossPreventionInspectTemplate#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce88e105070eaa3cf2fe82d43110bf5d3755da6d8f5496fa8c9c0a5e4e14e009)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1442d1fe0936da9ed18d8d5b39cc7d6724946125c60e0a6d3211272822bcc89a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfeab57dbdcaf8e648b2e419d84e5796a303f989f3ed2fdde6eb4f2a187b80c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a0f051798ebffcf00016bf7f59298a6bd7599573714482e02f3d4db850ab717)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudStoragePath")
    def put_cloud_storage_path(self, *, path: builtins.str) -> None:
        '''
        :param path: A url representing a file or path (no wildcards) in Cloud Storage. Example: 'gs://[BUCKET_NAME]/dictionary.txt'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#path GoogleDataLossPreventionInspectTemplate#path}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putCloudStoragePath", [value]))

    @jsii.member(jsii_name="putWordList")
    def put_word_list(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#words GoogleDataLossPreventionInspectTemplate#words}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(
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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference, jsii.get(self, "cloudStoragePath"))

    @builtins.property
    @jsii.member(jsii_name="wordList")
    def word_list(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference", jsii.get(self, "wordList"))

    @builtins.property
    @jsii.member(jsii_name="cloudStoragePathInput")
    def cloud_storage_path_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath], jsii.get(self, "cloudStoragePathInput"))

    @builtins.property
    @jsii.member(jsii_name="wordListInput")
    def word_list_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct"], jsii.get(self, "wordListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a38c64b546d03a977d91b8273ead2205756c0e9e136acd76305c59802423547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    jsii_struct_bases=[],
    name_mapping={"words": "words"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct:
    def __init__(self, *, words: typing.Sequence[builtins.str]) -> None:
        '''
        :param words: Words or phrases defining the dictionary. The dictionary must contain at least one phrase and every phrase must contain at least 2 characters that are letters or digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#words GoogleDataLossPreventionInspectTemplate#words}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c91fcaab61fccb488bce5bd772ae833934e6dbed3b49eb2728131b3fc28643)
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "words": words,
        }

    @builtins.property
    def words(self) -> typing.List[builtins.str]:
        '''Words or phrases defining the dictionary.

        The dictionary must contain at least one
        phrase and every phrase must contain at least 2 characters that are letters or digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#words GoogleDataLossPreventionInspectTemplate#words}
        '''
        result = self._values.get("words")
        assert result is not None, "Required property 'words' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d9781f5bf01c6154dd8c9ab5706c8529d17cdf35543c91cb54bd2ab2dfe5e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6fde608c727ba718473a7556028ae1cc2c5bcbf0f8931f6555afe50a340da5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42c3b6d98cec9306c63da9b9fbed042e5868a4c3090c74bc26860ec62284e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    jsii_struct_bases=[],
    name_mapping={"hotword_regex": "hotwordRegex", "proximity": "proximity"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword:
    def __init__(
        self,
        *,
        hotword_regex: typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex", typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_regex GoogleDataLossPreventionInspectTemplate#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#proximity GoogleDataLossPreventionInspectTemplate#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(**hotword_regex)
        if isinstance(proximity, dict):
            proximity = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b55e8aa52489933294a851b2fc9d1ebabd4575e577c8efbf3a15e920bec4e8)
            check_type(argname="argument hotword_regex", value=hotword_regex, expected_type=type_hints["hotword_regex"])
            check_type(argname="argument proximity", value=proximity, expected_type=type_hints["proximity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hotword_regex": hotword_regex,
            "proximity": proximity,
        }

    @builtins.property
    def hotword_regex(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex":
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_regex GoogleDataLossPreventionInspectTemplate#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        assert result is not None, "Required property 'hotword_regex' is missing"
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex", result)

    @builtins.property
    def proximity(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity":
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#proximity GoogleDataLossPreventionInspectTemplate#proximity}
        '''
        result = self._values.get("proximity")
        assert result is not None, "Required property 'proximity' is missing"
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27fdd935206f16da45f3002b973361220cf70bbde85014b64e697b4fb70e3bfe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified,
        the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e536535ba86ba8f26f93271ffed5790a7118c8c556288d840d00921aec583d1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7cb46e749122e23e0e78e9c250eeb6b4eda07d35150b1305e4c00a9bdbf214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f692171bcf772fd53f8d91cd750a4fcaa780652f06fdad5493a6f10cd155db14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b216cd317344f65d071c598f16584cc0e642bf4450547eadad6961de03665cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f7b64f12a46a20abf9c2fd73a8b01ecf052c8dc221c4d4962c0bee6e5a38f30)
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex(
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
        :param window_after: Number of characters after the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_after GoogleDataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_before GoogleDataLossPreventionInspectTemplate#window_before}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(
            window_after=window_after, window_before=window_before
        )

        return typing.cast(None, jsii.invoke(self, "putProximity", [value]))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegex")
    def hotword_regex(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0572c5a12a6d6097354b97a0fd89b79afefc65f1d77d95fd5fe7398a184329b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_after GoogleDataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_before GoogleDataLossPreventionInspectTemplate#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b58b1aa01157858fe4284e2b1f7f8540c3e1a40dbc4903166da10fdeec9164)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_after GoogleDataLossPreventionInspectTemplate#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_before GoogleDataLossPreventionInspectTemplate#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51607fa27a163556d85df0d8a450d05e475182a9075e7f7d647a8a0df66c3613)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f6f2f81d47689784340116348d25cafc2db2f1413d0ac18a18b7806e5685b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade5bc29ed9d982421d78498ef153f79ce8af294920299775f5a5874c98cea40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f88a65ea84365a6685bcab0772bce2b48a8c1bf7b1bf0328b62fdbdaea93ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    jsii_struct_bases=[],
    name_mapping={"info_types": "infoTypes"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes:
    def __init__(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55677a0ad53a4a6b550b18cd46a4bdffe4f10687623f432ba0a2ee89401f30d0)
            check_type(argname="argument info_types", value=info_types, expected_type=type_hints["info_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_types": info_types,
        }

    @builtins.property
    def info_types(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]]:
        '''info_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        '''
        result = self._values.get("info_types")
        assert result is not None, "Required property 'info_types' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sensitivity_score": "sensitivityScore",
        "version": "version",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        sensitivity_score: typing.Optional[typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the information type. Either a name of your choosing when creating a CustomInfoType, or one of the names listed at https://cloud.google.com/dlp/docs/infotypes-reference when specifying a built-in type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        :param sensitivity_score: sensitivity_score block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        :param version: Version name for this InfoType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        if isinstance(sensitivity_score, dict):
            sensitivity_score = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(**sensitivity_score)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef5dcb3b93cdf772209aaccacb1e2fab8a3114fd9e0d7870bcecc471bfa63b7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#name GoogleDataLossPreventionInspectTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitivity_score(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        '''sensitivity_score block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#sensitivity_score GoogleDataLossPreventionInspectTemplate#sensitivity_score}
        '''
        result = self._values.get("sensitivity_score")
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version name for this InfoType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#version GoogleDataLossPreventionInspectTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c62cf8e72fdbf1d687910ad081f535d188114a2d84e373ba3fcb618f23ee6bb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef49175d4e352491e5df1c3a8600c463589fa90d8291902842a62ed46a210287)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f143af99a0320bb8bf4016367776908dac22f1c1b255018ba61e7a4becbaa0aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90f03a84b7f6a2cc7d105e27aba16520a4d005ec3564c2757d72fcb10f77adf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a0b0bad44ebdf7d3f685df44a2a878096edea27d090a2db5771cd192f5391b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff3b1fc12d4a432088705553408ada44be9349763a24ff213a877f9a9e86f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__352dcf3fc0ccacd3c57fd843b48501fe74d13ec2180a36a7842ed266d794c3f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSensitivityScore")
    def put_sensitivity_score(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference", jsii.get(self, "sensitivityScore"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityScoreInput")
    def sensitivity_score_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore"], jsii.get(self, "sensitivityScoreInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0239238b8e30f88a63868c8b1c9c1b9e3c5ffe40a8489a046b88989fd53845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586b824990f659fb1e15a31f72778cb96d87ace197fce6d620592311edda5134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b1fd2b86fa907d91d1e9584354a2f4bdf03272f0e5adc8c62e70d4b63e55a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    jsii_struct_bases=[],
    name_mapping={"score": "score"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore:
    def __init__(self, *, score: builtins.str) -> None:
        '''
        :param score: The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757398509038bfcb8b931121c18ea95bbc3b4540577ec71f0ee264a668c18e03)
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "score": score,
        }

    @builtins.property
    def score(self) -> builtins.str:
        '''The sensitivity score applied to the resource. Possible values: ["SENSITIVITY_LOW", "SENSITIVITY_MODERATE", "SENSITIVITY_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#score GoogleDataLossPreventionInspectTemplate#score}
        '''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74ccbaea1d228a3df817a3300e5a3641d1f57e3e6de46b916915c4d8054055a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea0674980e8eb99364b21f3e967b241ce930a7150af1dd1cb47e4d04c3fa252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7d983f81672bf72a30c38038afca2d494882c46e7af5c5b44fb4c44ec6f31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3280d7404e48a185a783337eb8fdb15a0cb6d39c5521182a922694138e810123)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfoTypes")
    def put_info_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4f2d3c0c9b915004dac0917be56895caa635f56013f0fecfef61650de4aa7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfoTypes", [value]))

    @builtins.property
    @jsii.member(jsii_name="infoTypes")
    def info_types(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList, jsii.get(self, "infoTypes"))

    @builtins.property
    @jsii.member(jsii_name="infoTypesInput")
    def info_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]], jsii.get(self, "infoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1f1d9eb14c89ef94af83c83abdc9c020d541a6197ea7df40d64f81d0c6aafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d3ba7e9ad62d89d6c1bfb988e8745e99707bce45f474b313d0083d47193edfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDictionary")
    def put_dictionary(
        self,
        *,
        cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
        word_list: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_storage_path: cloud_storage_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#cloud_storage_path GoogleDataLossPreventionInspectTemplate#cloud_storage_path}
        :param word_list: word_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#word_list GoogleDataLossPreventionInspectTemplate#word_list}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary(
            cloud_storage_path=cloud_storage_path, word_list=word_list
        )

        return typing.cast(None, jsii.invoke(self, "putDictionary", [value]))

    @jsii.member(jsii_name="putExcludeByHotword")
    def put_exclude_by_hotword(
        self,
        *,
        hotword_regex: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_regex GoogleDataLossPreventionInspectTemplate#hotword_regex}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#proximity GoogleDataLossPreventionInspectTemplate#proximity}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword(
            hotword_regex=hotword_regex, proximity=proximity
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeByHotword", [value]))

    @jsii.member(jsii_name="putExcludeInfoTypes")
    def put_exclude_info_types(
        self,
        *,
        info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param info_types: info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#info_types GoogleDataLossPreventionInspectTemplate#info_types}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes(
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex(
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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference, jsii.get(self, "dictionary"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotword")
    def exclude_by_hotword(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference, jsii.get(self, "excludeByHotword"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypes")
    def exclude_info_types(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference, jsii.get(self, "excludeInfoTypes"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference", jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryInput")
    def dictionary_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary], jsii.get(self, "dictionaryInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeByHotwordInput")
    def exclude_by_hotword_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword], jsii.get(self, "excludeByHotwordInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInfoTypesInput")
    def exclude_info_types_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes], jsii.get(self, "excludeInfoTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingTypeInput")
    def matching_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex"], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingType")
    def matching_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchingType"))

    @matching_type.setter
    def matching_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f4ff60ca997d61910ee974e1e5c9c54a2c30ca509f4398161d1fc234a013f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a7b3d260d2856929714322bca44289a80cc1dd779f26df7f63c03428e3da91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2946aada25ac05d8b44377a1ac2240c04d4b20de0d04df2f7c2cc0f0658532)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified, the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9db3e07a41bd7da275e5d506d58e10eb9a99ec2e825175c7322f1db5e332d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7db0fd3f86a23dd0736ac57a6865d9abdcf00d26b7e630eff4ac67dc406292e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d3a595453e004c34c7b843d5938a03536a94ecd32ab6d40e6ce64d37b82f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193148530a5427886de09d7f9f03a74b77a96fd0306025d170f5f9f40ad298f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule",
    jsii_struct_bases=[],
    name_mapping={
        "hotword_regex": "hotwordRegex",
        "likelihood_adjustment": "likelihoodAdjustment",
        "proximity": "proximity",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule:
    def __init__(
        self,
        *,
        hotword_regex: typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex", typing.Dict[builtins.str, typing.Any]],
        likelihood_adjustment: typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment", typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_regex GoogleDataLossPreventionInspectTemplate#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#likelihood_adjustment GoogleDataLossPreventionInspectTemplate#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#proximity GoogleDataLossPreventionInspectTemplate#proximity}
        '''
        if isinstance(hotword_regex, dict):
            hotword_regex = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex(**hotword_regex)
        if isinstance(likelihood_adjustment, dict):
            likelihood_adjustment = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(**likelihood_adjustment)
        if isinstance(proximity, dict):
            proximity = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity(**proximity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5063b342f31c42c1e8093782affcceff09a62a3c8ce1490c2e7c26e31ef0030b)
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
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex":
        '''hotword_regex block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_regex GoogleDataLossPreventionInspectTemplate#hotword_regex}
        '''
        result = self._values.get("hotword_regex")
        assert result is not None, "Required property 'hotword_regex' is missing"
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex", result)

    @builtins.property
    def likelihood_adjustment(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment":
        '''likelihood_adjustment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#likelihood_adjustment GoogleDataLossPreventionInspectTemplate#likelihood_adjustment}
        '''
        result = self._values.get("likelihood_adjustment")
        assert result is not None, "Required property 'likelihood_adjustment' is missing"
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment", result)

    @builtins.property
    def proximity(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity":
        '''proximity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#proximity GoogleDataLossPreventionInspectTemplate#proximity}
        '''
        result = self._values.get("proximity")
        assert result is not None, "Required property 'proximity' is missing"
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern", "group_indexes": "groupIndexes"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex:
    def __init__(
        self,
        *,
        pattern: builtins.str,
        group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb2c0b41ff7f8ddfe21ad21aea2cd8ed56b130e19ae68d8507166a3c8824176)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_indexes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The index of the submatch to extract as findings.

        When not specified,
        the entire match is returned. No more than 3 may be included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        result = self._values.get("group_indexes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc69ac3fa2339364344afa6a06609f07d772ae831826f9e63e38ccd8f5640423)
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
            type_hints = typing.get_type_hints(_typecheckingstub__131c871ce60bd7a16bd56b394506f19215b2e2d3e7abc07aea4ba18688d4ed0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupIndexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358a076a88fa34eedc9f1524fc38306a04bb57ae2328aae8e4a5ea42868b1f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d19c65550ee658a80d71fd8d9a446e3a212d6167a2b375689316710dcdd035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_likelihood": "fixedLikelihood",
        "relative_likelihood": "relativeLikelihood",
    },
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment:
    def __init__(
        self,
        *,
        fixed_likelihood: typing.Optional[builtins.str] = None,
        relative_likelihood: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#fixed_likelihood GoogleDataLossPreventionInspectTemplate#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#relative_likelihood GoogleDataLossPreventionInspectTemplate#relative_likelihood}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf99eeda2ce7fc7d797747e0c8cf12f47cc093a2aef1c08cfe1a03778f36a24)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#fixed_likelihood GoogleDataLossPreventionInspectTemplate#fixed_likelihood}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#relative_likelihood GoogleDataLossPreventionInspectTemplate#relative_likelihood}
        '''
        result = self._values.get("relative_likelihood")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97b2a09a76bb32b25f27f45a0d4cb48aa5786d169cd030a8ec40142a1a63bd54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd862a12814d156242e15c1b3876375a63900841c3a2e2cdf95ee6efc161253c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeLikelihood")
    def relative_likelihood(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "relativeLikelihood"))

    @relative_likelihood.setter
    def relative_likelihood(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e14b87681289deaa40d49de25eb075eb274f6040d808ec27379ffad1abf11d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeLikelihood", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742086c7fc239e94eddbb0016701188d9c6422d53cfd62a154305f57faaf3924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bbbc9d201197a15516a9f3b9322f614ffd0cfb30991aba4f53da77d2040f61b)
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
        :param pattern: Pattern defining the regular expression. Its syntax (https://github.com/google/re2/wiki/Syntax) can be found under the google/re2 repository on GitHub. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#pattern GoogleDataLossPreventionInspectTemplate#pattern}
        :param group_indexes: The index of the submatch to extract as findings. When not specified, the entire match is returned. No more than 3 may be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#group_indexes GoogleDataLossPreventionInspectTemplate#group_indexes}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex(
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
        :param fixed_likelihood: Set the likelihood of a finding to a fixed value. Either this or relative_likelihood can be set. Possible values: ["VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#fixed_likelihood GoogleDataLossPreventionInspectTemplate#fixed_likelihood}
        :param relative_likelihood: Increase or decrease the likelihood by the specified number of levels. For example, if a finding would be POSSIBLE without the detection rule and relativeLikelihood is 1, then it is upgraded to LIKELY, while a value of -1 would downgrade it to UNLIKELY. Likelihood may never drop below VERY_UNLIKELY or exceed VERY_LIKELY, so applying an adjustment of 1 followed by an adjustment of -1 when base likelihood is VERY_LIKELY will result in a final likelihood of LIKELY. Either this or fixed_likelihood can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#relative_likelihood GoogleDataLossPreventionInspectTemplate#relative_likelihood}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment(
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
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_after GoogleDataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_before GoogleDataLossPreventionInspectTemplate#window_before}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity(
            window_after=window_after, window_before=window_before
        )

        return typing.cast(None, jsii.invoke(self, "putProximity", [value]))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegex")
    def hotword_regex(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference, jsii.get(self, "hotwordRegex"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustment")
    def likelihood_adjustment(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference, jsii.get(self, "likelihoodAdjustment"))

    @builtins.property
    @jsii.member(jsii_name="proximity")
    def proximity(
        self,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference":
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference", jsii.get(self, "proximity"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRegexInput")
    def hotword_regex_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex], jsii.get(self, "hotwordRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="likelihoodAdjustmentInput")
    def likelihood_adjustment_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment], jsii.get(self, "likelihoodAdjustmentInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityInput")
    def proximity_input(
        self,
    ) -> typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity"]:
        return typing.cast(typing.Optional["GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity"], jsii.get(self, "proximityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4ac097c8b4fb2984e28386c4fd9807dc7d472ce44f539f098d3994cee06e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity",
    jsii_struct_bases=[],
    name_mapping={"window_after": "windowAfter", "window_before": "windowBefore"},
)
class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity:
    def __init__(
        self,
        *,
        window_after: typing.Optional[jsii.Number] = None,
        window_before: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param window_after: Number of characters after the finding to consider. Either this or window_before must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_after GoogleDataLossPreventionInspectTemplate#window_after}
        :param window_before: Number of characters before the finding to consider. Either this or window_after must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_before GoogleDataLossPreventionInspectTemplate#window_before}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953a096caf815fad1b8b106c450c9a4addf9719405504ade17b2af9723b64b93)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_after GoogleDataLossPreventionInspectTemplate#window_after}
        '''
        result = self._values.get("window_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window_before(self) -> typing.Optional[jsii.Number]:
        '''Number of characters before the finding to consider. Either this or window_after must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#window_before GoogleDataLossPreventionInspectTemplate#window_before}
        '''
        result = self._values.get("window_before")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9497dffe5c815cb06e73a1748990022618b4ecddb3886ba539d4ae4aba991a3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e25b925205daceafdac391d1e82ef2a319eec5478e09e8b1b75b5e9dc87212d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowBefore")
    def window_before(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "windowBefore"))

    @window_before.setter
    def window_before(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da095ebcd7e7303f60dfb2d53cf0b9f2e7a61f77c8a980cf75c36ee7e1cf0ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4110aea435c9e19004b71917301dd6a48535da99715bcccd97200cfadc2bb6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08c007c82ca8cec6ac0866af62f5888a03f1f134221d2e3ed01fcea1f2e86d31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdea00741e7c124a05de2173a0bb855dcb3bd5985f67a39d18bf0d57f5f9165)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1575fbe3302c8e7168b4ad9971ecdb7896f296d429eafbd45aedf518534c085)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4a26db08fbc466d3d16cc95884268495b0baf475768a5e35b9b8b355b07fcef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4ec335816a94e0749e861a428ee7836f42d0b62363ebd1d05482dc338b8d5bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fb06502e64d24edf5f3d073a2fab26b7cb807671cb4972e29cc52a8ca8f3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b40d3d216b510e7efe208b1b87c012a3385185f32f2e1f285d023befefc84da)
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
        dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_by_hotword: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_info_types: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param matching_type: How the rule is applied. See the documentation for more information: https://cloud.google.com/dlp/docs/reference/rest/v2/InspectConfig#MatchingType Possible values: ["MATCHING_TYPE_FULL_MATCH", "MATCHING_TYPE_PARTIAL_MATCH", "MATCHING_TYPE_INVERSE_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#matching_type GoogleDataLossPreventionInspectTemplate#matching_type}
        :param dictionary: dictionary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#dictionary GoogleDataLossPreventionInspectTemplate#dictionary}
        :param exclude_by_hotword: exclude_by_hotword block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_by_hotword GoogleDataLossPreventionInspectTemplate#exclude_by_hotword}
        :param exclude_info_types: exclude_info_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#exclude_info_types GoogleDataLossPreventionInspectTemplate#exclude_info_types}
        :param regex: regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#regex GoogleDataLossPreventionInspectTemplate#regex}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule(
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
        hotword_regex: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]],
        likelihood_adjustment: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]],
        proximity: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hotword_regex: hotword_regex block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#hotword_regex GoogleDataLossPreventionInspectTemplate#hotword_regex}
        :param likelihood_adjustment: likelihood_adjustment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#likelihood_adjustment GoogleDataLossPreventionInspectTemplate#likelihood_adjustment}
        :param proximity: proximity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#proximity GoogleDataLossPreventionInspectTemplate#proximity}
        '''
        value = GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule(
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
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference, jsii.get(self, "exclusionRule"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRule")
    def hotword_rule(
        self,
    ) -> GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference:
        return typing.cast(GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference, jsii.get(self, "hotwordRule"))

    @builtins.property
    @jsii.member(jsii_name="exclusionRuleInput")
    def exclusion_rule_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule], jsii.get(self, "exclusionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="hotwordRuleInput")
    def hotword_rule_input(
        self,
    ) -> typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule]:
        return typing.cast(typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule], jsii.get(self, "hotwordRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2e81ac3ff2c6ef2de54eb72a200cacc921586623cc0963277669037b8cb231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataLossPreventionInspectTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#create GoogleDataLossPreventionInspectTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#delete GoogleDataLossPreventionInspectTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#update GoogleDataLossPreventionInspectTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48d863788419d6eb4d91ff82be0e7e45477c566bc328ad98ab455b7b51bc97e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#create GoogleDataLossPreventionInspectTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#delete GoogleDataLossPreventionInspectTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_loss_prevention_inspect_template#update GoogleDataLossPreventionInspectTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataLossPreventionInspectTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataLossPreventionInspectTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataLossPreventionInspectTemplate.GoogleDataLossPreventionInspectTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3c84fbdee5e7d5c624300d38b1417d4bff694e409c8c64ca421707061dd9dea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ec5522b5fe6cf05425bf401645016de29cd970c33d855c6825bc8c318ae5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8977e6d53e519effb9025a76d58ce54b80cffc22fb24b38c1811d9e61f08451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80666f5ca4825b124ca5ade8b9630a7cef78740f6ad8c69020eb8bc38dcf7a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1481a12349996d1c97268e18c9fdfffd146d99aeb82aefe26f5e0505dc4ff291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataLossPreventionInspectTemplate",
    "GoogleDataLossPreventionInspectTemplateConfig",
    "GoogleDataLossPreventionInspectTemplateInspectConfig",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePathOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStructOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScoreOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegexOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredTypeOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType",
    "GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateTypeOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes",
    "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore",
    "GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimits",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScoreOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigLimitsOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePathOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStructOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegexOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximityOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScoreOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegexOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegexOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustmentOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximityOutputReference",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesList",
    "GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesOutputReference",
    "GoogleDataLossPreventionInspectTemplateTimeouts",
    "GoogleDataLossPreventionInspectTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f103ff1da08637f8d6abc72f77463ec9bdbe67f5e109e8d39056406159a47ea8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    parent: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_config: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__79da7c3860b6a60bbfb3f096f310fd2739d0c21b1cebbdf417d1500184ec24aa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e034cd9368bd1b9bd7e3a0236694a1a57b923826e8a1635a73e23678da1af57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04db4281e862d05f52816629fd234c67a00782feecc15ab41ba465330190a6b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb748014957aa2b65a4131b30f67417a49ff5dfa80bb208b1c1affceec22c05f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a176a5358f5f1ea9eca2f3359b571501257e73c88912881851518e2cd969be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98362cce9d1c1c21b14f59a81373318bc70a1fad52f6efb7cdce865cc171cd8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde1ba894bdafec5d7af05c5048d8e78a5a63d88d2117910f1920e01cc1815b8(
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
    inspect_config: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b30d67ddebcffc9eafb240b2e8b6585ada3edf1e4a116ee70c8d8425cb50523(
    *,
    content_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclude_info_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_quote: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    info_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    limits: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    min_likelihood: typing.Optional[builtins.str] = None,
    rule_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34c7a831c8a87f1a8632320b2834be3d9b6ddeb2d3d8df48bcae90dba37c63c(
    *,
    info_type: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType, typing.Dict[builtins.str, typing.Any]],
    dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusion_type: typing.Optional[builtins.str] = None,
    likelihood: typing.Optional[builtins.str] = None,
    regex: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    stored_type: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType, typing.Dict[builtins.str, typing.Any]]] = None,
    surrogate_type: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299e2956b8e644a0ab7b6f26ccede6a33075fcc39e0060455834d6d778ed79c3(
    *,
    cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a70d5ef26e6232c8ad21104e5ad44cd259e807bc102bb9b49c03e54046969ad(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af5c9e706d23acc11be7e7dedbaad913ef46731b7ceaf35eac4271f9886e133(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f4597e4f1ffe74757bfe970b9ba8674a479e1c5a5d80e7be04dd703d9080d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54a2de392e03b4a1858e0c48d23360cf5d8deb76b1caabcaa24340e5b933d70(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47acfa5a98caee273c31b4d4a9204c931a5ede0ab1d1bc4ccedf5987d49a269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a660e3cf26ed9c95aa86d5ef1c456eebc3f644b08c9812caa54d451e1b2992af(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c0a0e591e9c95e06cc45b747c533e2ae19d2cb27347a3e46bd37aba1565602(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed638c796c36da19ba9dc59ea0327599563c1d73128af83c85c0401d5f4873e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4147c2dbe1c106dbfad6fd0599b78a42ae769e9eb628f2ffa9342aab845fed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b425f3b7d42d86e44090d4ba0f02cf948ed925f601241bcd294d20d12ba2dcb9(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cf3d914f580f4a4f848afbea2aea8e693112841bd728f894dfcb2d6344f412(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8199e84718ddb44e5fd6a3caab314c56e7dee5f909681491128735299af3046(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b0c414a08f22f81140cccff0c8d60d9c4bc0eb8235155d420a97e2980a3ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ae97dc661cf6c0bcdf1cb54d3e05c264b90904bbd3a3c4d57bf7fecb9a7439(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002a5cc78cd417577c78104588cdd5d61571f55bb50f9f109753eb4146d734b2(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9a29adec81866e519f63acf59c9fbad30581ff4d4a34594018abea57cd8830(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094a4ad7c696eae1635efe5b3da61f87c026df5f435a519eab11c501a7734ed5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10351dadb08f5387affd2dde963ba64489d01299d972ba7250bd273f0b14dc41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e99a1ffa752688c0aee86144dbce5602f81804e8ae3b41530e0b8eb2c3d6685(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a3668a1f935ebd13d4c77caaeffdcae7bb79b73dc31fb76c0105001db18ef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667b60cfd414a96b206d5d3571ca6492c91f90d1d5477578769099ae75556353(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce52076390cca56712418f765c838a84d600743401f4e4ec5fa7070780736ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b7622286a587b434c5f05247a3f7e3f8c8c245eb429ad9bd780915c0a0763e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a7d6a2e54fe6bc1ef7abe099b61cc8a99f06193697a0405d5261c15c8bde96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10a0ba8d65be39c6d304779202f18496c4f80699b7eb3c7b5fd1ae982840e3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d161556534e0cd2b3d7e08cca4f470d76baf11a44dc163d4782a093a2a7900a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3878f229ccab3210a36465096046d389b4a164e5fa935424493abbbe3c760290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b9502d61ee092e4c4a0e4fd530b5121046c7cfd2d0ad7f40f2cacbf77bef54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd2a1cd49fb4d7f8940a81bdae26b4b900c517e169c93c8e4b73ddca9d3cc66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4894c147dc86ff480ad2bd62bca1ee95d19eca1402871baf8f31d6b9d1482248(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876c7db9ffb2d024ffbc11e81a8e64e8312a6c0af74e15d374e7b0a5248725b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23ee53832a565e9369f186acac91f2f459c7d5095857d187373ca46d63146f0(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7741e0194865f01e1570db9a0e9e70e90e63aa38e0c2c5675b9df6a3dd7827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8758bd0d973fb82dfd9ef60446bd75e81d9184c1afa38ef2f35abc2bdd41bf(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87926d915ce9debde35f422d3ed902cbd3b8795d2e3ab4a2598eca9fdf926840(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be7111e40f72d36596dd4fe423f1c3f6824511176522c1a5a63df8c776637e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe00eb5f931fb4d73fa4e60faa1bb56fd64d57d605c7dedd796d0bf2227a5ee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea1e5cd724b2e93a2a6ccb27fc08b25db4da2ede925612e95c196f501afd234(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc6f531e5c1e01afdc8cd12c636607b7f25ddddb1b1d6da4791a7fac01efa4a(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf625be13b9547b2eb59f8c7d4bfd954558951b269afec16128e1fd9f17ca25d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2825fa45c36854d42d71b537ada89c88e5709d3034453057fee51ca5b72029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c3607998f34e23f9a4e84276e5499132e4a1b585b4c76adcd2ed43873d476a(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesStoredType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f1f391ce948157c3934b1c19689cca7ec6ac4a6e5ee19c3e364129b0b96499(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8001317d9b1e46e1f1d66dd9bd1cc5052dd52138477a09a0de91f0e6682d1721(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypesSurrogateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80876e69afce67e2b81400902ce097a6e5164f567b1e13907b36932df3cb8153(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af8c32a23340e360b71b7f8b72f5386a95de4b544809642d88b37dadbe71a44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc8a4e4b36aeb221987e0b67058fe21ef00637434b34d744802d9cd457a15ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f132b3e05286b45e26708e10a51e8ea2f08b562622ad77ac7bbf0cf6de9759d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089eec203433153cc62c2da77aeb7bb82698f581a2ddda0c4b82972d506a73a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2e159f0d426fd76ff5b1691540f997ff34248c6de80fa2660b52c4663f59b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cef9bdc8196094a533e5c46244bb3f3e2691e6415e968602381ebbe9734dfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1a512209ad6f4a7d5e1ad083160081b59e8559f366e784d1f09cc48016ecad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b44130b60166b4fbc241b3c578a74fab9a58e5577ebc4fb4787aeca9c43ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f0bc1da658f2677e5ead39955741d6632b937fe8e7c831c4563fa802c95712(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4547c5e00926d020efdd37e1889c056943e6300f56ed3c431be2e64a4bbc98ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d682b62351799823072a04f32c1e9d128aa3887385b8c78860389e896334cb(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bae2159dc60c5ff51532d9feb21ee50204c2879faa925412445b7fa00bfee3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e4a37ed74fb4cea304d5e407792fa32a7c9caefe72f4aa93b22857a01be0b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152d608c6bffa6d3e8d13b6435bc34af671c58247adc75b94589d891f18d53ab(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae35a08bf43e661488872419108aef12c60065d808475d46cd3fa9bff6216a0(
    *,
    max_findings_per_item: jsii.Number,
    max_findings_per_request: jsii.Number,
    max_findings_per_info_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c755349974c88eb9a95cd625d1ede517e764e6792dcbfb47a7b40206d0aa9b(
    *,
    max_findings: jsii.Number,
    info_type: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1995751165870ce1327f2de7b36e181543b451b54d23792cdf1dd292ce6e1bc2(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92271261ba9ae1c9ab3166ae85c287b00f1a8c0d261b6289b1fe711608fb369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d1c65fbaeaf8b2fd77baca44ddd031ad508859bfdc87c0cdf90deeebe6e6b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6280c262dd50098956cb54908d1ca7b7879e701c93c78ee275f256332ecb9138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace4b2b8e8b19c499954ac6b361edf210982e9c16d16fd3739e5b8af6c68dc58(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cfb64d21349863129abd0a424e5a9b6828443d1864f5d250621b94e6488098(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68497e04a820a94dd1759552a8fc933d873d34b845320e0cdbfa909b05cf8115(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2ba04ce5d4c82d07fa933bc6110cbfbf647edc26e48326a2259f3a0282949f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916fd644c44eabe4d35fd171f250bb8469305d47b056af07249d00ea9a6bea3a(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoTypeInfoTypeSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23d26c7d587e1df40d968b947290a2ef1291dc27121fd8dc9e742b9bd665c66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4853b86f310f478ba4d52b907401848735bdfa581763dac4a845579aec0ecbdd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96146dc81d9d590267f86ef1490b57f8e2a8012f7186cd4141a78c5f3ee5f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d40475013a56fe1b7cf2c8e03288b8e6de4f7a8be1e5c12a9c7b2fa232003c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0d2c0b2d96676ce193851fdd55ac025642a972d280e0273b07fb1031cd1236(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8d9f2f797283762dacb2493d7ece4cc7ac079a22044f2e541990e954724a0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f8afb4049e0af57c4187c1733743438e64d6a47e16a3398b92e447664f9aea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7453a2d98f077ba146fcaa17282fd3d2b400ddd101120570ab984daa67fcc5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a470ae69007aceae01c76b33d8b2c436ad4c9cdae7ef2fedb3a61d7573621ac1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9c8351d95ce45f348a488ed21757a57ef9e0720c52f82604ed5dcc52820d2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35577bd101cd2e1a094035bed8df61a164820cff148dc6644497e37ecfde9475(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigLimitsMaxFindingsPerInfoType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e5fed614bfd3213cdd36a61a19ab858fdbdc62640202d74a7005e92be73e58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559a3bb6d67fe57c8baec6b46854a3f3436eae90c62dbf7760c1074ab7714d96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7f95ecace248275c27d675fe333c712414e2ac4f866e742e0f90b16783b442(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5502e30675e4fd6457cdb00656f89d678257f665f296cd7c884ce41130adc91a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6dd62ac71d32f7ea6f1cf4f13e18a4e41eb5d8cf0381de7ea39af9c4e92a44(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigCustomInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab72fa6b96375ace8044969c32b815930a6d10d2eee58505439e5448e31a3be0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd059197f974ca3661f8a53def8286a4c4896001595b279fa5375ba79fe5a4a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da4ba5b0143e08b6e4a698eab79a1e5287bf57e108ba629e94262890fec8160(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754c47a7e03de9190fe9f19ac8f3a4e7ff55b518475471e377741a769141caf3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7391521a2b12154db3c7b29d465212a54fb63dc3e2cc6ba3f0a1ed480ce9c21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f73244c1a07b164b4bedea21f4ad6a3bab66c940d1431f6bc16cd9f37d6fcc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3f42b6601e7199030ca725dee2bcc752024dc797a910be436a8d687f283141(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb3c687005bb10f66ff50506ac419646ebb4d45e7205f4549a3732832cbe97e(
    *,
    info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400e1a0875546fe13e8c9a780a5c22fa4cbb979327c9906b98d7cf924d3001ac(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf57a2458c1d21131caa614ad96ae3972f24144198c0003e0ae8dae8506d0c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603d943a111b0584a0426a0a3348c9415dea2e45bfdca7fb68419d16d827661b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e44c7fd3c5fbf805d098dae05c0a49c95f1c00048d195b89880af05d544808(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0718a4bedcd69b9dd97a2ac785530355d0ae2d1a0d57384fc98253dcba81a4d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467535a21ad5bfe8274a82128b62343bd334b7c0f8ef62326fd7df5c780b8d74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e98cc0fa0f7c8d0627d053b035363bcfbbd7f567e3c8e9e1df9334cf0abc94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3920f871e64bac413ecf1ad1bfa5c31f537a8e0ca2003a370360468d3a8e8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a131d4fd4118f8be1d0cb2671421a3938461afa474e8f6068ccf0385ef99a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37b7f2a5ab798d3b57bb65761e2d348915cc32dbb0021015282c86f75545922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfad68b0cce1f1e4b3bdd80951cb73ca71b30d9fc10d53fa56fee767487f61c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e23879830054712b8f2b6d3e444b09e7f92343a36d94064701bba5260b8ebc(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd9326031683ac929345b475db3e509defd3d3243fa0975ce1e25349f1468a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c1011d8122ef0da7046d4ed9d613944fa04176ce98a9b24630f89398ab52a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27cc69f82a271fe9b27c75d592258439cdcb690779e00e45ff6dd9ce2d512bd(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230ed78ce11f6241cb2b25ad4e3eb77d14274680c871a97debde3bdb84a9bbc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2720b4d68c5c6a9cb497cac6bf138c95c3f48bb3ed901c2fbee80fae6b764f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ebb399cad614a176b0036a33d19681e62dda3bcf727f627659089239d7235f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b42b2da088a5ce6c30bdc6070e069a7249926504c0ca1de48a51f218fa5795(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7082ee3d7398ccd3cf365c3ec204402c75c062812affe9252e3ec8a8f60b9032(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7149e419365fcbe3995c09df8f4380d5c1b6081d8fc26a09449877844db680bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514223bdbfe46449a92ab11d727b374e362208ea990e9a49bf1cdcb9df88b9c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7408fa50875835e4332ecb87c7e62f96bd2f7ecc55700869a1e1029d3d4638b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0ab6ed16a84f7522e208ef02e4bbcb79931101e5dbe10913226630b2620a4c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09104965804ecad9058d105e3e48eebe4d0efa9be9948792e5784514d0bf3c80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1db436982dbcee610d573bffda97a7e59697e8d4ee3ffd28f1d73eff48e803b(
    *,
    exclusion_rule: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule, typing.Dict[builtins.str, typing.Any]]] = None,
    hotword_rule: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd9debc19fc9db273f102b3f78500057157450a0f98174fb3d8e75dae6d9bf2(
    *,
    matching_type: builtins.str,
    dictionary: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_by_hotword: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_info_types: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec69c27be9fbe51fd80ed1a114ceb48e2675d2b2f5db9d251696519567a4c796(
    *,
    cloud_storage_path: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath, typing.Dict[builtins.str, typing.Any]]] = None,
    word_list: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02891eb911cf9f87710b71866865bbac4b6846aabfa5055bbb2a5427e81b79fe(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce88e105070eaa3cf2fe82d43110bf5d3755da6d8f5496fa8c9c0a5e4e14e009(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1442d1fe0936da9ed18d8d5b39cc7d6724946125c60e0a6d3211272822bcc89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfeab57dbdcaf8e648b2e419d84e5796a303f989f3ed2fdde6eb4f2a187b80c9(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryCloudStoragePath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0f051798ebffcf00016bf7f59298a6bd7599573714482e02f3d4db850ab717(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a38c64b546d03a977d91b8273ead2205756c0e9e136acd76305c59802423547(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c91fcaab61fccb488bce5bd772ae833934e6dbed3b49eb2728131b3fc28643(
    *,
    words: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d9781f5bf01c6154dd8c9ab5706c8529d17cdf35543c91cb54bd2ab2dfe5e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fde608c727ba718473a7556028ae1cc2c5bcbf0f8931f6555afe50a340da5b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42c3b6d98cec9306c63da9b9fbed042e5868a4c3090c74bc26860ec62284e3b(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleDictionaryWordListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b55e8aa52489933294a851b2fc9d1ebabd4575e577c8efbf3a15e920bec4e8(
    *,
    hotword_regex: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex, typing.Dict[builtins.str, typing.Any]],
    proximity: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fdd935206f16da45f3002b973361220cf70bbde85014b64e697b4fb70e3bfe(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e536535ba86ba8f26f93271ffed5790a7118c8c556288d840d00921aec583d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7cb46e749122e23e0e78e9c250eeb6b4eda07d35150b1305e4c00a9bdbf214(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f692171bcf772fd53f8d91cd750a4fcaa780652f06fdad5493a6f10cd155db14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b216cd317344f65d071c598f16584cc0e642bf4450547eadad6961de03665cb(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7b64f12a46a20abf9c2fd73a8b01ecf052c8dc221c4d4962c0bee6e5a38f30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0572c5a12a6d6097354b97a0fd89b79afefc65f1d77d95fd5fe7398a184329b8(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b58b1aa01157858fe4284e2b1f7f8540c3e1a40dbc4903166da10fdeec9164(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51607fa27a163556d85df0d8a450d05e475182a9075e7f7d647a8a0df66c3613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6f2f81d47689784340116348d25cafc2db2f1413d0ac18a18b7806e5685b7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade5bc29ed9d982421d78498ef153f79ce8af294920299775f5a5874c98cea40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f88a65ea84365a6685bcab0772bce2b48a8c1bf7b1bf0328b62fdbdaea93ef4(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeByHotwordProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55677a0ad53a4a6b550b18cd46a4bdffe4f10687623f432ba0a2ee89401f30d0(
    *,
    info_types: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef5dcb3b93cdf772209aaccacb1e2fab8a3114fd9e0d7870bcecc471bfa63b7(
    *,
    name: builtins.str,
    sensitivity_score: typing.Optional[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62cf8e72fdbf1d687910ad081f535d188114a2d84e373ba3fcb618f23ee6bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef49175d4e352491e5df1c3a8600c463589fa90d8291902842a62ed46a210287(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f143af99a0320bb8bf4016367776908dac22f1c1b255018ba61e7a4becbaa0aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f03a84b7f6a2cc7d105e27aba16520a4d005ec3564c2757d72fcb10f77adf2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0b0bad44ebdf7d3f685df44a2a878096edea27d090a2db5771cd192f5391b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff3b1fc12d4a432088705553408ada44be9349763a24ff213a877f9a9e86f29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352dcf3fc0ccacd3c57fd843b48501fe74d13ec2180a36a7842ed266d794c3f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0239238b8e30f88a63868c8b1c9c1b9e3c5ffe40a8489a046b88989fd53845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586b824990f659fb1e15a31f72778cb96d87ace197fce6d620592311edda5134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b1fd2b86fa907d91d1e9584354a2f4bdf03272f0e5adc8c62e70d4b63e55a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757398509038bfcb8b931121c18ea95bbc3b4540577ec71f0ee264a668c18e03(
    *,
    score: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ccbaea1d228a3df817a3300e5a3641d1f57e3e6de46b916915c4d8054055a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea0674980e8eb99364b21f3e967b241ce930a7150af1dd1cb47e4d04c3fa252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7d983f81672bf72a30c38038afca2d494882c46e7af5c5b44fb4c44ec6f31b(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypesSensitivityScore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3280d7404e48a185a783337eb8fdb15a0cb6d39c5521182a922694138e810123(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4f2d3c0c9b915004dac0917be56895caa635f56013f0fecfef61650de4aa7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypesInfoTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1f1d9eb14c89ef94af83c83abdc9c020d541a6197ea7df40d64f81d0c6aafa(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleExcludeInfoTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3ba7e9ad62d89d6c1bfb988e8745e99707bce45f474b313d0083d47193edfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f4ff60ca997d61910ee974e1e5c9c54a2c30ca509f4398161d1fc234a013f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a7b3d260d2856929714322bca44289a80cc1dd779f26df7f63c03428e3da91(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2946aada25ac05d8b44377a1ac2240c04d4b20de0d04df2f7c2cc0f0658532(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9db3e07a41bd7da275e5d506d58e10eb9a99ec2e825175c7322f1db5e332d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7db0fd3f86a23dd0736ac57a6865d9abdcf00d26b7e630eff4ac67dc406292e(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d3a595453e004c34c7b843d5938a03536a94ecd32ab6d40e6ce64d37b82f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193148530a5427886de09d7f9f03a74b77a96fd0306025d170f5f9f40ad298f8(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesExclusionRuleRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5063b342f31c42c1e8093782affcceff09a62a3c8ce1490c2e7c26e31ef0030b(
    *,
    hotword_regex: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex, typing.Dict[builtins.str, typing.Any]],
    likelihood_adjustment: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment, typing.Dict[builtins.str, typing.Any]],
    proximity: typing.Union[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb2c0b41ff7f8ddfe21ad21aea2cd8ed56b130e19ae68d8507166a3c8824176(
    *,
    pattern: builtins.str,
    group_indexes: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc69ac3fa2339364344afa6a06609f07d772ae831826f9e63e38ccd8f5640423(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131c871ce60bd7a16bd56b394506f19215b2e2d3e7abc07aea4ba18688d4ed0b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358a076a88fa34eedc9f1524fc38306a04bb57ae2328aae8e4a5ea42868b1f4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d19c65550ee658a80d71fd8d9a446e3a212d6167a2b375689316710dcdd035(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleHotwordRegex],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf99eeda2ce7fc7d797747e0c8cf12f47cc093a2aef1c08cfe1a03778f36a24(
    *,
    fixed_likelihood: typing.Optional[builtins.str] = None,
    relative_likelihood: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b2a09a76bb32b25f27f45a0d4cb48aa5786d169cd030a8ec40142a1a63bd54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd862a12814d156242e15c1b3876375a63900841c3a2e2cdf95ee6efc161253c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e14b87681289deaa40d49de25eb075eb274f6040d808ec27379ffad1abf11d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742086c7fc239e94eddbb0016701188d9c6422d53cfd62a154305f57faaf3924(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleLikelihoodAdjustment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbbc9d201197a15516a9f3b9322f614ffd0cfb30991aba4f53da77d2040f61b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4ac097c8b4fb2984e28386c4fd9807dc7d472ce44f539f098d3994cee06e0a(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953a096caf815fad1b8b106c450c9a4addf9719405504ade17b2af9723b64b93(
    *,
    window_after: typing.Optional[jsii.Number] = None,
    window_before: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9497dffe5c815cb06e73a1748990022618b4ecddb3886ba539d4ae4aba991a3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e25b925205daceafdac391d1e82ef2a319eec5478e09e8b1b75b5e9dc87212d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da095ebcd7e7303f60dfb2d53cf0b9f2e7a61f77c8a980cf75c36ee7e1cf0ed6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4110aea435c9e19004b71917301dd6a48535da99715bcccd97200cfadc2bb6c(
    value: typing.Optional[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRulesHotwordRuleProximity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c007c82ca8cec6ac0866af62f5888a03f1f134221d2e3ed01fcea1f2e86d31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdea00741e7c124a05de2173a0bb855dcb3bd5985f67a39d18bf0d57f5f9165(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1575fbe3302c8e7168b4ad9971ecdb7896f296d429eafbd45aedf518534c085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a26db08fbc466d3d16cc95884268495b0baf475768a5e35b9b8b355b07fcef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ec335816a94e0749e861a428ee7836f42d0b62363ebd1d05482dc338b8d5bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fb06502e64d24edf5f3d073a2fab26b7cb807671cb4972e29cc52a8ca8f3c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b40d3d216b510e7efe208b1b87c012a3385185f32f2e1f285d023befefc84da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2e81ac3ff2c6ef2de54eb72a200cacc921586623cc0963277669037b8cb231(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateInspectConfigRuleSetRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48d863788419d6eb4d91ff82be0e7e45477c566bc328ad98ab455b7b51bc97e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c84fbdee5e7d5c624300d38b1417d4bff694e409c8c64ca421707061dd9dea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ec5522b5fe6cf05425bf401645016de29cd970c33d855c6825bc8c318ae5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8977e6d53e519effb9025a76d58ce54b80cffc22fb24b38c1811d9e61f08451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80666f5ca4825b124ca5ade8b9630a7cef78740f6ad8c69020eb8bc38dcf7a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1481a12349996d1c97268e18c9fdfffd146d99aeb82aefe26f5e0505dc4ff291(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataLossPreventionInspectTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
