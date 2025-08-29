from typing import Optional
from urllib.parse import urlparse

from ._actions import _Actions
from ._data_fabric import _DataFabric
from .uiform import (
    ApplicationUiForm,
    DesignUiForm,
    DesignObjectUiForm,
    RecordInstanceUiForm,
    RecordListUiForm,
    SailUiForm,
    AISkillUiForm
)
from ._design import _Design, AI_SKILL_DESCRIPTOR, validate_design_object_access_method
from ._interactor import _Interactor
from ._portals import _Portals
from ._rdo_interactor import _RDOInteractor
from ._records import _Records
from ._reports import _Reports
from ._sites import _Sites
from ._admin import _Admin
from ._tasks import _Tasks
from .uiform.InterfaceDesignerUiForm import InterfaceDesignerUiForm
from .utilities.helper import format_label
from .objects import DesignObjectType, PageType

_RDO_TYPE_TO_VISITOR_METHOD = {
    "aiSkill": "visit_ai_skill_by_id"
}


class Visitor:
    """
    Provides methods to get an interactable ``SailUiForm`` from an Appian instance. Each method will return the respected ``SailUiForm`` type for which it will allow
    interactions with the visited page.
    """

    def __init__(self, interactor: _Interactor, tasks: _Tasks, reports: _Reports, actions: _Actions, records: _Records,
                 sites: _Sites):
        self.__interactor = interactor
        self.__tasks = tasks
        self.__reports = reports
        self.__records = records
        self.__sites = sites
        self.__actions = actions
        self.__data_fabric = _DataFabric(self.__interactor)
        self.__design = _Design(self.__interactor)
        self.__admin = _Admin(self.__interactor)
        self.__portals = _Portals(self.__interactor)

    def visit_task(self, task_name: str, exact_match: bool = True, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Gets the SailUiForm given a task name

        Args:
            task_name (str): Name of the task to search for
            exact_match (bool, optional): Whether or not a full match is returned. Defaults to True.
            locust_request_label (str, optional): label to be used within locust

        Returns:
            SailUiForm: SAIL form for the task
        """
        initial_task_resp: dict = self.__tasks.get_task(task_name, exact_match)
        children = initial_task_resp.get("content", {}).get("children", [])
        task_title = children[0]

        if not locust_request_label:
            breadcrumb = f"Tasks.{task_title}"
        else:
            breadcrumb = locust_request_label
        return SailUiForm(self.__interactor, self.__tasks.get_task_form_json(task_name=task_title, locust_request_label=breadcrumb, exact_match=False), breadcrumb=breadcrumb)

    def visit_report(self, report_name: str, exact_match: bool = True, locust_request_label: Optional[str] = None) -> 'SailUiForm':
        """
        Navigate to a report and return a SailUiForm for that report's UI

        Args:
            report_name (str): Name of the report to be called.
            exact_match (bool, optional): Should report name match exactly or to be partial match. Default : True
            locust_request_label (str, optional): Label locust should associate this request with

        Returns (SailUiForm): Response of report's Get UI call in SailUiForm

        """
        breadcrumb = f'Reports.SailUi.{format_label(report_name, "::", 0)}'
        locust_request_label = locust_request_label or f"Visit.Report.{report_name}"
        return SailUiForm(self.__interactor, self.__reports.fetch_report_json(report_name, exact_match, locust_request_label=locust_request_label), breadcrumb=breadcrumb)

    def visit_design(self, locust_request_label: Optional[str] = None) -> DesignUiForm:
        """
        Navigate to /design
        Args:
            locust_request_label (str, optional): label to be used within locust

        Returns (DesignUiForm): UiForm representing /design

        """
        return DesignUiForm(self.__interactor, self.__design.fetch_design_json(locust_request_label), breadcrumb="Design.ApplicationList.SailUi")

    def visit_data_fabric(self, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Navigate to Data Fabric
        Args:
            locust_request_label (str, optional): label to be used within locust

        Returns (SailUiForm): UiForm representing Data Fabric

        """
        return SailUiForm(self.__interactor, self.__data_fabric.fetch_data_fabric_json(locust_request_label), breadcrumb="DataFabric.SailUi")

    def visit_data_fabric_dashboard(self, encoded_uri_stub: str = "new", locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Navigate to a Data Fabric Dashboard
        Args:
            encoded_uri_stub (str): encoded uri stub of the dashboard to load. Defaults to "new" if not provided,
            bringing the user to an empty dashboard.
            locust_request_label (str, optional): label to be used within locust

        Returns (SailUiForm): UiForm representing a Data Fabric Dashboard

        """
        return SailUiForm(self.__interactor,
                          self.__data_fabric.fetch_data_fabric_dashboard_json(encoded_uri_stub, locust_request_label),
                          breadcrumb="DataFabricDashboard.SailUi")

    def visit_data_fabric_report(self, encoded_uri_stub: str = "new", locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Navigate to a Data Fabric Report
        Args:
            encoded_uri_stub (str): encoded uri stub of the report to load. Defaults to "new" if not provided,
            bringing the user to an empty report.
            locust_request_label (str, optional): label to be used within locust

        Returns (SailUiForm): UiForm representing a Data Fabric Report

        """
        return SailUiForm(self.__interactor,
                          self.__data_fabric.fetch_data_fabric_report_json(encoded_uri_stub, locust_request_label),
                          breadcrumb="DataFabricReport.SailUi")

    def visit_application_by_id(self, application_id: str, locust_request_label: Optional[str] = None) -> ApplicationUiForm:
        """
        Visit an application by its opaque id

        Args:
            application_id (str): The opaque id of the application
            locust_request_label (str, optional): label to be used within locust

        Returns (ApplicationUiForm): UiForm representing design application page

        """
        breadcrumb = f"Design.SelectedApplication.{application_id}.SailUi"
        return ApplicationUiForm(self.__interactor, self.__design.fetch_application_json(application_id, locust_request_label), breadcrumb)

    def visit_application_by_name(self, application_name: str, application_prefix: Optional[str] = None, locust_request_label: Optional[str] = None) -> ApplicationUiForm:
        """
        Visit an application by name

        Args:
            application_name (str): The name of the application
            application_prefix (str, optional): The prefix of the application. Required if the application has a prefix.
            locust_request_label (str, optional): label to be used within locust

        Returns (ApplicationUiForm): UiForm representing design application page

        """
        design_uiForm = self.visit_design()
        design_uiForm.search_applications(application_name)
        if application_prefix:
            application_name = f"{application_name} ({application_prefix})"
        application_uiform = design_uiForm.click_application(application_name, locust_request_label)
        return application_uiform

    def visit_design_object_by_id(self, opaque_id: str, locust_request_label: Optional[str] = None) -> DesignObjectUiForm:
        """
        Visit a design object by its opaque id
        Args:
            opaque_id (str): opaque id of the design object
            locust_request_label (str, optional): label to be used within locust

        Returns (DesignObjectUiForm): UiForm representing design object

        """
        breadcrumb = "Design.SelectedObject." + opaque_id[0:10] + ".SailUi"
        design_object_json = self.__design.fetch_design_object_json(opaque_id, locust_request_label)
        validate_design_object_access_method(design_object_json, _RDO_TYPE_TO_VISITOR_METHOD)
        return DesignObjectUiForm(self.__interactor, design_object_json, breadcrumb)

    def visit_interface_object_by_id(self, opaque_id: str, locust_request_label: Optional[str] = None) -> InterfaceDesignerUiForm:
        """
        Visit an interface object by its opaque id. This does not validate that the given opaque_id actually refers to an interface.
        Args:
            opaque_id (str): opaque id of the interface object
            locust_request_label (str, optional): label to be used within locust

        Returns (InterfaceDesignerUiForm): UiForm representing interface object
        """
        breadcrumb = "Design.SelectedInterface." + opaque_id[0:10] + ".SailUi"
        design_object_json = self.__design.fetch_design_object_json(opaque_id, locust_request_label)
        validate_design_object_access_method(design_object_json, _RDO_TYPE_TO_VISITOR_METHOD)
        return InterfaceDesignerUiForm(self.__interactor, design_object_json, breadcrumb)

    def visit_design_object_by_name(self, object_name: str, object_type: DesignObjectType, locust_request_label: Optional[str] = None) -> DesignObjectUiForm:
        """
        Visit a design object by its name and type
        Args:
            object_name (str): The name of the design object
            object_type (DesignObjectType): The type of the design object
            locust_request_label (str, optional): label to be used within locust

        Returns (DesignObjectUiForm): UiForm representing design object

        """
        design_ui_form: DesignUiForm = self.visit_design()
        design_ui_form.select_nav_card_by_index(nav_group_label="leftNavbar", is_test_label=True, index=1)
        indices = self.__design.find_design_object_type_indices(current_state=design_ui_form.get_latest_state(), design_object_types=[object_type.value])
        design_ui_form.check_checkbox_by_test_label(test_label="object-type-checkbox", indices=indices)
        design_ui_form.search_objects(object_name)
        design_object_opaque_id = self.__design.find_design_object_opaque_id_in_grid(object_name, design_ui_form.get_latest_state())
        return self.visit_design_object_by_id(design_object_opaque_id, locust_request_label)

    def visit_record_instance(self, record_type: str = "", record_name: str = "", view_url_stub: str = "",
                              exact_match: bool = False, summary_view: bool = True,
                              locust_request_label: Optional[str] = None) -> RecordInstanceUiForm:
        """
        Navigate to a specific record and return a RecordUiForm

        Args:
            record_type (str): Record Type Name. If not specified, a random record type will be selected.
            record_name (str): Name of the record to be called. If not specified, a random record will be selected.
            view_url_stub (str, optional): page/tab to be visited in the record. If not specified, "summary" dashboard will be selected.
            exact_match (bool, optional): Should record type and record name matched exactly as it is or partial match.
            summary_view (bool, optional): Should the Record UI be returned in Summary View, if false will return Header View
            locust_request_label (str, optional): Label locust should associate this request with

        Returns (RecordUiForm): The UI for the record instance

        """
        self.__records.get_records_nav(locust_request_label=locust_request_label)
        form_json = self.__records.visit_record_instance(record_type, record_name, view_url_stub=view_url_stub,
                                                         exact_match=exact_match, locust_request_label=locust_request_label)
        breadcrumb = f'Records.{record_type}.{format_label(record_name, "::", 0)}.SailUi'
        return RecordInstanceUiForm(self.__interactor, form_json, summary_view=summary_view, breadcrumb=breadcrumb)

    def visit_record_type(self, record_type: str = "",
                          locust_request_label: Optional[str] = None) -> RecordListUiForm:
        """
        This function calls the API for the specific record type and returns a SAIL form representing the list of records for that record type.

        Args:
            record_type (str): Record Type Name. If not specified, a random record type will be selected.
            locust_request_label (str, optional): Label locust should associate this request with

        Returns (SailUiForm): UI representing list of records for that record type
        """

        locust_request_label = locust_request_label or f'Records.{record_type}.ListView'
        self.__records.get_records_nav(locust_request_label=locust_request_label)
        form_json = self.__records.visit_record_type(record_type, locust_request_label=locust_request_label)
        breadcrumb = f'Records.{record_type}.RecordListUi'
        return RecordListUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_site(self, site_name: str, page_name: str, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Get a SailUiForm for a Task, Report or Action

        Args:
            site_name(str): Site where the page exists
            page_name(str): Page to navigate to
            locust_request_label (str, optional): Label locust should associate this request with

        Returns: SailUiForm

        Example:
            >>> self.appian.visitor.visit_site("site_name","page_name")

        """
        form_json = self.__sites.fetch_site_tab_json(site_name, page_name, locust_request_label)

        breadcrumb = f"Sites.{site_name}.{page_name}.SailUi"
        return SailUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_admin(self, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Navigates to /admin
        Args:
            locust_request_label (str, optional): label to be used within locust

        Returns: SailUiForm

        """
        form_json = self.__admin.fetch_admin_json(locust_request_label)

        breadcrumb = f"Admin.MainMenu.SailUi"
        return SailUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_site_recordlist(self, site_name: str, page_name: str, locust_request_label: Optional[str] = None) -> 'RecordListUiForm':
        """
        Get a RecordListUiForm for a record list page on a site

        Args:
            site_name(str): Site where the page exists
            page_name(str): Page to navigate to
            locust_request_label (str, optional): label to be used within locust

        NOTE: The actual Type of the Site Page MUST be "Record List", this will not work for sites that are of other page types,
              such as an Interface with a record grid.

        Returns: SailUiForm

        Example:
            >>> self.appian.visitor.visit_site_recordlist("site_name","page_name")

        """
        page_type = self.__sites.get_site_page_type(site_name, page_name)
        if page_type != PageType.RECORD:
            raise Exception(f"Page {page_name} on site {site_name} is not of type record")
        form_json = self.__sites.fetch_site_tab_json(site_name, page_name, locust_request_label)

        breadcrumb = f"Sites.{site_name}.{page_name}.SailUi"
        return RecordListUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_site_recordlist_and_get_random_record_form(self, site_name: str, page_name: str, locust_request_label: Optional[str] = None) -> RecordInstanceUiForm:
        """
        Navigates to a site page that is a recordlist then clicks on a random record instance on the first page

        Args:
            site_name: Site Url stub
            page_name: Page Url stub
            locust_request_label (str, optional): label to be used within locust

        NOTE: The actual Type of the Site Page MUST be "Record List", this will not work for sites that are of other page types,
              such as an Interface with a record grid.

        Returns: RecordInstanceUiForm
        """

        site_page_json_response = self.__sites.fetch_site_tab_record_json(site_name, page_name, locust_request_label)
        summary_view = site_page_json_response.get("feed") is not None
        breadcrumb = f"Sites.{site_name}.{page_name}.SailUi"
        return RecordInstanceUiForm(self.__interactor, site_page_json_response, summary_view=summary_view, breadcrumb=breadcrumb)

    def visit_action(self, action_name: str, exact_match: bool = False, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Gets the action by name and returns the corresponding SailUiForm to interact with

        If the action is activity chained, this will attempt to start the process and retrieve the chained SAIL form.

        Args:
            action_name (str): Name of the action to be called. Name of the action will be in the below pattern.
                         "displayLabel::opaquqId"
            exact_match (bool, optional): Should action name match exactly or to be partial match. Default : False
            locust_request_label (str, optional): label to be used within locust. Default: '' (empty string)

        Returns: SailUiForm

        Examples:

            If the full name of the action is known, with the opaque ID,

            >>> self.appian.visitor.visit_action("action_name:igB0K7YxC0UQ2Fhx4hicRw...", exact_match=True)

            If only the display name is known, or part of the display name

            >>> self.appian.visitor.visit_action("action_name")
            >>> self.appian.visitor.visit_action("actio")
        """
        action_key = format_label(action_name, "::", 0)
        label = locust_request_label or f'Actions.GetUi.{action_key}'
        form_json = self.__actions.fetch_action_json(action_name, exact_match, label)
        return SailUiForm(self.__interactor, form_json, breadcrumb=label)

    def visit_portal_page(self, portal_unique_identifier: str, portal_page_unique_identifier: str, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Navigate to portal's page by url and returns the corresponding SailUiForm to interact with

        Args:
            portal_unique_identifier (str): portal web address unique identifier
            portal_page_unique_identifier (str): web address unique identifier for specific page in portal
            locust_request_label (str, optional): label to be used within locust

        Returns: SailUiForm

        Examples:

            If we have portal up and running with 2 pages with title "page1" and "page2", we can
            visit any portal page with help of this method.

            In order to visit "page1" with url (in browser: https://mysite.appian-internal.com/performance-testing/page/page1),
            we would use

            >>> self.appian.visitor.visit_portal_page("performance-testing", "page1")

            In order to visit "page2" with url (in browser: https://mysite.appian-internal.com/performance-testing/page/page2),
            we would use

            >>> self.appian.visitor.visit_portal_page("performance-testing", "page2")

        Note: sometimes when portal has just 1 page (for example page with title 'page1').
        appian use only "https://mysite.appian-internal.com/performance-testing" (in browser)
        instead of https://mysite.appian-internal.com/performance-testing/page/page1 . although it still works.
        """
        form_json = self.__portals.fetch_page_json(portal_unique_identifier, portal_page_unique_identifier, locust_request_label=locust_request_label)
        breadcrumb = f"Portals.{_Portals.get_full_url(portal_unique_identifier, portal_page_unique_identifier)}.SailUi"
        return SailUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_ai_skill_by_id(self, opaque_id: str, locust_request_label: Optional[str] = None) -> AISkillUiForm:
        """
        Visit an AI Skill by its opaque id
        Args:
            opaque_id (str): opaque id of the AI Skill
            locust_request_label (str, optional): label to be used within locust

        Returns (AISkillUiForm): UiForm representing AI Skill

        """
        locust_request_label = locust_request_label or f"Design.AiSkill.{opaque_id}"
        object_json = self.__design.fetch_design_object_json(opaque_id=opaque_id,
                                                             locust_request_label=f"{locust_request_label}.DesignObject")
        ai_skill_info = self.__design.extract_ai_skill_info(object_json)

        rdo_interactor = _RDOInteractor(interactor=self.__interactor, rdo_host=ai_skill_info.host_url)
        ai_skill_json = rdo_interactor.fetch_ai_skill_designer_json(ai_skill_id=ai_skill_info.object_uuid)
        return AISkillUiForm(rdo_interactor=rdo_interactor,
                             rdo_state=ai_skill_json,
                             ai_skill_id=ai_skill_info.object_uuid,
                             breadcrumb=locust_request_label
                             )

    def visit_ai_skill_by_name(self, ai_skill_name: str, locust_request_label: Optional[str] = None) -> AISkillUiForm:
        """
        Visit an AI Skill by its name
        Args:
            ai_skill_name (str): The name of the AI Skill
            locust_request_label (str, optional): label to be used within locust

        Returns (AISkillUiForm): UiForm representing AI Skill

        """
        design_ui_form = self.visit_design()
        design_ui_form.select_nav_card_by_index(nav_group_label="leftNavbar", is_test_label=True, index=1)
        ai_skill_index_in_list = self.__design.find_design_object_type_indices(current_state=design_ui_form.get_latest_state(), design_object_types=[AI_SKILL_DESCRIPTOR])
        design_ui_form.check_checkbox_by_test_label(test_label="object-type-checkbox", indices=ai_skill_index_in_list)
        design_ui_form.search_objects(ai_skill_name)
        design_object_opaque_id = self.__design.find_design_object_opaque_id_in_grid(ai_skill_name,
                                                                                     design_ui_form.get_latest_state())
        return self.visit_ai_skill_by_id(design_object_opaque_id, locust_request_label)
