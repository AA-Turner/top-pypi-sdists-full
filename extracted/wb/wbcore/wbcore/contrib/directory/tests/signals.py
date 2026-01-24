from django.dispatch import receiver
from dynamic_preferences.registries import global_preferences_registry

from wbcore.test.signals import custom_update_kwargs, get_custom_factory

from ..factories import (
    BankFactory,
    ParentRelationshipTypeFactory,
    RandomClientFactory,
    UserIsManagerEntryFactory,
)
from ..viewsets import (
    BankModelViewSet,
    EmployeeEmployerModelViewSet,
    EmployerEmployeeModelViewSet,
    PersonInChargeRepresentationViewSet,
    RelationshipModelEntryViewSet,
    RelationshipTypeModelViewSet,
    SystemEmployeeModelViewSet,
    UserIsManagerViewSet,
)

# =================================================================================================================
#                                              CUSTOM FACTORY
# =================================================================================================================


@receiver(get_custom_factory, sender=PersonInChargeRepresentationViewSet)
def receive_factory_person_in_charge(sender, *args, **kwargs):
    return RandomClientFactory


@receiver(get_custom_factory, sender=RelationshipTypeModelViewSet)
def receive_factory_relationship_type(sender, *args, **kwargs):
    return ParentRelationshipTypeFactory


@receiver(get_custom_factory, sender=BankModelViewSet)
def receive_factory_bank(sender, *args, **kwargs):
    return BankFactory


@receiver(get_custom_factory, sender=UserIsManagerViewSet)
def receive_factory_user_is_manager(sender, *args, **kwargs):
    return UserIsManagerEntryFactory


# =================================================================================================================
#                                              UPDATE KWARGS
# =================================================================================================================


@receiver(custom_update_kwargs, sender=RelationshipModelEntryViewSet)
def receive_kwargs_relationship(sender, *args, **kwargs):
    if kwargs.get("from_entry_id"):
        return {"entry_id": kwargs.get("from_entry_id")}
    return {}


@receiver(custom_update_kwargs, sender=EmployeeEmployerModelViewSet)
def receive_kwargs_employee_company(sender, *args, **kwargs):
    if obj := kwargs.get("obj_factory"):
        return {"company_id": obj.employer.id}
    return {}


@receiver(custom_update_kwargs, sender=EmployerEmployeeModelViewSet)
def receive_kwargs_employer_person(sender, *args, **kwargs):
    if obj := kwargs.get("obj_factory"):
        return {"employee_id": obj.employee.id}
    return {}


@receiver(custom_update_kwargs, sender=SystemEmployeeModelViewSet)
def receive_kwargs_system_employee(sender, *args, **kwargs):
    if obj := kwargs.get("obj_factory"):
        company_id = obj.employer.id
        global_preferences_registry.manager()["directory__main_company"] = company_id
        return {"employer_id": company_id}
    return {}


@receiver(custom_update_kwargs, sender=UserIsManagerViewSet)
def receive_kwargs_user_is_manager(sender, *args, **kwargs):
    if (obj := kwargs.get("obj_factory")) and (user := kwargs.get("user")):
        if cmr := obj.client_of.first():
            cmr.relationship_manager = user.profile
            cmr.save()
    return {}
