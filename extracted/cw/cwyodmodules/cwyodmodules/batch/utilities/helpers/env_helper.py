import json
import threading

from ..helpers.config.conversation_flow import ConversationFlow
from mgmt_config import logger, identity, configuration_manager

KEYVAULT_TTL = 3600 # 1 hour

class EnvHelper:
    """
    Singleton for environment and configuration variables used throughout the project.
    Each variable is commented with where it is used (file/class/function).
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                instance = super(EnvHelper, cls).__new__(cls)
                instance.__load_config()
                cls._instance = instance
            return cls._instance

    @logger.trace_function(log_execution=True, log_args=False, log_result=False)
    def __load_config(self, **kwargs) -> None:
        """Load all environment/configuration variables."""
        logger.info("Initializing EnvHelper!")

        # --- General/Azure Identity ---
        self.AZURE_CLIENT_ID = configuration_manager.get_config(key="AZURE_CLIENT_ID", default="Not set")  # Used in: Azure auth flows
        configuration_manager.set_config(key="APPLICATIONINSIGHTS_ENABLED", value="true")
        self.LOGLEVEL = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="logging-level", ttl=KEYVAULT_TTL)  # Used in: logging setup
        self.LOG_EXECUTION = configuration_manager.get_config(key="LOG_EXECUTION", default="True") == "True"  # Used in: logging decorators
        self.LOG_ARGS = configuration_manager.get_config(key="LOG_ARGS", default="True") == "True"  # Used in: logging decorators
        self.LOG_RESULT = configuration_manager.get_config(key="LOG_RESULT", default="True") == "True"  # Used in: logging decorators

        # --- Azure Resource Info ---
        self.AZURE_SUBSCRIPTION_ID = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="subscription-id", ttl=KEYVAULT_TTL)  # Used in: create_app.py (speech key)
        self.AZURE_RESOURCE_GROUP = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="resource-group-name", ttl=KEYVAULT_TTL)
        self.AZURE_HEAD_RESOURCE_GROUP = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name="resource-group-name", ttl=KEYVAULT_TTL)  # Used in: create_app.py (speech key)
        self.AZURE_RESOURCE_ENVIRONMENT = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="resource-group-environment", ttl=KEYVAULT_TTL)
        self.AZURE_RESOURCE_PRIVATE = (
            configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="run-private-endpoint", ttl=KEYVAULT_TTL).lower() == "true"
        )  # Used in: create_app.py (speech endpoint)
        self.PROJECT_CODE = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="project-code", ttl=KEYVAULT_TTL)
        self.APP_NAME = configuration_manager.get_config(key="REFLECTION_NAME", default="Default")
        self.POSTGRESQL_NAME = (
            f"psql-main-{self.PROJECT_CODE}-{self.AZURE_RESOURCE_ENVIRONMENT}"
        )
        self.AZURE_AUTH_TYPE = "rbac"  # Used in: helpers, LLM, content safety, etc.
        access_information = identity.get_token_provider(scopes="https://cognitiveservices.azure.com/.default")
        self.AZURE_TOKEN_PROVIDER = access_information  # Used in: LLMHelper, chat_history
        self.AZURE_BLOB_ACCOUNT_NAME = (
            f"stqueue{self.PROJECT_CODE}{self.AZURE_RESOURCE_ENVIRONMENT}"
        )  # Used in: blob storage helpers, batch, frontend
        self.AZURE_STORAGE_ACCOUNT_ENDPOINT = (
            f"https://{self.AZURE_BLOB_ACCOUNT_NAME}.blob.core.windows.net/"
        )
        self.AZURE_FUNCTION_APP_ENDPOINT = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name=f"func-backend-{self.PROJECT_CODE}-{self.AZURE_RESOURCE_ENVIRONMENT}-endpoint", ttl=KEYVAULT_TTL)  # Used in: admin frontend
        self.AZURE_BLOB_CONTAINER_NAME = "documents"  # Used in: blob helpers, batch, frontend
        self.DOCUMENT_PROCESSING_QUEUE_NAME = "doc-processing"  # Used in: batch_start_processing.py
        self.AZURE_POSTGRES_SEARCH_TOP_K = 5  # Used in: search handlers

        # --- PostgreSQL ---
        azure_postgresql_info = self.get_info_from_env("AZURE_POSTGRESQL_INFO", "")
        if azure_postgresql_info:
            self.POSTGRESQL_USER = azure_postgresql_info.get("user", "")  # Used in: postgres_db.py, azure_postgres_helper.py, database_factory.py
            self.POSTGRESQL_DATABASE = azure_postgresql_info.get("dbname", "")
            self.POSTGRESQL_HOST = azure_postgresql_info.get("host", "")
        else:
            self.POSTGRESQL_USER = "cwyod_project_uai"
            self.POSTGRESQL_DATABASE = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name=f"{self.POSTGRESQL_NAME}-default-database-name", ttl=KEYVAULT_TTL)
            self.POSTGRESQL_HOST = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name=f"{self.POSTGRESQL_NAME}-server-name", ttl=KEYVAULT_TTL)

        # --- Feature Flags ---
        self.USE_ADVANCED_IMAGE_PROCESSING = False  # Used in: question_answer_tool.py, config_helper.py
        self.ADVANCED_IMAGE_PROCESSING_MAX_IMAGES = 1  # Used in: question_answer_tool.py
        self.CONVERSATION_FLOW = ConversationFlow.CUSTOM.value  # Used in: config_helper.py
        self.ORCHESTRATION_STRATEGY = "semantic_kernel"  # Used in: admin frontend, get_test_response.py

        # --- Azure OpenAI ---
        self.AZURE_OPENAI_MODEL = "gpt-4o-default"  # Used in: LLMHelper, create_app.py, get_conversation_response.py
        self.AZURE_OPENAI_MODEL_NAME = self.AZURE_OPENAI_MODEL
        self.AZURE_OPENAI_VISION_MODEL = "gpt-4"  # Used in: question_answer_tool.py
        self.AZURE_OPENAI_TEMPERATURE = "0"  # Used in: LLMHelper
        self.AZURE_OPENAI_TOP_P = "1.0"  # Used in: LLMHelper
        self.AZURE_OPENAI_MAX_TOKENS = "1500"  # Used in: LLMHelper
        self.AZURE_OPENAI_STOP_SEQUENCE = ""  # Used in: LLMHelper
        self.AZURE_OPENAI_SYSTEM_MESSAGE = (
            "You are an AI assistant that helps people find information."
        )  # Used in: question_answer_tool.py
        self.AZURE_OPENAI_API_VERSION = "2024-02-01"  # Used in: LLMHelper, chat_history, etc.
        self.AZURE_OPENAI_STREAM = "true"  # Used in: LLMHelper
        self.AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"  # Used in: LLMHelper, admin frontend
        self.SHOULD_STREAM = (
            True if self.AZURE_OPENAI_STREAM.lower() == "true" else False
        )  # Used in: LLMHelper

        if self.AZURE_AUTH_TYPE == "rbac":
            self.AZURE_OPENAI_API_KEY = ""  # Used in: LLMHelper, chat_history
        else:
            self.AZURE_OPENAI_API_KEY = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="AZURE_OPENAI_API_KEY", ttl=KEYVAULT_TTL)

        # --- Azure OpenAI Endpoint ---
        self.AZURE_AI_SERVICES_NAME = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name="cognitive-kind-AIServices", ttl=KEYVAULT_TTL)  # Used in: LLMHelper
        self.AZURE_OPENAI_ENDPOINT = (
            f"https://{self.AZURE_AI_SERVICES_NAME}.openai.azure.com/"
        )  # Used in: LLMHelper, chat_history

        # --- OpenAI SDK ---
        self.OPENAI_API_TYPE = "azure" if self.AZURE_AUTH_TYPE == "keys" else "azure_ad"  # Used in: LLMHelper
        self.OPENAI_API_KEY = self.AZURE_OPENAI_API_KEY  # Used in: LLMHelper
        self.OPENAI_API_VERSION = self.AZURE_OPENAI_API_VERSION  # Used in: LLMHelper
        configuration_manager.set_config(key="OPENAI_API_TYPE", value=self.OPENAI_API_TYPE, env=True)
        configuration_manager.set_config(key="OPENAI_API_KEY", value=self.OPENAI_API_KEY, env=True)
        configuration_manager.set_config(key="OPENAI_API_VERSION", value=self.OPENAI_API_VERSION, env=True)

        # --- Azure Functions - Batch processing ---
        self.BACKEND_URL = self.AZURE_FUNCTION_APP_ENDPOINT  # Used in: admin frontend
        self.FUNCTION_KEY = None  # Used in: admin frontend

        # --- Azure Form Recognizer ---
        self.AZURE_FORM_RECOGNIZER_NAME = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name="cognitive-kind-FormRecognizer", ttl=KEYVAULT_TTL)  # Used in: azure_form_recognizer_helper.py
        self.AZURE_FORM_RECOGNIZER_ENDPOINT = configuration_manager.get_keyvault_secret(keyvault_name="main", secret_name=f"{self.AZURE_FORM_RECOGNIZER_NAME}-endpoint", ttl=KEYVAULT_TTL)  # Used in: azure_form_recognizer_helper.py

        # --- Azure App Insights ---
        self.APPLICATIONINSIGHTS_ENABLED = "True"  # Used in: logging setup

        # --- Azure AI Content Safety ---
        self.AZURE_CONTENT_SAFETY_NAME = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name="cognitive-kind-ContentSafety", ttl=KEYVAULT_TTL)  # Used in: content_safety_checker.py
        self.AZURE_CONTENT_SAFETY_ENDPOINT = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name=f"{self.AZURE_CONTENT_SAFETY_NAME}-endpoint", ttl=KEYVAULT_TTL)  # Used in: content_safety_checker.py

        # --- Speech Service ---
        self.AZURE_SPEECH_SERVICE_NAME = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name="cognitive-kind-SpeechServices", ttl=KEYVAULT_TTL)  # Used in: create_app.py
        self.AZURE_SPEECH_ENDPOINT = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name=f"{self.AZURE_SPEECH_SERVICE_NAME}-endpoint", ttl=KEYVAULT_TTL)  # Used in: create_app.py
        self.AZURE_SPEECH_SERVICE_REGION = "westeurope"  # Used in: create_app.py
        self.AZURE_SPEECH_RECOGNIZER_LANGUAGES = configuration_manager.get_config(key="AZURE_SPEECH_RECOGNIZER_LANGUAGES", default="en-US").split(",")  # Used in: create_app.py
        self.AZURE_MAIN_CHAT_LANGUAGE = "en-US"  # Used in: semantic_kernel_orchestrator.py, outlook_calendar_plugin.py
        self.AZURE_SPEECH_REGION_ENDPOINT = (
            f"https://{self.AZURE_SPEECH_SERVICE_REGION}.api.cognitive.microsoft.com/"
        )  # Used in: create_app.py
        self.AZURE_SPEECH_KEY = configuration_manager.get_keyvault_secret(keyvault_name="head", secret_name=f"{self.AZURE_SPEECH_SERVICE_NAME}-key", ttl=KEYVAULT_TTL)  # Used in: create_app.py
        self.SEMENTIC_KERNEL_SYSTEM_PROMPT = configuration_manager.get_config(key="SEMENTIC_KERNEL_SYSTEM_PROMPT", default="")  # Used in: semantic_kernel_orchestrator.py
        logger.info("Initializing EnvHelper completed")

    def get_info_from_env(self, env_var: str, default_info: str) -> dict:
        """Fetch and parse model info from the environment variable."""
        info_str = configuration_manager.get_config(key=env_var, default=default_info)
        if "\\" in info_str:
            info_str = json.loads(f'"{info_str}"')
        try:
            return {} if not info_str else json.loads(info_str)
        except (json.JSONDecodeError, ValueError, TypeError):
            try:
                return json.loads(default_info) if default_info else {}
            except (json.JSONDecodeError, ValueError, TypeError):
                return {}