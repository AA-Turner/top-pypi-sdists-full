import logging
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from zeep import Settings
from zeep.helpers import serialize_object as zeep_serialize
from ...interfaces.SOAPClient import SOAPClient
from ...interfaces.flow import FlowComponent
from ...conf import (
    WORKDAY_CLIENT_ID,
    WORKDAY_CLIENT_SECRET,
    WORKDAY_TOKEN_URL,
    WORKDAY_WSDL_PATH,
    WORKDAY_WSDL_TIME,
    WORKDAY_WSDL_HUMAN_RESOURCES,
    WORKDAY_WSDL_FINANCIAL_MANAGEMENT,
    WORKDAY_WSDL_RECRUITING,
    WORKDAY_WSDL_ABSENCE_MANAGEMENT,
    WORKDAY_WSDL_TIME_BLOCK_REPORT,
    WORKDAY_WSDL_CUSTOM_PUNCH_FIELD_REPORT,
    WORKDAY_WSDL_INTEGRATIONS,
    WORKDAY_REFRESH_TOKEN,
    WORKDAY_REPORT_USERNAME,
    WORKDAY_REPORT_PASSWORD,
)
from .types import (
    WorkerType,
    TimeBlockType,
    LocationType,
    TimeRequestType,
    OrganizationType,
    CostCenterType,
    ApplicantType,
    CandidateType,
    JobRequisitionType,
    JobPostingType,
    JobPostingSiteType,
    TimeOffBalanceType,
    TimeBlockReportType,
    CustomReportType,
    CustomPunchFieldReportType,
    CustomPunchFieldReportRestType,
    RecruitingAgencyUsersType,
    ReferencesType,
)
from .types.organization_single import GetOrganization
from .types.location_hierarchy_assignments import LocationHierarchyAssignmentsType


class Workday(SOAPClient, FlowComponent):
    """
    Workday Component

    Overview:
        The Workday class is a Flowtask component for the Workday SOAP API.
        It encapsulates all Workday-specific logic, including authentication,
        request/response handling, and data normalization.

    Properties:
        type (str): Operation type to perform (e.g. 'get_workers', 'get_time_blocks')
        worker_id (str): Optional worker ID to fetch a specific worker
        use_storage (bool): Enable data storage functionality
        storage_path (str): Path where to store the data files
        masks (dict): Dictionary of masks for dynamic value replacement

    Returns:
        Returns a pandas DataFrame with the requested data.

    Examples:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          # Basic usage
          Workday:
          type: get_workers
          worker_id: "72037046323885"

          # With storage enabled
          Workday:
          type: get_workers
          use_storage: true
          storage_path: "/data/workday"

          # With mask replacement for dynamic dates
          Workday:
          type: get_time_blocks
          start_date: "{yesterday}"
          end_date: "{today}"
          masks:
          yesterday:
          - yesterday
          - mask: "%Y-%m-%d"
          today:
          - today
          - mask: "%Y-%m-%d"
          use_storage: true
          storage_path: "/data/workday"

          # Location hierarchy assignments with storage
          Workday:
          type: get_location_hierarchy_assignments
          use_storage: true
          storage_path: "/data/workday"

          # Organizations with storage and dynamic parameters
          Workday:
          type: get_organizations
          organization_type: "Cost_Center"
          use_storage: true
          storage_path: "/data/workday"
          masks:
          date_suffix:
          - today
          - mask: "%Y%m%d"

          # Cost Centers with storage
          Workday:
          type: get_cost_centers
          use_storage: true
          storage_path: "/data/workday"

          # Specific Cost Center by ID
          Workday:
          type: get_cost_centers
          cost_center_id: "CC_123456"
          cost_center_id_type: "Cost_Center_Reference_ID"

          # Cost Centers with date filtering
          Workday:
          type: get_cost_centers
          updated_from_date: "{last_week}"
          updated_to_date: "{today}"
          include_inactive: true
          masks:
          last_week:
          - yesterday
          - days_offset: -7
          - mask: "%Y-%m-%d"
          today:
          - today
          - mask: "%Y-%m-%d"

          # Get all Applicants/Pre-hires (from Recruiting API)
          Workday:
          type: get_applicants
          use_storage: true
          storage_path: "/data/workday"

          # Get specific applicant by ID
          Workday:
          type: get_applicants
          applicant_id: "APPLICANT-123"

          # Get pre-hires only (candidates with future hire dates)
          Workday:
          type: get_applicants
          is_pre_hire: true
          use_storage: true
          storage_path: "/data/workday"

          # Get applicants for specific job requisition
          Workday:
          type: get_applicants
          job_requisition_id: "JR-000123"

          # Get applicants with date range filtering
          Workday:
          type: get_applicants
          application_date_from: "{last_month}"
          application_date_to: "{today}"
          masks:
          last_month:
          - today
          - days_offset: -30
          - mask: "%Y-%m-%d"
          today:
          - today
          - mask: "%Y-%m-%d"

          # Get all Candidates (from Recruiting API)
          Workday:
          type: get_candidates
          use_storage: true
          storage_path: "/data/workday"

          # Get candidates with PDF resume storage
          Workday:
          type: get_candidates
          use_storage: true
          storage_path: "/data/workday"
          pdf_directory: "/data/workday/candidate_resumes"

          # Get specific candidate by ID
          Workday:
          type: get_candidates
          candidate_id: "CANDIDATE-123"
          pdf_directory: "/data/workday/candidate_resumes"

          # Get candidates for specific job requisition
          Workday:
          type: get_candidates
          job_requisition_id: "JR-000456"

          # Get candidates with date range filtering
          Workday:
          type: get_candidates
          applied_from_date: "{last_week}"
          applied_to_date: "{today}"
          masks:
          last_week:
          - yesterday
          - days_offset: -7
          - mask: "%Y-%m-%d"
          today:
          - today
          - mask: "%Y-%m-%d"

          # Get candidates created in last month
          Workday:
          type: get_candidates
          created_from_date: "{last_month}"
          created_to_date: "{today}"
          use_storage: true
          storage_path: "/data/workday"
          masks:
          last_month:
          - today
          - days_offset: -30
          - mask: "%Y-%m-%d"
          today:
          - today
          - mask: "%Y-%m-%d"
        ```
    """
    _version = "1.0.0"
    
    def __init__(self, *, loop=None, job=None, stat=None, **kwargs):
        # Get kwargs first to determine operation type
        self.type = kwargs.get('type', 'get_workers')
        self.worker_id = kwargs.get('worker_id')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')

        # Storage parameters
        self.use_storage: bool = kwargs.get('use_storage', False)
        self.storage_path: str = kwargs.get('storage_path')
        if self.use_storage and not self.storage_path:
            raise ValueError(
                "Workday: storage_path is required when use_storage is True"
            )

        # Location parameters
        self.location_id = kwargs.get('location_id')
        self.location_name = kwargs.get('location_name')
        self.location_type = kwargs.get('location_type')
        self.location_usage = kwargs.get('location_usage')
        self.inactive = kwargs.get('inactive')

        # Time Request parameters
        self.time_request_id = kwargs.get('time_request_id')
        self.supervisory_organization_id = kwargs.get('supervisory_organization_id')

        # Organization parameters
        self.organization_id = kwargs.get('organization_id')
        self.organization_id_type = kwargs.get('organization_id_type', 'Organization_Reference_ID')
        self.organization_type = kwargs.get('organization_type')
        self.include_inactive = kwargs.get('include_inactive')
        self.enable_transaction_log_lite = kwargs.get('enable_transaction_log_lite')

        # Cost center parameters
        self.cost_center_id = kwargs.get('cost_center_id')
        self.cost_center_id_type = kwargs.get('cost_center_id_type', 'Cost_Center_Reference_ID')
        self.updated_from_date = kwargs.get('updated_from_date')
        self.updated_to_date = kwargs.get('updated_to_date')

        # Applicant parameters
        self.applicant_id = kwargs.get('applicant_id')
        self.job_requisition_id = kwargs.get('job_requisition_id')
        self.application_date_from = kwargs.get('application_date_from')
        self.application_date_to = kwargs.get('application_date_to')
        self.is_pre_hire = kwargs.get('is_pre_hire')

        # Candidate parameters
        self.candidate_id = kwargs.get('candidate_id')
        self.applied_from_date = kwargs.get('applied_from_date')
        self.applied_to_date = kwargs.get('applied_to_date')
        self.created_from_date = kwargs.get('created_from_date')
        self.created_to_date = kwargs.get('created_to_date')
        self.pdf_directory = kwargs.get('pdf_directory')  # Directory to save candidate PDFs/resumes

        # Job Requisition parameters
        self.job_requisition_status = kwargs.get('job_requisition_status')

        # Job Posting parameters
        self.job_posting_id = kwargs.get('job_posting_id')
        self.job_posting_site_id = kwargs.get('job_posting_site_id')
        self.posting_status = kwargs.get('posting_status')
        self.posted_from_date = kwargs.get('posted_from_date')
        self.posted_to_date = kwargs.get('posted_to_date')

        # Job Posting Site parameters
        self.is_active = kwargs.get('is_active')

        # References (Integrations service) parameters
        self.reference_id_type = kwargs.get('reference_id_type')

        # Debug parameters
        self.zeep_debug = kwargs.get('zeep_debug', False)

        # Attachment parameters
        self.exclude_all_attachments = kwargs.get('exclude_all_attachments', False)

        # Configure Zeep logging
        if self.zeep_debug:
            # Enable detailed SOAP request/response logging
            logging.getLogger("zeep").setLevel(logging.DEBUG)
            logging.getLogger("zeep.transports").setLevel(logging.DEBUG)
            logging.getLogger("zeep.wsdl").setLevel(logging.DEBUG)
            logging.getLogger("httpx").setLevel(logging.DEBUG)  # Show HTTP headers
            logging.getLogger("httpcore").setLevel(logging.DEBUG)  # Show lower-level HTTP details
            logging.getLogger("flowtask.workday").info("SOAP debugging enabled (zeep_debug=True)")
        else:
            logging.getLogger("zeep").setLevel(logging.INFO)

        # Select WSDL based on operation type
        wsdl_mapping = {
            'get_time_blocks': WORKDAY_WSDL_TIME,
            'get_workers': WORKDAY_WSDL_PATH,
            'get_locations': WORKDAY_WSDL_HUMAN_RESOURCES,
            'get_time_requests': WORKDAY_WSDL_TIME,
            'get_organizations': WORKDAY_WSDL_PATH,
            'get_organization': WORKDAY_WSDL_HUMAN_RESOURCES,
            'get_location_hierarchy_assignments': WORKDAY_WSDL_HUMAN_RESOURCES,
            'get_cost_centers': WORKDAY_WSDL_FINANCIAL_MANAGEMENT,
            'get_applicants': WORKDAY_WSDL_RECRUITING,
            'get_candidates': WORKDAY_WSDL_RECRUITING,
            'get_job_requisitions': WORKDAY_WSDL_RECRUITING,
            'get_job_postings': WORKDAY_WSDL_RECRUITING,
            'get_job_posting_sites': WORKDAY_WSDL_RECRUITING,
            'get_recruiting_agency_users': WORKDAY_WSDL_RECRUITING,
            'get_time_off_balances': WORKDAY_WSDL_ABSENCE_MANAGEMENT,
            'extract_time_blocks_report': WORKDAY_WSDL_TIME_BLOCK_REPORT,
            'custom_punch_field_report': WORKDAY_WSDL_CUSTOM_PUNCH_FIELD_REPORT,
            'get_references': WORKDAY_WSDL_INTEGRATIONS,
            # Add more mappings as needed
        }
        wsdl_path = wsdl_mapping.get(self.type, WORKDAY_WSDL_PATH)

        # Determine if this is a REST custom report (needs basic auth)
        # SOAP custom reports use OAuth + Proxy_User_Name in SOAP body
        rest_report_types = ('custom_report', 'custom_punch_field_report_rest')
        is_rest_custom_report = (
            self.type in rest_report_types or self.type.startswith('extract_')
        )
        is_soap_custom_report = self.type.endswith('_report') and not is_rest_custom_report

        # Configure credentials with appropriate WSDL
        creds = {
            "client_id": WORKDAY_CLIENT_ID,
            "client_secret": WORKDAY_CLIENT_SECRET,
            "token_url": WORKDAY_TOKEN_URL,
            "wsdl_path": wsdl_path,
            "refresh_token": WORKDAY_REFRESH_TOKEN,
        }

        # Add report credentials ONLY for REST custom reports
        # SOAP custom reports use OAuth + Proxy_User_Name instead
        _using_basic_auth = False
        _missing_report_creds = False
        if is_rest_custom_report:
            # Allow override from YAML, otherwise use env variables
            report_username = getattr(self, 'report_username', None) or WORKDAY_REPORT_USERNAME
            report_password = getattr(self, 'report_password', None) or WORKDAY_REPORT_PASSWORD

            # Debug logging for credentials (partially masked)
            if report_username:
                logging.getLogger("flowtask.workday").debug(
                    f"Report username loaded: {report_username[:20]}... (length: {len(report_username)})"
                )
            if report_password:
                logging.getLogger("flowtask.workday").debug(
                    f"Report password loaded: {report_password[:3]}...{report_password[-3:]} (length: {len(report_password)})"
                )

            if report_username and report_password:
                creds["report_username"] = report_username
                creds["report_password"] = report_password
                _using_basic_auth = True
            else:
                _missing_report_creds = True

        # Configure SOAP settings
        settings = Settings(strict=False, xml_huge_tree=True)

        # Use a much higher timeout for Workday operations (300 seconds = 5 minutes)
        # Workday can return thousands of records and needs more time
        super().__init__(
            credentials=creds,
            settings=settings,
            timeout=300,  # 5 minutes timeout instead of default 30 seconds
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

        # Component configuration
        self._logger = logging.getLogger("flowtask.workday")

        # Store report credentials and configuration as component attributes
        if is_rest_custom_report or is_soap_custom_report:
            self.report_username = creds.get("report_username")
            self.report_password = creds.get("report_password")
            # Store Workday instance configuration for REST API URLs and SOAP proxy user
            self.tenant = kwargs.get('tenant', 'troc')
            self.report_owner = kwargs.get('report_owner', 'jtorres@trocglobal.com')
            self.workday_url = kwargs.get('workday_url', 'https://services1.wd501.myworkday.com')

        # Log which WSDL is being used
        self._logger.info(f"Using WSDL: {wsdl_path} for operation type: {self.type}")

        # Log authentication method for custom reports
        if is_soap_custom_report:
            self._logger.info(f"Using OAuth + Proxy_User_Name for SOAP custom report: {self.type}")
        elif _using_basic_auth:
            self._logger.info(f"Using basic auth for REST custom report: {self.type}")
        elif _missing_report_creds and is_rest_custom_report:
            self._logger.warning(
                f"REST custom report '{self.type}' detected but no credentials provided. "
                "Set WORKDAY_REPORT_USERNAME and WORKDAY_REPORT_PASSWORD or pass "
                "report_username/report_password in YAML."
            )

        # Log storage information after logger is initialized
        if self.use_storage:
            self._logger.info(
                f"Storage enabled. Data will be saved in: {self.storage_path}"
            )

        # Register available types
        self._type_handlers = {
            # Original handlers
            "get_workers": WorkerType(self),
            "get_time_blocks": TimeBlockType(self),
            "get_locations": LocationType(self),
            "get_time_requests": TimeRequestType(self),
            "get_organizations": OrganizationType(self),
            "get_organization": GetOrganization(self),
            "get_location_hierarchy_assignments": LocationHierarchyAssignmentsType(self),
            "get_cost_centers": CostCenterType(self),
            "get_applicants": ApplicantType(self),
            "get_candidates": CandidateType(self),
            "get_job_requisitions": JobRequisitionType(self),
            "get_job_postings": JobPostingType(self),
            "get_job_posting_sites": JobPostingSiteType(self),
            "get_recruiting_agency_users": RecruitingAgencyUsersType(self),
            "get_time_off_balances": TimeOffBalanceType(self),
            "extract_time_blocks_report": TimeBlockReportType(self),
            "custom_report": CustomReportType(self),
            "custom_punch_field_report": CustomPunchFieldReportType(self),
            "custom_punch_field_report_rest": CustomPunchFieldReportRestType(self),
            "get_references": ReferencesType(self),
        }

        # Initialize metrics
        self.metrics = {}
        self._result = None

    def _get_storage_file(self) -> str:
        """Get the storage file path for the current execution."""
        today = datetime.now().strftime('%Y%m%d')
        filename = f"workday_{self.type}_{today}.csv"
        storage_dir = Path(self.storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)
        return str(storage_dir / filename)

    def _get_wsdl_path(self, operation_type: str) -> str:
        """
        Get the appropriate WSDL path based on operation type.

        Args:
            operation_type: The type of operation ('get_workers', 'get_time_blocks', etc.)

        Returns:
            The WSDL path to use for the operation
        """
        wsdl_mapping = {
            'get_time_blocks': WORKDAY_WSDL_TIME,
            'get_workers': WORKDAY_WSDL_PATH,
            'get_locations': WORKDAY_WSDL_HUMAN_RESOURCES,
            'get_time_requests': WORKDAY_WSDL_TIME,
            'get_organizations': WORKDAY_WSDL_PATH,
            'get_organization': WORKDAY_WSDL_PATH,
            'get_cost_centers': WORKDAY_WSDL_FINANCIAL_MANAGEMENT,
            'get_applicants': WORKDAY_WSDL_RECRUITING,
            'get_candidates': WORKDAY_WSDL_RECRUITING,
            'get_job_requisitions': WORKDAY_WSDL_RECRUITING,
            'get_job_postings': WORKDAY_WSDL_RECRUITING,
            'get_job_posting_sites': WORKDAY_WSDL_RECRUITING,
            'get_recruiting_agency_users': WORKDAY_WSDL_RECRUITING,
            # Add more mappings as needed
        }

        return wsdl_mapping.get(operation_type, WORKDAY_WSDL_PATH)

    def add_metric(self, key: str, value: any) -> None:
        """Add a metric to track"""
        self.metrics[key] = value

    def serialize_object(self, obj):
        """Custom serializer que preserva IDs y atributos"""
        def _serialize(o):
            if isinstance(o, list):
                return [_serialize(i) for i in o]
            if isinstance(o, dict):
                return {k: _serialize(v) for k, v in o.items()}
            # Zeep ID object: tiene .type y ._value_1
            if hasattr(o, "type") and hasattr(o, "_value_1"):
                return {"type": getattr(o, "type", None), "_value_1": getattr(o, "_value_1", None)}
            return o

        raw = zeep_serialize(obj, target_cls=dict)
        return _serialize(raw)


    async def start(self, **_kwargs) -> None:
        """Initialize the component"""
        await super().start()

        # Process masks for dynamic parameter replacement
        if hasattr(self, '_mask') and self._mask:
            self._logger.info(f"Processing masks: {list(self._mask.keys())}")

            # Apply mask replacement to date parameters
            if hasattr(self, 'start_date') and self.start_date:
                original_start = self.start_date
                self.start_date = self.mask_replacement(self.start_date)
                if original_start != self.start_date:
                    self._logger.info(f"Processed start_date with masks: {original_start} -> {self.start_date}")

            if hasattr(self, 'end_date') and self.end_date:
                original_end = self.end_date
                self.end_date = self.mask_replacement(self.end_date)
                if original_end != self.end_date:
                    self._logger.info(f"Processed end_date with masks: {original_end} -> {self.end_date}")

            if hasattr(self, 'updated_from_date') and self.updated_from_date:
                original = self.updated_from_date
                self.updated_from_date = self.mask_replacement(self.updated_from_date)
                if original != self.updated_from_date:
                    self._logger.info(f"Processed updated_from_date with masks: {original} -> {self.updated_from_date}")

            if hasattr(self, 'updated_to_date') and self.updated_to_date:
                original = self.updated_to_date
                self.updated_to_date = self.mask_replacement(self.updated_to_date)
                if original != self.updated_to_date:
                    self._logger.info(f"Processed updated_to_date with masks: {original} -> {self.updated_to_date}")

            # Apply mask replacement to storage path if it contains masks
            if hasattr(self, 'storage_path') and self.storage_path:
                original_path = self.storage_path
                self.storage_path = self.mask_replacement(self.storage_path)
                if original_path != self.storage_path:
                    self._logger.info(f"Processed storage_path with masks: {original_path} -> {self.storage_path}")

    async def run(self, operation: str = None, **kwargs):
        """Execute the component's main operation"""
        if operation:
            # If operation is provided, this is a SOAP call
            return await super().run(operation=operation, **kwargs)

        # Try to load from storage first
        if self.use_storage:
            storage_file = self._get_storage_file()
            if os.path.exists(storage_file):
                self._logger.info(
                    f"Found existing data file: {storage_file}. Using stored data."
                )
                try:
                    self._result = pd.read_csv(storage_file)
                    return self._result
                except Exception as e:
                    self._logger.error(f"Error loading storage file: {e}")
            else:
                self._logger.info(
                    f"No existing data file found. Will generate new file: {storage_file}"
                )

        # Otherwise this is a component operation
        self._logger.info(f"Starting Workday operation: {self.type}")

        # Get the appropriate handler for the operation type
        handler = self._type_handlers.get(self.type)
        if not handler:
            raise ValueError(f"Unknown operation type: {self.type}")

        # Add parameters to kwargs if specified
        if self.worker_id:
            kwargs['worker_id'] = self.worker_id

        # Add document_directory for workers if specified
        if hasattr(self, 'document_directory') and self.document_directory:
            kwargs['document_directory'] = self.document_directory

        # For get_workers: inject incremental date filter directly into the handler's
        # request_payload so start_date/end_date never leak as top-level SOAP kwargs.
        if self.type == 'get_workers':
            start_date = getattr(self, 'start_date', None)
            end_date = getattr(self, 'end_date', None)
            if start_date:
                # Updated_Through: use explicit end_date if provided, otherwise UTC now minus
                # 5 minutes to avoid clock-skew rejections (Workday validates against UTC).
                from datetime import timezone, timedelta
                updated_through = end_date or (
                    datetime.now(timezone.utc) - timedelta(minutes=5)
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
                self._logger.info(
                    f"📅 Incremental load: Updated_From={start_date}, Updated_Through={updated_through}"
                )
                handler.request_payload["Request_Criteria"]["Transaction_Log_Criteria_Data"] = [
                    {
                        "Transaction_Date_Range_Data": {
                            "Updated_From": start_date,
                            "Updated_Through": updated_through,
                        }
                    }
                ]
        else:
            # For other operation types that use start_date/end_date as direct kwargs
            if hasattr(self, 'start_date') and self.start_date:
                kwargs['start_date'] = self.start_date
            if hasattr(self, 'end_date') and self.end_date:
                kwargs['end_date'] = self.end_date

        # Add time block parameters if they exist in the component (only for time_blocks type)
        if self.type == 'get_time_blocks':
            if hasattr(self, 'time_block_id') and self.time_block_id:
                kwargs['time_block_id'] = self.time_block_id
            if hasattr(self, 'time_block_wid') and self.time_block_wid:
                kwargs['time_block_wid'] = self.time_block_wid
            if hasattr(self, 'status') and self.status:
                kwargs['status'] = self.status
            if hasattr(self, 'supervisory_org') and self.supervisory_org:
                kwargs['supervisory_org'] = self.supervisory_org
            if hasattr(self, 'include_deleted') and self.include_deleted is not None:
                kwargs['include_deleted'] = self.include_deleted

        # Add location parameters if they exist in the component (only for locations type)
        if self.type == 'get_locations':
            if hasattr(self, 'location_id') and self.location_id:
                kwargs['location_id'] = self.location_id
            if hasattr(self, 'location_name') and self.location_name:
                kwargs['location_name'] = self.location_name
            if hasattr(self, 'location_type') and self.location_type:
                kwargs['location_type'] = self.location_type
            if hasattr(self, 'location_usage') and self.location_usage:
                kwargs['location_usage'] = self.location_usage
            if hasattr(self, 'inactive') and self.inactive is not None:
                kwargs['inactive'] = self.inactive

        # Add time request parameters if they exist in the component (only for time_requests type)
        if self.type == 'get_time_requests':
            if hasattr(self, 'time_request_id') and self.time_request_id:
                kwargs['time_request_id'] = self.time_request_id
            if hasattr(self, 'supervisory_organization_id') and self.supervisory_organization_id:
                kwargs['supervisory_organization_id'] = self.supervisory_organization_id

        # Add organization parameters if they exist in the component (only for organizations type)
        if self.type == 'get_organizations':
            if hasattr(self, 'organization_id') and self.organization_id:
                kwargs['organization_id'] = self.organization_id
            if hasattr(self, 'organization_id_type') and self.organization_id_type:
                kwargs['organization_id_type'] = self.organization_id_type
            if hasattr(self, 'organization_type') and self.organization_type:
                kwargs['organization_type'] = self.organization_type
            if hasattr(self, 'include_inactive') and self.include_inactive is not None:
                kwargs['include_inactive'] = self.include_inactive
            if hasattr(self, 'enable_transaction_log_lite') and self.enable_transaction_log_lite is not None:
                kwargs['enable_transaction_log_lite'] = self.enable_transaction_log_lite

        # Add organization parameters if they exist in the component (only for get_organization type)
        if self.type == 'get_organization':
            if hasattr(self, 'organization_id') and self.organization_id:
                kwargs['organization_id'] = self.organization_id
            if hasattr(self, 'organization_id_type') and self.organization_id_type:
                kwargs['organization_id_type'] = self.organization_id_type

        # Add cost center parameters if they exist in the component (only for cost_centers type)
        if self.type == 'get_cost_centers':
            if hasattr(self, 'cost_center_id') and self.cost_center_id:
                kwargs['cost_center_id'] = self.cost_center_id
            if hasattr(self, 'cost_center_id_type') and self.cost_center_id_type:
                kwargs['cost_center_id_type'] = self.cost_center_id_type
            if hasattr(self, 'updated_from_date') and self.updated_from_date:
                kwargs['updated_from_date'] = self.updated_from_date
            if hasattr(self, 'updated_to_date') and self.updated_to_date:
                kwargs['updated_to_date'] = self.updated_to_date
            if hasattr(self, 'include_inactive') and self.include_inactive is not None:
                kwargs['include_inactive'] = self.include_inactive

        # Add applicant parameters if they exist in the component (only for applicants type)
        if self.type == 'get_applicants':
            if hasattr(self, 'applicant_id') and self.applicant_id:
                kwargs['applicant_id'] = self.applicant_id
            if hasattr(self, 'job_requisition_id') and self.job_requisition_id:
                kwargs['job_requisition_id'] = self.job_requisition_id
            if hasattr(self, 'application_date_from') and self.application_date_from:
                kwargs['application_date_from'] = self.application_date_from
            if hasattr(self, 'application_date_to') and self.application_date_to:
                kwargs['application_date_to'] = self.application_date_to
            if hasattr(self, 'is_pre_hire') and self.is_pre_hire is not None:
                kwargs['is_pre_hire'] = self.is_pre_hire

        # Add candidate parameters if they exist in the component (only for candidates type)
        if self.type == 'get_candidates':
            if hasattr(self, 'candidate_id') and self.candidate_id:
                kwargs['candidate_id'] = self.candidate_id
            if hasattr(self, 'job_requisition_id') and self.job_requisition_id:
                kwargs['job_requisition_id'] = self.job_requisition_id
            if hasattr(self, 'applied_from_date') and self.applied_from_date:
                kwargs['applied_from_date'] = self.applied_from_date
            if hasattr(self, 'applied_to_date') and self.applied_to_date:
                kwargs['applied_to_date'] = self.applied_to_date
            if hasattr(self, 'created_from_date') and self.created_from_date:
                kwargs['created_from_date'] = self.created_from_date
            if hasattr(self, 'created_to_date') and self.created_to_date:
                kwargs['created_to_date'] = self.created_to_date
            if hasattr(self, 'pdf_directory') and self.pdf_directory:
                kwargs['pdf_directory'] = self.pdf_directory
            if hasattr(self, 'exclude_all_attachments'):
                kwargs['exclude_all_attachments'] = self.exclude_all_attachments

        # Add job requisition parameters if they exist in the component (only for job_requisitions type)
        if self.type == 'get_job_requisitions':
            if hasattr(self, 'job_requisition_id') and self.job_requisition_id:
                kwargs['job_requisition_id'] = self.job_requisition_id
            if hasattr(self, 'job_requisition_status') and self.job_requisition_status:
                kwargs['job_requisition_status'] = self.job_requisition_status
            if hasattr(self, 'supervisory_organization_id') and self.supervisory_organization_id:
                kwargs['supervisory_organization_id'] = self.supervisory_organization_id
            if hasattr(self, 'location_id') and self.location_id:
                kwargs['location_id'] = self.location_id
            if hasattr(self, 'updated_from_date') and self.updated_from_date:
                kwargs['updated_from_date'] = self.updated_from_date
            if hasattr(self, 'updated_to_date') and self.updated_to_date:
                kwargs['updated_to_date'] = self.updated_to_date

        # Add job posting parameters if they exist in the component (only for job_postings type)
        if self.type == 'get_job_postings':
            if hasattr(self, 'job_posting_id') and self.job_posting_id:
                kwargs['job_posting_id'] = self.job_posting_id
            if hasattr(self, 'job_requisition_id') and self.job_requisition_id:
                kwargs['job_requisition_id'] = self.job_requisition_id
            if hasattr(self, 'job_posting_site_id') and self.job_posting_site_id:
                kwargs['job_posting_site_id'] = self.job_posting_site_id
            if hasattr(self, 'posting_status') and self.posting_status:
                kwargs['posting_status'] = self.posting_status
            if hasattr(self, 'posted_from_date') and self.posted_from_date:
                kwargs['posted_from_date'] = self.posted_from_date
            if hasattr(self, 'posted_to_date') and self.posted_to_date:
                kwargs['posted_to_date'] = self.posted_to_date

        # Add job posting site parameters if they exist in the component (only for job_posting_sites type)
        if self.type == 'get_job_posting_sites':
            if hasattr(self, 'job_posting_site_id') and self.job_posting_site_id:
                kwargs['job_posting_site_id'] = self.job_posting_site_id
            if hasattr(self, 'is_active') and self.is_active is not None:
                kwargs['is_active'] = self.is_active

        # Add references parameters (Integrations service: Get_References)
        if self.type == 'get_references':
            if getattr(self, 'reference_id_type', None):
                kwargs['reference_id_type'] = self.reference_id_type

        # Add time off balance parameters if they exist in the component (only for time_off_balances type)
        if self.type == 'get_time_off_balances':
            if hasattr(self, 'time_off_plan_id') and self.time_off_plan_id:
                kwargs['time_off_plan_id'] = self.time_off_plan_id
            if hasattr(self, 'organization_id') and self.organization_id:
                kwargs['organization_id'] = self.organization_id

        if self.type == 'extract_time_blocks_report':
            if hasattr(self, 'supervisory_organization') and self.supervisory_organization:
                kwargs['supervisory_organization'] = self.supervisory_organization
            if hasattr(self, 'worker') and self.worker:
                kwargs['worker'] = self.worker
            if hasattr(self, 'start_date') and self.start_date:
                kwargs['start_date'] = self.start_date
            if hasattr(self, 'end_date') and self.end_date:
                kwargs['end_date'] = self.end_date

        # Add custom report parameters (generic - passes through all YAML parameters)
        if self.type == 'custom_report':
            # report_name is required
            if hasattr(self, 'report_name') and self.report_name:
                kwargs['report_name'] = self.report_name

            # report_owner is optional
            if hasattr(self, 'report_owner') and self.report_owner:
                kwargs['report_owner'] = self.report_owner

            # Pass through all other attributes as query parameters
            # This allows any report-specific parameters to be passed dynamically
            # Common ones: Start_Date, End_Date, Worker, Year, Month, etc.

            # List of component internal attributes that should NOT be passed as report parameters
            excluded_attrs = {
                # Core component attributes
                'type', 'report_name', 'report_owner', 'component', 'run', 'close',
                'add_metric', 'credentials', 'arguments', 'loop', 'job', 'stat',
                # OAuth/Auth config
                'client_id', 'client_secret', 'refresh_token', 'token_url',
                'report_username', 'report_password',
                # Workday instance config
                'tenant', 'workday_url', 'wsdl_path', 'zeep_debug',
                # Component config
                'timeout', 'encoding', 'use_memory', 'use_storage', 'storage_path',
                # Redis config
                'redis_url', 'redis_key',
                # ID types and other internal flags
                'cost_center_id_type', 'organization_id_type', 'worker_id_type',
                'exclude_all_attachments', 'exclude_employees', 'exclude_contingent_workers',
                # FloTask framework attributes
                'StepName', 'TaskName', 'debug', 'step_name', 'task_name',
            }

            for attr_name in dir(self):
                # Skip private/protected attributes and methods
                if attr_name.startswith('_'):
                    continue
                # Skip excluded attributes
                if attr_name in excluded_attrs:
                    continue
                # Get attribute value
                attr_value = getattr(self, attr_name, None)
                # Only add if it's a simple value (not a method or complex object)
                if attr_value is not None and not callable(attr_value):
                    # Check if it's a simple type (str, int, float, bool, date)
                    if isinstance(attr_value, (str, int, float, bool)):
                        kwargs[attr_name] = attr_value

        # Execute the operation
        result = None
        try:
            result = await handler.execute(**kwargs)

            # Save to storage after successful execution
            if self.use_storage and result is not None and isinstance(result, pd.DataFrame):
                try:
                    storage_file = self._get_storage_file()
                    result.to_csv(storage_file, index=False)
                    self._logger.info(
                        f"Successfully saved data to: {storage_file}"
                    )
                except Exception as e:
                    self._logger.error(f"Error saving to storage: {e}")

        except Exception as exc:
            self._logger.error(f"Error during Workday operation: {exc}")
            raise

        # Add metrics if result is a DataFrame
        if isinstance(result, pd.DataFrame):
            self.add_metric("NUMROWS", len(result.index))
            self.add_metric("NUMCOLS", len(result.columns))

        # Store and return result
        self._result = result

        if getattr(self, '_debug', False):
            self._print_data("Workday Result", result)

        self._logger.info("Workday operation finished successfully")
        return self._result

    def _print_data(self, title: str, data_df: pd.DataFrame) -> None:
        """Debug helper to print DataFrame information"""
        print(f"::: Printing {title} === ")
        print("Data: ", data_df)
        for column, t in data_df.dtypes.items():
            print(f"{column} -> {t} -> {data_df[column].iloc[0] if not data_df.empty else None}")

    async def get_custom_report(
        self,
        report_name: str,
        report_owner: str = None,
        **query_params
    ) -> pd.DataFrame:
        """
        Execute any Workday RaaS (Reports as a Service) custom report.

        This is a generic method that can execute ANY Workday custom report
        without requiring specific type implementations. It automatically:
        - Builds the correct RaaS REST API URL
        - Authenticates with Basic Auth credentials
        - Converts JSON response to DataFrame with automatic column detection
        - Handles nested structures appropriately

        Args:
            report_name: Name of the report in Workday (required)
                Example: "Extract_Time_Blocks_-_Navigator"
            report_owner: Email/ID of report owner (optional)
                Defaults to configured report_owner or 'jleon@trocglobal.com'
            **query_params: Any report-specific parameters
                Examples: Start_Date, End_Date, Worker, Year, Month, etc.
                The method accepts any parameters the report needs.

        Returns:
            DataFrame with automatic column detection from JSON response

        Examples:
            # Time blocks report with date range and worker
            df = await wd.get_custom_report(
                report_name="Extract_Time_Blocks_-_Navigator",
                Start_Date="2025-11-17",
                End_Date="2025-11-17",
                Worker="12345"
            )

            # Absence calendar with different parameters
            df = await wd.get_custom_report(
                report_name="Absence_Calendar_Report",
                Year="2025",
                Month="11",
                Employee_Type="Full_Time"
            )

            # Payroll report with custom report owner
            df = await wd.get_custom_report(
                report_name="Payroll_Summary_Report",
                report_owner="hr@company.com",
                Start_Date="2025-01-01",
                End_Date="2025-12-31"
            )
        """
        # Set the operation type to custom_report
        self.type = "custom_report"

        # Execute using the generic CustomReportType handler
        return await self.run(
            report_name=report_name,
            report_owner=report_owner,
            **query_params
        )

    async def close(self) -> None:
        """Cleanup resources"""
        await super().close()
