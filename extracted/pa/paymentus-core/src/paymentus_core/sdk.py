"""
SDK class for Paymentus API
"""
import uuid
from typing import Dict, List, Optional, Any, Type

from paymentus_auth.auth import PaymentData, PixelType
from pydantic import BaseModel, Field

from paymentus_auth import Auth, AuthConfig, ConfigurationError
from paymentus_xotp import (
    XotpApiClient, ApiClient, Configuration,
    LogLevel, MaskingLevel, Logger
)
from paymentus_xotp.middlewares import LoggingConfiguration
from .version import LIB_VERSION


class AuthOptions(AuthConfig):
    """Auth options for SDK"""
    base_url: Optional[str] = None
    pre_shared_key: Optional[str] = None
    tla: Optional[str] = None


class LoggingOptions(BaseModel):
    """Logging options for SDK"""
    
    level: Optional[LogLevel] = LogLevel.NORMAL
    masking: Optional[MaskingLevel] = MaskingLevel.PCI_ONLY
    logger: Optional[Type[Logger]] = Logger
    
    model_config = {
        "arbitrary_types_allowed": True
    }


class SessionOptions(BaseModel):
    """Session options for SDK"""
    id: Optional[str] = None


class CoreConfig(BaseModel):
    """Configuration for Core SDK"""
    base_url: str
    pre_shared_key: str
    tla: str
    auth: Optional[AuthOptions] = Field(default_factory=AuthOptions)
    xotp: Optional[Dict[str, Any]] = None
    logging: Optional[LoggingOptions] = LoggingOptions()
    session: Optional[SessionOptions] = None
    timeout: Optional[int] = 5000
    
    model_config = {
        "arbitrary_types_allowed": True
    }


class AuthInterface:
    """Interface for auth operations"""
    
    def __init__(self, sdk):
        """Initialize with reference to parent SDK"""
        self._sdk = sdk
    
    async def fetch_token(self) -> str:
        """Fetch a new token"""
        return await self._sdk._fetch_token()
    
    def get_current_token(self) -> Optional[str]:
        """Get the current token"""
        return self._sdk._get_current_token()
    
    def is_token_expired(self) -> bool:
        """Check if the token is expired"""
        return self._sdk._is_token_expired()


class SDK:
    """SDK class for Paymentus API"""
    
    def __init__(self, config: CoreConfig):
        """Initialize SDK with configuration
        
        Args:
            config: Core SDK configuration
        """
        self.validate_config(config)
        
        sdk_session_id = config.session.id if config.session and config.session.id else str(uuid.uuid4())
        
        # Initialize Auth client
        self.auth_client = Auth(AuthConfig(
            base_url=config.base_url,
            pre_shared_key=config.pre_shared_key,
            tla=config.tla,
            scope=config.auth.scope if config.auth else [],
            pixels=config.auth.pixels if config.auth else None,
            user_login=config.auth.user_login if config.auth else None,
            payments_data=config.auth.payments_data if config.auth else None,
            pm_token=config.auth.pm_token if config.auth else None,
            aud=config.auth.aud if config.auth else None,
            kid=config.auth.kid if config.auth else "001",
            timeout=config.auth.timeout if config.auth else 5000,
            session={"id": sdk_session_id}
        ))
        
        self.current_token = None
        
        # Prepare XOTP base URL
        xotp_base_url = config.base_url
        if not xotp_base_url.endswith('/api'):
            xotp_base_url = f"{xotp_base_url}/api"
        
        configuration = Configuration(
            host=xotp_base_url
        )

        # TODO: Remove this after development
        # configuration.verify_ssl = False

        api_client = ApiClient(
            configuration=configuration
        )

        # Set session headers
        api_client.set_default_header("X-Ext-Session-Id", sdk_session_id)
        api_client.set_default_header("X-Ext-Session-App", f"python-server-sdk@{LIB_VERSION}")

        # Set up logging configuration if provided
        logging_config = None
        if config.logging:
            log_level = config.logging.level or LogLevel.NORMAL
            LoggerClass = config.logging.logger or Logger
            
            # Instantiate the logger class with the specified log level.
            logger_instance = LoggerClass(log_level)
            
            logging_config = LoggingConfiguration(
                level=log_level,
                masking=config.logging.masking,
                logger=logger_instance
            )

        # Initialize XOTP client with session headers, token provider and logging
        self._xotp_client = XotpApiClient(
            base_url=xotp_base_url,
            tla=config.tla,
            api_client=api_client,
            token_provider=self._token_provider,
            logging_config=logging_config
        )
        
        # Initialize auth interface
        self._auth_interface = AuthInterface(self)
        
    def validate_config(self, config: CoreConfig) -> None:
        """Validate the configuration"""
        if not config.base_url or not config.base_url.strip():
            raise ConfigurationError("Invalid base_url")
        if not config.pre_shared_key or not config.pre_shared_key.strip():
            raise ConfigurationError("Invalid pre_shared_key")
        if not config.tla or not config.tla.strip():
            raise ConfigurationError("Invalid tla")
    
    async def _token_provider(self) -> str:
        """
        Token provider function that returns a valid JWT token.
        This will be called by the XotpApiClient before each API request.
        
        Returns:
            A valid JWT token string
        """
        # Use current token if available and not expired
        current_token = self._get_current_token()
        if current_token and not self._is_token_expired():
            return current_token
            
        # Otherwise fetch a new token
        return await self._fetch_token()
    
    @property
    def auth(self):
        """Auth interface"""
        return self._auth_interface
    
    async def _fetch_token(self) -> str:
        """Fetch a new token"""
        token = await self.auth_client.fetch_token()
        self.current_token = token
        return token
    
    def _get_current_token(self) -> Optional[str]:
        """Get the current token"""
        return self.current_token or self.auth_client.get_current_token()
    
    def _is_token_expired(self) -> bool:
        """Check if the token is expired"""
        return self.auth_client.is_token_expired()
    
    @property
    def xotp(self) -> XotpApiClient:
        """XOTP client proxy that ensures token is available"""
        return self._xotp_client 