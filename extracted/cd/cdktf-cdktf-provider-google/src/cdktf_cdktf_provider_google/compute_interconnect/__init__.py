r'''
# `google_compute_interconnect`

Refer to the Terraform Registry for docs: [`google_compute_interconnect`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect).
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


class ComputeInterconnect(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnect",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect google_compute_interconnect}.'''

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
        macsec: typing.Optional[typing.Union["ComputeInterconnectMacsec", typing.Dict[builtins.str, typing.Any]]] = None,
        macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        noc_contact_email: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_location: typing.Optional[builtins.str] = None,
        requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInterconnectTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect google_compute_interconnect} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param interconnect_type: Type of interconnect. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED. Can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Possible values: ["DEDICATED", "PARTNER", "IT_PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#interconnect_type ComputeInterconnect#interconnect_type}
        :param link_type: Type of link requested. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle. Can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics. - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. - LINK_TYPE_ETHERNET_400G_LR4: A 400G Ethernet with LR4 optics Possible values: ["LINK_TYPE_ETHERNET_10G_LR", "LINK_TYPE_ETHERNET_100G_LR", "LINK_TYPE_ETHERNET_400G_LR4"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#link_type ComputeInterconnect#link_type}
        :param location: URL of the InterconnectLocation object that represents where this connection is to be provisioned. Specifies the location inside Google's Networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#location ComputeInterconnect#location}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#name ComputeInterconnect#name}
        :param requested_link_count: Target number of physical links in the link bundle, as requested by the customer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#requested_link_count ComputeInterconnect#requested_link_count}
        :param admin_enabled: Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#admin_enabled ComputeInterconnect#admin_enabled}
        :param customer_name: Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect. This field is required for Dedicated and Partner Interconnect, should not be specified for cross-cloud interconnect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#customer_name ComputeInterconnect#customer_name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#description ComputeInterconnect#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#id ComputeInterconnect#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#labels ComputeInterconnect#labels}
        :param macsec: macsec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#macsec ComputeInterconnect#macsec}
        :param macsec_enabled: Enable or disable MACsec on this Interconnect connection. MACsec enablement fails if the MACsec object is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#macsec_enabled ComputeInterconnect#macsec_enabled}
        :param noc_contact_email: Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Cloud Monitoring logs alerting and Cloud Notifications. This field is required for users who sign up for Cloud Interconnect using workforce identity federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#noc_contact_email ComputeInterconnect#noc_contact_email}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#project ComputeInterconnect#project}.
        :param remote_location: Indicates that this is a Cross-Cloud Interconnect. This field specifies the location outside of Google's network that the interconnect is connected to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#remote_location ComputeInterconnect#remote_location}
        :param requested_features: interconnects.list of features requested for this Interconnect connection. Options: IF_MACSEC ( If specified then the connection is created on MACsec capable hardware ports. If not specified, the default value is false, which allocates non-MACsec capable ports first if available). Note that MACSEC is still technically allowed for compatibility reasons, but it does not work with the API, and will be removed in an upcoming major version. Possible values: ["MACSEC", "CROSS_SITE_NETWORK", "IF_MACSEC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#requested_features ComputeInterconnect#requested_features}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#timeouts ComputeInterconnect#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb64385f02e4b50332653752020c1f508e2fed6a3074f370de8a7e10e363dfd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInterconnectConfig(
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
        '''Generates CDKTF code for importing a ComputeInterconnect resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInterconnect to import.
        :param import_from_id: The id of the existing ComputeInterconnect that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInterconnect to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2841f10e0e4cf08e2c2843abe2f1f43c61c79a7fcf78f0999104b152b59194ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMacsec")
    def put_macsec(
        self,
        *,
        pre_shared_keys: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInterconnectMacsecPreSharedKeys", typing.Dict[builtins.str, typing.Any]]]],
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pre_shared_keys: pre_shared_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#pre_shared_keys ComputeInterconnect#pre_shared_keys}
        :param fail_open: If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established. By default, the Interconnect connection is configured with a must-secure security policy that drops all traffic if the MKA session cannot be established with your router. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#fail_open ComputeInterconnect#fail_open}
        '''
        value = ComputeInterconnectMacsec(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#create ComputeInterconnect#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#delete ComputeInterconnect#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#update ComputeInterconnect#update}.
        '''
        value = ComputeInterconnectTimeouts(
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
    def circuit_infos(self) -> "ComputeInterconnectCircuitInfosList":
        return typing.cast("ComputeInterconnectCircuitInfosList", jsii.get(self, "circuitInfos"))

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
    def expected_outages(self) -> "ComputeInterconnectExpectedOutagesList":
        return typing.cast("ComputeInterconnectExpectedOutagesList", jsii.get(self, "expectedOutages"))

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
    def macsec(self) -> "ComputeInterconnectMacsecOutputReference":
        return typing.cast("ComputeInterconnectMacsecOutputReference", jsii.get(self, "macsec"))

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
    def timeouts(self) -> "ComputeInterconnectTimeoutsOutputReference":
        return typing.cast("ComputeInterconnectTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def macsec_input(self) -> typing.Optional["ComputeInterconnectMacsec"]:
        return typing.cast(typing.Optional["ComputeInterconnectMacsec"], jsii.get(self, "macsecInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInterconnectTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInterconnectTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b88a9f825bcd3a2c73c5e88a1dc96fdc571c687a97e5e9ed0f16b7933eca5c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerName")
    def customer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerName"))

    @customer_name.setter
    def customer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83fc49c7de0cff730eb31c45c8bc771d2d72b24e13082511a203a217d8cdf7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a326f72bd74f460e879f4ac8d56463dc95ed400d4a6eb2e3085f5327b31196d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6665cb2a04b210ac0ef876c9f4382b0aa3fc7af7d84fca92812b29595e2bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interconnectType")
    def interconnect_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interconnectType"))

    @interconnect_type.setter
    def interconnect_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e208625afb5286299387661bd3086726eb2bfe455c8572bcf954da6c51ff5101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interconnectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1fb3cf5dcc424561367245ae3fe69a29d6e55356dfbe33ab08269a6f665bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkType")
    def link_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkType"))

    @link_type.setter
    def link_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d11113369394a7e894417c5e9bc6c31ba9ff27cff8a22858cd4c80bb42e416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27f5a13ddde4643fca86757dd1298b42965954ea02d6fa76916ad54ddd25824)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6329d187d217cf5e5501d65d33310ddce06251f124a7e5f2974fbf78fa280677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493871e13790315304b897c526b7f07a36bc0e70339e92a438361b80036c6c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nocContactEmail")
    def noc_contact_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nocContactEmail"))

    @noc_contact_email.setter
    def noc_contact_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe77c09e2e50269473b49ef86f721c5f8bad5d2b86efcc8dcbf2b3db8cd38d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nocContactEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8580b7b1fe1760d739e253d0416d8ec16921d8f31a8585f9fad8a4fdcbe94add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteLocation")
    def remote_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteLocation"))

    @remote_location.setter
    def remote_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309a29644041441eee173a8677e4ad1c2f562102feac80f03af8397ce38e5df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedFeatures")
    def requested_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requestedFeatures"))

    @requested_features.setter
    def requested_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5cb1de250222af18c6b61e2acc7436157b16cadad331e4b705cada4084490c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestedLinkCount")
    def requested_link_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestedLinkCount"))

    @requested_link_count.setter
    def requested_link_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d7563614f0eebb760f2a2eeeb88e1549ae9d7da4e236c0477351c7a5dc75ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedLinkCount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectCircuitInfos",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInterconnectCircuitInfos:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectCircuitInfos(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectCircuitInfosList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectCircuitInfosList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70d5a94394221383990405f22be63fdc3e1d03311a5c17d5b83e0a1538d7832a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInterconnectCircuitInfosOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e79138b2cbedd50a1c266b12f449fcd4563876dcf95733b26c9feac9e61015d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInterconnectCircuitInfosOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d743d035c68efcc029db957cacd7478309931ed8f9524c9ac316dfd76f1c0f06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15991d68a0219a5354b542ea92cd1354f2ff15c50fbf8cf98095c2289863a4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22e8064e95945bb2ef0ac38302ab8af18443d64e3ad77d41d68a0d910afdaf9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInterconnectCircuitInfosOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectCircuitInfosOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bac48730e69fd1c3529148f45c33a0fa9b83bb00a6e81839675355c681b6e71)
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
    def internal_value(self) -> typing.Optional[ComputeInterconnectCircuitInfos]:
        return typing.cast(typing.Optional[ComputeInterconnectCircuitInfos], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInterconnectCircuitInfos],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53510c29e50345f302146d550e4b39ec39537feb970bc670e0e123c517cf3135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectConfig",
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
class ComputeInterconnectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        macsec: typing.Optional[typing.Union["ComputeInterconnectMacsec", typing.Dict[builtins.str, typing.Any]]] = None,
        macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        noc_contact_email: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_location: typing.Optional[builtins.str] = None,
        requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInterconnectTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param interconnect_type: Type of interconnect. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED. Can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Possible values: ["DEDICATED", "PARTNER", "IT_PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#interconnect_type ComputeInterconnect#interconnect_type}
        :param link_type: Type of link requested. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle. Can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics. - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. - LINK_TYPE_ETHERNET_400G_LR4: A 400G Ethernet with LR4 optics Possible values: ["LINK_TYPE_ETHERNET_10G_LR", "LINK_TYPE_ETHERNET_100G_LR", "LINK_TYPE_ETHERNET_400G_LR4"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#link_type ComputeInterconnect#link_type}
        :param location: URL of the InterconnectLocation object that represents where this connection is to be provisioned. Specifies the location inside Google's Networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#location ComputeInterconnect#location}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#name ComputeInterconnect#name}
        :param requested_link_count: Target number of physical links in the link bundle, as requested by the customer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#requested_link_count ComputeInterconnect#requested_link_count}
        :param admin_enabled: Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#admin_enabled ComputeInterconnect#admin_enabled}
        :param customer_name: Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect. This field is required for Dedicated and Partner Interconnect, should not be specified for cross-cloud interconnect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#customer_name ComputeInterconnect#customer_name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#description ComputeInterconnect#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#id ComputeInterconnect#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#labels ComputeInterconnect#labels}
        :param macsec: macsec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#macsec ComputeInterconnect#macsec}
        :param macsec_enabled: Enable or disable MACsec on this Interconnect connection. MACsec enablement fails if the MACsec object is not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#macsec_enabled ComputeInterconnect#macsec_enabled}
        :param noc_contact_email: Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Cloud Monitoring logs alerting and Cloud Notifications. This field is required for users who sign up for Cloud Interconnect using workforce identity federation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#noc_contact_email ComputeInterconnect#noc_contact_email}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#project ComputeInterconnect#project}.
        :param remote_location: Indicates that this is a Cross-Cloud Interconnect. This field specifies the location outside of Google's network that the interconnect is connected to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#remote_location ComputeInterconnect#remote_location}
        :param requested_features: interconnects.list of features requested for this Interconnect connection. Options: IF_MACSEC ( If specified then the connection is created on MACsec capable hardware ports. If not specified, the default value is false, which allocates non-MACsec capable ports first if available). Note that MACSEC is still technically allowed for compatibility reasons, but it does not work with the API, and will be removed in an upcoming major version. Possible values: ["MACSEC", "CROSS_SITE_NETWORK", "IF_MACSEC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#requested_features ComputeInterconnect#requested_features}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#timeouts ComputeInterconnect#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(macsec, dict):
            macsec = ComputeInterconnectMacsec(**macsec)
        if isinstance(timeouts, dict):
            timeouts = ComputeInterconnectTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d27dbf511fed3903e079da20dc4511876291a26015e397700eb06f11f5093b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#interconnect_type ComputeInterconnect#interconnect_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#link_type ComputeInterconnect#link_type}
        '''
        result = self._values.get("link_type")
        assert result is not None, "Required property 'link_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''URL of the InterconnectLocation object that represents where this connection is to be provisioned. Specifies the location inside Google's Networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#location ComputeInterconnect#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#name ComputeInterconnect#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def requested_link_count(self) -> jsii.Number:
        '''Target number of physical links in the link bundle, as requested by the customer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#requested_link_count ComputeInterconnect#requested_link_count}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#admin_enabled ComputeInterconnect#admin_enabled}
        '''
        result = self._values.get("admin_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def customer_name(self) -> typing.Optional[builtins.str]:
        '''Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect.

        This field is required for Dedicated and Partner Interconnect, should not be specified
        for cross-cloud interconnect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#customer_name ComputeInterconnect#customer_name}
        '''
        result = self._values.get("customer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#description ComputeInterconnect#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#id ComputeInterconnect#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#labels ComputeInterconnect#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def macsec(self) -> typing.Optional["ComputeInterconnectMacsec"]:
        '''macsec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#macsec ComputeInterconnect#macsec}
        '''
        result = self._values.get("macsec")
        return typing.cast(typing.Optional["ComputeInterconnectMacsec"], result)

    @builtins.property
    def macsec_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable MACsec on this Interconnect connection. MACsec enablement fails if the MACsec object is not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#macsec_enabled ComputeInterconnect#macsec_enabled}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#noc_contact_email ComputeInterconnect#noc_contact_email}
        '''
        result = self._values.get("noc_contact_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#project ComputeInterconnect#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_location(self) -> typing.Optional[builtins.str]:
        '''Indicates that this is a Cross-Cloud Interconnect.

        This field specifies the location outside
        of Google's network that the interconnect is connected to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#remote_location ComputeInterconnect#remote_location}
        '''
        result = self._values.get("remote_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requested_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''interconnects.list of features requested for this Interconnect connection. Options: IF_MACSEC ( If specified then the connection is created on MACsec capable hardware ports. If not specified, the default value is false, which allocates non-MACsec capable ports first if available). Note that MACSEC is still technically allowed for compatibility reasons, but it does not work with the API, and will be removed in an upcoming major version. Possible values: ["MACSEC", "CROSS_SITE_NETWORK", "IF_MACSEC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#requested_features ComputeInterconnect#requested_features}
        '''
        result = self._values.get("requested_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInterconnectTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#timeouts ComputeInterconnect#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInterconnectTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectExpectedOutages",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeInterconnectExpectedOutages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectExpectedOutages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectExpectedOutagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectExpectedOutagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f5a6671df47baf95b7c4635b0233be8e046bb6d506f04ee3d46a205b8996d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInterconnectExpectedOutagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a0c5762fa3b1ad2e5db25bcd4e244605a418b1a78bb59c8b0bb6b9d33d41ad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInterconnectExpectedOutagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba882b4fb395c44410da2b9ff170674cf30234b564bfc7b02b84831087587e9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3816ba87194b2a07d05b67d66e83022136d337be8d37cfc8cec67b21e24b0a3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba83d38000f6a9ced23389e8fb68ecb85f968dff816d79d7cc6cd0afd6773abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeInterconnectExpectedOutagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectExpectedOutagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e22fb196931d6703de8e54039adb4f885559ea4a96a68db546106c6053ec8198)
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
    def internal_value(self) -> typing.Optional[ComputeInterconnectExpectedOutages]:
        return typing.cast(typing.Optional[ComputeInterconnectExpectedOutages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInterconnectExpectedOutages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b45bcf2ee4f35fd5d1ba2acfba6321d7411beab13e09378f5e7e9acbf96be00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectMacsec",
    jsii_struct_bases=[],
    name_mapping={"pre_shared_keys": "preSharedKeys", "fail_open": "failOpen"},
)
class ComputeInterconnectMacsec:
    def __init__(
        self,
        *,
        pre_shared_keys: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInterconnectMacsecPreSharedKeys", typing.Dict[builtins.str, typing.Any]]]],
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pre_shared_keys: pre_shared_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#pre_shared_keys ComputeInterconnect#pre_shared_keys}
        :param fail_open: If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established. By default, the Interconnect connection is configured with a must-secure security policy that drops all traffic if the MKA session cannot be established with your router. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#fail_open ComputeInterconnect#fail_open}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d18210cc183fd6bd47de113f9f07f79025b8b5a2de1004258eb364180409540)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInterconnectMacsecPreSharedKeys"]]:
        '''pre_shared_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#pre_shared_keys ComputeInterconnect#pre_shared_keys}
        '''
        result = self._values.get("pre_shared_keys")
        assert result is not None, "Required property 'pre_shared_keys' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInterconnectMacsecPreSharedKeys"]], result)

    @builtins.property
    def fail_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established.

        By default, the Interconnect
        connection is configured with a must-secure security policy that drops all traffic
        if the MKA session cannot be established with your router.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#fail_open ComputeInterconnect#fail_open}
        '''
        result = self._values.get("fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectMacsec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectMacsecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectMacsecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__667590f8dca4254180575d113bbf7f1f42403d66589e465d50e186929013bfa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPreSharedKeys")
    def put_pre_shared_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInterconnectMacsecPreSharedKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecf64af567a39b9ea33be0b535460266a567506cbbc46c5c897b22ff7a1460e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPreSharedKeys", [value]))

    @jsii.member(jsii_name="resetFailOpen")
    def reset_fail_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOpen", []))

    @builtins.property
    @jsii.member(jsii_name="preSharedKeys")
    def pre_shared_keys(self) -> "ComputeInterconnectMacsecPreSharedKeysList":
        return typing.cast("ComputeInterconnectMacsecPreSharedKeysList", jsii.get(self, "preSharedKeys"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInterconnectMacsecPreSharedKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInterconnectMacsecPreSharedKeys"]]], jsii.get(self, "preSharedKeysInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__637a8ae76bacae5ec51a0c2f6def939a48eb2756cd8502aa52e6743934628f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInterconnectMacsec]:
        return typing.cast(typing.Optional[ComputeInterconnectMacsec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeInterconnectMacsec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217df55510064d0422ab250e0dee16c2fbb7a50a4f0eb14c8c0fe7ee511e966d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectMacsecPreSharedKeys",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "fail_open": "failOpen", "start_time": "startTime"},
)
class ComputeInterconnectMacsecPreSharedKeys:
    def __init__(
        self,
        *,
        name: builtins.str,
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: A name for this pre-shared key. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#name ComputeInterconnect#name}
        :param fail_open: If set to true, the Interconnect connection is configured with a should-secure MACsec security policy, that allows the Google router to fallback to cleartext traffic if the MKA session cannot be established. By default, the Interconnect connection is configured with a must-secure security policy that drops all traffic if the MKA session cannot be established with your router. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#fail_open ComputeInterconnect#fail_open}
        :param start_time: A RFC3339 timestamp on or after which the key is valid. startTime can be in the future. If the keychain has a single key, startTime can be omitted. If the keychain has multiple keys, startTime is mandatory for each key. The start times of keys must be in increasing order. The start times of two consecutive keys must be at least 6 hours apart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#start_time ComputeInterconnect#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7984a58095e693975d0e9d7dec9fc8e078a109acb08c59a7256d491c40aa7e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#name ComputeInterconnect#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#fail_open ComputeInterconnect#fail_open}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#start_time ComputeInterconnect#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectMacsecPreSharedKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectMacsecPreSharedKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectMacsecPreSharedKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3ff8ca53fb14c2e323129c5ebc83254d795ba4fa8353a00b22671c95b426ac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInterconnectMacsecPreSharedKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cf6bcf5ee9b3c870bc6a97704e4abe31fdd8e1bf5f9001ca71d5cb42ff6aa3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInterconnectMacsecPreSharedKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c6d450e9c8ebc0102ad287f549b307f2f6ba905d29e2ba6146798370e138be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4b9d9eb13f3b173049a3e52fa0e74c8696afeccae0702b7e65ff035bf7cdec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__687085a8ba2a867e8bbf6b7466fbb5face34973ec31f644d4ff57ede64b736b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInterconnectMacsecPreSharedKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInterconnectMacsecPreSharedKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInterconnectMacsecPreSharedKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f10a057c4e8f18860b44adf22fa9593a5fa5dcda67cab2271c7b7f30a8eaf69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInterconnectMacsecPreSharedKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectMacsecPreSharedKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba1a3d85316c11d15522e60cd64ff036ae1fb9f5ceef130ecd7783d454aed60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0760c8b4457a35ae2a775e75779619db1b99d412188f92bd1426ad8c51a1e237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4028e30d8be78f1a1a1718ccbfa1720e24350ce2a3aa527974e50c8602da1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c51ebe5735df90a2f339c6d8ba0e088e844541f728c9361260c130adfcef41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectMacsecPreSharedKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectMacsecPreSharedKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectMacsecPreSharedKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351b36b8b84c04eb24e23e0a607887024277794c77c6578114bb30e88617bc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInterconnectTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#create ComputeInterconnect#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#delete ComputeInterconnect#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#update ComputeInterconnect#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2632f1a6b0ef313cf406357e154281fd1267f9b0cbb7755499d36b8c56367d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#create ComputeInterconnect#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#delete ComputeInterconnect#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_interconnect#update ComputeInterconnect#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInterconnectTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInterconnectTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInterconnect.ComputeInterconnectTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c0876863701b1fcebdfed5f249b2cf346e722293fa127b6a4b7bd37a4433426)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ff7068235cf5cb95b0e46c7a3f793239624bd9af3787978684c7e911e133da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165752aa7715373cec878eaae790002b5634c93bd71c9d317118622fa134cb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8432b1a28d7dee1c95681d71e6d927366f4d9e9b7d1aef9fbadc6d7b774ed772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66764d7ee59b2948096fe344bc7e52fc53ed6a5d98e0c67baadfcccc3961098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInterconnect",
    "ComputeInterconnectCircuitInfos",
    "ComputeInterconnectCircuitInfosList",
    "ComputeInterconnectCircuitInfosOutputReference",
    "ComputeInterconnectConfig",
    "ComputeInterconnectExpectedOutages",
    "ComputeInterconnectExpectedOutagesList",
    "ComputeInterconnectExpectedOutagesOutputReference",
    "ComputeInterconnectMacsec",
    "ComputeInterconnectMacsecOutputReference",
    "ComputeInterconnectMacsecPreSharedKeys",
    "ComputeInterconnectMacsecPreSharedKeysList",
    "ComputeInterconnectMacsecPreSharedKeysOutputReference",
    "ComputeInterconnectTimeouts",
    "ComputeInterconnectTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4eb64385f02e4b50332653752020c1f508e2fed6a3074f370de8a7e10e363dfd(
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
    macsec: typing.Optional[typing.Union[ComputeInterconnectMacsec, typing.Dict[builtins.str, typing.Any]]] = None,
    macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    noc_contact_email: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_location: typing.Optional[builtins.str] = None,
    requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInterconnectTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2841f10e0e4cf08e2c2843abe2f1f43c61c79a7fcf78f0999104b152b59194ca(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88a9f825bcd3a2c73c5e88a1dc96fdc571c687a97e5e9ed0f16b7933eca5c6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83fc49c7de0cff730eb31c45c8bc771d2d72b24e13082511a203a217d8cdf7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a326f72bd74f460e879f4ac8d56463dc95ed400d4a6eb2e3085f5327b31196d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6665cb2a04b210ac0ef876c9f4382b0aa3fc7af7d84fca92812b29595e2bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e208625afb5286299387661bd3086726eb2bfe455c8572bcf954da6c51ff5101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1fb3cf5dcc424561367245ae3fe69a29d6e55356dfbe33ab08269a6f665bf0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d11113369394a7e894417c5e9bc6c31ba9ff27cff8a22858cd4c80bb42e416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27f5a13ddde4643fca86757dd1298b42965954ea02d6fa76916ad54ddd25824(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6329d187d217cf5e5501d65d33310ddce06251f124a7e5f2974fbf78fa280677(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493871e13790315304b897c526b7f07a36bc0e70339e92a438361b80036c6c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe77c09e2e50269473b49ef86f721c5f8bad5d2b86efcc8dcbf2b3db8cd38d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8580b7b1fe1760d739e253d0416d8ec16921d8f31a8585f9fad8a4fdcbe94add(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309a29644041441eee173a8677e4ad1c2f562102feac80f03af8397ce38e5df6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5cb1de250222af18c6b61e2acc7436157b16cadad331e4b705cada4084490c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d7563614f0eebb760f2a2eeeb88e1549ae9d7da4e236c0477351c7a5dc75ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d5a94394221383990405f22be63fdc3e1d03311a5c17d5b83e0a1538d7832a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e79138b2cbedd50a1c266b12f449fcd4563876dcf95733b26c9feac9e61015d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d743d035c68efcc029db957cacd7478309931ed8f9524c9ac316dfd76f1c0f06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15991d68a0219a5354b542ea92cd1354f2ff15c50fbf8cf98095c2289863a4a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e8064e95945bb2ef0ac38302ab8af18443d64e3ad77d41d68a0d910afdaf9a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bac48730e69fd1c3529148f45c33a0fa9b83bb00a6e81839675355c681b6e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53510c29e50345f302146d550e4b39ec39537feb970bc670e0e123c517cf3135(
    value: typing.Optional[ComputeInterconnectCircuitInfos],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d27dbf511fed3903e079da20dc4511876291a26015e397700eb06f11f5093b2(
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
    macsec: typing.Optional[typing.Union[ComputeInterconnectMacsec, typing.Dict[builtins.str, typing.Any]]] = None,
    macsec_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    noc_contact_email: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_location: typing.Optional[builtins.str] = None,
    requested_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInterconnectTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f5a6671df47baf95b7c4635b0233be8e046bb6d506f04ee3d46a205b8996d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a0c5762fa3b1ad2e5db25bcd4e244605a418b1a78bb59c8b0bb6b9d33d41ad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba882b4fb395c44410da2b9ff170674cf30234b564bfc7b02b84831087587e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3816ba87194b2a07d05b67d66e83022136d337be8d37cfc8cec67b21e24b0a3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba83d38000f6a9ced23389e8fb68ecb85f968dff816d79d7cc6cd0afd6773abb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22fb196931d6703de8e54039adb4f885559ea4a96a68db546106c6053ec8198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b45bcf2ee4f35fd5d1ba2acfba6321d7411beab13e09378f5e7e9acbf96be00(
    value: typing.Optional[ComputeInterconnectExpectedOutages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d18210cc183fd6bd47de113f9f07f79025b8b5a2de1004258eb364180409540(
    *,
    pre_shared_keys: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInterconnectMacsecPreSharedKeys, typing.Dict[builtins.str, typing.Any]]]],
    fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667590f8dca4254180575d113bbf7f1f42403d66589e465d50e186929013bfa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecf64af567a39b9ea33be0b535460266a567506cbbc46c5c897b22ff7a1460e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInterconnectMacsecPreSharedKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637a8ae76bacae5ec51a0c2f6def939a48eb2756cd8502aa52e6743934628f9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217df55510064d0422ab250e0dee16c2fbb7a50a4f0eb14c8c0fe7ee511e966d(
    value: typing.Optional[ComputeInterconnectMacsec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7984a58095e693975d0e9d7dec9fc8e078a109acb08c59a7256d491c40aa7e(
    *,
    name: builtins.str,
    fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ff8ca53fb14c2e323129c5ebc83254d795ba4fa8353a00b22671c95b426ac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cf6bcf5ee9b3c870bc6a97704e4abe31fdd8e1bf5f9001ca71d5cb42ff6aa3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c6d450e9c8ebc0102ad287f549b307f2f6ba905d29e2ba6146798370e138be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4b9d9eb13f3b173049a3e52fa0e74c8696afeccae0702b7e65ff035bf7cdec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687085a8ba2a867e8bbf6b7466fbb5face34973ec31f644d4ff57ede64b736b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f10a057c4e8f18860b44adf22fa9593a5fa5dcda67cab2271c7b7f30a8eaf69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInterconnectMacsecPreSharedKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba1a3d85316c11d15522e60cd64ff036ae1fb9f5ceef130ecd7783d454aed60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0760c8b4457a35ae2a775e75779619db1b99d412188f92bd1426ad8c51a1e237(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4028e30d8be78f1a1a1718ccbfa1720e24350ce2a3aa527974e50c8602da1d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c51ebe5735df90a2f339c6d8ba0e088e844541f728c9361260c130adfcef41d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351b36b8b84c04eb24e23e0a607887024277794c77c6578114bb30e88617bc92(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectMacsecPreSharedKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2632f1a6b0ef313cf406357e154281fd1267f9b0cbb7755499d36b8c56367d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0876863701b1fcebdfed5f249b2cf346e722293fa127b6a4b7bd37a4433426(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ff7068235cf5cb95b0e46c7a3f793239624bd9af3787978684c7e911e133da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165752aa7715373cec878eaae790002b5634c93bd71c9d317118622fa134cb72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8432b1a28d7dee1c95681d71e6d927366f4d9e9b7d1aef9fbadc6d7b774ed772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66764d7ee59b2948096fe344bc7e52fc53ed6a5d98e0c67baadfcccc3961098(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInterconnectTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
