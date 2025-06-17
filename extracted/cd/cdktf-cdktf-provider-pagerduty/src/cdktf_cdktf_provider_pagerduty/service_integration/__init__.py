r'''
# `pagerduty_service_integration`

Refer to the Terraform Registry for docs: [`pagerduty_service_integration`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration).
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


class ServiceIntegration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegration",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration pagerduty_service_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service: builtins.str,
        email_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        email_filter_mode: typing.Optional[builtins.str] = None,
        email_incident_creation: typing.Optional[builtins.str] = None,
        email_parser: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParser", typing.Dict[builtins.str, typing.Any]]]]] = None,
        email_parsing_fallback: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_email: typing.Optional[builtins.str] = None,
        integration_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration pagerduty_service_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#service ServiceIntegration#service}.
        :param email_filter: email_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_filter ServiceIntegration#email_filter}
        :param email_filter_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_filter_mode ServiceIntegration#email_filter_mode}.
        :param email_incident_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_incident_creation ServiceIntegration#email_incident_creation}.
        :param email_parser: email_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_parser ServiceIntegration#email_parser}
        :param email_parsing_fallback: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_parsing_fallback ServiceIntegration#email_parsing_fallback}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#id ServiceIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#integration_email ServiceIntegration#integration_email}.
        :param integration_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#integration_key ServiceIntegration#integration_key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#name ServiceIntegration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        :param vendor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#vendor ServiceIntegration#vendor}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3265ee2c5506612ba6f6298fa6edab59088c4bfbad1b666121d042368edb66fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceIntegrationConfig(
            service=service,
            email_filter=email_filter,
            email_filter_mode=email_filter_mode,
            email_incident_creation=email_incident_creation,
            email_parser=email_parser,
            email_parsing_fallback=email_parsing_fallback,
            id=id,
            integration_email=integration_email,
            integration_key=integration_key,
            name=name,
            type=type,
            vendor=vendor,
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
        '''Generates CDKTF code for importing a ServiceIntegration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceIntegration to import.
        :param import_from_id: The id of the existing ServiceIntegration that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceIntegration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d2671bf5df079a7eb59ee1fb4e3abdb8f249edec55ba99a9de6d48ca5028e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEmailFilter")
    def put_email_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d713f9b645a6888268bdcca99204888cc8d12c5f3c7be765c5e314f60f101621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEmailFilter", [value]))

    @jsii.member(jsii_name="putEmailParser")
    def put_email_parser(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParser", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68a2d63bd5264fb257597b2b7431118327a343114bf335fe7fe47536d7d7ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEmailParser", [value]))

    @jsii.member(jsii_name="resetEmailFilter")
    def reset_email_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailFilter", []))

    @jsii.member(jsii_name="resetEmailFilterMode")
    def reset_email_filter_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailFilterMode", []))

    @jsii.member(jsii_name="resetEmailIncidentCreation")
    def reset_email_incident_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailIncidentCreation", []))

    @jsii.member(jsii_name="resetEmailParser")
    def reset_email_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailParser", []))

    @jsii.member(jsii_name="resetEmailParsingFallback")
    def reset_email_parsing_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailParsingFallback", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIntegrationEmail")
    def reset_integration_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationEmail", []))

    @jsii.member(jsii_name="resetIntegrationKey")
    def reset_integration_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationKey", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVendor")
    def reset_vendor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVendor", []))

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
    @jsii.member(jsii_name="emailFilter")
    def email_filter(self) -> "ServiceIntegrationEmailFilterList":
        return typing.cast("ServiceIntegrationEmailFilterList", jsii.get(self, "emailFilter"))

    @builtins.property
    @jsii.member(jsii_name="emailParser")
    def email_parser(self) -> "ServiceIntegrationEmailParserList":
        return typing.cast("ServiceIntegrationEmailParserList", jsii.get(self, "emailParser"))

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlUrl"))

    @builtins.property
    @jsii.member(jsii_name="emailFilterInput")
    def email_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailFilter"]]], jsii.get(self, "emailFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="emailFilterModeInput")
    def email_filter_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailFilterModeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailIncidentCreationInput")
    def email_incident_creation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailIncidentCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="emailParserInput")
    def email_parser_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParser"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParser"]]], jsii.get(self, "emailParserInput"))

    @builtins.property
    @jsii.member(jsii_name="emailParsingFallbackInput")
    def email_parsing_fallback_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailParsingFallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationEmailInput")
    def integration_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationKeyInput")
    def integration_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vendorInput")
    def vendor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vendorInput"))

    @builtins.property
    @jsii.member(jsii_name="emailFilterMode")
    def email_filter_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailFilterMode"))

    @email_filter_mode.setter
    def email_filter_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6595a31bd3aeaeb4cd70ce418f334db96104f2a19e4c3d69885659513ddea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailFilterMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailIncidentCreation")
    def email_incident_creation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailIncidentCreation"))

    @email_incident_creation.setter
    def email_incident_creation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a898f86297062c2304c4056ac9d505c75be009b87de6368ca3b97e2693682c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailIncidentCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailParsingFallback")
    def email_parsing_fallback(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailParsingFallback"))

    @email_parsing_fallback.setter
    def email_parsing_fallback(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b18ff7eaf6599f300155292890bf6078ad4a2557036322b5611498dd184a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailParsingFallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ac86ff7ffb5ccfb109f3073bcd8ea84600941c53809d1c72a7c2283c76b303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationEmail")
    def integration_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationEmail"))

    @integration_email.setter
    def integration_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c473d23f201aa5636c585533818d1ef85da1a41e0d3f62b921e62086ac7dff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationKey")
    def integration_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationKey"))

    @integration_key.setter
    def integration_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf6247f2d73ed76b2981ff901dfc693311ceffde3af5c2352b0cf05ec6de144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41d12a7accb1bdf5b8d114c6677e49a420848400c95977a3b655d1226046d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb31cdb686c176df598aac1aababc30d58485a9354846406fd314a6c2463674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d366fac0e1a2215f0d95f74ae424520c2ec515c518e1a4919ccf28abc3140ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vendor")
    def vendor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vendor"))

    @vendor.setter
    def vendor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec6302b361f69081908015fee637028b327aea9dac32e24c9690041a5562bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vendor", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "service": "service",
        "email_filter": "emailFilter",
        "email_filter_mode": "emailFilterMode",
        "email_incident_creation": "emailIncidentCreation",
        "email_parser": "emailParser",
        "email_parsing_fallback": "emailParsingFallback",
        "id": "id",
        "integration_email": "integrationEmail",
        "integration_key": "integrationKey",
        "name": "name",
        "type": "type",
        "vendor": "vendor",
    },
)
class ServiceIntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service: builtins.str,
        email_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        email_filter_mode: typing.Optional[builtins.str] = None,
        email_incident_creation: typing.Optional[builtins.str] = None,
        email_parser: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParser", typing.Dict[builtins.str, typing.Any]]]]] = None,
        email_parsing_fallback: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_email: typing.Optional[builtins.str] = None,
        integration_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#service ServiceIntegration#service}.
        :param email_filter: email_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_filter ServiceIntegration#email_filter}
        :param email_filter_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_filter_mode ServiceIntegration#email_filter_mode}.
        :param email_incident_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_incident_creation ServiceIntegration#email_incident_creation}.
        :param email_parser: email_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_parser ServiceIntegration#email_parser}
        :param email_parsing_fallback: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_parsing_fallback ServiceIntegration#email_parsing_fallback}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#id ServiceIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#integration_email ServiceIntegration#integration_email}.
        :param integration_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#integration_key ServiceIntegration#integration_key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#name ServiceIntegration#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        :param vendor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#vendor ServiceIntegration#vendor}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b081556899eb1e863483c9e4015a5bacd642df9f1e4cee99568bf27f5d1e4345)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument email_filter", value=email_filter, expected_type=type_hints["email_filter"])
            check_type(argname="argument email_filter_mode", value=email_filter_mode, expected_type=type_hints["email_filter_mode"])
            check_type(argname="argument email_incident_creation", value=email_incident_creation, expected_type=type_hints["email_incident_creation"])
            check_type(argname="argument email_parser", value=email_parser, expected_type=type_hints["email_parser"])
            check_type(argname="argument email_parsing_fallback", value=email_parsing_fallback, expected_type=type_hints["email_parsing_fallback"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument integration_email", value=integration_email, expected_type=type_hints["integration_email"])
            check_type(argname="argument integration_key", value=integration_key, expected_type=type_hints["integration_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
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
        if email_filter is not None:
            self._values["email_filter"] = email_filter
        if email_filter_mode is not None:
            self._values["email_filter_mode"] = email_filter_mode
        if email_incident_creation is not None:
            self._values["email_incident_creation"] = email_incident_creation
        if email_parser is not None:
            self._values["email_parser"] = email_parser
        if email_parsing_fallback is not None:
            self._values["email_parsing_fallback"] = email_parsing_fallback
        if id is not None:
            self._values["id"] = id
        if integration_email is not None:
            self._values["integration_email"] = integration_email
        if integration_key is not None:
            self._values["integration_key"] = integration_key
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type
        if vendor is not None:
            self._values["vendor"] = vendor

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
    def service(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#service ServiceIntegration#service}.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailFilter"]]]:
        '''email_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_filter ServiceIntegration#email_filter}
        '''
        result = self._values.get("email_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailFilter"]]], result)

    @builtins.property
    def email_filter_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_filter_mode ServiceIntegration#email_filter_mode}.'''
        result = self._values.get("email_filter_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_incident_creation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_incident_creation ServiceIntegration#email_incident_creation}.'''
        result = self._values.get("email_incident_creation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_parser(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParser"]]]:
        '''email_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_parser ServiceIntegration#email_parser}
        '''
        result = self._values.get("email_parser")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParser"]]], result)

    @builtins.property
    def email_parsing_fallback(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#email_parsing_fallback ServiceIntegration#email_parsing_fallback}.'''
        result = self._values.get("email_parsing_fallback")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#id ServiceIntegration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#integration_email ServiceIntegration#integration_email}.'''
        result = self._values.get("integration_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#integration_key ServiceIntegration#integration_key}.'''
        result = self._values.get("integration_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#name ServiceIntegration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vendor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#vendor ServiceIntegration#vendor}.'''
        result = self._values.get("vendor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailFilter",
    jsii_struct_bases=[],
    name_mapping={
        "body_mode": "bodyMode",
        "body_regex": "bodyRegex",
        "from_email_mode": "fromEmailMode",
        "from_email_regex": "fromEmailRegex",
        "subject_mode": "subjectMode",
        "subject_regex": "subjectRegex",
    },
)
class ServiceIntegrationEmailFilter:
    def __init__(
        self,
        *,
        body_mode: typing.Optional[builtins.str] = None,
        body_regex: typing.Optional[builtins.str] = None,
        from_email_mode: typing.Optional[builtins.str] = None,
        from_email_regex: typing.Optional[builtins.str] = None,
        subject_mode: typing.Optional[builtins.str] = None,
        subject_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param body_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#body_mode ServiceIntegration#body_mode}.
        :param body_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#body_regex ServiceIntegration#body_regex}.
        :param from_email_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#from_email_mode ServiceIntegration#from_email_mode}.
        :param from_email_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#from_email_regex ServiceIntegration#from_email_regex}.
        :param subject_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#subject_mode ServiceIntegration#subject_mode}.
        :param subject_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#subject_regex ServiceIntegration#subject_regex}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad0238f631d306435845d8c33b3f01ac25e9d9fbf4fc06f3cef40db54fef070)
            check_type(argname="argument body_mode", value=body_mode, expected_type=type_hints["body_mode"])
            check_type(argname="argument body_regex", value=body_regex, expected_type=type_hints["body_regex"])
            check_type(argname="argument from_email_mode", value=from_email_mode, expected_type=type_hints["from_email_mode"])
            check_type(argname="argument from_email_regex", value=from_email_regex, expected_type=type_hints["from_email_regex"])
            check_type(argname="argument subject_mode", value=subject_mode, expected_type=type_hints["subject_mode"])
            check_type(argname="argument subject_regex", value=subject_regex, expected_type=type_hints["subject_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body_mode is not None:
            self._values["body_mode"] = body_mode
        if body_regex is not None:
            self._values["body_regex"] = body_regex
        if from_email_mode is not None:
            self._values["from_email_mode"] = from_email_mode
        if from_email_regex is not None:
            self._values["from_email_regex"] = from_email_regex
        if subject_mode is not None:
            self._values["subject_mode"] = subject_mode
        if subject_regex is not None:
            self._values["subject_regex"] = subject_regex

    @builtins.property
    def body_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#body_mode ServiceIntegration#body_mode}.'''
        result = self._values.get("body_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def body_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#body_regex ServiceIntegration#body_regex}.'''
        result = self._values.get("body_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_email_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#from_email_mode ServiceIntegration#from_email_mode}.'''
        result = self._values.get("from_email_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_email_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#from_email_regex ServiceIntegration#from_email_regex}.'''
        result = self._values.get("from_email_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#subject_mode ServiceIntegration#subject_mode}.'''
        result = self._values.get("subject_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#subject_regex ServiceIntegration#subject_regex}.'''
        result = self._values.get("subject_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationEmailFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIntegrationEmailFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2df4c5203268eab713efa69c46c35d4db4165d60f885d7abfb36e57b157aaf15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceIntegrationEmailFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b934075963cd26035ee665ca8e4b8a77fcfe16d9019c7eaba5724a63a51edcae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceIntegrationEmailFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f118a6c8df1e15c5ad4cff123afac2019d30650802213f4e9d6bf450d8d45d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d3a14bc5c426ba4d998b8dc6f5c3353032e28c7b5171189a06434a811f6daa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f465495c82bc01d28d3e2f57974aeae03d5e774096b248373c2346918effca52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b6513a48eb17e167f6548bec5e823fcc9061cd5496ba0c2cd72b7cd1751179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceIntegrationEmailFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcabc6070d821ed2adca083c5b6415c3daf8d069437e2bd1e774b5263b46b4b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBodyMode")
    def reset_body_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyMode", []))

    @jsii.member(jsii_name="resetBodyRegex")
    def reset_body_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyRegex", []))

    @jsii.member(jsii_name="resetFromEmailMode")
    def reset_from_email_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromEmailMode", []))

    @jsii.member(jsii_name="resetFromEmailRegex")
    def reset_from_email_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromEmailRegex", []))

    @jsii.member(jsii_name="resetSubjectMode")
    def reset_subject_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMode", []))

    @jsii.member(jsii_name="resetSubjectRegex")
    def reset_subject_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectRegex", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="bodyModeInput")
    def body_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyRegexInput")
    def body_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="fromEmailModeInput")
    def from_email_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromEmailModeInput"))

    @builtins.property
    @jsii.member(jsii_name="fromEmailRegexInput")
    def from_email_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromEmailRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectModeInput")
    def subject_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectModeInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectRegexInput")
    def subject_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyMode")
    def body_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bodyMode"))

    @body_mode.setter
    def body_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8775d65935751f43edcc2e7f577995cc5af14f53adec2e788c6f8f8231e1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bodyRegex")
    def body_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bodyRegex"))

    @body_regex.setter
    def body_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86e1aacfb7126ad4a603ec7ec6f17f75b34eaf7c9c9519a3e7d3a1737aab64e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fromEmailMode")
    def from_email_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromEmailMode"))

    @from_email_mode.setter
    def from_email_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727dee8430f856cfeccc7f4e6ead883ea55be8db2168b8f156acbb6533036bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromEmailMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fromEmailRegex")
    def from_email_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromEmailRegex"))

    @from_email_regex.setter
    def from_email_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce655edea3777d270096b6d7572585e181f0f856edf7aac9a9e151dd61d2c277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromEmailRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectMode")
    def subject_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMode"))

    @subject_mode.setter
    def subject_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fda141024e0415a09d87a265ad73be8a4bba08aede3fae5554b81dfe299edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectRegex")
    def subject_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectRegex"))

    @subject_regex.setter
    def subject_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a232a1185c6a02102dc324f003e32aa606bbdcaaa9a6878924242777e1031148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c756fa180c309f0600efa324390923eccf672e5addeb28d38e4abc40ea3c5588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParser",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match_predicate": "matchPredicate",
        "value_extractor": "valueExtractor",
    },
)
class ServiceIntegrationEmailParser:
    def __init__(
        self,
        *,
        action: builtins.str,
        match_predicate: typing.Union["ServiceIntegrationEmailParserMatchPredicate", typing.Dict[builtins.str, typing.Any]],
        value_extractor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParserValueExtractor", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#action ServiceIntegration#action}.
        :param match_predicate: match_predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#match_predicate ServiceIntegration#match_predicate}
        :param value_extractor: value_extractor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#value_extractor ServiceIntegration#value_extractor}
        '''
        if isinstance(match_predicate, dict):
            match_predicate = ServiceIntegrationEmailParserMatchPredicate(**match_predicate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ecbe672d232528fafb619c9dbef092efc0e8efa64c0a28316c6d5a20e2202e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match_predicate", value=match_predicate, expected_type=type_hints["match_predicate"])
            check_type(argname="argument value_extractor", value=value_extractor, expected_type=type_hints["value_extractor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match_predicate": match_predicate,
        }
        if value_extractor is not None:
            self._values["value_extractor"] = value_extractor

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#action ServiceIntegration#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_predicate(self) -> "ServiceIntegrationEmailParserMatchPredicate":
        '''match_predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#match_predicate ServiceIntegration#match_predicate}
        '''
        result = self._values.get("match_predicate")
        assert result is not None, "Required property 'match_predicate' is missing"
        return typing.cast("ServiceIntegrationEmailParserMatchPredicate", result)

    @builtins.property
    def value_extractor(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserValueExtractor"]]]:
        '''value_extractor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#value_extractor ServiceIntegration#value_extractor}
        '''
        result = self._values.get("value_extractor")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserValueExtractor"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationEmailParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIntegrationEmailParserList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5857e71f93ca4461ab382af742304bd1522c42b24c1dd91d3b02bcd195a39537)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceIntegrationEmailParserOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d628d7d8e9b7c8bccc813e7ae7c5137eec0c6721f18926a6bdd5c7fd4daa0a36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceIntegrationEmailParserOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d952adaae25aa6de517e1f468ffeede856882990840750bd968b009a864c066)
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
            type_hints = typing.get_type_hints(_typecheckingstub__519e7dbc257d60929ee3b6070ece7ddc133726c8aca98da5710bf04505b2d910)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb7943dae864716b75c8b53885177bb74cef2c4e35a0d8acb43d34a41b72ceb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParser]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParser]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParser]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5e25c7e686afb79be82ad61b70ffd018d405ab33908c10ec8bb4bc2598fae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicate",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "predicate": "predicate"},
)
class ServiceIntegrationEmailParserMatchPredicate:
    def __init__(
        self,
        *,
        type: builtins.str,
        predicate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParserMatchPredicatePredicate", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#predicate ServiceIntegration#predicate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee283bacec3e82a3cb11f1a7bc2ba09e0e6cd68279092d4dc9686210d38a41e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if predicate is not None:
            self._values["predicate"] = predicate

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def predicate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicate"]]]:
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#predicate ServiceIntegration#predicate}
        '''
        result = self._values.get("predicate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicate"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationEmailParserMatchPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIntegrationEmailParserMatchPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa1625db303ac3c8e78882eee2c70943d20e36139d26e05ddb4628432b9b3604)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPredicate")
    def put_predicate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParserMatchPredicatePredicate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0afe478856c73da80805276dae0e0378732c03c7f6806824f00d21b87144ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPredicate", [value]))

    @jsii.member(jsii_name="resetPredicate")
    def reset_predicate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredicate", []))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> "ServiceIntegrationEmailParserMatchPredicatePredicateList":
        return typing.cast("ServiceIntegrationEmailParserMatchPredicatePredicateList", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicate"]]], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2389f31b8f2bf576414691cdababb871b1231028d896447b7f91e028bda25e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceIntegrationEmailParserMatchPredicate]:
        return typing.cast(typing.Optional[ServiceIntegrationEmailParserMatchPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceIntegrationEmailParserMatchPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65750e4ffc33af9b46b17a578b204fde3b07e0bf51bc429b9685f05e979552d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicatePredicate",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "matcher": "matcher",
        "part": "part",
        "predicate": "predicate",
    },
)
class ServiceIntegrationEmailParserMatchPredicatePredicate:
    def __init__(
        self,
        *,
        type: builtins.str,
        matcher: typing.Optional[builtins.str] = None,
        part: typing.Optional[builtins.str] = None,
        predicate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParserMatchPredicatePredicatePredicate", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        :param matcher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#matcher ServiceIntegration#matcher}.
        :param part: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#part ServiceIntegration#part}.
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#predicate ServiceIntegration#predicate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a83f8d13eec4ccd17d187c3401988ff2b12bb13176d07eba6a0911c3fbdb64b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument part", value=part, expected_type=type_hints["part"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if matcher is not None:
            self._values["matcher"] = matcher
        if part is not None:
            self._values["part"] = part
        if predicate is not None:
            self._values["predicate"] = predicate

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def matcher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#matcher ServiceIntegration#matcher}.'''
        result = self._values.get("matcher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def part(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#part ServiceIntegration#part}.'''
        result = self._values.get("part")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predicate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicatePredicate"]]]:
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#predicate ServiceIntegration#predicate}
        '''
        result = self._values.get("predicate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicatePredicate"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationEmailParserMatchPredicatePredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIntegrationEmailParserMatchPredicatePredicateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicatePredicateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe9d07c9849a683645af7a3220ce96c56b693ac45665ff6f783cab5eb0f00750)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceIntegrationEmailParserMatchPredicatePredicateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475e6b2ce368b9d466e757327f26b708de8c7fb136e5c481b563456beff28ac6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceIntegrationEmailParserMatchPredicatePredicateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e028f68fc48fe025f6d8b1131bf00bf8aa1fb5896b947f8573794a18f9511cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dc73153ce2ecb16f94462aa070b2c60c49abe13d56f297f5d74911124344d60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb510d215dbd084d4e7903ffaa3427a596908ffaf86e43a7721a48fd5ad71e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579ce5dc7ab07c24cbb292b9fea257bd8ba1bbae020d0e96d1c538d47110de97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceIntegrationEmailParserMatchPredicatePredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicatePredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4171f38804421ac144de9e703def4730aad9679c5301aface3dc20dfc183f2cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPredicate")
    def put_predicate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParserMatchPredicatePredicatePredicate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ccad8f33447a122b24f55a5e390ffa4629f67e1b4e3617a1e122fce43e518b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPredicate", [value]))

    @jsii.member(jsii_name="resetMatcher")
    def reset_matcher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatcher", []))

    @jsii.member(jsii_name="resetPart")
    def reset_part(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPart", []))

    @jsii.member(jsii_name="resetPredicate")
    def reset_predicate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredicate", []))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "ServiceIntegrationEmailParserMatchPredicatePredicatePredicateList":
        return typing.cast("ServiceIntegrationEmailParserMatchPredicatePredicatePredicateList", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="matcherInput")
    def matcher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matcherInput"))

    @builtins.property
    @jsii.member(jsii_name="partInput")
    def part_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicatePredicate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserMatchPredicatePredicatePredicate"]]], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="matcher")
    def matcher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matcher"))

    @matcher.setter
    def matcher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac1e42e4590feee9a2e7a325d265d1d38bd664a781da65a38ccd1c73b3aa0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matcher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="part")
    def part(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "part"))

    @part.setter
    def part(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb877c0b92f820f5d7a05bf72bcd5cdbd1ba8132a0374c2229b8871c0cd4c419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "part", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64fec4a37a9651ed0daeb7d9d20b499d3ecf37ca64206c34bf20b0a4730631e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84665d50562b69937d7abda5787c3597f26e071255cf91da4f6a3657dc1a153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicatePredicatePredicate",
    jsii_struct_bases=[],
    name_mapping={"matcher": "matcher", "part": "part", "type": "type"},
)
class ServiceIntegrationEmailParserMatchPredicatePredicatePredicate:
    def __init__(
        self,
        *,
        matcher: builtins.str,
        part: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param matcher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#matcher ServiceIntegration#matcher}.
        :param part: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#part ServiceIntegration#part}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda4b9e769f618ae79431c3418d50b4c12b5b5ae2b0ebac30ebf0e48d738cef1)
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument part", value=part, expected_type=type_hints["part"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matcher": matcher,
            "part": part,
            "type": type,
        }

    @builtins.property
    def matcher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#matcher ServiceIntegration#matcher}.'''
        result = self._values.get("matcher")
        assert result is not None, "Required property 'matcher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def part(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#part ServiceIntegration#part}.'''
        result = self._values.get("part")
        assert result is not None, "Required property 'part' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationEmailParserMatchPredicatePredicatePredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIntegrationEmailParserMatchPredicatePredicatePredicateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicatePredicatePredicateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4131755b445659cbbfd7b4cc658f9bb52cc30cd64ff6fd068bb6a438ecc0d10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceIntegrationEmailParserMatchPredicatePredicatePredicateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89dcd78e3be781f05c6c1da273483cfd19a79c4050c0c622ccc3551d727dca26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceIntegrationEmailParserMatchPredicatePredicatePredicateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62b9154d357c6111ede5dbe30e49d1d057590c40ac3c2edb5315d317861eca0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__286f152e0c97f131d44dac356ff6f0da624741264f7c23a5cfba7ba47d0d3efb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff7ca8dfb7a1b32f9e0873be32413cf81c3b3304ace1fb86c6131c11cb4bd42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca596e4e9f2d08d5b04f8b78b4f1413ae3aeaef90f16b96120f3aaea4e6af7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceIntegrationEmailParserMatchPredicatePredicatePredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserMatchPredicatePredicatePredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e39a21ef607d296ac55561f80dab2c9f0655d04536b02316b50f29955b930623)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="matcherInput")
    def matcher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matcherInput"))

    @builtins.property
    @jsii.member(jsii_name="partInput")
    def part_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="matcher")
    def matcher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matcher"))

    @matcher.setter
    def matcher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4a3a3a0d9fd13677142c88992dd79022632a90291b1520a39029bc7b800230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matcher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="part")
    def part(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "part"))

    @part.setter
    def part(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13c46f9fc033db347624b165a3f21c2fa3060438f0652fbf195b3104585c9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "part", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc80b72cf5ddf7e09e5512d84180c5c38e025f9214b6f5ac13a880f7b0d00f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ab99d63164ce7f1065035fa446abe736e46c55fcbbdfed3f36a357170d4c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceIntegrationEmailParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba8399c5edef1669f41e421a25d8e24efc97fcfe86c10d6d2862b204c44a149e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchPredicate")
    def put_match_predicate(
        self,
        *,
        type: builtins.str,
        predicate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserMatchPredicatePredicate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#predicate ServiceIntegration#predicate}
        '''
        value = ServiceIntegrationEmailParserMatchPredicate(
            type=type, predicate=predicate
        )

        return typing.cast(None, jsii.invoke(self, "putMatchPredicate", [value]))

    @jsii.member(jsii_name="putValueExtractor")
    def put_value_extractor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceIntegrationEmailParserValueExtractor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c5972dc715e80785425a04f43675ea2d55591c18bd75cd58ebe33e252d62ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putValueExtractor", [value]))

    @jsii.member(jsii_name="resetValueExtractor")
    def reset_value_extractor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueExtractor", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="matchPredicate")
    def match_predicate(
        self,
    ) -> ServiceIntegrationEmailParserMatchPredicateOutputReference:
        return typing.cast(ServiceIntegrationEmailParserMatchPredicateOutputReference, jsii.get(self, "matchPredicate"))

    @builtins.property
    @jsii.member(jsii_name="valueExtractor")
    def value_extractor(self) -> "ServiceIntegrationEmailParserValueExtractorList":
        return typing.cast("ServiceIntegrationEmailParserValueExtractorList", jsii.get(self, "valueExtractor"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchPredicateInput")
    def match_predicate_input(
        self,
    ) -> typing.Optional[ServiceIntegrationEmailParserMatchPredicate]:
        return typing.cast(typing.Optional[ServiceIntegrationEmailParserMatchPredicate], jsii.get(self, "matchPredicateInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExtractorInput")
    def value_extractor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserValueExtractor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceIntegrationEmailParserValueExtractor"]]], jsii.get(self, "valueExtractorInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66df8226dee8ba930eb558e5f68df5961103f5939d05f72545c3fc19ea128dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParser]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParser]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParser]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3d3d0c90f8831f39681c0de8731e2dafd8457daeb773779b0b8d4b29c3939b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserValueExtractor",
    jsii_struct_bases=[],
    name_mapping={
        "part": "part",
        "type": "type",
        "value_name": "valueName",
        "ends_before": "endsBefore",
        "regex": "regex",
        "starts_after": "startsAfter",
    },
)
class ServiceIntegrationEmailParserValueExtractor:
    def __init__(
        self,
        *,
        part: builtins.str,
        type: builtins.str,
        value_name: builtins.str,
        ends_before: typing.Optional[builtins.str] = None,
        regex: typing.Optional[builtins.str] = None,
        starts_after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param part: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#part ServiceIntegration#part}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.
        :param value_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#value_name ServiceIntegration#value_name}.
        :param ends_before: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#ends_before ServiceIntegration#ends_before}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#regex ServiceIntegration#regex}.
        :param starts_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#starts_after ServiceIntegration#starts_after}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89af65eb7c799f43315d773c6b8fec02d0a64bc8ad70c169cd0fcb22faa1e3d0)
            check_type(argname="argument part", value=part, expected_type=type_hints["part"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value_name", value=value_name, expected_type=type_hints["value_name"])
            check_type(argname="argument ends_before", value=ends_before, expected_type=type_hints["ends_before"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument starts_after", value=starts_after, expected_type=type_hints["starts_after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "part": part,
            "type": type,
            "value_name": value_name,
        }
        if ends_before is not None:
            self._values["ends_before"] = ends_before
        if regex is not None:
            self._values["regex"] = regex
        if starts_after is not None:
            self._values["starts_after"] = starts_after

    @builtins.property
    def part(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#part ServiceIntegration#part}.'''
        result = self._values.get("part")
        assert result is not None, "Required property 'part' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#type ServiceIntegration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#value_name ServiceIntegration#value_name}.'''
        result = self._values.get("value_name")
        assert result is not None, "Required property 'value_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ends_before(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#ends_before ServiceIntegration#ends_before}.'''
        result = self._values.get("ends_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#regex ServiceIntegration#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starts_after(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_integration#starts_after ServiceIntegration#starts_after}.'''
        result = self._values.get("starts_after")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIntegrationEmailParserValueExtractor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIntegrationEmailParserValueExtractorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserValueExtractorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1059cb398988d29b4d4bea1f713462a95a01e4343e1141fc3db600c8698e7f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceIntegrationEmailParserValueExtractorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435efccfd732bcc943ef6c1763df692863eae2d4321232c742426624a325e427)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceIntegrationEmailParserValueExtractorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35406bcce65a082857e0b85434472ac5555523de8777fce4cf9e758d41910b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c24a74c51e20171f0439f67a5d5446725b1509ea77bd104e86f5f272529d9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0db423961e09f9656b8a9b2ac3b4bfb6c0c4f88df22ed73be778a53e8a20fc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserValueExtractor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserValueExtractor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserValueExtractor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d33368091e9910cd6875c0b614b9eaf5f8bd0fc87d735ba3817b66f66e5150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceIntegrationEmailParserValueExtractorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceIntegration.ServiceIntegrationEmailParserValueExtractorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9a0327dc0c2e5c5cffe503b2106b34c2d8248214902a2faefbc54d4caf81aa3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEndsBefore")
    def reset_ends_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndsBefore", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetStartsAfter")
    def reset_starts_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartsAfter", []))

    @builtins.property
    @jsii.member(jsii_name="endsBeforeInput")
    def ends_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endsBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="partInput")
    def part_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="startsAfterInput")
    def starts_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startsAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueNameInput")
    def value_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endsBefore")
    def ends_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endsBefore"))

    @ends_before.setter
    def ends_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2d1ccfe09d4ee456b6af52432aec00bb402d416592c67c2e0fee261c73e8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endsBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="part")
    def part(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "part"))

    @part.setter
    def part(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da54361000009cf2bff514c7b2e2c194c49651c34b82fbab548610a76b6b33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "part", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d30b867c66ac849215cf2350eebc7a5b710509516592f5bba4cf80472520df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startsAfter")
    def starts_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startsAfter"))

    @starts_after.setter
    def starts_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6259ade1b7e1ef8dbb7f123293eb5cc3c674251df1413643ebf1e69fdd75697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startsAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc43b6cce9087e365af68e742f4f31195b5f5f87a9a3a1345fcc8423a17477b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueName")
    def value_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueName"))

    @value_name.setter
    def value_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c3d11f8b8c527a48c9bcda83499c2afef12cd0da24478b86ddb77f2841d15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserValueExtractor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserValueExtractor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserValueExtractor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ccc0fdf23327cfefb8ebf1cbd233b19425ec86eeeb7375a1fbedc8dee880ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceIntegration",
    "ServiceIntegrationConfig",
    "ServiceIntegrationEmailFilter",
    "ServiceIntegrationEmailFilterList",
    "ServiceIntegrationEmailFilterOutputReference",
    "ServiceIntegrationEmailParser",
    "ServiceIntegrationEmailParserList",
    "ServiceIntegrationEmailParserMatchPredicate",
    "ServiceIntegrationEmailParserMatchPredicateOutputReference",
    "ServiceIntegrationEmailParserMatchPredicatePredicate",
    "ServiceIntegrationEmailParserMatchPredicatePredicateList",
    "ServiceIntegrationEmailParserMatchPredicatePredicateOutputReference",
    "ServiceIntegrationEmailParserMatchPredicatePredicatePredicate",
    "ServiceIntegrationEmailParserMatchPredicatePredicatePredicateList",
    "ServiceIntegrationEmailParserMatchPredicatePredicatePredicateOutputReference",
    "ServiceIntegrationEmailParserOutputReference",
    "ServiceIntegrationEmailParserValueExtractor",
    "ServiceIntegrationEmailParserValueExtractorList",
    "ServiceIntegrationEmailParserValueExtractorOutputReference",
]

publication.publish()

def _typecheckingstub__3265ee2c5506612ba6f6298fa6edab59088c4bfbad1b666121d042368edb66fe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service: builtins.str,
    email_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email_filter_mode: typing.Optional[builtins.str] = None,
    email_incident_creation: typing.Optional[builtins.str] = None,
    email_parser: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParser, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email_parsing_fallback: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_email: typing.Optional[builtins.str] = None,
    integration_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    vendor: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__46d2671bf5df079a7eb59ee1fb4e3abdb8f249edec55ba99a9de6d48ca5028e0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d713f9b645a6888268bdcca99204888cc8d12c5f3c7be765c5e314f60f101621(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68a2d63bd5264fb257597b2b7431118327a343114bf335fe7fe47536d7d7ee7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParser, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6595a31bd3aeaeb4cd70ce418f334db96104f2a19e4c3d69885659513ddea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a898f86297062c2304c4056ac9d505c75be009b87de6368ca3b97e2693682c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b18ff7eaf6599f300155292890bf6078ad4a2557036322b5611498dd184a3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ac86ff7ffb5ccfb109f3073bcd8ea84600941c53809d1c72a7c2283c76b303(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c473d23f201aa5636c585533818d1ef85da1a41e0d3f62b921e62086ac7dff6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf6247f2d73ed76b2981ff901dfc693311ceffde3af5c2352b0cf05ec6de144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41d12a7accb1bdf5b8d114c6677e49a420848400c95977a3b655d1226046d12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb31cdb686c176df598aac1aababc30d58485a9354846406fd314a6c2463674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d366fac0e1a2215f0d95f74ae424520c2ec515c518e1a4919ccf28abc3140ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec6302b361f69081908015fee637028b327aea9dac32e24c9690041a5562bc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b081556899eb1e863483c9e4015a5bacd642df9f1e4cee99568bf27f5d1e4345(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service: builtins.str,
    email_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email_filter_mode: typing.Optional[builtins.str] = None,
    email_incident_creation: typing.Optional[builtins.str] = None,
    email_parser: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParser, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email_parsing_fallback: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_email: typing.Optional[builtins.str] = None,
    integration_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    vendor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad0238f631d306435845d8c33b3f01ac25e9d9fbf4fc06f3cef40db54fef070(
    *,
    body_mode: typing.Optional[builtins.str] = None,
    body_regex: typing.Optional[builtins.str] = None,
    from_email_mode: typing.Optional[builtins.str] = None,
    from_email_regex: typing.Optional[builtins.str] = None,
    subject_mode: typing.Optional[builtins.str] = None,
    subject_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df4c5203268eab713efa69c46c35d4db4165d60f885d7abfb36e57b157aaf15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b934075963cd26035ee665ca8e4b8a77fcfe16d9019c7eaba5724a63a51edcae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f118a6c8df1e15c5ad4cff123afac2019d30650802213f4e9d6bf450d8d45d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d3a14bc5c426ba4d998b8dc6f5c3353032e28c7b5171189a06434a811f6daa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f465495c82bc01d28d3e2f57974aeae03d5e774096b248373c2346918effca52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b6513a48eb17e167f6548bec5e823fcc9061cd5496ba0c2cd72b7cd1751179(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcabc6070d821ed2adca083c5b6415c3daf8d069437e2bd1e774b5263b46b4b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8775d65935751f43edcc2e7f577995cc5af14f53adec2e788c6f8f8231e1c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86e1aacfb7126ad4a603ec7ec6f17f75b34eaf7c9c9519a3e7d3a1737aab64e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727dee8430f856cfeccc7f4e6ead883ea55be8db2168b8f156acbb6533036bb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce655edea3777d270096b6d7572585e181f0f856edf7aac9a9e151dd61d2c277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fda141024e0415a09d87a265ad73be8a4bba08aede3fae5554b81dfe299edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a232a1185c6a02102dc324f003e32aa606bbdcaaa9a6878924242777e1031148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756fa180c309f0600efa324390923eccf672e5addeb28d38e4abc40ea3c5588(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ecbe672d232528fafb619c9dbef092efc0e8efa64c0a28316c6d5a20e2202e(
    *,
    action: builtins.str,
    match_predicate: typing.Union[ServiceIntegrationEmailParserMatchPredicate, typing.Dict[builtins.str, typing.Any]],
    value_extractor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserValueExtractor, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5857e71f93ca4461ab382af742304bd1522c42b24c1dd91d3b02bcd195a39537(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d628d7d8e9b7c8bccc813e7ae7c5137eec0c6721f18926a6bdd5c7fd4daa0a36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d952adaae25aa6de517e1f468ffeede856882990840750bd968b009a864c066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519e7dbc257d60929ee3b6070ece7ddc133726c8aca98da5710bf04505b2d910(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7943dae864716b75c8b53885177bb74cef2c4e35a0d8acb43d34a41b72ceb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5e25c7e686afb79be82ad61b70ffd018d405ab33908c10ec8bb4bc2598fae9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParser]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee283bacec3e82a3cb11f1a7bc2ba09e0e6cd68279092d4dc9686210d38a41e(
    *,
    type: builtins.str,
    predicate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserMatchPredicatePredicate, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1625db303ac3c8e78882eee2c70943d20e36139d26e05ddb4628432b9b3604(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0afe478856c73da80805276dae0e0378732c03c7f6806824f00d21b87144ee6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserMatchPredicatePredicate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2389f31b8f2bf576414691cdababb871b1231028d896447b7f91e028bda25e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65750e4ffc33af9b46b17a578b204fde3b07e0bf51bc429b9685f05e979552d(
    value: typing.Optional[ServiceIntegrationEmailParserMatchPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a83f8d13eec4ccd17d187c3401988ff2b12bb13176d07eba6a0911c3fbdb64b(
    *,
    type: builtins.str,
    matcher: typing.Optional[builtins.str] = None,
    part: typing.Optional[builtins.str] = None,
    predicate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserMatchPredicatePredicatePredicate, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9d07c9849a683645af7a3220ce96c56b693ac45665ff6f783cab5eb0f00750(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475e6b2ce368b9d466e757327f26b708de8c7fb136e5c481b563456beff28ac6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e028f68fc48fe025f6d8b1131bf00bf8aa1fb5896b947f8573794a18f9511cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc73153ce2ecb16f94462aa070b2c60c49abe13d56f297f5d74911124344d60(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb510d215dbd084d4e7903ffaa3427a596908ffaf86e43a7721a48fd5ad71e7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579ce5dc7ab07c24cbb292b9fea257bd8ba1bbae020d0e96d1c538d47110de97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4171f38804421ac144de9e703def4730aad9679c5301aface3dc20dfc183f2cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ccad8f33447a122b24f55a5e390ffa4629f67e1b4e3617a1e122fce43e518b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserMatchPredicatePredicatePredicate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac1e42e4590feee9a2e7a325d265d1d38bd664a781da65a38ccd1c73b3aa0bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb877c0b92f820f5d7a05bf72bcd5cdbd1ba8132a0374c2229b8871c0cd4c419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64fec4a37a9651ed0daeb7d9d20b499d3ecf37ca64206c34bf20b0a4730631e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84665d50562b69937d7abda5787c3597f26e071255cf91da4f6a3657dc1a153(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda4b9e769f618ae79431c3418d50b4c12b5b5ae2b0ebac30ebf0e48d738cef1(
    *,
    matcher: builtins.str,
    part: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4131755b445659cbbfd7b4cc658f9bb52cc30cd64ff6fd068bb6a438ecc0d10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89dcd78e3be781f05c6c1da273483cfd19a79c4050c0c622ccc3551d727dca26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62b9154d357c6111ede5dbe30e49d1d057590c40ac3c2edb5315d317861eca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286f152e0c97f131d44dac356ff6f0da624741264f7c23a5cfba7ba47d0d3efb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7ca8dfb7a1b32f9e0873be32413cf81c3b3304ace1fb86c6131c11cb4bd42d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca596e4e9f2d08d5b04f8b78b4f1413ae3aeaef90f16b96120f3aaea4e6af7df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39a21ef607d296ac55561f80dab2c9f0655d04536b02316b50f29955b930623(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4a3a3a0d9fd13677142c88992dd79022632a90291b1520a39029bc7b800230(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13c46f9fc033db347624b165a3f21c2fa3060438f0652fbf195b3104585c9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc80b72cf5ddf7e09e5512d84180c5c38e025f9214b6f5ac13a880f7b0d00f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ab99d63164ce7f1065035fa446abe736e46c55fcbbdfed3f36a357170d4c40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserMatchPredicatePredicatePredicate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8399c5edef1669f41e421a25d8e24efc97fcfe86c10d6d2862b204c44a149e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c5972dc715e80785425a04f43675ea2d55591c18bd75cd58ebe33e252d62ba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceIntegrationEmailParserValueExtractor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66df8226dee8ba930eb558e5f68df5961103f5939d05f72545c3fc19ea128dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3d3d0c90f8831f39681c0de8731e2dafd8457daeb773779b0b8d4b29c3939b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParser]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89af65eb7c799f43315d773c6b8fec02d0a64bc8ad70c169cd0fcb22faa1e3d0(
    *,
    part: builtins.str,
    type: builtins.str,
    value_name: builtins.str,
    ends_before: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
    starts_after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1059cb398988d29b4d4bea1f713462a95a01e4343e1141fc3db600c8698e7f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435efccfd732bcc943ef6c1763df692863eae2d4321232c742426624a325e427(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35406bcce65a082857e0b85434472ac5555523de8777fce4cf9e758d41910b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c24a74c51e20171f0439f67a5d5446725b1509ea77bd104e86f5f272529d9d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db423961e09f9656b8a9b2ac3b4bfb6c0c4f88df22ed73be778a53e8a20fc20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d33368091e9910cd6875c0b614b9eaf5f8bd0fc87d735ba3817b66f66e5150(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceIntegrationEmailParserValueExtractor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a0327dc0c2e5c5cffe503b2106b34c2d8248214902a2faefbc54d4caf81aa3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2d1ccfe09d4ee456b6af52432aec00bb402d416592c67c2e0fee261c73e8f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da54361000009cf2bff514c7b2e2c194c49651c34b82fbab548610a76b6b33f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d30b867c66ac849215cf2350eebc7a5b710509516592f5bba4cf80472520df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6259ade1b7e1ef8dbb7f123293eb5cc3c674251df1413643ebf1e69fdd75697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc43b6cce9087e365af68e742f4f31195b5f5f87a9a3a1345fcc8423a17477b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c3d11f8b8c527a48c9bcda83499c2afef12cd0da24478b86ddb77f2841d15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ccc0fdf23327cfefb8ebf1cbd233b19425ec86eeeb7375a1fbedc8dee880ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceIntegrationEmailParserValueExtractor]],
) -> None:
    """Type checking stubs"""
    pass
