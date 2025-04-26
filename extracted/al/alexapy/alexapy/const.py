"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Constants.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"

CALL_VERSION = "2.2.556530.0"
APP_NAME = "Alexa Media Player"
USER_AGENT = f"AmazonWebView/Amazon Alexa/{CALL_VERSION}/iOS/16.6/iPhone"
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
