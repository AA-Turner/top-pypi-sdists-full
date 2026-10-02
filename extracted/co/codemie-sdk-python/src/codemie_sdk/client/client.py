"""Base client implementation for CodeMie SDK."""

from typing import Callable

from ..auth.credentials import KeycloakCredentials, LocalAuthCredentials
from ..services.a2a import A2AService
from ..services.admin import AdminService
from ..services.analytics import AnalyticsService
from ..services.assistant import AssistantService
from ..services.categories import CategoryService
from ..services.conversation import ConversationService
from ..services.datasource import DatasourceService
from ..services.llm import LLMService
from ..services.integration import IntegrationService
from ..services.mermaid import MermaidService
from ..services.project import ProjectService
from ..services.skill import SkillService
from ..services.task import TaskService
from ..services.user import UserService
from ..services.workflow import WorkflowService
from ..services.files import FileOperationService
from ..services.webhook import WebhookService
from ..services.vendor_assistant import VendorAssistantService
from ..services.vendor_workflow import VendorWorkflowService
from ..services.vendor_knowledgebase import VendorKnowledgeBaseService
from ..services.vendor_guardrail import VendorGuardrailService
from ..services.vendor_runtime import VendorRuntimeService
from ..services.activity_event import ActivityEventService
from ..services.codemie_guardrails import CodemieGuardrailService
from ..services.dynamic_config import DynamicConfigService
from ..services.mcp_configs import MCPConfigsService
from ..services.cost_center import CostCenterService
from ..services.customer_config_service import CustomerConfigService
from ..services.project_budget_groups import ProjectBudgetGroupsService


class CodeMieClient:
    """Main client class for interacting with CodeMie API."""

    def __init__(
        self,
        auth_server_url: str,
        auth_realm_name: str,
        codemie_api_domain: str,
        auth_client_id: str | None = None,
        auth_client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        external_token: str | Callable[[], str] | None = None,
        external_idp: str | None = None,
        verify_ssl: bool = True,
    ):
        """Initialize CodeMie client with authentication credentials.

        Args:
            auth_server_url: Keycloak server URL
            auth_realm_name: Realm name for authentication
            codemie_api_domain: CodeMie API domain
            auth_client_id: Client ID for authentication (optional if using username/password)
            auth_client_secret: Client secret for authentication (optional if using username/password)
            username: Username/email for password grant (optional if using client credentials)
            password: Password for password grant (optional if using client credentials)
            external_token: External token for authentication (optional, replaces username/password)
            external_idp: Identity provider ID to validate extern_token with (optional, required if using external_token)
            verify_ssl: Whether to verify SSL certificates (default: True)
        """
        self._token: str | None = None
        self._api_domain = codemie_api_domain.rstrip("/")
        self._is_localhost = self._is_localhost_domain(self._api_domain)
        self._verify_ssl = verify_ssl
        if not verify_ssl:
            import requests
            from urllib3.exceptions import InsecureRequestWarning

            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        if self._is_localhost and username and password:
            self._local_auth: LocalAuthCredentials | None = LocalAuthCredentials(
                api_domain=codemie_api_domain,
                email=username,
                password=password,
                verify_ssl=verify_ssl,
            )
            self._token = self._local_auth.get_token()
            _token_source = self._local_auth.get_token
        elif self._is_localhost:
            self._local_auth = None
            self._token = ""
            _token_source = ""
        else:
            self._local_auth = None
            self.auth = KeycloakCredentials(
                server_url=auth_server_url,
                realm_name=auth_realm_name,
                client_id=auth_client_id,
                client_secret=auth_client_secret,
                username=username,
                password=password,
                external_token=external_token,
                external_idp=external_idp,
                verify_ssl=verify_ssl,
            )
            self._token = self.auth.get_token()
            _token_source = self.auth.get_token

        # Initialize services with verify_ssl parameter and token
        self.admin = AdminService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.analytics = AnalyticsService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.assistants = AssistantService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.categories = CategoryService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.llms = LLMService(self._api_domain, _token_source, verify_ssl=verify_ssl)
        self.mermaid = MermaidService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.integrations = IntegrationService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.projects = ProjectService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.skills = SkillService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.tasks = TaskService(self._api_domain, _token_source, verify_ssl=verify_ssl)
        self.users = UserService(self._api_domain, _token_source, verify_ssl=verify_ssl)
        self.datasources = DatasourceService(
            self._api_domain, _token_source, verify_ssl=verify_ssl
        )
        self.workflows = WorkflowService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.conversations = ConversationService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.files = FileOperationService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.webhook = WebhookService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.vendor_assistants = VendorAssistantService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.vendor_workflows = VendorWorkflowService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.vendor_knowledgebases = VendorKnowledgeBaseService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.vendor_guardrails = VendorGuardrailService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.vendor_runtimes = VendorRuntimeService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.codemie_guardrails = CodemieGuardrailService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.activity_events = ActivityEventService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.mcp_configs = MCPConfigsService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.dynamic_config = DynamicConfigService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.customer_config = CustomerConfigService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.cost_centers = CostCenterService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.project_budget_groups = ProjectBudgetGroupsService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )
        self.a2a = A2AService(
            self._api_domain, _token_source, verify_ssl=self._verify_ssl
        )

    @property
    def token(self) -> str:
        """Get current token or fetch new one if not available."""
        if self._is_localhost and self._local_auth:
            self._token = self._local_auth.get_token()
        elif not self._is_localhost:
            self._token = self.auth.get_token()
        return self._token

    @staticmethod
    def _is_localhost_domain(domain: str) -> bool:
        """Check if the domain is a localhost variant."""
        domain_lower = domain.lower()
        localhost_patterns = [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "192.168",
        ]
        return any(pattern in domain_lower for pattern in localhost_patterns)

    def refresh_token(self) -> str:
        """Force token refresh."""
        if self._is_localhost and self._local_auth:
            self._local_auth._cached_token = None
            self._local_auth._token_expires_at = 0.0
            self._token = self._local_auth.get_token()
        elif self._is_localhost:
            self._token = ""
        else:
            self.auth._cached_token = None
            self.auth._token_expires_at = 0.0
            self._token = self.auth.get_token()
        return self._token
