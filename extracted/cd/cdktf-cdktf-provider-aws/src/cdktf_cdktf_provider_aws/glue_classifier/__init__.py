r'''
# `aws_glue_classifier`

Refer to the Terraform Registry for docs: [`aws_glue_classifier`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier).
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


class GlueClassifier(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifier",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier aws_glue_classifier}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        csv_classifier: typing.Optional[typing.Union["GlueClassifierCsvClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        grok_classifier: typing.Optional[typing.Union["GlueClassifierGrokClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        json_classifier: typing.Optional[typing.Union["GlueClassifierJsonClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        xml_classifier: typing.Optional[typing.Union["GlueClassifierXmlClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier aws_glue_classifier} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#name GlueClassifier#name}.
        :param csv_classifier: csv_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#csv_classifier GlueClassifier#csv_classifier}
        :param grok_classifier: grok_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#grok_classifier GlueClassifier#grok_classifier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#id GlueClassifier#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param json_classifier: json_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#json_classifier GlueClassifier#json_classifier}
        :param xml_classifier: xml_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#xml_classifier GlueClassifier#xml_classifier}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d8c82fc7bdd41e4bd4297df980d580fd7382ca1785ea85dc10af1736e72956)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GlueClassifierConfig(
            name=name,
            csv_classifier=csv_classifier,
            grok_classifier=grok_classifier,
            id=id,
            json_classifier=json_classifier,
            xml_classifier=xml_classifier,
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
        '''Generates CDKTF code for importing a GlueClassifier resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GlueClassifier to import.
        :param import_from_id: The id of the existing GlueClassifier that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GlueClassifier to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ef07356048f94fed34a52c4fcebae322caf4e18bb02c918c6bb819e4241402)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCsvClassifier")
    def put_csv_classifier(
        self,
        *,
        allow_single_column: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        contains_header: typing.Optional[builtins.str] = None,
        custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_datatypes: typing.Optional[typing.Sequence[builtins.str]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Sequence[builtins.str]] = None,
        quote_symbol: typing.Optional[builtins.str] = None,
        serde: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_single_column: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#allow_single_column GlueClassifier#allow_single_column}.
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#contains_header GlueClassifier#contains_header}.
        :param custom_datatype_configured: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_datatype_configured GlueClassifier#custom_datatype_configured}.
        :param custom_datatypes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_datatypes GlueClassifier#custom_datatypes}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#delimiter GlueClassifier#delimiter}.
        :param disable_value_trimming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#disable_value_trimming GlueClassifier#disable_value_trimming}.
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#header GlueClassifier#header}.
        :param quote_symbol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#quote_symbol GlueClassifier#quote_symbol}.
        :param serde: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#serde GlueClassifier#serde}.
        '''
        value = GlueClassifierCsvClassifier(
            allow_single_column=allow_single_column,
            contains_header=contains_header,
            custom_datatype_configured=custom_datatype_configured,
            custom_datatypes=custom_datatypes,
            delimiter=delimiter,
            disable_value_trimming=disable_value_trimming,
            header=header,
            quote_symbol=quote_symbol,
            serde=serde,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvClassifier", [value]))

    @jsii.member(jsii_name="putGrokClassifier")
    def put_grok_classifier(
        self,
        *,
        classification: builtins.str,
        grok_pattern: builtins.str,
        custom_patterns: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param grok_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#grok_pattern GlueClassifier#grok_pattern}.
        :param custom_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_patterns GlueClassifier#custom_patterns}.
        '''
        value = GlueClassifierGrokClassifier(
            classification=classification,
            grok_pattern=grok_pattern,
            custom_patterns=custom_patterns,
        )

        return typing.cast(None, jsii.invoke(self, "putGrokClassifier", [value]))

    @jsii.member(jsii_name="putJsonClassifier")
    def put_json_classifier(self, *, json_path: builtins.str) -> None:
        '''
        :param json_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#json_path GlueClassifier#json_path}.
        '''
        value = GlueClassifierJsonClassifier(json_path=json_path)

        return typing.cast(None, jsii.invoke(self, "putJsonClassifier", [value]))

    @jsii.member(jsii_name="putXmlClassifier")
    def put_xml_classifier(
        self,
        *,
        classification: builtins.str,
        row_tag: builtins.str,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param row_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#row_tag GlueClassifier#row_tag}.
        '''
        value = GlueClassifierXmlClassifier(
            classification=classification, row_tag=row_tag
        )

        return typing.cast(None, jsii.invoke(self, "putXmlClassifier", [value]))

    @jsii.member(jsii_name="resetCsvClassifier")
    def reset_csv_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvClassifier", []))

    @jsii.member(jsii_name="resetGrokClassifier")
    def reset_grok_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrokClassifier", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJsonClassifier")
    def reset_json_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonClassifier", []))

    @jsii.member(jsii_name="resetXmlClassifier")
    def reset_xml_classifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXmlClassifier", []))

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
    @jsii.member(jsii_name="csvClassifier")
    def csv_classifier(self) -> "GlueClassifierCsvClassifierOutputReference":
        return typing.cast("GlueClassifierCsvClassifierOutputReference", jsii.get(self, "csvClassifier"))

    @builtins.property
    @jsii.member(jsii_name="grokClassifier")
    def grok_classifier(self) -> "GlueClassifierGrokClassifierOutputReference":
        return typing.cast("GlueClassifierGrokClassifierOutputReference", jsii.get(self, "grokClassifier"))

    @builtins.property
    @jsii.member(jsii_name="jsonClassifier")
    def json_classifier(self) -> "GlueClassifierJsonClassifierOutputReference":
        return typing.cast("GlueClassifierJsonClassifierOutputReference", jsii.get(self, "jsonClassifier"))

    @builtins.property
    @jsii.member(jsii_name="xmlClassifier")
    def xml_classifier(self) -> "GlueClassifierXmlClassifierOutputReference":
        return typing.cast("GlueClassifierXmlClassifierOutputReference", jsii.get(self, "xmlClassifier"))

    @builtins.property
    @jsii.member(jsii_name="csvClassifierInput")
    def csv_classifier_input(self) -> typing.Optional["GlueClassifierCsvClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierCsvClassifier"], jsii.get(self, "csvClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="grokClassifierInput")
    def grok_classifier_input(self) -> typing.Optional["GlueClassifierGrokClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierGrokClassifier"], jsii.get(self, "grokClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonClassifierInput")
    def json_classifier_input(self) -> typing.Optional["GlueClassifierJsonClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierJsonClassifier"], jsii.get(self, "jsonClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="xmlClassifierInput")
    def xml_classifier_input(self) -> typing.Optional["GlueClassifierXmlClassifier"]:
        return typing.cast(typing.Optional["GlueClassifierXmlClassifier"], jsii.get(self, "xmlClassifierInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbe6a48c984550d0d325f27e05978c5a775c40f9eec447a6bcf16018131c03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0359df8a32cdebc0c6bc414ba5eef477cc6d2fd0a16afd2456f830274d0a9aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierConfig",
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
        "csv_classifier": "csvClassifier",
        "grok_classifier": "grokClassifier",
        "id": "id",
        "json_classifier": "jsonClassifier",
        "xml_classifier": "xmlClassifier",
    },
)
class GlueClassifierConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        csv_classifier: typing.Optional[typing.Union["GlueClassifierCsvClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        grok_classifier: typing.Optional[typing.Union["GlueClassifierGrokClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        json_classifier: typing.Optional[typing.Union["GlueClassifierJsonClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
        xml_classifier: typing.Optional[typing.Union["GlueClassifierXmlClassifier", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#name GlueClassifier#name}.
        :param csv_classifier: csv_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#csv_classifier GlueClassifier#csv_classifier}
        :param grok_classifier: grok_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#grok_classifier GlueClassifier#grok_classifier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#id GlueClassifier#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param json_classifier: json_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#json_classifier GlueClassifier#json_classifier}
        :param xml_classifier: xml_classifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#xml_classifier GlueClassifier#xml_classifier}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(csv_classifier, dict):
            csv_classifier = GlueClassifierCsvClassifier(**csv_classifier)
        if isinstance(grok_classifier, dict):
            grok_classifier = GlueClassifierGrokClassifier(**grok_classifier)
        if isinstance(json_classifier, dict):
            json_classifier = GlueClassifierJsonClassifier(**json_classifier)
        if isinstance(xml_classifier, dict):
            xml_classifier = GlueClassifierXmlClassifier(**xml_classifier)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1b3abb85e36f6323b6125fa118e01892de537f720d37986b080a81bbfd77b6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument csv_classifier", value=csv_classifier, expected_type=type_hints["csv_classifier"])
            check_type(argname="argument grok_classifier", value=grok_classifier, expected_type=type_hints["grok_classifier"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument json_classifier", value=json_classifier, expected_type=type_hints["json_classifier"])
            check_type(argname="argument xml_classifier", value=xml_classifier, expected_type=type_hints["xml_classifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if csv_classifier is not None:
            self._values["csv_classifier"] = csv_classifier
        if grok_classifier is not None:
            self._values["grok_classifier"] = grok_classifier
        if id is not None:
            self._values["id"] = id
        if json_classifier is not None:
            self._values["json_classifier"] = json_classifier
        if xml_classifier is not None:
            self._values["xml_classifier"] = xml_classifier

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#name GlueClassifier#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csv_classifier(self) -> typing.Optional["GlueClassifierCsvClassifier"]:
        '''csv_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#csv_classifier GlueClassifier#csv_classifier}
        '''
        result = self._values.get("csv_classifier")
        return typing.cast(typing.Optional["GlueClassifierCsvClassifier"], result)

    @builtins.property
    def grok_classifier(self) -> typing.Optional["GlueClassifierGrokClassifier"]:
        '''grok_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#grok_classifier GlueClassifier#grok_classifier}
        '''
        result = self._values.get("grok_classifier")
        return typing.cast(typing.Optional["GlueClassifierGrokClassifier"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#id GlueClassifier#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def json_classifier(self) -> typing.Optional["GlueClassifierJsonClassifier"]:
        '''json_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#json_classifier GlueClassifier#json_classifier}
        '''
        result = self._values.get("json_classifier")
        return typing.cast(typing.Optional["GlueClassifierJsonClassifier"], result)

    @builtins.property
    def xml_classifier(self) -> typing.Optional["GlueClassifierXmlClassifier"]:
        '''xml_classifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#xml_classifier GlueClassifier#xml_classifier}
        '''
        result = self._values.get("xml_classifier")
        return typing.cast(typing.Optional["GlueClassifierXmlClassifier"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierCsvClassifier",
    jsii_struct_bases=[],
    name_mapping={
        "allow_single_column": "allowSingleColumn",
        "contains_header": "containsHeader",
        "custom_datatype_configured": "customDatatypeConfigured",
        "custom_datatypes": "customDatatypes",
        "delimiter": "delimiter",
        "disable_value_trimming": "disableValueTrimming",
        "header": "header",
        "quote_symbol": "quoteSymbol",
        "serde": "serde",
    },
)
class GlueClassifierCsvClassifier:
    def __init__(
        self,
        *,
        allow_single_column: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        contains_header: typing.Optional[builtins.str] = None,
        custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_datatypes: typing.Optional[typing.Sequence[builtins.str]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Sequence[builtins.str]] = None,
        quote_symbol: typing.Optional[builtins.str] = None,
        serde: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_single_column: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#allow_single_column GlueClassifier#allow_single_column}.
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#contains_header GlueClassifier#contains_header}.
        :param custom_datatype_configured: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_datatype_configured GlueClassifier#custom_datatype_configured}.
        :param custom_datatypes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_datatypes GlueClassifier#custom_datatypes}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#delimiter GlueClassifier#delimiter}.
        :param disable_value_trimming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#disable_value_trimming GlueClassifier#disable_value_trimming}.
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#header GlueClassifier#header}.
        :param quote_symbol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#quote_symbol GlueClassifier#quote_symbol}.
        :param serde: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#serde GlueClassifier#serde}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf384b2033682e5f43e199a8a85dad8fdc7181cab76acfb58d56f7d91e88a5c)
            check_type(argname="argument allow_single_column", value=allow_single_column, expected_type=type_hints["allow_single_column"])
            check_type(argname="argument contains_header", value=contains_header, expected_type=type_hints["contains_header"])
            check_type(argname="argument custom_datatype_configured", value=custom_datatype_configured, expected_type=type_hints["custom_datatype_configured"])
            check_type(argname="argument custom_datatypes", value=custom_datatypes, expected_type=type_hints["custom_datatypes"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument disable_value_trimming", value=disable_value_trimming, expected_type=type_hints["disable_value_trimming"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument quote_symbol", value=quote_symbol, expected_type=type_hints["quote_symbol"])
            check_type(argname="argument serde", value=serde, expected_type=type_hints["serde"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_single_column is not None:
            self._values["allow_single_column"] = allow_single_column
        if contains_header is not None:
            self._values["contains_header"] = contains_header
        if custom_datatype_configured is not None:
            self._values["custom_datatype_configured"] = custom_datatype_configured
        if custom_datatypes is not None:
            self._values["custom_datatypes"] = custom_datatypes
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if disable_value_trimming is not None:
            self._values["disable_value_trimming"] = disable_value_trimming
        if header is not None:
            self._values["header"] = header
        if quote_symbol is not None:
            self._values["quote_symbol"] = quote_symbol
        if serde is not None:
            self._values["serde"] = serde

    @builtins.property
    def allow_single_column(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#allow_single_column GlueClassifier#allow_single_column}.'''
        result = self._values.get("allow_single_column")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def contains_header(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#contains_header GlueClassifier#contains_header}.'''
        result = self._values.get("contains_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_datatype_configured(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_datatype_configured GlueClassifier#custom_datatype_configured}.'''
        result = self._values.get("custom_datatype_configured")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_datatypes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_datatypes GlueClassifier#custom_datatypes}.'''
        result = self._values.get("custom_datatypes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#delimiter GlueClassifier#delimiter}.'''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_value_trimming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#disable_value_trimming GlueClassifier#disable_value_trimming}.'''
        result = self._values.get("disable_value_trimming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#header GlueClassifier#header}.'''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quote_symbol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#quote_symbol GlueClassifier#quote_symbol}.'''
        result = self._values.get("quote_symbol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serde(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#serde GlueClassifier#serde}.'''
        result = self._values.get("serde")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierCsvClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierCsvClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierCsvClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b4b413e689384f8aefd30464e668a4df844edf4596fc626a142999c4af037e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowSingleColumn")
    def reset_allow_single_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowSingleColumn", []))

    @jsii.member(jsii_name="resetContainsHeader")
    def reset_contains_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainsHeader", []))

    @jsii.member(jsii_name="resetCustomDatatypeConfigured")
    def reset_custom_datatype_configured(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDatatypeConfigured", []))

    @jsii.member(jsii_name="resetCustomDatatypes")
    def reset_custom_datatypes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDatatypes", []))

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetDisableValueTrimming")
    def reset_disable_value_trimming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableValueTrimming", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetQuoteSymbol")
    def reset_quote_symbol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuoteSymbol", []))

    @jsii.member(jsii_name="resetSerde")
    def reset_serde(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerde", []))

    @builtins.property
    @jsii.member(jsii_name="allowSingleColumnInput")
    def allow_single_column_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSingleColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="containsHeaderInput")
    def contains_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="customDatatypeConfiguredInput")
    def custom_datatype_configured_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customDatatypeConfiguredInput"))

    @builtins.property
    @jsii.member(jsii_name="customDatatypesInput")
    def custom_datatypes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customDatatypesInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="disableValueTrimmingInput")
    def disable_value_trimming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableValueTrimmingInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteSymbolInput")
    def quote_symbol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteSymbolInput"))

    @builtins.property
    @jsii.member(jsii_name="serdeInput")
    def serde_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serdeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSingleColumn")
    def allow_single_column(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSingleColumn"))

    @allow_single_column.setter
    def allow_single_column(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41255671c411231fde6f4c3a697a1d306d3d999c52eb2efaa3f7dfe58d0cfdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSingleColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containsHeader")
    def contains_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containsHeader"))

    @contains_header.setter
    def contains_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68c04efe6cefd2bf9b9dc4c2ab2637c1a581e0edb17c70fce54442777e4d5f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containsHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDatatypeConfigured")
    def custom_datatype_configured(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customDatatypeConfigured"))

    @custom_datatype_configured.setter
    def custom_datatype_configured(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4445bb2a9d780e4ffd3b6fef49befca09d850a5f3e9dfdaf01fea05ba46889dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDatatypeConfigured", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDatatypes")
    def custom_datatypes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customDatatypes"))

    @custom_datatypes.setter
    def custom_datatypes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0f9dd2b3241a4022e1aa87359c7de4fd7488fbcda14b299af3b88e2555bae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDatatypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9c2b7c250f12a793650ee0aa403d54f4bf6f3fdca4c4c43e31af92fe206960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableValueTrimming")
    def disable_value_trimming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableValueTrimming"))

    @disable_value_trimming.setter
    def disable_value_trimming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff48d913bb416c0bddfeb0d829d57b73e9adabf96ede00f53bb460cde4f7f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableValueTrimming", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "header"))

    @header.setter
    def header(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc18416f2b3d2027db7b63475838a1888b4be01382512db228a45fefadd745c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteSymbol")
    def quote_symbol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quoteSymbol"))

    @quote_symbol.setter
    def quote_symbol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334960410790d3a98c0089dcca9a5751acf35e1e03ffcdbec88ca697084639a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteSymbol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serde")
    def serde(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serde"))

    @serde.setter
    def serde(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b07499cc7e5e04d26ade81523f77f31fbd90755cfacad40a655efdebfbeabe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serde", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierCsvClassifier]:
        return typing.cast(typing.Optional[GlueClassifierCsvClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierCsvClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f942e5f8f09b22f2760e55f2a0ce5f9729b851ba7ef4bdb7af07168e0ca85597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierGrokClassifier",
    jsii_struct_bases=[],
    name_mapping={
        "classification": "classification",
        "grok_pattern": "grokPattern",
        "custom_patterns": "customPatterns",
    },
)
class GlueClassifierGrokClassifier:
    def __init__(
        self,
        *,
        classification: builtins.str,
        grok_pattern: builtins.str,
        custom_patterns: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param grok_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#grok_pattern GlueClassifier#grok_pattern}.
        :param custom_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_patterns GlueClassifier#custom_patterns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f9563c226ca9fb1eadfb4e77c752e7304db3634f5215862d141abc6440baa3)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument grok_pattern", value=grok_pattern, expected_type=type_hints["grok_pattern"])
            check_type(argname="argument custom_patterns", value=custom_patterns, expected_type=type_hints["custom_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
            "grok_pattern": grok_pattern,
        }
        if custom_patterns is not None:
            self._values["custom_patterns"] = custom_patterns

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grok_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#grok_pattern GlueClassifier#grok_pattern}.'''
        result = self._values.get("grok_pattern")
        assert result is not None, "Required property 'grok_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_patterns(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#custom_patterns GlueClassifier#custom_patterns}.'''
        result = self._values.get("custom_patterns")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierGrokClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierGrokClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierGrokClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f5430b453a44a511dc07059e611a181faeeb4095ae2c3a04c7e8ad1c9ba8dfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomPatterns")
    def reset_custom_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="customPatternsInput")
    def custom_patterns_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="grokPatternInput")
    def grok_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grokPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cce7c08ec062c5c0b83b0d94ab222c1fff508d04dde9a4b84028659aadc8497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPatterns")
    def custom_patterns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPatterns"))

    @custom_patterns.setter
    def custom_patterns(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bd54a1bf5f6526bc4a2a947d5e447a6597c5c314e064a942e9359d40fda428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grokPattern")
    def grok_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grokPattern"))

    @grok_pattern.setter
    def grok_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55e5e6aa0d1927828815f422a5541d1a7d92ce2975685657d403b9f5a7be22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grokPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierGrokClassifier]:
        return typing.cast(typing.Optional[GlueClassifierGrokClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierGrokClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e6b90cd76d4196a4ccbe13c06642ff66d9b99b92f2fd7783cb879dcf2ee765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierJsonClassifier",
    jsii_struct_bases=[],
    name_mapping={"json_path": "jsonPath"},
)
class GlueClassifierJsonClassifier:
    def __init__(self, *, json_path: builtins.str) -> None:
        '''
        :param json_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#json_path GlueClassifier#json_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dee8b808df81d2c48cddcb548d3bf2199d48a2f8668217e6f68c90717937f3e)
            check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "json_path": json_path,
        }

    @builtins.property
    def json_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#json_path GlueClassifier#json_path}.'''
        result = self._values.get("json_path")
        assert result is not None, "Required property 'json_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierJsonClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierJsonClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierJsonClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97328ae5e6fd37a47c8327a6b5ac2a1f913e17e33585f12d38092ddf8ef6bd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="jsonPathInput")
    def json_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonPathInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonPath")
    def json_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonPath"))

    @json_path.setter
    def json_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8683c9a381f6c0fd120d770dc5b597af0196a87ca4deba88d29ddfd7e68985fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierJsonClassifier]:
        return typing.cast(typing.Optional[GlueClassifierJsonClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierJsonClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6307ae38af9d450ca42a6364b553d94fb23ba5dddc4d35565350a191c5dd5b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierXmlClassifier",
    jsii_struct_bases=[],
    name_mapping={"classification": "classification", "row_tag": "rowTag"},
)
class GlueClassifierXmlClassifier:
    def __init__(self, *, classification: builtins.str, row_tag: builtins.str) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.
        :param row_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#row_tag GlueClassifier#row_tag}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0cba07eca4763aa94920efceee794fdb14b8cf75105ad9d4b3bc4f0b90563d)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument row_tag", value=row_tag, expected_type=type_hints["row_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
            "row_tag": row_tag,
        }

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#classification GlueClassifier#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def row_tag(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_classifier#row_tag GlueClassifier#row_tag}.'''
        result = self._values.get("row_tag")
        assert result is not None, "Required property 'row_tag' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueClassifierXmlClassifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueClassifierXmlClassifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueClassifier.GlueClassifierXmlClassifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8047b222f275443b3e00846ce67f7bded687e3a507a8c66d4ce2185bd9b16127)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="rowTagInput")
    def row_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rowTagInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c136f6364486bfdaddb38db0cbb1a4faa506bbe6426029edaf3c7ee13d57ccf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowTag")
    def row_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rowTag"))

    @row_tag.setter
    def row_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a71655b0e650e7413bcfb71068d499cb9f57fb649d36b4cc124769c7687353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueClassifierXmlClassifier]:
        return typing.cast(typing.Optional[GlueClassifierXmlClassifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueClassifierXmlClassifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ff3b69b851f6ec63e4229445d8f9a1c023357fe956cdc005d6c8fa119515fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GlueClassifier",
    "GlueClassifierConfig",
    "GlueClassifierCsvClassifier",
    "GlueClassifierCsvClassifierOutputReference",
    "GlueClassifierGrokClassifier",
    "GlueClassifierGrokClassifierOutputReference",
    "GlueClassifierJsonClassifier",
    "GlueClassifierJsonClassifierOutputReference",
    "GlueClassifierXmlClassifier",
    "GlueClassifierXmlClassifierOutputReference",
]

publication.publish()

def _typecheckingstub__36d8c82fc7bdd41e4bd4297df980d580fd7382ca1785ea85dc10af1736e72956(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    csv_classifier: typing.Optional[typing.Union[GlueClassifierCsvClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    grok_classifier: typing.Optional[typing.Union[GlueClassifierGrokClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    json_classifier: typing.Optional[typing.Union[GlueClassifierJsonClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    xml_classifier: typing.Optional[typing.Union[GlueClassifierXmlClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__50ef07356048f94fed34a52c4fcebae322caf4e18bb02c918c6bb819e4241402(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbe6a48c984550d0d325f27e05978c5a775c40f9eec447a6bcf16018131c03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0359df8a32cdebc0c6bc414ba5eef477cc6d2fd0a16afd2456f830274d0a9aa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1b3abb85e36f6323b6125fa118e01892de537f720d37986b080a81bbfd77b6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    csv_classifier: typing.Optional[typing.Union[GlueClassifierCsvClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    grok_classifier: typing.Optional[typing.Union[GlueClassifierGrokClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    json_classifier: typing.Optional[typing.Union[GlueClassifierJsonClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
    xml_classifier: typing.Optional[typing.Union[GlueClassifierXmlClassifier, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf384b2033682e5f43e199a8a85dad8fdc7181cab76acfb58d56f7d91e88a5c(
    *,
    allow_single_column: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    contains_header: typing.Optional[builtins.str] = None,
    custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_datatypes: typing.Optional[typing.Sequence[builtins.str]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Sequence[builtins.str]] = None,
    quote_symbol: typing.Optional[builtins.str] = None,
    serde: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4b413e689384f8aefd30464e668a4df844edf4596fc626a142999c4af037e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41255671c411231fde6f4c3a697a1d306d3d999c52eb2efaa3f7dfe58d0cfdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68c04efe6cefd2bf9b9dc4c2ab2637c1a581e0edb17c70fce54442777e4d5f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4445bb2a9d780e4ffd3b6fef49befca09d850a5f3e9dfdaf01fea05ba46889dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0f9dd2b3241a4022e1aa87359c7de4fd7488fbcda14b299af3b88e2555bae1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9c2b7c250f12a793650ee0aa403d54f4bf6f3fdca4c4c43e31af92fe206960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff48d913bb416c0bddfeb0d829d57b73e9adabf96ede00f53bb460cde4f7f33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc18416f2b3d2027db7b63475838a1888b4be01382512db228a45fefadd745c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334960410790d3a98c0089dcca9a5751acf35e1e03ffcdbec88ca697084639a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b07499cc7e5e04d26ade81523f77f31fbd90755cfacad40a655efdebfbeabe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f942e5f8f09b22f2760e55f2a0ce5f9729b851ba7ef4bdb7af07168e0ca85597(
    value: typing.Optional[GlueClassifierCsvClassifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f9563c226ca9fb1eadfb4e77c752e7304db3634f5215862d141abc6440baa3(
    *,
    classification: builtins.str,
    grok_pattern: builtins.str,
    custom_patterns: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5430b453a44a511dc07059e611a181faeeb4095ae2c3a04c7e8ad1c9ba8dfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cce7c08ec062c5c0b83b0d94ab222c1fff508d04dde9a4b84028659aadc8497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bd54a1bf5f6526bc4a2a947d5e447a6597c5c314e064a942e9359d40fda428(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55e5e6aa0d1927828815f422a5541d1a7d92ce2975685657d403b9f5a7be22d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e6b90cd76d4196a4ccbe13c06642ff66d9b99b92f2fd7783cb879dcf2ee765(
    value: typing.Optional[GlueClassifierGrokClassifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dee8b808df81d2c48cddcb548d3bf2199d48a2f8668217e6f68c90717937f3e(
    *,
    json_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97328ae5e6fd37a47c8327a6b5ac2a1f913e17e33585f12d38092ddf8ef6bd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8683c9a381f6c0fd120d770dc5b597af0196a87ca4deba88d29ddfd7e68985fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6307ae38af9d450ca42a6364b553d94fb23ba5dddc4d35565350a191c5dd5b13(
    value: typing.Optional[GlueClassifierJsonClassifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0cba07eca4763aa94920efceee794fdb14b8cf75105ad9d4b3bc4f0b90563d(
    *,
    classification: builtins.str,
    row_tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8047b222f275443b3e00846ce67f7bded687e3a507a8c66d4ce2185bd9b16127(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c136f6364486bfdaddb38db0cbb1a4faa506bbe6426029edaf3c7ee13d57ccf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a71655b0e650e7413bcfb71068d499cb9f57fb649d36b4cc124769c7687353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ff3b69b851f6ec63e4229445d8f9a1c023357fe956cdc005d6c8fa119515fd(
    value: typing.Optional[GlueClassifierXmlClassifier],
) -> None:
    """Type checking stubs"""
    pass
