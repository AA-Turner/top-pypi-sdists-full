from django.utils.translation import gettext as _

from wbcore.contrib.directory.models import ClientManagerRelationship, Company, Entry, Person
from wbcore.metadata.configs.titles import TitleViewConfig


class RelationshipEntryModelTitleConfig(TitleViewConfig):
    def get_list_title(self):
        entry = Entry.all_objects.get(id=self.view.kwargs["entry_id"])
        return _("Relationships of {entry}").format(entry=str(entry))

    def get_create_title(self):
        entry = Entry.all_objects.get(id=self.view.kwargs["entry_id"])
        return _("New Relationship for {entry}").format(entry=str(entry))


class RelationshipTypeModelTitleConfig(TitleViewConfig):
    def get_list_title(self):
        return _("Relationship Types")

    def get_instance_title(self):
        return _("Relationship Type")

    def get_create_title(self):
        return _("New Relationship Type")


class ClientManagerTitleConfig(TitleViewConfig):
    def get_instance_title(self):
        if pk := self.view.kwargs.get("pk"):
            cmr_request = ClientManagerRelationship.objects.get(id=pk)
            return _("Client Manager Relationship Between {client} & {person}").format(
                client=str(cmr_request.client), person=str(cmr_request.relationship_manager)
            )

    def get_list_title(self):
        if client_id := self.request.GET.get("client"):
            client = Entry.all_objects.get(id=client_id)
            return _("Relationship Managers for {client}").format(client=str(client))

        elif relationship_manager_id := self.request.GET.get("relationship_manager"):
            relationship_manager = Person.all_objects.get(id=relationship_manager_id)
            return _("Clients of {relationship_manager}").format(relationship_manager=str(relationship_manager))

        return _("Client Manager Relationships")

    def get_create_title(self):
        if client_id := self.request.GET.get("client"):
            client = Entry.all_objects.get(id=client_id)
            return _("New Client Relationship for {client}").format(client=str(client))

        elif relationship_manager_id := self.request.GET.get("relationship_manager"):
            relationship_manager = Person.all_objects.get(id=relationship_manager_id)
            return _("New Manager Relationship for {relationship_manager}").format(
                relationship_manager=str(relationship_manager)
            )

        return _("New Client Manager Relationship")


class EmployerEmployeeRelationshipTitleConfig(TitleViewConfig):
    def get_list_title(self) -> str | None:
        if employee_id := self.view.kwargs.get("employee_id"):
            person = Person.all_objects.get(id=employee_id)
            return f"Employers of {str(person)}"
        if employer_id := self.view.kwargs.get("employer_id"):
            company = Company.all_objects.get(id=employer_id)
            return f"Employees of {str(company)}"
        return super().get_list_title()

    def get_instance_title(self) -> str:
        return _("Employer Employee Relationship")

    def get_create_title(self) -> str | None:
        if employee_id := self.view.kwargs.get("employee_id"):
            person = Person.all_objects.get(id=employee_id)
            return f"New Employer for {str(person)}"
        if employer_id := self.view.kwargs.get("employer_id"):
            company = Company.all_objects.get(id=employer_id)
            return f"New Employee for {str(company)}"
        return super().get_create_title()


class UserIsClientTitleConfig(TitleViewConfig):
    def get_list_title(self) -> str:
        return _("Your Contacts")
