from enum import Enum


class OfferingTypeEnum(str, Enum):
    MARKETPLACE_BASIC = "Marketplace.Basic"
    MARKETPLACE_BOOKING = "Marketplace.Booking"
    MARKETPLACE_RANCHER = "Marketplace.Rancher"
    MARKETPLACE_SCRIPT = "Marketplace.Script"
    MARKETPLACE_SLURM = "Marketplace.Slurm"
    OPENSTACK_INSTANCE = "OpenStack.Instance"
    OPENSTACK_TENANT = "OpenStack.Tenant"
    OPENSTACK_VOLUME = "OpenStack.Volume"
    SLURMINVOICES_SLURMPACKAGE = "SlurmInvoices.SlurmPackage"
    SUPPORT_OFFERINGTEMPLATE = "Support.OfferingTemplate"
    VMWARE_VIRTUALMACHINE = "VMware.VirtualMachine"
    WALDUR_REMOTEOFFERING = "Waldur.RemoteOffering"

    def __str__(self) -> str:
        return str(self.value)
