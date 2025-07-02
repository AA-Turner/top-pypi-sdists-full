r'''
# `azurerm_shared_image`

Refer to the Terraform Registry for docs: [`azurerm_shared_image`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image).
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


class SharedImage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImage",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image azurerm_shared_image}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gallery_name: builtins.str,
        identifier: typing.Union["SharedImageIdentifier", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        os_type: builtins.str,
        resource_group_name: builtins.str,
        accelerated_network_support_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        architecture: typing.Optional[builtins.str] = None,
        confidential_vm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_vm_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        disk_controller_type_nvme_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_types_not_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_of_life_date: typing.Optional[builtins.str] = None,
        eula: typing.Optional[builtins.str] = None,
        hibernation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hyper_v_generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
        max_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
        min_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
        min_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
        privacy_statement_uri: typing.Optional[builtins.str] = None,
        purchase_plan: typing.Optional[typing.Union["SharedImagePurchasePlan", typing.Dict[builtins.str, typing.Any]]] = None,
        release_note_uri: typing.Optional[builtins.str] = None,
        specialized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SharedImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trusted_launch_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image azurerm_shared_image} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gallery_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#gallery_name SharedImage#gallery_name}.
        :param identifier: identifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#identifier SharedImage#identifier}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#location SharedImage#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#name SharedImage#name}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#os_type SharedImage#os_type}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#resource_group_name SharedImage#resource_group_name}.
        :param accelerated_network_support_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#accelerated_network_support_enabled SharedImage#accelerated_network_support_enabled}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#architecture SharedImage#architecture}.
        :param confidential_vm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#confidential_vm_enabled SharedImage#confidential_vm_enabled}.
        :param confidential_vm_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#confidential_vm_supported SharedImage#confidential_vm_supported}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#description SharedImage#description}.
        :param disk_controller_type_nvme_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#disk_controller_type_nvme_enabled SharedImage#disk_controller_type_nvme_enabled}.
        :param disk_types_not_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#disk_types_not_allowed SharedImage#disk_types_not_allowed}.
        :param end_of_life_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#end_of_life_date SharedImage#end_of_life_date}.
        :param eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#eula SharedImage#eula}.
        :param hibernation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#hibernation_enabled SharedImage#hibernation_enabled}.
        :param hyper_v_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#hyper_v_generation SharedImage#hyper_v_generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#id SharedImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_recommended_memory_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#max_recommended_memory_in_gb SharedImage#max_recommended_memory_in_gb}.
        :param max_recommended_vcpu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#max_recommended_vcpu_count SharedImage#max_recommended_vcpu_count}.
        :param min_recommended_memory_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#min_recommended_memory_in_gb SharedImage#min_recommended_memory_in_gb}.
        :param min_recommended_vcpu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#min_recommended_vcpu_count SharedImage#min_recommended_vcpu_count}.
        :param privacy_statement_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#privacy_statement_uri SharedImage#privacy_statement_uri}.
        :param purchase_plan: purchase_plan block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#purchase_plan SharedImage#purchase_plan}
        :param release_note_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#release_note_uri SharedImage#release_note_uri}.
        :param specialized: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#specialized SharedImage#specialized}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#tags SharedImage#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#timeouts SharedImage#timeouts}
        :param trusted_launch_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#trusted_launch_enabled SharedImage#trusted_launch_enabled}.
        :param trusted_launch_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#trusted_launch_supported SharedImage#trusted_launch_supported}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670c2b89970318502d5fce7979d78698df2fa4374009d4c9eeac2bba2881c270)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SharedImageConfig(
            gallery_name=gallery_name,
            identifier=identifier,
            location=location,
            name=name,
            os_type=os_type,
            resource_group_name=resource_group_name,
            accelerated_network_support_enabled=accelerated_network_support_enabled,
            architecture=architecture,
            confidential_vm_enabled=confidential_vm_enabled,
            confidential_vm_supported=confidential_vm_supported,
            description=description,
            disk_controller_type_nvme_enabled=disk_controller_type_nvme_enabled,
            disk_types_not_allowed=disk_types_not_allowed,
            end_of_life_date=end_of_life_date,
            eula=eula,
            hibernation_enabled=hibernation_enabled,
            hyper_v_generation=hyper_v_generation,
            id=id,
            max_recommended_memory_in_gb=max_recommended_memory_in_gb,
            max_recommended_vcpu_count=max_recommended_vcpu_count,
            min_recommended_memory_in_gb=min_recommended_memory_in_gb,
            min_recommended_vcpu_count=min_recommended_vcpu_count,
            privacy_statement_uri=privacy_statement_uri,
            purchase_plan=purchase_plan,
            release_note_uri=release_note_uri,
            specialized=specialized,
            tags=tags,
            timeouts=timeouts,
            trusted_launch_enabled=trusted_launch_enabled,
            trusted_launch_supported=trusted_launch_supported,
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
        '''Generates CDKTF code for importing a SharedImage resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SharedImage to import.
        :param import_from_id: The id of the existing SharedImage that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SharedImage to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd1f9f1ff11abb0de41cf685d8b2e20514bc3ab4a8746d479248edc1d86867d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentifier")
    def put_identifier(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#offer SharedImage#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#publisher SharedImage#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#sku SharedImage#sku}.
        '''
        value = SharedImageIdentifier(offer=offer, publisher=publisher, sku=sku)

        return typing.cast(None, jsii.invoke(self, "putIdentifier", [value]))

    @jsii.member(jsii_name="putPurchasePlan")
    def put_purchase_plan(
        self,
        *,
        name: builtins.str,
        product: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#name SharedImage#name}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#product SharedImage#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#publisher SharedImage#publisher}.
        '''
        value = SharedImagePurchasePlan(
            name=name, product=product, publisher=publisher
        )

        return typing.cast(None, jsii.invoke(self, "putPurchasePlan", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#create SharedImage#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#delete SharedImage#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#read SharedImage#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#update SharedImage#update}.
        '''
        value = SharedImageTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAcceleratedNetworkSupportEnabled")
    def reset_accelerated_network_support_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratedNetworkSupportEnabled", []))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetConfidentialVmEnabled")
    def reset_confidential_vm_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialVmEnabled", []))

    @jsii.member(jsii_name="resetConfidentialVmSupported")
    def reset_confidential_vm_supported(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialVmSupported", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskControllerTypeNvmeEnabled")
    def reset_disk_controller_type_nvme_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskControllerTypeNvmeEnabled", []))

    @jsii.member(jsii_name="resetDiskTypesNotAllowed")
    def reset_disk_types_not_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskTypesNotAllowed", []))

    @jsii.member(jsii_name="resetEndOfLifeDate")
    def reset_end_of_life_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndOfLifeDate", []))

    @jsii.member(jsii_name="resetEula")
    def reset_eula(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEula", []))

    @jsii.member(jsii_name="resetHibernationEnabled")
    def reset_hibernation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHibernationEnabled", []))

    @jsii.member(jsii_name="resetHyperVGeneration")
    def reset_hyper_v_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHyperVGeneration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxRecommendedMemoryInGb")
    def reset_max_recommended_memory_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRecommendedMemoryInGb", []))

    @jsii.member(jsii_name="resetMaxRecommendedVcpuCount")
    def reset_max_recommended_vcpu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRecommendedVcpuCount", []))

    @jsii.member(jsii_name="resetMinRecommendedMemoryInGb")
    def reset_min_recommended_memory_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRecommendedMemoryInGb", []))

    @jsii.member(jsii_name="resetMinRecommendedVcpuCount")
    def reset_min_recommended_vcpu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRecommendedVcpuCount", []))

    @jsii.member(jsii_name="resetPrivacyStatementUri")
    def reset_privacy_statement_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacyStatementUri", []))

    @jsii.member(jsii_name="resetPurchasePlan")
    def reset_purchase_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurchasePlan", []))

    @jsii.member(jsii_name="resetReleaseNoteUri")
    def reset_release_note_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReleaseNoteUri", []))

    @jsii.member(jsii_name="resetSpecialized")
    def reset_specialized(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecialized", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrustedLaunchEnabled")
    def reset_trusted_launch_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedLaunchEnabled", []))

    @jsii.member(jsii_name="resetTrustedLaunchSupported")
    def reset_trusted_launch_supported(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedLaunchSupported", []))

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
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> "SharedImageIdentifierOutputReference":
        return typing.cast("SharedImageIdentifierOutputReference", jsii.get(self, "identifier"))

    @builtins.property
    @jsii.member(jsii_name="purchasePlan")
    def purchase_plan(self) -> "SharedImagePurchasePlanOutputReference":
        return typing.cast("SharedImagePurchasePlanOutputReference", jsii.get(self, "purchasePlan"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SharedImageTimeoutsOutputReference":
        return typing.cast("SharedImageTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="acceleratedNetworkSupportEnabledInput")
    def accelerated_network_support_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceleratedNetworkSupportEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialVmEnabledInput")
    def confidential_vm_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confidentialVmEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialVmSupportedInput")
    def confidential_vm_supported_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confidentialVmSupportedInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskControllerTypeNvmeEnabledInput")
    def disk_controller_type_nvme_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskControllerTypeNvmeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypesNotAllowedInput")
    def disk_types_not_allowed_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "diskTypesNotAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="endOfLifeDateInput")
    def end_of_life_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endOfLifeDateInput"))

    @builtins.property
    @jsii.member(jsii_name="eulaInput")
    def eula_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eulaInput"))

    @builtins.property
    @jsii.member(jsii_name="galleryNameInput")
    def gallery_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "galleryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hibernationEnabledInput")
    def hibernation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hibernationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hyperVGenerationInput")
    def hyper_v_generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hyperVGenerationInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional["SharedImageIdentifier"]:
        return typing.cast(typing.Optional["SharedImageIdentifier"], jsii.get(self, "identifierInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRecommendedMemoryInGbInput")
    def max_recommended_memory_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRecommendedMemoryInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRecommendedVcpuCountInput")
    def max_recommended_vcpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRecommendedVcpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minRecommendedMemoryInGbInput")
    def min_recommended_memory_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRecommendedMemoryInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="minRecommendedVcpuCountInput")
    def min_recommended_vcpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRecommendedVcpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyStatementUriInput")
    def privacy_statement_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyStatementUriInput"))

    @builtins.property
    @jsii.member(jsii_name="purchasePlanInput")
    def purchase_plan_input(self) -> typing.Optional["SharedImagePurchasePlan"]:
        return typing.cast(typing.Optional["SharedImagePurchasePlan"], jsii.get(self, "purchasePlanInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseNoteUriInput")
    def release_note_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseNoteUriInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="specializedInput")
    def specialized_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "specializedInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SharedImageTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SharedImageTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedLaunchEnabledInput")
    def trusted_launch_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trustedLaunchEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedLaunchSupportedInput")
    def trusted_launch_supported_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trustedLaunchSupportedInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratedNetworkSupportEnabled")
    def accelerated_network_support_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceleratedNetworkSupportEnabled"))

    @accelerated_network_support_enabled.setter
    def accelerated_network_support_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89edd8422151d91e045214b597f93e374cf66213c27a3644a5ee3cab0c468700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratedNetworkSupportEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5570f6b860320f8ff6c108562e2dba19b0ade9f1689e071be30282f240d01fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidentialVmEnabled")
    def confidential_vm_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "confidentialVmEnabled"))

    @confidential_vm_enabled.setter
    def confidential_vm_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7187f7945f7b96bbf74c54204b852dc3931285c743619b7bb86d79139a6380e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialVmEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confidentialVmSupported")
    def confidential_vm_supported(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "confidentialVmSupported"))

    @confidential_vm_supported.setter
    def confidential_vm_supported(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c476c5b5e46408dcb4561b86b4875c7a963c71a40e6e3dc3f84b028627536a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialVmSupported", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fbc3143d3b13a017868567e4ae93b3e8bce0f9d896c2e660acc878e99c6116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskControllerTypeNvmeEnabled")
    def disk_controller_type_nvme_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskControllerTypeNvmeEnabled"))

    @disk_controller_type_nvme_enabled.setter
    def disk_controller_type_nvme_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e72db8f9bceb77876ce1639fa9ba4804e6e1b3decc6527cd3548a2f9cf0231f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskControllerTypeNvmeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskTypesNotAllowed")
    def disk_types_not_allowed(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "diskTypesNotAllowed"))

    @disk_types_not_allowed.setter
    def disk_types_not_allowed(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b75b870e46a711dc9c3dfe5d409a55f6a83198d64dc046bb9016cda232daf11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskTypesNotAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endOfLifeDate")
    def end_of_life_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endOfLifeDate"))

    @end_of_life_date.setter
    def end_of_life_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9f9c43a65d63688de3b17fc2284ab81dea8ccc370e3e2acf6db436c893a30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endOfLifeDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eula")
    def eula(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eula"))

    @eula.setter
    def eula(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a15772f6b7333d1e1c9dff7e9c16c912128d4d9f63cb71ddcc8066f0a6014ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="galleryName")
    def gallery_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "galleryName"))

    @gallery_name.setter
    def gallery_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0bb01ad229c32e5f674cd50bbe0b19d7f234ef488d16af82d667542214b79e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "galleryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hibernationEnabled")
    def hibernation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hibernationEnabled"))

    @hibernation_enabled.setter
    def hibernation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3de0933572d128be13078411c36fe220730660742009e469fd6e1d2894246a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hibernationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hyperVGeneration")
    def hyper_v_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hyperVGeneration"))

    @hyper_v_generation.setter
    def hyper_v_generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7507e80f10c234d95ac751d4f1cbdf045a26f49985fd558957e847ca14efba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hyperVGeneration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cf05531d359710a9c04f4aa1dfdcfa264e5738e772520957b17a3fcc9a0cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc19d63c7d907781b792b42dda67c4b2e06efe290d73be554aecf26289f0164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRecommendedMemoryInGb")
    def max_recommended_memory_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRecommendedMemoryInGb"))

    @max_recommended_memory_in_gb.setter
    def max_recommended_memory_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de468ffad53679ad3bf5ac47e831230ab0345dd34fb0620b0aff63048b6231a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRecommendedMemoryInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRecommendedVcpuCount")
    def max_recommended_vcpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRecommendedVcpuCount"))

    @max_recommended_vcpu_count.setter
    def max_recommended_vcpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61bae9d738cd251dfd78ed9fac5ab63c8cc646557da8426d5419225eae1c4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRecommendedVcpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRecommendedMemoryInGb")
    def min_recommended_memory_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRecommendedMemoryInGb"))

    @min_recommended_memory_in_gb.setter
    def min_recommended_memory_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8511eeba45c5356810b69fbcb718b6c88f47d06ce4f9ac68b300d52b2dc667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRecommendedMemoryInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRecommendedVcpuCount")
    def min_recommended_vcpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRecommendedVcpuCount"))

    @min_recommended_vcpu_count.setter
    def min_recommended_vcpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3a4f7a67072c35ca8f41c5bfbdc69825b35afe072ad20111efe04ac4bd6c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRecommendedVcpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767da99741d1e9aff5dee3153e8c83a5505eb41d80030d75c8ff20c2bcf40aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9e8c928fbd331799210346b651cca30b1e547aba7bbffdd6e17acd39b214ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privacyStatementUri")
    def privacy_statement_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacyStatementUri"))

    @privacy_statement_uri.setter
    def privacy_statement_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff01b1b489e6a5917b181d2197a8eacc37d6547225f6ea24fbc7cf977cc6946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacyStatementUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseNoteUri")
    def release_note_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseNoteUri"))

    @release_note_uri.setter
    def release_note_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7cec368f92f29e8ee7e55ed02173ca109ee4ae155e1f2691764047f3645af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseNoteUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801db240810a8d9f217c1910c708f3147be01fd8e152745605a2059704cc024b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specialized")
    def specialized(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "specialized"))

    @specialized.setter
    def specialized(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0061d793f270abb7813233aa3883d059a894a8761b0e3bfccbc5b7fe0e1c7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specialized", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81d8b88e7842fdb79756621c758116929a4c8cb282327d697200bb3a8a52850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedLaunchEnabled")
    def trusted_launch_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trustedLaunchEnabled"))

    @trusted_launch_enabled.setter
    def trusted_launch_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045e1105dd48aacb23c1eabfbf6089927497c0a02f32fc28dead4bf669617d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedLaunchEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedLaunchSupported")
    def trusted_launch_supported(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trustedLaunchSupported"))

    @trusted_launch_supported.setter
    def trusted_launch_supported(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08890738427afce1fe53a9eed0507c041feb5d056fac6c6f3ee5d1d4ceacc1d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedLaunchSupported", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImageConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "gallery_name": "galleryName",
        "identifier": "identifier",
        "location": "location",
        "name": "name",
        "os_type": "osType",
        "resource_group_name": "resourceGroupName",
        "accelerated_network_support_enabled": "acceleratedNetworkSupportEnabled",
        "architecture": "architecture",
        "confidential_vm_enabled": "confidentialVmEnabled",
        "confidential_vm_supported": "confidentialVmSupported",
        "description": "description",
        "disk_controller_type_nvme_enabled": "diskControllerTypeNvmeEnabled",
        "disk_types_not_allowed": "diskTypesNotAllowed",
        "end_of_life_date": "endOfLifeDate",
        "eula": "eula",
        "hibernation_enabled": "hibernationEnabled",
        "hyper_v_generation": "hyperVGeneration",
        "id": "id",
        "max_recommended_memory_in_gb": "maxRecommendedMemoryInGb",
        "max_recommended_vcpu_count": "maxRecommendedVcpuCount",
        "min_recommended_memory_in_gb": "minRecommendedMemoryInGb",
        "min_recommended_vcpu_count": "minRecommendedVcpuCount",
        "privacy_statement_uri": "privacyStatementUri",
        "purchase_plan": "purchasePlan",
        "release_note_uri": "releaseNoteUri",
        "specialized": "specialized",
        "tags": "tags",
        "timeouts": "timeouts",
        "trusted_launch_enabled": "trustedLaunchEnabled",
        "trusted_launch_supported": "trustedLaunchSupported",
    },
)
class SharedImageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gallery_name: builtins.str,
        identifier: typing.Union["SharedImageIdentifier", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        os_type: builtins.str,
        resource_group_name: builtins.str,
        accelerated_network_support_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        architecture: typing.Optional[builtins.str] = None,
        confidential_vm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_vm_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        disk_controller_type_nvme_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_types_not_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_of_life_date: typing.Optional[builtins.str] = None,
        eula: typing.Optional[builtins.str] = None,
        hibernation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hyper_v_generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
        max_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
        min_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
        min_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
        privacy_statement_uri: typing.Optional[builtins.str] = None,
        purchase_plan: typing.Optional[typing.Union["SharedImagePurchasePlan", typing.Dict[builtins.str, typing.Any]]] = None,
        release_note_uri: typing.Optional[builtins.str] = None,
        specialized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SharedImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trusted_launch_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param gallery_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#gallery_name SharedImage#gallery_name}.
        :param identifier: identifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#identifier SharedImage#identifier}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#location SharedImage#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#name SharedImage#name}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#os_type SharedImage#os_type}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#resource_group_name SharedImage#resource_group_name}.
        :param accelerated_network_support_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#accelerated_network_support_enabled SharedImage#accelerated_network_support_enabled}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#architecture SharedImage#architecture}.
        :param confidential_vm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#confidential_vm_enabled SharedImage#confidential_vm_enabled}.
        :param confidential_vm_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#confidential_vm_supported SharedImage#confidential_vm_supported}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#description SharedImage#description}.
        :param disk_controller_type_nvme_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#disk_controller_type_nvme_enabled SharedImage#disk_controller_type_nvme_enabled}.
        :param disk_types_not_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#disk_types_not_allowed SharedImage#disk_types_not_allowed}.
        :param end_of_life_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#end_of_life_date SharedImage#end_of_life_date}.
        :param eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#eula SharedImage#eula}.
        :param hibernation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#hibernation_enabled SharedImage#hibernation_enabled}.
        :param hyper_v_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#hyper_v_generation SharedImage#hyper_v_generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#id SharedImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_recommended_memory_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#max_recommended_memory_in_gb SharedImage#max_recommended_memory_in_gb}.
        :param max_recommended_vcpu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#max_recommended_vcpu_count SharedImage#max_recommended_vcpu_count}.
        :param min_recommended_memory_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#min_recommended_memory_in_gb SharedImage#min_recommended_memory_in_gb}.
        :param min_recommended_vcpu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#min_recommended_vcpu_count SharedImage#min_recommended_vcpu_count}.
        :param privacy_statement_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#privacy_statement_uri SharedImage#privacy_statement_uri}.
        :param purchase_plan: purchase_plan block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#purchase_plan SharedImage#purchase_plan}
        :param release_note_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#release_note_uri SharedImage#release_note_uri}.
        :param specialized: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#specialized SharedImage#specialized}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#tags SharedImage#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#timeouts SharedImage#timeouts}
        :param trusted_launch_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#trusted_launch_enabled SharedImage#trusted_launch_enabled}.
        :param trusted_launch_supported: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#trusted_launch_supported SharedImage#trusted_launch_supported}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identifier, dict):
            identifier = SharedImageIdentifier(**identifier)
        if isinstance(purchase_plan, dict):
            purchase_plan = SharedImagePurchasePlan(**purchase_plan)
        if isinstance(timeouts, dict):
            timeouts = SharedImageTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a074f8495c23b3514ebd248c8f30d37e361c066254698751bcdf1d8497c60e1f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gallery_name", value=gallery_name, expected_type=type_hints["gallery_name"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument accelerated_network_support_enabled", value=accelerated_network_support_enabled, expected_type=type_hints["accelerated_network_support_enabled"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument confidential_vm_enabled", value=confidential_vm_enabled, expected_type=type_hints["confidential_vm_enabled"])
            check_type(argname="argument confidential_vm_supported", value=confidential_vm_supported, expected_type=type_hints["confidential_vm_supported"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_controller_type_nvme_enabled", value=disk_controller_type_nvme_enabled, expected_type=type_hints["disk_controller_type_nvme_enabled"])
            check_type(argname="argument disk_types_not_allowed", value=disk_types_not_allowed, expected_type=type_hints["disk_types_not_allowed"])
            check_type(argname="argument end_of_life_date", value=end_of_life_date, expected_type=type_hints["end_of_life_date"])
            check_type(argname="argument eula", value=eula, expected_type=type_hints["eula"])
            check_type(argname="argument hibernation_enabled", value=hibernation_enabled, expected_type=type_hints["hibernation_enabled"])
            check_type(argname="argument hyper_v_generation", value=hyper_v_generation, expected_type=type_hints["hyper_v_generation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_recommended_memory_in_gb", value=max_recommended_memory_in_gb, expected_type=type_hints["max_recommended_memory_in_gb"])
            check_type(argname="argument max_recommended_vcpu_count", value=max_recommended_vcpu_count, expected_type=type_hints["max_recommended_vcpu_count"])
            check_type(argname="argument min_recommended_memory_in_gb", value=min_recommended_memory_in_gb, expected_type=type_hints["min_recommended_memory_in_gb"])
            check_type(argname="argument min_recommended_vcpu_count", value=min_recommended_vcpu_count, expected_type=type_hints["min_recommended_vcpu_count"])
            check_type(argname="argument privacy_statement_uri", value=privacy_statement_uri, expected_type=type_hints["privacy_statement_uri"])
            check_type(argname="argument purchase_plan", value=purchase_plan, expected_type=type_hints["purchase_plan"])
            check_type(argname="argument release_note_uri", value=release_note_uri, expected_type=type_hints["release_note_uri"])
            check_type(argname="argument specialized", value=specialized, expected_type=type_hints["specialized"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trusted_launch_enabled", value=trusted_launch_enabled, expected_type=type_hints["trusted_launch_enabled"])
            check_type(argname="argument trusted_launch_supported", value=trusted_launch_supported, expected_type=type_hints["trusted_launch_supported"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gallery_name": gallery_name,
            "identifier": identifier,
            "location": location,
            "name": name,
            "os_type": os_type,
            "resource_group_name": resource_group_name,
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
        if accelerated_network_support_enabled is not None:
            self._values["accelerated_network_support_enabled"] = accelerated_network_support_enabled
        if architecture is not None:
            self._values["architecture"] = architecture
        if confidential_vm_enabled is not None:
            self._values["confidential_vm_enabled"] = confidential_vm_enabled
        if confidential_vm_supported is not None:
            self._values["confidential_vm_supported"] = confidential_vm_supported
        if description is not None:
            self._values["description"] = description
        if disk_controller_type_nvme_enabled is not None:
            self._values["disk_controller_type_nvme_enabled"] = disk_controller_type_nvme_enabled
        if disk_types_not_allowed is not None:
            self._values["disk_types_not_allowed"] = disk_types_not_allowed
        if end_of_life_date is not None:
            self._values["end_of_life_date"] = end_of_life_date
        if eula is not None:
            self._values["eula"] = eula
        if hibernation_enabled is not None:
            self._values["hibernation_enabled"] = hibernation_enabled
        if hyper_v_generation is not None:
            self._values["hyper_v_generation"] = hyper_v_generation
        if id is not None:
            self._values["id"] = id
        if max_recommended_memory_in_gb is not None:
            self._values["max_recommended_memory_in_gb"] = max_recommended_memory_in_gb
        if max_recommended_vcpu_count is not None:
            self._values["max_recommended_vcpu_count"] = max_recommended_vcpu_count
        if min_recommended_memory_in_gb is not None:
            self._values["min_recommended_memory_in_gb"] = min_recommended_memory_in_gb
        if min_recommended_vcpu_count is not None:
            self._values["min_recommended_vcpu_count"] = min_recommended_vcpu_count
        if privacy_statement_uri is not None:
            self._values["privacy_statement_uri"] = privacy_statement_uri
        if purchase_plan is not None:
            self._values["purchase_plan"] = purchase_plan
        if release_note_uri is not None:
            self._values["release_note_uri"] = release_note_uri
        if specialized is not None:
            self._values["specialized"] = specialized
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trusted_launch_enabled is not None:
            self._values["trusted_launch_enabled"] = trusted_launch_enabled
        if trusted_launch_supported is not None:
            self._values["trusted_launch_supported"] = trusted_launch_supported

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
    def gallery_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#gallery_name SharedImage#gallery_name}.'''
        result = self._values.get("gallery_name")
        assert result is not None, "Required property 'gallery_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> "SharedImageIdentifier":
        '''identifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#identifier SharedImage#identifier}
        '''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast("SharedImageIdentifier", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#location SharedImage#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#name SharedImage#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#os_type SharedImage#os_type}.'''
        result = self._values.get("os_type")
        assert result is not None, "Required property 'os_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#resource_group_name SharedImage#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerated_network_support_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#accelerated_network_support_enabled SharedImage#accelerated_network_support_enabled}.'''
        result = self._values.get("accelerated_network_support_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#architecture SharedImage#architecture}.'''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def confidential_vm_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#confidential_vm_enabled SharedImage#confidential_vm_enabled}.'''
        result = self._values.get("confidential_vm_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def confidential_vm_supported(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#confidential_vm_supported SharedImage#confidential_vm_supported}.'''
        result = self._values.get("confidential_vm_supported")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#description SharedImage#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_controller_type_nvme_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#disk_controller_type_nvme_enabled SharedImage#disk_controller_type_nvme_enabled}.'''
        result = self._values.get("disk_controller_type_nvme_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_types_not_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#disk_types_not_allowed SharedImage#disk_types_not_allowed}.'''
        result = self._values.get("disk_types_not_allowed")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def end_of_life_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#end_of_life_date SharedImage#end_of_life_date}.'''
        result = self._values.get("end_of_life_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eula(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#eula SharedImage#eula}.'''
        result = self._values.get("eula")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hibernation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#hibernation_enabled SharedImage#hibernation_enabled}.'''
        result = self._values.get("hibernation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hyper_v_generation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#hyper_v_generation SharedImage#hyper_v_generation}.'''
        result = self._values.get("hyper_v_generation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#id SharedImage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_recommended_memory_in_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#max_recommended_memory_in_gb SharedImage#max_recommended_memory_in_gb}.'''
        result = self._values.get("max_recommended_memory_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_recommended_vcpu_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#max_recommended_vcpu_count SharedImage#max_recommended_vcpu_count}.'''
        result = self._values.get("max_recommended_vcpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_recommended_memory_in_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#min_recommended_memory_in_gb SharedImage#min_recommended_memory_in_gb}.'''
        result = self._values.get("min_recommended_memory_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_recommended_vcpu_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#min_recommended_vcpu_count SharedImage#min_recommended_vcpu_count}.'''
        result = self._values.get("min_recommended_vcpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def privacy_statement_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#privacy_statement_uri SharedImage#privacy_statement_uri}.'''
        result = self._values.get("privacy_statement_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purchase_plan(self) -> typing.Optional["SharedImagePurchasePlan"]:
        '''purchase_plan block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#purchase_plan SharedImage#purchase_plan}
        '''
        result = self._values.get("purchase_plan")
        return typing.cast(typing.Optional["SharedImagePurchasePlan"], result)

    @builtins.property
    def release_note_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#release_note_uri SharedImage#release_note_uri}.'''
        result = self._values.get("release_note_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def specialized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#specialized SharedImage#specialized}.'''
        result = self._values.get("specialized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#tags SharedImage#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SharedImageTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#timeouts SharedImage#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SharedImageTimeouts"], result)

    @builtins.property
    def trusted_launch_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#trusted_launch_enabled SharedImage#trusted_launch_enabled}.'''
        result = self._values.get("trusted_launch_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trusted_launch_supported(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#trusted_launch_supported SharedImage#trusted_launch_supported}.'''
        result = self._values.get("trusted_launch_supported")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImageIdentifier",
    jsii_struct_bases=[],
    name_mapping={"offer": "offer", "publisher": "publisher", "sku": "sku"},
)
class SharedImageIdentifier:
    def __init__(
        self,
        *,
        offer: builtins.str,
        publisher: builtins.str,
        sku: builtins.str,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#offer SharedImage#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#publisher SharedImage#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#sku SharedImage#sku}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911cf423281b4e0524d90d224d43091f5347a00c77b74c9038e08a6f568b2d2c)
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "offer": offer,
            "publisher": publisher,
            "sku": sku,
        }

    @builtins.property
    def offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#offer SharedImage#offer}.'''
        result = self._values.get("offer")
        assert result is not None, "Required property 'offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#publisher SharedImage#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#sku SharedImage#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedImageIdentifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SharedImageIdentifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImageIdentifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e254384632277debb814768e3c83e6737f05dc0c2d45362ef76fb31c2b8f0632)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2eaa639a4cef379799f6de79319149c9c7ee8e57462915ceca2a3be5998b39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75ec7c14f07c3a676a16022eb08f27a4604b408c66773247c13387c301df8ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ce568790a8683e1c373f1c829034990b345dc707b5b87ffe7a93e87b58c6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SharedImageIdentifier]:
        return typing.cast(typing.Optional[SharedImageIdentifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SharedImageIdentifier]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db820aaf63a0d8243495b1930529ad17e0c1434926353a870ae3a42b02ed2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImagePurchasePlan",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "product": "product", "publisher": "publisher"},
)
class SharedImagePurchasePlan:
    def __init__(
        self,
        *,
        name: builtins.str,
        product: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#name SharedImage#name}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#product SharedImage#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#publisher SharedImage#publisher}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded5f754db05c1abe8bd3223c2f2fa41d24aa71d776ba2fcfcd440b45a14ddf0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if product is not None:
            self._values["product"] = product
        if publisher is not None:
            self._values["publisher"] = publisher

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#name SharedImage#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#product SharedImage#product}.'''
        result = self._values.get("product")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#publisher SharedImage#publisher}.'''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedImagePurchasePlan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SharedImagePurchasePlanOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImagePurchasePlanOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53c385bb601390e4ad3dfd1f2ed0d08e3718746915b3ed30f8383167b23a3c44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProduct")
    def reset_product(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProduct", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="productInput")
    def product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add7433257431f97398b99a2cc963fea970f38f826c78055a6eabfc790ee36e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="product")
    def product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "product"))

    @product.setter
    def product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c48cb0ba7841d5f4836bab73d93e5dc79cca0fa1f07db3b968f2d5ae685f010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "product", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef2e478a7c1c53bbbed89e7484f2307cf1155596ff809eebee12dd12d9c9fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SharedImagePurchasePlan]:
        return typing.cast(typing.Optional[SharedImagePurchasePlan], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SharedImagePurchasePlan]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd2ab1697f5ad69a28c560c882ca8e24922b9b43c6f9cdbd19013a55b0bb9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImageTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SharedImageTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#create SharedImage#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#delete SharedImage#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#read SharedImage#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#update SharedImage#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd42afec800fc577b32773c1eaa2f664b900f4c8af86aeeaec81f649fdf4bb6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#create SharedImage#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#delete SharedImage#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#read SharedImage#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/shared_image#update SharedImage#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharedImageTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SharedImageTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sharedImage.SharedImageTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b2fc495a8c1cc69409d4861ebdd82df54f38f56b4dd9381b0aeb858b1b285ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a68335b80743ce741e2931ea62963d07fe8f6c3b2d6a713066149a0e219651dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d4c56d98632485dd0c4115f2354b8f9f867d08b359a5f9c5ecefc84b7c4be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06dc72c74f6a1018a12541a47f018835a97d9aeb8560f33cbed162742d2faf58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97aa17162d162833f5d2fd586d757aa47aedfcadc70ced3a0315852498a49719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SharedImageTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SharedImageTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SharedImageTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89bc1730d7e0d62cf2dac3f2c3fba96edb8b976a9e20239a7037765d7712142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SharedImage",
    "SharedImageConfig",
    "SharedImageIdentifier",
    "SharedImageIdentifierOutputReference",
    "SharedImagePurchasePlan",
    "SharedImagePurchasePlanOutputReference",
    "SharedImageTimeouts",
    "SharedImageTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__670c2b89970318502d5fce7979d78698df2fa4374009d4c9eeac2bba2881c270(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gallery_name: builtins.str,
    identifier: typing.Union[SharedImageIdentifier, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    os_type: builtins.str,
    resource_group_name: builtins.str,
    accelerated_network_support_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    architecture: typing.Optional[builtins.str] = None,
    confidential_vm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_vm_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    disk_controller_type_nvme_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_types_not_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_of_life_date: typing.Optional[builtins.str] = None,
    eula: typing.Optional[builtins.str] = None,
    hibernation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hyper_v_generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
    max_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
    min_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
    min_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
    privacy_statement_uri: typing.Optional[builtins.str] = None,
    purchase_plan: typing.Optional[typing.Union[SharedImagePurchasePlan, typing.Dict[builtins.str, typing.Any]]] = None,
    release_note_uri: typing.Optional[builtins.str] = None,
    specialized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SharedImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trusted_launch_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__ffd1f9f1ff11abb0de41cf685d8b2e20514bc3ab4a8746d479248edc1d86867d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89edd8422151d91e045214b597f93e374cf66213c27a3644a5ee3cab0c468700(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5570f6b860320f8ff6c108562e2dba19b0ade9f1689e071be30282f240d01fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7187f7945f7b96bbf74c54204b852dc3931285c743619b7bb86d79139a6380e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c476c5b5e46408dcb4561b86b4875c7a963c71a40e6e3dc3f84b028627536a8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fbc3143d3b13a017868567e4ae93b3e8bce0f9d896c2e660acc878e99c6116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e72db8f9bceb77876ce1639fa9ba4804e6e1b3decc6527cd3548a2f9cf0231f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b75b870e46a711dc9c3dfe5d409a55f6a83198d64dc046bb9016cda232daf11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9f9c43a65d63688de3b17fc2284ab81dea8ccc370e3e2acf6db436c893a30e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a15772f6b7333d1e1c9dff7e9c16c912128d4d9f63cb71ddcc8066f0a6014ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0bb01ad229c32e5f674cd50bbe0b19d7f234ef488d16af82d667542214b79e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3de0933572d128be13078411c36fe220730660742009e469fd6e1d2894246a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7507e80f10c234d95ac751d4f1cbdf045a26f49985fd558957e847ca14efba2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cf05531d359710a9c04f4aa1dfdcfa264e5738e772520957b17a3fcc9a0cb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc19d63c7d907781b792b42dda67c4b2e06efe290d73be554aecf26289f0164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de468ffad53679ad3bf5ac47e831230ab0345dd34fb0620b0aff63048b6231a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61bae9d738cd251dfd78ed9fac5ab63c8cc646557da8426d5419225eae1c4fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8511eeba45c5356810b69fbcb718b6c88f47d06ce4f9ac68b300d52b2dc667(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3a4f7a67072c35ca8f41c5bfbdc69825b35afe072ad20111efe04ac4bd6c5b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767da99741d1e9aff5dee3153e8c83a5505eb41d80030d75c8ff20c2bcf40aa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9e8c928fbd331799210346b651cca30b1e547aba7bbffdd6e17acd39b214ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff01b1b489e6a5917b181d2197a8eacc37d6547225f6ea24fbc7cf977cc6946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7cec368f92f29e8ee7e55ed02173ca109ee4ae155e1f2691764047f3645af8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801db240810a8d9f217c1910c708f3147be01fd8e152745605a2059704cc024b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0061d793f270abb7813233aa3883d059a894a8761b0e3bfccbc5b7fe0e1c7bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81d8b88e7842fdb79756621c758116929a4c8cb282327d697200bb3a8a52850(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045e1105dd48aacb23c1eabfbf6089927497c0a02f32fc28dead4bf669617d25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08890738427afce1fe53a9eed0507c041feb5d056fac6c6f3ee5d1d4ceacc1d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a074f8495c23b3514ebd248c8f30d37e361c066254698751bcdf1d8497c60e1f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gallery_name: builtins.str,
    identifier: typing.Union[SharedImageIdentifier, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    os_type: builtins.str,
    resource_group_name: builtins.str,
    accelerated_network_support_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    architecture: typing.Optional[builtins.str] = None,
    confidential_vm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_vm_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    disk_controller_type_nvme_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_types_not_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_of_life_date: typing.Optional[builtins.str] = None,
    eula: typing.Optional[builtins.str] = None,
    hibernation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hyper_v_generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
    max_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
    min_recommended_memory_in_gb: typing.Optional[jsii.Number] = None,
    min_recommended_vcpu_count: typing.Optional[jsii.Number] = None,
    privacy_statement_uri: typing.Optional[builtins.str] = None,
    purchase_plan: typing.Optional[typing.Union[SharedImagePurchasePlan, typing.Dict[builtins.str, typing.Any]]] = None,
    release_note_uri: typing.Optional[builtins.str] = None,
    specialized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SharedImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_launch_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trusted_launch_supported: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911cf423281b4e0524d90d224d43091f5347a00c77b74c9038e08a6f568b2d2c(
    *,
    offer: builtins.str,
    publisher: builtins.str,
    sku: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e254384632277debb814768e3c83e6737f05dc0c2d45362ef76fb31c2b8f0632(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2eaa639a4cef379799f6de79319149c9c7ee8e57462915ceca2a3be5998b39f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75ec7c14f07c3a676a16022eb08f27a4604b408c66773247c13387c301df8ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ce568790a8683e1c373f1c829034990b345dc707b5b87ffe7a93e87b58c6f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db820aaf63a0d8243495b1930529ad17e0c1434926353a870ae3a42b02ed2a7(
    value: typing.Optional[SharedImageIdentifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded5f754db05c1abe8bd3223c2f2fa41d24aa71d776ba2fcfcd440b45a14ddf0(
    *,
    name: builtins.str,
    product: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c385bb601390e4ad3dfd1f2ed0d08e3718746915b3ed30f8383167b23a3c44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add7433257431f97398b99a2cc963fea970f38f826c78055a6eabfc790ee36e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c48cb0ba7841d5f4836bab73d93e5dc79cca0fa1f07db3b968f2d5ae685f010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef2e478a7c1c53bbbed89e7484f2307cf1155596ff809eebee12dd12d9c9fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd2ab1697f5ad69a28c560c882ca8e24922b9b43c6f9cdbd19013a55b0bb9f9(
    value: typing.Optional[SharedImagePurchasePlan],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd42afec800fc577b32773c1eaa2f664b900f4c8af86aeeaec81f649fdf4bb6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2fc495a8c1cc69409d4861ebdd82df54f38f56b4dd9381b0aeb858b1b285ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68335b80743ce741e2931ea62963d07fe8f6c3b2d6a713066149a0e219651dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d4c56d98632485dd0c4115f2354b8f9f867d08b359a5f9c5ecefc84b7c4be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06dc72c74f6a1018a12541a47f018835a97d9aeb8560f33cbed162742d2faf58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97aa17162d162833f5d2fd586d757aa47aedfcadc70ced3a0315852498a49719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89bc1730d7e0d62cf2dac3f2c3fba96edb8b976a9e20239a7037765d7712142(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SharedImageTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
