import certifi
from zeep import Client
from requests import Session
from zeep.transports import Transport
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

from l10n_ar_api.afip_webservices import config

# Exclude DH ciphers to avoid "dh key too small" errors with AFIP servers
AFIP_CIPHERS = "DEFAULT:!DH"


class AfipHTTPAdapter(HTTPAdapter):
    """ An adapter to block DH ciphers which may not work for *.afip.gov.ar """

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=AFIP_CIPHERS)
        context.load_verify_locations(certifi.where())
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)


class Wsaa(object):

    def __init__(self, homologation=True, url=None, wsdl_cache=None):

        if not url:
            self.url = config.authorization_urls.get('homologation') if homologation\
                else config.authorization_urls.get('production')
        else:
            self.url = url

        self.wsdl_cache = wsdl_cache

    def login(self, tra):
        """
        :param tra: TRA que se usara para el logeo
        :return: XML con el login autorizado
        """

        try:
            session = Session()
            session.mount('https://', AfipHTTPAdapter())
            transport = Transport(session=session, cache=self.wsdl_cache)
            login_fault = Client(self.url, transport=transport).service.loginCms(tra)
        except Exception as e:
            raise Exception("Error al autenticarse\n{}".format(e))

        return login_fault
