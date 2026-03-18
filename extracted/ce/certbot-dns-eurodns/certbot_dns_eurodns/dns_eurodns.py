"""EuroDNS Certbot plugins.

For full examples, see `certbot.plugins`.

"""

import logging
import re

import requests
import json
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

# Documentation URL to show on error
ACCOUNT_URL = 'https://docapi.eurodns.com/'
DEFAULT_ENDPOINT = 'https://rest-api.eurodns.com/dns-zones/'

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """Certbot Authenticator for EuroDNS."""

    description = "Certbot Authenticator plugin for EuroDNS"

    # Implement all methods from IAuthenticator, remembering to add
    # "self" as first argument, e.g. def prepare(self)...
    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=30)
        add(
            "credentials",
            help="EuroDNS credentials INI file.",
            default="/etc/letsencrypt/eurodns.ini",
        )

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS CNAME record to respond to a dns-01 challenge using "
            + "the EuroDNS Remote REST API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'EuroDNS credentials INI file',
            {
                "applicationId": "User access for EuroDNS v2 API. (See {0}.)" . format(ACCOUNT_URL),
                "apiKey": "Key access for EuroDNS v2 API. (See {0}.)" . format(ACCOUNT_URL)
            }
        )
        if self.credentials.conf("endpoint"):
            logger.debug("endpoint: " + self.credentials.conf("endpoint"))
        logger.debug("appId: " + self.credentials.conf("applicationId"))
        logger.debug("apiKey: " + self.credentials.conf("apiKey"))

    def _perform(self, domain, validation_name, validation):
        logger.debug("domain: "+domain)
        logger.debug("validation_name: " + validation_name)
        logger.debug("validation: " + validation)
        clientRestAPI = self._get_RESTAPIconfig_client()
        clientRestAPI.addRecord(domain, validation_name, validation)
        return (
            "This plugin configures a DNS CNAME record to respond to a dns-01 challenge using "
            + "the EuroDNS Remote REST API."
        )

    def _cleanup(self, domain, validation_name, validation):
        clientRestAPI = self._get_RESTAPIconfig_client()
        clientRestAPI.delRecord(domain, validation_name, validation)
        return (
            "This plugin configures a DNS CNAME record to respond to a dns-01 challenge using "
            + "the EuroDNS Remote REST API."
        )

    def _getEndPoint(self):
        if not self.credentials.conf("endpoint"):
            endPoint = DEFAULT_ENDPOINT
        else:
            endPoint = self.credentials.conf("endpoint")
        return endPoint

    def _get_RESTAPIconfig_client(self):

        return _RESTAPIConfigClient(
            self._getEndPoint(),
            self.credentials.conf("applicationId"),
            self.credentials.conf("apiKey"),
        )

class _RESTAPIConfigClient(object):
    """
    Encapsulates all communication with the EuroDNS Remote REST API.
    """
    ttl = 600 # minimum valid value for EuroDNS
    type = 'TXT'

    def __init__(self, endpoint, appId, apiKey):
        logger.debug("creating RESTAPIconfigclient")
        self.endpoint = endpoint
        self.authinfo = {"X-APP-ID": appId, "X-API-KEY": apiKey}

    def addRecord(self, domain, validation_name, validation):
        logger.debug('addRecord call')

        # If it is a certificate for a subdomain we must try to find the domain name in DNS

        realDomain, zoneJSON = self._getRealDomain(domain)
        logger.debug('Real Domain: ' + realDomain)

        # EuroDNS DNS API requires only the subdomain part of the domain:

        host = self._getHost(realDomain, validation_name)
        logger.debug('Host: ' + host)

        zoneJSON = self._getZone(realDomain)
        zoneJSON['records'].append({
                        'type': self.type,
                        'host': host,
                        'ttl': self.ttl,
                        'rdata': validation
                         })
        zoneJSONCheck = self._prepZone(realDomain, zoneJSON)
        logger.debug(zoneJSONCheck)
        if (zoneJSONCheck['report']['isValid'] is False):
            logger.debug('zone is not valid to addRecord')
            raise errors.PluginError(
                "EuroDNS API Error during addRecord: {0}".format(zoneJSONCheck['report']['recordErrors'][0]['messages'])
            )
        logger.debug('addRecord ok')
        self._setZone(realDomain, zoneJSON)


    def delRecord(self, domain, validation_name, validation):
        logger.debug('delRecord call')

        # If it is a certificate for a subdomain we must try to find the domain name in DNS

        realDomain, zoneJSON = self._getRealDomain(domain)
        logger.debug('Real Domain: ' + realDomain)

        # EuroDNS DNS API requires only the subdomain part of the domain:

        host = self._getHost(realDomain, validation_name)
        logger.debug('Host: ' + host)

        zoneJSON['records'] = list(filter(
            lambda record: record['type'] != self.type or record['host'] != host or record['ttl'] != self.ttl or record[
                'rdata'] != validation, zoneJSON['records']))
        #logger.debug(json.dumps(zoneJSON))
        zoneJSONCheck = self._prepZone(realDomain, zoneJSON)

        if zoneJSONCheck['report']['isValid'] is False:
            logger.debug('zone is not valid to delRecord')
            raise errors.PluginError(
                "EuroDNS API Error during delRecord: {0}".format(zoneJSONCheck['report']['recordErrors'][0]['messages'])
            )

        logger.debug('delRecord ok')
        self._setZone(realDomain, zoneJSON)

    def _getZone(self, domain):
        logger.debug('getZone call')

        resp = requests.get(self.endpoint + domain, headers=self.authinfo)
        if resp.status_code != 200:
            respJson = resp.json()
            raise errors.PluginError(
                "EuroDNS API Error during _getZone: {0}".format(respJson['errors'][0]['title'])
            )

        logger.debug('getZone ok')
        #logger.debug(json.dumps(resp.json()))
        return resp.json()

    def _prepZone(self, domain, zone):
        logger.debug('prepZone call')
        #logger.debug(json.dumps(zone))
        resp = requests.post(self.endpoint + domain + '/check', json.dumps(zone), headers=self.authinfo)

        if resp.status_code != 200:
            respJson = resp.json()
            raise errors.PluginError(
                "EuroDNS API Error during _prepZone: {0}".format(respJson['errors'][0]['title'])
            )

        logger.debug('prepZone ok')
        #logger.debug(json.dumps(resp.json()))
        return resp.json()

    def _setZone(self, domain, zone):
        logger.debug('_setZone call')
        #logger.debug(json.dumps(zone))
        resp = requests.put(self.endpoint + domain, json.dumps(zone), headers=self.authinfo)

        if resp.status_code != 204:
            respJson = resp.json()
            raise errors.PluginError(
                "EuroDNS API Error during _setZone {0}".format(respJson['errors'][0]['title'])
            )
        logger.debug('setZone ok')

    def _getHost(self, domain, validation_name):
        host = re.sub(r"{0}$".format(domain), "", validation_name)
        #if it is a wildcard we remove *
        host = re.sub(r"\\*", "", host)
        return re.sub(r"\.$", "", host)

    def _getRealDomain(self, domain):
        # if it is a subdomain we must try to find its base domain in DNS
        domain_guesses = dns_common.base_domain_name_guesses(domain)
        found = False
        for domain_guess in domain_guesses:
            resp = requests.get(self.endpoint + domain_guess, headers=self.authinfo)
            respJson = resp.json()
            if resp.status_code == 200:
                return domain_guess, respJson
                break
        raise errors.PluginError(
            "EuroDNS API Failed to find domain {0} (Does your account have have access to this domain?)".format(
                domain
            )
        )
