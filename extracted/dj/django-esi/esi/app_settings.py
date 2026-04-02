from django.conf import settings

ESI_SSO_CLIENT_ID = getattr(settings, 'ESI_SSO_CLIENT_ID', None)
"""Client ID of your Eve Online SSO app. REQUIRED."""

ESI_SSO_CLIENT_SECRET = getattr(settings, 'ESI_SSO_CLIENT_SECRET', None)
"""Client Secret of your Eve Online SSO app. REQUIRED."""

ESI_SSO_CALLBACK_URL = getattr(settings, 'ESI_SSO_CALLBACK_URL', None)
"""Callback for your Eve Online SSO app. REQUIRED."""

# ESI_SSO_CLIENT_ID, ESI_SSO_CLIENT_SECRET ESI_SSO_CALLBACK_URL
# are required for SSO to function.
# Can be left blank if settings.DEBUG is set to True

ESI_ALWAYS_CREATE_TOKEN = getattr(settings, 'ESI_ALWAYS_CREATE_TOKEN', False)
"""Enable to force new token creation every callback."""

ESI_CACHE_RESPONSE = getattr(settings, 'ESI_CACHE_RESPONSE', True)
"""Disable to stop caching endpoint responses."""

ESI_USER_CONTACT_EMAIL = getattr(settings, 'ESI_USER_CONTACT_EMAIL', None)
"""Contact email address of server owner.

This will be included in the User-Agent header of every request.
"""

# https://www.python-httpx.org/advanced/resource-limits/
ESI_CONNECTION_POOL_MAX_CONNECTIONS = getattr(settings, 'ESI_CONNECTION_POOL_MAX_CONNECTIONS', 100)
"""Maximum number of allowable connections"""

ESI_CONNECTION_POOL_MAX_KEEPALIVE = getattr(settings, 'ESI_CONNECTION_POOL_MAX_KEEPALIVE', 20)
"""Number of allowable keep-alive connections"""

ESI_CONNECTION_POOL_KEEPALIVE_EXPIRY = getattr(settings, 'ESI_CONNECTION_POOL_KEEPALIVE_EXPIRY', 5)
"""Time limit on idle keep-alive connections in seconds"""

# https://tenacity.readthedocs.io/en/latest/api.html#tenacity.wait.wait_exponential
ESI_SERVER_ERROR_MAX_RETRIES = getattr(settings, 'ESI_SERVER_ERROR_MAX_RETRIES', 3)
"""Max retries on server errors."""

ESI_SERVER_ERROR_WAIT_EXPONENT = getattr(settings, 'ESI_SERVER_ERROR_WAIT_EXPONENT', 1)
""""""

# https://www.python-httpx.org/advanced/timeouts/
ESI_REQUESTS_CONNECT_TIMEOUT = getattr(settings, 'ESI_REQUESTS_CONNECT_TIMEOUT', 5)
"""Default connection timeouts for all requests to ESI."""

ESI_REQUESTS_READ_TIMEOUT = getattr(settings, 'ESI_REQUESTS_READ_TIMEOUT', 10)
"""Default read timeouts for all requests to ESI.
This should be a maximum of 10s as ESI cuts all requests to the monolith off @ 10s.
"""

ESI_REQUESTS_WRITE_TIMEOUT = getattr(settings, 'ESI_REQUESTS_WRITE_TIMEOUT', 5)
"""Default write timeouts for all requests to ESI."""

ESI_REQUESTS_POOL_TIMEOUT = getattr(settings, 'ESI_REQUESTS_POOL_TIMEOUT', 5)
"""Default pool timeouts for all requests to ESI"""

# These probably won't ever change. Override if needed.
ESI_API_URL = getattr(settings, 'ESI_API_URL', 'https://esi.evetech.net/')
ESI_OAUTH_URL = getattr(
    settings, 'ESI_SSO_BASE_URL', 'https://login.eveonline.com/v2/oauth'
)
ESI_OAUTH_LOGIN_URL = getattr(
    settings, 'ESI_SSO_LOGIN_URL', ESI_OAUTH_URL + "/authorize/"
)
ESI_TOKEN_URL = getattr(settings, 'ESI_CODE_EXCHANGE_URL', ESI_OAUTH_URL + "/token")

ESI_TOKEN_JWK_SET_URL = "https://login.eveonline.com/oauth/jwks"

ESI_TOKEN_VALID_DURATION = int(getattr(settings, 'ESI_TOKEN_VALID_DURATION', 1170))

# Audience claim for JWTs
ESI_TOKEN_JWT_AUDIENCE = str(getattr(settings, "ESI_TOKEN_JWT_AUDIENCE", "EVE Online"))

# list of all official language codes supported by ESI
ESI_LANGUAGES = getattr(settings, 'ESI_LANGUAGES', [
    'en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'
])
