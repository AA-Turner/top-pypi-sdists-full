r'''
# `google_compute_interconnect`

Refer to the Terraform Registry for docs: [`google_compute_interconnect`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect).
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


class GoogleComputeInterconnect(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnect",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect google_compute_interconnect}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        interconnect_type: builtins.str,
        link_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        requested_link_count: jsii.Number,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        customer_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        macsec: typing.Optional[typing.Union["GoogleComputeInterconnectMacsec", typing.Dict[builtins.str, typing.Any]]] = None,
        macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        noc_contact_email: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_location: typing.Optional[builtins.str] = None,
        requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeInterconnectTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect google_compute_interconnect} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param interconnect_type: Type of interconnect. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED. Can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Possible values: ["DEDICATED", "PARTNER", "IT_PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#interconnect_type GoogleComputeInterconnect#interconnect_type}
        :param link_type: Type of link requested. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle. Can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics. - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. - LINK_TYPE_ETHERNET_400G_LR4: A 400G Ethernet with LR4 optics Possible values: ["LINK_TYPE_ETHERNET_10G_LR", "LINK_TYPE_ETHERNET_100G_LR", "LINK_TYPE_ETHERNET_400G_LR4"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#link_type GoogleComputeInterconnect#link_type}
        :param location: URL of the InterconnectLocation object that represents where this connection is to be provisioned. Specifies the location inside Google's Networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#location GoogleComputeInterconnect#location}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#name GoogleComputeInterconnect#name}
        :param requested_link_count: Target number of physical links in the link bundle, as requested by the customer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#requested_link_count GoogleComputeInterconnect#requested_link_count}
        :param admin_enabled: Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#admin_enabled GoogleComputeInterconnect#admin_enabled}
        :param customer_name: Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect. This field is required for Dedicated and Partner Interconnect, should not be specified for cross-cloud interconnect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#customer_name GoogleComputeInterconnect#customer_name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#description GoogleComputeInterconnect#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#id GoogleComputeInterconnect#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#labels GoogleComputeInterconnect#labels}
        :param macsec: macsec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#macsec GoogleComputeInterconnect#macsec}
        :param macsec_enabled: Enable or disable MACsec on this Interconnect connection. MACsec enablement fails if the MACsec object is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#macsec_enabled GoogleComputeInterconnect#macsec_enabled}
        :param noc_contact_email: Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Cloud Monitoring logs alerting and Cloud Notifications. This field is required for users who sign up for Cloud Interconnect using workforce identity federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#noc_contact_email GoogleComputeInterconnect#noc_contact_email}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#project GoogleComputeInterconnect#project}.
        :param remote_location: Indicates that this is a Cross-Cloud Interconnect. This field specifies the location outside of Google's network that the interconnect is connected to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#remote_location GoogleComputeInterconnect#remote_location}
        :param requested_features: interconnects.list of features requested for this Interconnect connection. Options: IF_MACSEC ( If specified then the connection is created on MACsec capable hardware ports. If not specified, the default value is false, which allocates non-MACsec capable ports first if available). Note that MACSEC is still technically allowed for compatibility reasons, but it does not work with the API, and will be removed in an upcoming major version. Possible values: ["MACSEC", "IF_MACSEC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#requested_features GoogleComputeInterconnect#requested_features}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#timeouts GoogleComputeInterconnect#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e239bb58099e10433581ed5b3d5defa9d085015b9903d126e479b8ddd50c5e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeInterconnectConfig(
            interconnect_type=interconnect_type,
            link_type=link_type,
            location=location,
            name=name,
            requested_link_count=requested_link_count,
            admin_enabled=admin_enabled,
            customer_name=customer_name,
            description=description,
            id=id,
            labels=labels,
            macsec=macsec,
            macsec_enabled=macsec_enabled,
            noc_contact_email=noc_contact_email,
            project=project,
            remote_location=remote_location,
            requested_features=requested_features,
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
        '''Generates CDKTF code for importing a GoogleComputeInterconnect resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeInterconnect to import.
        :param import_from_id: The id of the existing GoogleComputeInterconnect that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeInterconnect to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c162070d35d96aae89d19e8bd6384f8c3a00dbfecaec902d9d7a4bfc03bdebbc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMacsec")
    def put_macsec(
        self,
        *,
        pre_shared_keys: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeInterconnectMacsecPreSharedKeys", typing.Dict[builtins.str, typing.Any]]]],
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pre_shared_keys: pre_shared_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#pre_shared_keys GoogleComputeInterconnect#pre_shared_keys}
        :param fail_open: If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established. By default, the Interconnect connection is configured with a must-secure security policy that drops all traffic if the MKA session cannot be established with your router. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#fail_open GoogleComputeInterconnect#fail_open}
        '''
        value = GoogleComputeInterconnectMacsec(
            pre_shared_keys=pre_shared_keys, fail_open=fail_open
        )

        return typing.cast(None, jsii.invoke(self, "putMacsec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#create GoogleComputeInterconnect#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#delete GoogleComputeInterconnect#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#update GoogleComputeInterconnect#update}.
        '''
        value = GoogleComputeInterconnectTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminEnabled")
    def reset_admin_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminEnabled", []))

    @jsii.member(jsii_name="resetCustomerName")
    def reset_customer_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerName", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMacsec")
    def reset_macsec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsec", []))

    @jsii.member(jsii_name="resetMacsecEnabled")
    def reset_macsec_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecEnabled", []))

    @jsii.member(jsii_name="resetNocContactEmail")
    def reset_noc_contact_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNocContactEmail", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRemoteLocation")
    def reset_remote_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteLocation", []))

    @jsii.member(jsii_name="resetRequestedFeatures")
    def reset_requested_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedFeatures", []))

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
    @jsii.member(jsii_name="availableFeatures")
    def available_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableFeatures"))

    @builtins.property
    @jsii.member(jsii_name="circuitInfos")
    def circuit_infos(self) -> "GoogleComputeInterconnectCircuitInfosList":
        return typing.cast("GoogleComputeInterconnectCircuitInfosList", jsii.get(self, "circuitInfos"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="expectedOutages")
    def expected_outages(self) -> "GoogleComputeInterconnectExpectedOutagesList":
        return typing.cast("GoogleComputeInterconnectExpectedOutagesList", jsii.get(self, "expectedOutages"))

    @builtins.property
    @jsii.member(jsii_name="googleIpAddress")
    def google_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="googleReferenceId")
    def google_reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleReferenceId"))

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachments")
    def interconnect_attachments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "interconnectAttachments"))

    @builtins.property
    @jsii.member(jsii_name="interconnectGroups")
    def interconnect_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "interconnectGroups"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="macsec")
    def macsec(self) -> "GoogleComputeInterconnectMacsecOutputReference":
        return typing.cast("GoogleComputeInterconnectMacsecOutputReference", jsii.get(self, "macsec"))

    @builtins.property
    @jsii.member(jsii_name="operationalStatus")
    def operational_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationalStatus"))

    @builtins.property
    @jsii.member(jsii_name="peerIpAddress")
    def peer_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="provisionedLinkCount")
    def provisioned_link_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedLinkCount"))

    @builtins.property
    @jsii.member(jsii_name="satisfiesPzs")
    def satisfies_pzs(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "satisfiesPzs"))

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
    def timeouts(self) -> "GoogleComputeInterconnectTimeoutsOutputReference":
        return typing.cast("GoogleComputeInterconnectTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabledInput")
    def admin_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="customerNameInput")
    def customer_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interconnectTypeInput")
    def interconnect_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interconnectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="linkTypeInput")
    def link_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecEnabledInput")
    def macsec_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "macsecEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecInput")
    def macsec_input(self) -> typing.Optional["GoogleComputeInterconnectMacsec"]:
        return typing.cast(typing.Optional["GoogleComputeInterconnectMacsec"], jsii.get(self, "macsecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nocContactEmailInput")
    def noc_contact_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nocContactEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteLocationInput")
    def remote_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedFeaturesInput")
    def requested_features_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requestedFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedLinkCountInput")
    def requested_link_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestedLinkCountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeInterconnectTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeInterconnectTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabled")
    def admin_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminEnabled"))

    @admin_enabled.setter
    def admin_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c500e73fed4aa94fa01ebbcaeb8a613888cade3b3f4677f8d6ed5814ba7f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerName")
    def customer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerName"))

    @customer_name.setter
    def customer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5a0b6c92e4a95ed51e84476719e85ca04447b2698b29b35acb52efe1f6643c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a05cb994aeaf7b61e350cbaa0c2c1154425e2674fa0983609d501331b6047d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c731fed45f12612a434e2db0c1e3d7338a575c2a125aa86db9ddca1c336be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interconnectType")
    def interconnect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interconnectType"))

    @interconnect_type.setter
    def interconnect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ceb5ab724ac683b71af270cbb4fc07a05a28ad37cd960947f86361d0468d9a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interconnectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192ec1c98aa328e7a3b6a9f29550e9b603a68d4fd7b2097664f583eaaafcc60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkType")
    def link_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkType"))

    @link_type.setter
    def link_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce891bca89f8ad9cd8f3bd7d3874dd16304cd8ece422f1f88b304524e43903d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b390ca7806fe319a3ae9c8c07ef4bae543b9fea48a893b593f2a3f49bba1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecEnabled")
    def macsec_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "macsecEnabled"))

    @macsec_enabled.setter
    def macsec_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16a2c57153e6cd6eba7e65ab1fd22f1b17582b959536778a7e096c7a3136a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832d7e80d26741997b0d8d03ae77a0b22c998c52162d38765008613eb8830cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nocContactEmail")
    def noc_contact_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nocContactEmail"))

    @noc_contact_email.setter
    def noc_contact_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dee9f30bdf4a9cfdcddde3b8cc8ba7ee679c98477777133ec85e8bc2180fa5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nocContactEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2c33cfd5b082fa22440476b398ddc5166b067e0c5c90d2ed02c26b26511026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteLocation")
    def remote_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteLocation"))

    @remote_location.setter
    def remote_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402d478454a9e7e7ee9856f3cd01d4077d5d27c7fdd910609ad167d5808961d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedFeatures")
    def requested_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requestedFeatures"))

    @requested_features.setter
    def requested_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c51c58fcb065d7d53a8b94562b73697e5079ca2f82e1cf4db90b9686ee8cedd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedLinkCount")
    def requested_link_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestedLinkCount"))

    @requested_link_count.setter
    def requested_link_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0e6aaed88a59db6a4bc9c75e63c276f01529bb662e32ce8db0b3b70419bded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedLinkCount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectCircuitInfos",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeInterconnectCircuitInfos:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectCircuitInfos(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectCircuitInfosList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectCircuitInfosList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c5ad13f519ca34dd9b243574e212fb6bdff6e9491adb5eb4be626f5caf170cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeInterconnectCircuitInfosOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151c9898cb7a69b3ffadce0dcc8a5bb74324eaf7ff6abaf71230c9e213ec0804)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeInterconnectCircuitInfosOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50944091db6077eedd1619af57b0c46a2dc58ee18391da453c9f2753de4f1e54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcf074e70b90b3b7a8ab1283b663d7d357168310e2563abefb7d810253995e88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8739583e8546b907fb82d557d6b16a623de535b748a4316c0fe09770d061c3a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeInterconnectCircuitInfosOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectCircuitInfosOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cce549e54b85b0c042e4f6da8acdc75d20afd9ba4033b22587c9028c9b83fc07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="customerDemarcId")
    def customer_demarc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerDemarcId"))

    @builtins.property
    @jsii.member(jsii_name="googleCircuitId")
    def google_circuit_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleCircuitId"))

    @builtins.property
    @jsii.member(jsii_name="googleDemarcId")
    def google_demarc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleDemarcId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeInterconnectCircuitInfos]:
        return typing.cast(typing.Optional[GoogleComputeInterconnectCircuitInfos], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeInterconnectCircuitInfos],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f23581a7c1c13690258897232662bae1ff0f9494e111df825413057ef304f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "interconnect_type": "interconnectType",
        "link_type": "linkType",
        "location": "location",
        "name": "name",
        "requested_link_count": "requestedLinkCount",
        "admin_enabled": "adminEnabled",
        "customer_name": "customerName",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "macsec": "macsec",
        "macsec_enabled": "macsecEnabled",
        "noc_contact_email": "nocContactEmail",
        "project": "project",
        "remote_location": "remoteLocation",
        "requested_features": "requestedFeatures",
        "timeouts": "timeouts",
    },
)
class GoogleComputeInterconnectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        interconnect_type: builtins.str,
        link_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        requested_link_count: jsii.Number,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        customer_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        macsec: typing.Optional[typing.Union["GoogleComputeInterconnectMacsec", typing.Dict[builtins.str, typing.Any]]] = None,
        macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        noc_contact_email: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_location: typing.Optional[builtins.str] = None,
        requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeInterconnectTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param interconnect_type: Type of interconnect. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED. Can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Possible values: ["DEDICATED", "PARTNER", "IT_PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#interconnect_type GoogleComputeInterconnect#interconnect_type}
        :param link_type: Type of link requested. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle. Can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics. - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. - LINK_TYPE_ETHERNET_400G_LR4: A 400G Ethernet with LR4 optics Possible values: ["LINK_TYPE_ETHERNET_10G_LR", "LINK_TYPE_ETHERNET_100G_LR", "LINK_TYPE_ETHERNET_400G_LR4"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#link_type GoogleComputeInterconnect#link_type}
        :param location: URL of the InterconnectLocation object that represents where this connection is to be provisioned. Specifies the location inside Google's Networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#location GoogleComputeInterconnect#location}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#name GoogleComputeInterconnect#name}
        :param requested_link_count: Target number of physical links in the link bundle, as requested by the customer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#requested_link_count GoogleComputeInterconnect#requested_link_count}
        :param admin_enabled: Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#admin_enabled GoogleComputeInterconnect#admin_enabled}
        :param customer_name: Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect. This field is required for Dedicated and Partner Interconnect, should not be specified for cross-cloud interconnect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#customer_name GoogleComputeInterconnect#customer_name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#description GoogleComputeInterconnect#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#id GoogleComputeInterconnect#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#labels GoogleComputeInterconnect#labels}
        :param macsec: macsec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#macsec GoogleComputeInterconnect#macsec}
        :param macsec_enabled: Enable or disable MACsec on this Interconnect connection. MACsec enablement fails if the MACsec object is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#macsec_enabled GoogleComputeInterconnect#macsec_enabled}
        :param noc_contact_email: Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Cloud Monitoring logs alerting and Cloud Notifications. This field is required for users who sign up for Cloud Interconnect using workforce identity federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#noc_contact_email GoogleComputeInterconnect#noc_contact_email}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#project GoogleComputeInterconnect#project}.
        :param remote_location: Indicates that this is a Cross-Cloud Interconnect. This field specifies the location outside of Google's network that the interconnect is connected to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#remote_location GoogleComputeInterconnect#remote_location}
        :param requested_features: interconnects.list of features requested for this Interconnect connection. Options: IF_MACSEC ( If specified then the connection is created on MACsec capable hardware ports. If not specified, the default value is false, which allocates non-MACsec capable ports first if available). Note that MACSEC is still technically allowed for compatibility reasons, but it does not work with the API, and will be removed in an upcoming major version. Possible values: ["MACSEC", "IF_MACSEC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#requested_features GoogleComputeInterconnect#requested_features}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#timeouts GoogleComputeInterconnect#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(macsec, dict):
            macsec = GoogleComputeInterconnectMacsec(**macsec)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeInterconnectTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16fcf544a1528cd2ed6efe2a778710d6f2fd0ca370d0d7adfa12d6b455d7078f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument interconnect_type", value=interconnect_type, expected_type=type_hints["interconnect_type"])
            check_type(argname="argument link_type", value=link_type, expected_type=type_hints["link_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument requested_link_count", value=requested_link_count, expected_type=type_hints["requested_link_count"])
            check_type(argname="argument admin_enabled", value=admin_enabled, expected_type=type_hints["admin_enabled"])
            check_type(argname="argument customer_name", value=customer_name, expected_type=type_hints["customer_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument macsec", value=macsec, expected_type=type_hints["macsec"])
            check_type(argname="argument macsec_enabled", value=macsec_enabled, expected_type=type_hints["macsec_enabled"])
            check_type(argname="argument noc_contact_email", value=noc_contact_email, expected_type=type_hints["noc_contact_email"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument remote_location", value=remote_location, expected_type=type_hints["remote_location"])
            check_type(argname="argument requested_features", value=requested_features, expected_type=type_hints["requested_features"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interconnect_type": interconnect_type,
            "link_type": link_type,
            "location": location,
            "name": name,
            "requested_link_count": requested_link_count,
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
        if admin_enabled is not None:
            self._values["admin_enabled"] = admin_enabled
        if customer_name is not None:
            self._values["customer_name"] = customer_name
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if macsec is not None:
            self._values["macsec"] = macsec
        if macsec_enabled is not None:
            self._values["macsec_enabled"] = macsec_enabled
        if noc_contact_email is not None:
            self._values["noc_contact_email"] = noc_contact_email
        if project is not None:
            self._values["project"] = project
        if remote_location is not None:
            self._values["remote_location"] = remote_location
        if requested_features is not None:
            self._values["requested_features"] = requested_features
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
    def interconnect_type(self) -> builtins.str:
        '''Type of interconnect.

        Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED.
        Can take one of the following values:

        - PARTNER: A partner-managed interconnection shared between customers though a partner.
        - DEDICATED: A dedicated physical interconnection with the customer. Possible values: ["DEDICATED", "PARTNER", "IT_PRIVATE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#interconnect_type GoogleComputeInterconnect#interconnect_type}
        '''
        result = self._values.get("interconnect_type")
        assert result is not None, "Required property 'interconnect_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def link_type(self) -> builtins.str:
        '''Type of link requested.

        Note that this field indicates the speed of each of the links in the
        bundle, not the speed of the entire bundle. Can take one of the following values:

        - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics.
        - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics.
        - LINK_TYPE_ETHERNET_400G_LR4: A 400G Ethernet with LR4 optics Possible values: ["LINK_TYPE_ETHERNET_10G_LR", "LINK_TYPE_ETHERNET_100G_LR", "LINK_TYPE_ETHERNET_400G_LR4"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#link_type GoogleComputeInterconnect#link_type}
        '''
        result = self._values.get("link_type")
        assert result is not None, "Required property 'link_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''URL of the InterconnectLocation object that represents where this connection is to be provisioned. Specifies the location inside Google's Networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#location GoogleComputeInterconnect#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        Provided by the client when the resource is created. The name must be
        1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first
        character must be a lowercase letter, and all following characters must be a dash,
        lowercase letter, or digit, except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#name GoogleComputeInterconnect#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def requested_link_count(self) -> jsii.Number:
        '''Target number of physical links in the link bundle, as requested by the customer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#requested_link_count GoogleComputeInterconnect#requested_link_count}
        '''
        result = self._values.get("requested_link_count")
        assert result is not None, "Required property 'requested_link_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def admin_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Administrative status of the interconnect.

        When this is set to true, the Interconnect is
        functional and can carry traffic. When set to false, no packets can be carried over the
        interconnect and no BGP routes are exchanged over it. By default, the status is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#admin_enabled GoogleComputeInterconnect#admin_enabled}
        '''
        result = self._values.get("admin_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def customer_name(self) -> typing.Optional[builtins.str]:
        '''Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect.

        This field is required for Dedicated and Partner Interconnect, should not be specified
        for cross-cloud interconnect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#customer_name GoogleComputeInterconnect#customer_name}
        '''
        result = self._values.get("customer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#description GoogleComputeInterconnect#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#id GoogleComputeInterconnect#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for this resource.

        These can only be added or modified by the setLabels
        method. Each label key/value pair must comply with RFC1035. Label values may be empty.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#labels GoogleComputeInterconnect#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def macsec(self) -> typing.Optional["GoogleComputeInterconnectMacsec"]:
        '''macsec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#macsec GoogleComputeInterconnect#macsec}
        '''
        result = self._values.get("macsec")
        return typing.cast(typing.Optional["GoogleComputeInterconnectMacsec"], result)

    @builtins.property
    def macsec_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable MACsec on this Interconnect connection. MACsec enablement fails if the MACsec object is not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#macsec_enabled GoogleComputeInterconnect#macsec_enabled}
        '''
        result = self._values.get("macsec_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def noc_contact_email(self) -> typing.Optional[builtins.str]:
        '''Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect.

        If specified, this will be used for notifications in addition to
        all other forms described, such as Cloud Monitoring logs alerting and Cloud Notifications.
        This field is required for users who sign up for Cloud Interconnect using workforce identity
        federation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#noc_contact_email GoogleComputeInterconnect#noc_contact_email}
        '''
        result = self._values.get("noc_contact_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#project GoogleComputeInterconnect#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_location(self) -> typing.Optional[builtins.str]:
        '''Indicates that this is a Cross-Cloud Interconnect.

        This field specifies the location outside
        of Google's network that the interconnect is connected to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#remote_location GoogleComputeInterconnect#remote_location}
        '''
        result = self._values.get("remote_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requested_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''interconnects.list of features requested for this Interconnect connection. Options: IF_MACSEC ( If specified then the connection is created on MACsec capable hardware ports. If not specified, the default value is false, which allocates non-MACsec capable ports first if available). Note that MACSEC is still technically allowed for compatibility reasons, but it does not work with the API, and will be removed in an upcoming major version. Possible values: ["MACSEC", "IF_MACSEC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#requested_features GoogleComputeInterconnect#requested_features}
        '''
        result = self._values.get("requested_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeInterconnectTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#timeouts GoogleComputeInterconnect#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeInterconnectTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectExpectedOutages",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeInterconnectExpectedOutages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectExpectedOutages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectExpectedOutagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectExpectedOutagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eff9d065f60be58dee9c9c088d67f3934e8bcbea1560bb245f78095af4447a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeInterconnectExpectedOutagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68177ac8ea72122469d82f0cdadf431fcdf9a1b936dd9f3d16071c33b200f310)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeInterconnectExpectedOutagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73426d43a8df7d27f2f0c8f0cf52b56c6a099a5cab5052741550a7a4a340582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52ecffc8519c1d7b4de2038f674455bcfbfbe4dee12db3844eef996f37dd459)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8296575a394ea47d7adc14f55f1814efed79b44c7748479657a39ed9d8eb5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeInterconnectExpectedOutagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectExpectedOutagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1132f881949c795192c705a7146c4bca2f13e13a96faae2ba2dc7e2f6a67355f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="affectedCircuits")
    def affected_circuits(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "affectedCircuits"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="issueType")
    def issue_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issueType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeInterconnectExpectedOutages]:
        return typing.cast(typing.Optional[GoogleComputeInterconnectExpectedOutages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeInterconnectExpectedOutages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b086f05c29479fc4020f19b6b9d48d584d1b235f34193eb4092a4b2b7c41f0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectMacsec",
    jsii_struct_bases=[],
    name_mapping={"pre_shared_keys": "preSharedKeys", "fail_open": "failOpen"},
)
class GoogleComputeInterconnectMacsec:
    def __init__(
        self,
        *,
        pre_shared_keys: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeInterconnectMacsecPreSharedKeys", typing.Dict[builtins.str, typing.Any]]]],
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pre_shared_keys: pre_shared_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#pre_shared_keys GoogleComputeInterconnect#pre_shared_keys}
        :param fail_open: If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established. By default, the Interconnect connection is configured with a must-secure security policy that drops all traffic if the MKA session cannot be established with your router. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#fail_open GoogleComputeInterconnect#fail_open}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6763a5f46d2ad9e6075a67f1c68bc4aba8b4c0b9b9a8ecb0b5d7c349be288b19)
            check_type(argname="argument pre_shared_keys", value=pre_shared_keys, expected_type=type_hints["pre_shared_keys"])
            check_type(argname="argument fail_open", value=fail_open, expected_type=type_hints["fail_open"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pre_shared_keys": pre_shared_keys,
        }
        if fail_open is not None:
            self._values["fail_open"] = fail_open

    @builtins.property
    def pre_shared_keys(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeInterconnectMacsecPreSharedKeys"]]:
        '''pre_shared_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#pre_shared_keys GoogleComputeInterconnect#pre_shared_keys}
        '''
        result = self._values.get("pre_shared_keys")
        assert result is not None, "Required property 'pre_shared_keys' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeInterconnectMacsecPreSharedKeys"]], result)

    @builtins.property
    def fail_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established.

        By default, the Interconnect
        connection is configured with a must-secure security policy that drops all traffic
        if the MKA session cannot be established with your router.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#fail_open GoogleComputeInterconnect#fail_open}
        '''
        result = self._values.get("fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectMacsec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectMacsecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectMacsecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2276f4e1282af9a279c9e9ed5d59470242d54a6890e6c11f1f3b12154ee1fcab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPreSharedKeys")
    def put_pre_shared_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeInterconnectMacsecPreSharedKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0e5f48e80d4a72624dbfbddaccce66cdb0a904ae715f1eeadd9088e08e4195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPreSharedKeys", [value]))

    @jsii.member(jsii_name="resetFailOpen")
    def reset_fail_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOpen", []))

    @builtins.property
    @jsii.member(jsii_name="preSharedKeys")
    def pre_shared_keys(self) -> "GoogleComputeInterconnectMacsecPreSharedKeysList":
        return typing.cast("GoogleComputeInterconnectMacsecPreSharedKeysList", jsii.get(self, "preSharedKeys"))

    @builtins.property
    @jsii.member(jsii_name="failOpenInput")
    def fail_open_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="preSharedKeysInput")
    def pre_shared_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeInterconnectMacsecPreSharedKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeInterconnectMacsecPreSharedKeys"]]], jsii.get(self, "preSharedKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="failOpen")
    def fail_open(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOpen"))

    @fail_open.setter
    def fail_open(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9185861032736ad0c04f837d7df128cae106a46096beeedab4f63554137e3eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeInterconnectMacsec]:
        return typing.cast(typing.Optional[GoogleComputeInterconnectMacsec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeInterconnectMacsec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ace2e0d837236e028ce002c63436387de23c2a095eaa2fc68e2581211cf0f5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectMacsecPreSharedKeys",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "fail_open": "failOpen", "start_time": "startTime"},
)
class GoogleComputeInterconnectMacsecPreSharedKeys:
    def __init__(
        self,
        *,
        name: builtins.str,
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: A name for this pre-shared key. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#name GoogleComputeInterconnect#name}
        :param fail_open: If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established. By default, the Interconnect connection is configured with a must-secure security policy that drops all traffic if the MKA session cannot be established with your router. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#fail_open GoogleComputeInterconnect#fail_open}
        :param start_time: A RFC3339 timestamp on or after which the key is valid. startTime can be in the future. If the keychain has a single key, startTime can be omitted. If the keychain has multiple keys, startTime is mandatory for each key. The start times of keys must be in increasing order. The start times of two consecutive keys must be at least 6 hours apart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#start_time GoogleComputeInterconnect#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114153f3d14e6b064ffe2b610d2f69bed89c6fdff2773bb0cb58e691d2cba583)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument fail_open", value=fail_open, expected_type=type_hints["fail_open"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if fail_open is not None:
            self._values["fail_open"] = fail_open
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for this pre-shared key.

        The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character
        must be a lowercase letter, and all following characters must be a dash, lowercase
        letter, or digit, except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#name GoogleComputeInterconnect#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fail_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established.

        By default, the Interconnect
        connection is configured with a must-secure security policy that drops all traffic
        if the MKA session cannot be established with your router.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#fail_open GoogleComputeInterconnect#fail_open}
        '''
        result = self._values.get("fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''A RFC3339 timestamp on or after which the key is valid.

        startTime can be in the
        future. If the keychain has a single key, startTime can be omitted. If the keychain
        has multiple keys, startTime is mandatory for each key. The start times of keys must
        be in increasing order. The start times of two consecutive keys must be at least 6
        hours apart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#start_time GoogleComputeInterconnect#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectMacsecPreSharedKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectMacsecPreSharedKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectMacsecPreSharedKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__316a097ae7caff5b654841ab6791745f9e786a7d79ec21dab08140babf55209c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeInterconnectMacsecPreSharedKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354594ce268813b4e6199ddb6777dc55ee6be0556523006af0cc4bde68a88a3c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeInterconnectMacsecPreSharedKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443a8253d86bb7d7e938865a37855c0930c55084f55e39e30eaec588bdbf6d17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be4d8f37251f3a63d82358b92de3ea3a6273c634dfd8ac42d867d23dae689656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46cf5743235231d9c24614e1bc08c6d37c5133f452743084bf04de612f18b248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeInterconnectMacsecPreSharedKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeInterconnectMacsecPreSharedKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeInterconnectMacsecPreSharedKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e654e27913ac200f0725018858a4aa1b5da9e0308bc74514827948bcccaded7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeInterconnectMacsecPreSharedKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectMacsecPreSharedKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f65b08a8b704dfe3f7f87cf463acb64032c6a6c2f843d72f1c7ec36b320d3223)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFailOpen")
    def reset_fail_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOpen", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="failOpenInput")
    def fail_open_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="failOpen")
    def fail_open(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOpen"))

    @fail_open.setter
    def fail_open(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c9b552e49e7bf0e6d7759da438b640ba8cb4e9df67a56330dcb13e2406dd15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced11e36a8fd012f4ee496568ad45f28e60da3d0b6ce4994508b15382f75ffc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebce1f740dfaa04d196365a5ac4a0140f89d19d63ab2bc465cfc6741e2b61c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectMacsecPreSharedKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectMacsecPreSharedKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectMacsecPreSharedKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc97fbdb9badc79c66341084173bc0279c5aa78bb109497d79169060e9a2d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeInterconnectTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#create GoogleComputeInterconnect#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#delete GoogleComputeInterconnect#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#update GoogleComputeInterconnect#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb79a846adecd24ae62f21a0ea8b60861bad58e5971a51b07153beef8b3a31d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#create GoogleComputeInterconnect#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#delete GoogleComputeInterconnect#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_interconnect#update GoogleComputeInterconnect#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeInterconnectTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeInterconnectTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeInterconnect.GoogleComputeInterconnectTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0da781941dc08dc7ff33f46d60c1b0db3fad96f100b88d3e296002d0020ba4f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a072067d3d099d6c1d4bed80d57cd80fea5b47cb406427e171f60b5f0ee3542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac258ebb73887d3d618c67e86d48b961c8f95779ef0eb306a944908930fd17f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe0fbcdcacaf24697720fcc5bd75a834529c0e84bc1ab20f23fdd2d0298dfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dcf1d4ee1ba059fc0d14eeb7324e655774d488f5289b8c57a3adddd7ba99566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeInterconnect",
    "GoogleComputeInterconnectCircuitInfos",
    "GoogleComputeInterconnectCircuitInfosList",
    "GoogleComputeInterconnectCircuitInfosOutputReference",
    "GoogleComputeInterconnectConfig",
    "GoogleComputeInterconnectExpectedOutages",
    "GoogleComputeInterconnectExpectedOutagesList",
    "GoogleComputeInterconnectExpectedOutagesOutputReference",
    "GoogleComputeInterconnectMacsec",
    "GoogleComputeInterconnectMacsecOutputReference",
    "GoogleComputeInterconnectMacsecPreSharedKeys",
    "GoogleComputeInterconnectMacsecPreSharedKeysList",
    "GoogleComputeInterconnectMacsecPreSharedKeysOutputReference",
    "GoogleComputeInterconnectTimeouts",
    "GoogleComputeInterconnectTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0e239bb58099e10433581ed5b3d5defa9d085015b9903d126e479b8ddd50c5e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    interconnect_type: builtins.str,
    link_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    requested_link_count: jsii.Number,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    customer_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    macsec: typing.Optional[typing.Union[GoogleComputeInterconnectMacsec, typing.Dict[builtins.str, typing.Any]]] = None,
    macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    noc_contact_email: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_location: typing.Optional[builtins.str] = None,
    requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeInterconnectTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c162070d35d96aae89d19e8bd6384f8c3a00dbfecaec902d9d7a4bfc03bdebbc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c500e73fed4aa94fa01ebbcaeb8a613888cade3b3f4677f8d6ed5814ba7f3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5a0b6c92e4a95ed51e84476719e85ca04447b2698b29b35acb52efe1f6643c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a05cb994aeaf7b61e350cbaa0c2c1154425e2674fa0983609d501331b6047d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c731fed45f12612a434e2db0c1e3d7338a575c2a125aa86db9ddca1c336be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ceb5ab724ac683b71af270cbb4fc07a05a28ad37cd960947f86361d0468d9a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192ec1c98aa328e7a3b6a9f29550e9b603a68d4fd7b2097664f583eaaafcc60c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce891bca89f8ad9cd8f3bd7d3874dd16304cd8ece422f1f88b304524e43903d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b390ca7806fe319a3ae9c8c07ef4bae543b9fea48a893b593f2a3f49bba1d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16a2c57153e6cd6eba7e65ab1fd22f1b17582b959536778a7e096c7a3136a5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832d7e80d26741997b0d8d03ae77a0b22c998c52162d38765008613eb8830cd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dee9f30bdf4a9cfdcddde3b8cc8ba7ee679c98477777133ec85e8bc2180fa5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2c33cfd5b082fa22440476b398ddc5166b067e0c5c90d2ed02c26b26511026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402d478454a9e7e7ee9856f3cd01d4077d5d27c7fdd910609ad167d5808961d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c51c58fcb065d7d53a8b94562b73697e5079ca2f82e1cf4db90b9686ee8cedd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0e6aaed88a59db6a4bc9c75e63c276f01529bb662e32ce8db0b3b70419bded(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5ad13f519ca34dd9b243574e212fb6bdff6e9491adb5eb4be626f5caf170cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151c9898cb7a69b3ffadce0dcc8a5bb74324eaf7ff6abaf71230c9e213ec0804(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50944091db6077eedd1619af57b0c46a2dc58ee18391da453c9f2753de4f1e54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf074e70b90b3b7a8ab1283b663d7d357168310e2563abefb7d810253995e88(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8739583e8546b907fb82d557d6b16a623de535b748a4316c0fe09770d061c3a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce549e54b85b0c042e4f6da8acdc75d20afd9ba4033b22587c9028c9b83fc07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f23581a7c1c13690258897232662bae1ff0f9494e111df825413057ef304f67(
    value: typing.Optional[GoogleComputeInterconnectCircuitInfos],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fcf544a1528cd2ed6efe2a778710d6f2fd0ca370d0d7adfa12d6b455d7078f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interconnect_type: builtins.str,
    link_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    requested_link_count: jsii.Number,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    customer_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    macsec: typing.Optional[typing.Union[GoogleComputeInterconnectMacsec, typing.Dict[builtins.str, typing.Any]]] = None,
    macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    noc_contact_email: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_location: typing.Optional[builtins.str] = None,
    requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeInterconnectTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eff9d065f60be58dee9c9c088d67f3934e8bcbea1560bb245f78095af4447a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68177ac8ea72122469d82f0cdadf431fcdf9a1b936dd9f3d16071c33b200f310(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73426d43a8df7d27f2f0c8f0cf52b56c6a099a5cab5052741550a7a4a340582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52ecffc8519c1d7b4de2038f674455bcfbfbe4dee12db3844eef996f37dd459(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8296575a394ea47d7adc14f55f1814efed79b44c7748479657a39ed9d8eb5f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1132f881949c795192c705a7146c4bca2f13e13a96faae2ba2dc7e2f6a67355f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b086f05c29479fc4020f19b6b9d48d584d1b235f34193eb4092a4b2b7c41f0f4(
    value: typing.Optional[GoogleComputeInterconnectExpectedOutages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6763a5f46d2ad9e6075a67f1c68bc4aba8b4c0b9b9a8ecb0b5d7c349be288b19(
    *,
    pre_shared_keys: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeInterconnectMacsecPreSharedKeys, typing.Dict[builtins.str, typing.Any]]]],
    fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2276f4e1282af9a279c9e9ed5d59470242d54a6890e6c11f1f3b12154ee1fcab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0e5f48e80d4a72624dbfbddaccce66cdb0a904ae715f1eeadd9088e08e4195(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeInterconnectMacsecPreSharedKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9185861032736ad0c04f837d7df128cae106a46096beeedab4f63554137e3eff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ace2e0d837236e028ce002c63436387de23c2a095eaa2fc68e2581211cf0f5e(
    value: typing.Optional[GoogleComputeInterconnectMacsec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114153f3d14e6b064ffe2b610d2f69bed89c6fdff2773bb0cb58e691d2cba583(
    *,
    name: builtins.str,
    fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316a097ae7caff5b654841ab6791745f9e786a7d79ec21dab08140babf55209c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354594ce268813b4e6199ddb6777dc55ee6be0556523006af0cc4bde68a88a3c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443a8253d86bb7d7e938865a37855c0930c55084f55e39e30eaec588bdbf6d17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4d8f37251f3a63d82358b92de3ea3a6273c634dfd8ac42d867d23dae689656(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cf5743235231d9c24614e1bc08c6d37c5133f452743084bf04de612f18b248(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e654e27913ac200f0725018858a4aa1b5da9e0308bc74514827948bcccaded7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeInterconnectMacsecPreSharedKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65b08a8b704dfe3f7f87cf463acb64032c6a6c2f843d72f1c7ec36b320d3223(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c9b552e49e7bf0e6d7759da438b640ba8cb4e9df67a56330dcb13e2406dd15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced11e36a8fd012f4ee496568ad45f28e60da3d0b6ce4994508b15382f75ffc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebce1f740dfaa04d196365a5ac4a0140f89d19d63ab2bc465cfc6741e2b61c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc97fbdb9badc79c66341084173bc0279c5aa78bb109497d79169060e9a2d16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectMacsecPreSharedKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb79a846adecd24ae62f21a0ea8b60861bad58e5971a51b07153beef8b3a31d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da781941dc08dc7ff33f46d60c1b0db3fad96f100b88d3e296002d0020ba4f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a072067d3d099d6c1d4bed80d57cd80fea5b47cb406427e171f60b5f0ee3542(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac258ebb73887d3d618c67e86d48b961c8f95779ef0eb306a944908930fd17f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe0fbcdcacaf24697720fcc5bd75a834529c0e84bc1ab20f23fdd2d0298dfbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dcf1d4ee1ba059fc0d14eeb7324e655774d488f5289b8c57a3adddd7ba99566(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeInterconnectTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
