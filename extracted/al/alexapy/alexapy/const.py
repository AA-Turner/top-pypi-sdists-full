"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Constants.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"

LOGIN_APP_VERSION = "2.2.556530.0"
CALL_VERSION = LOGIN_APP_VERSION  # Compatibility alias
APP_NAME = "Alexa Media Player"

# The skills store answers the app's JSON pages only with this media type.
SKILLS_STORE_ACCEPT = "application/vnd+amazon.uitoolkit+json;ns=1;fl=0"

# Cookie persistence format used by alexapy.
#
# This is intentionally owned by alexapy rather than relying on aiohttp
# CookieJar.save/load internals, which can change across aiohttp/Python
# versions and may not support newly introduced cookie attributes.
COOKIE_SERIALIZATION_FORMAT = "alexapy.cookies"
COOKIE_SERIALIZATION_VERSION = 1

# REST-style Alexa API hosts (for things like /api/notifications)
ALEXA_API_NA = "https://na-api-alexa.amazon.com"
ALEXA_API_EU = "https://eu-api-alexa.amazon.com"
ALEXA_API_FE = "https://fe-api-alexa.amazon.com"

ALEXA_API_BASE = {
    ".com": ALEXA_API_NA,
    ".ca": ALEXA_API_NA,
    ".com.mx": ALEXA_API_NA,
    ".com.br": ALEXA_API_NA,
    ".co.uk": ALEXA_API_EU,
    ".de": ALEXA_API_EU,
    ".fr": ALEXA_API_EU,
    ".es": ALEXA_API_EU,
    ".it": ALEXA_API_EU,
    ".in": ALEXA_API_FE,
    ".co.jp": ALEXA_API_FE,
    ".com.au": ALEXA_API_FE,
    ".co.nz": ALEXA_API_FE,
}

# Historical notifications identity retained for callers importing API_USER_AGENT.
ANDROID_NOTIFICATIONS_USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.101 Mobile Safari/537.36"
)

# Default Accept-Language header for REST API calls.
# Amazon documentation and Alexa mobile clients are consistently en-US.
DEFAULT_ACCEPT_LANGUAGE = "en-US"

# Centralize default locale for other operations
DEFAULT_LOCALE = "en-US"

LOGIN_WEBVIEW_USER_AGENT = (
    f"AmazonWebView/Amazon Alexa/{LOGIN_APP_VERSION}/iOS/16.6/iPhone"
)
LOGIN_BROWSER_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "PitanguiBridge/2.2.345247.0-[HARDWARE=iPhone10_4][SOFTWARE=13.5.1]"
)
PITANGUI_API_USER_AGENT = (
    "AppleWebKit PitanguiBridge/2.2.785556.0-"
    "[HARDWARE=iPhone19_7][SOFTWARE=27.2.1][DEVICE=iPhone]"
)

# Preserve the values exposed to existing importers.
USER_AGENT = LOGIN_WEBVIEW_USER_AGENT
API_USER_AGENT = ANDROID_NOTIFICATIONS_USER_AGENT

LOCALE_KEY = {
    ".de": "de_DE",
    ".com.au": "en_AU",
    ".ca": "en_CA",
    ".co.uk": "en_GB",
    ".in": "en_IN",
    ".com": "en_US",
    ".es": "es_ES",
    ".mx": "es_MX",
    ".fr": "fr_FR",
    ".it": "it_IT",
    ".co.jp": "ja_JP",
    ".com.br": "pt_BR",
}
# Retail marketplace identifiers used by the Alexa lists service.
LIST_MARKETPLACE_IDS = {
    "amazon.com": "ATVPDKIKX0DER",
    "amazon.co.uk": "A1F83G8C2ARO7P",
    "amazon.de": "A1PA6795UKMFR9",
    "amazon.in": "A21TJRUUN4KGV",
    "amazon.co.jp": "A1VC38T7YXB528",
    "amazon.com.au": "A39IBJ37TRP1C6",
    "amazon.ca": "A2EUQ1WTGCTBG2",
    "amazon.fr": "A13V1IB3VIYZZH",
    "amazon.it": "APJ6JRA9NG5V4",
    "amazon.es": "A1RKKUPIHCS9HS",
    "amazon.com.mx": "A1AM78C64UM0Y8",
    "amazon.com.br": "A2Q3Y263D00KWC",
}
# https://developer.amazon.com/en-US/docs/alexa/alexa-voice-service/api-overview.html#endpoints
HTTP2_NA = "alexa.na.gateway.devices.a2z.com"
HTTP2_EU = "alexa.eu.gateway.devices.a2z.com"
HTTP2_FE = "alexa.fe.gateway.devices.a2z.com"
HTTP2_AUTHORITY = {
    ".com": HTTP2_NA,
    ".ca": HTTP2_NA,
    ".com.mx": HTTP2_NA,
    ".com.br": HTTP2_NA,
    ".co.jp": HTTP2_FE,
    ".com.au": HTTP2_FE,
    ".com.in": HTTP2_FE,
    ".co.nz": HTTP2_FE,
}
HTTP2_DEFAULT = HTTP2_EU

GQL_SMARTHOME_QUERY = """
query CustomerSmartHome {
    endpoints(
      endpointsQueryParams: { paginationParams: { disablePagination: true } }
    ) {
        items {
            id
            friendlyName
            model {
                type
                value {
                    text
                    locale
                }
            }
            dmsIdentifier {
                deviceType
                dsn
            }
            legacyAppliance {
                applianceId
                applianceTypes
                friendlyName
                friendlyDescription
                manufacturerName
                connectedVia
                modelName
                entityId
                aliases
                capabilities
                customerDefinedDeviceType
                alexaDeviceIdentifierList
                driverIdentity
                additionalApplianceDetails
            }
        }
    }
}
"""

# The original query, used when Amazon rejects the expanded query above.
GQL_SMARTHOME_QUERY_LEGACY = """
query CustomerSmartHome {
    endpoints(
      endpointsQueryParams: { paginationParams: { disablePagination: true } }
    ) {
        items {
            legacyAppliance {
                applianceId
                applianceTypes
                friendlyName
                friendlyDescription
                manufacturerName
                connectedVia
                modelName
                entityId
                aliases
                capabilities
                customerDefinedDeviceType
                alexaDeviceIdentifierList
                driverIdentity
            }
        }
    }
}
"""

# Smart-home endpoint mutations. They take the endpoint ``id`` of
# GQL_SMARTHOME_QUERY (amzn1.alexa.endpoint...), not the legacy applianceId.
GQL_SET_ENDPOINT_FRIENDLY_NAME = """
mutation SetEndpointFriendlyName($input: SetEndpointFriendlyNameInput!) {
    setEndpointFriendlyName(input: $input) {
        endpoint {
            id
            friendlyName
        }
    }
}
"""

GQL_SET_ENDPOINT_ENABLEMENT = """
mutation SetEndpointEnablement($input: SetEndpointEnablementInput!) {
    setEndpointEnablement(input: $input) {
        endpoint {
            id
            enablement
        }
        error {
            __typename
        }
    }
}
"""

GQL_FORGET_ENDPOINT = """
mutation ForgetEndpoint($input: ForgetEndpointInput!) {
    forgetEndpoint(forgetEndpointInput: $input) {
        endpointId
    }
}
"""

# Amazon Kids dashboard naming convention and marketplace exceptions.
PARENT_DASHBOARD_SUBDOMAIN_DEFAULT = "parents"
PARENT_DASHBOARD_SUBDOMAIN_EXCEPTIONS = {"amazon.de": "eltern"}
# A DNS timeout or resolver error does not prove the dashboard host is missing, so it
# is retried after this long. A definitive "no such host" answer is never retried.
PARENT_DASHBOARD_DNS_RETRY_SECONDS = 1800
