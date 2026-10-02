import requests
import xml.etree.ElementTree as ET

URLS = dict(
    homologation='https://cot.test.arba.gov.ar',
    production='https://cot.arba.gov.ar',
)

class XmlResponseHandler(object):
    def handleResponse(self, response):
        xml = ET.fromstring(response.text)
        return self.handleXml(xml)
        
    def handleXml(self, xml):
        res = {}
        for child in xml.iter():
           if xml.tag != child.tag:
               if len(child):
                   res[child.tag] = self.handleXml(child)
               else: 
                   res[child.tag] = child.text        
        return res

class Configuracion(object):
    def __init__(self, user, password, tipo='homologation'):
        self.base_url = URLS[tipo]
        self.user = user
        self.password = password
        self.handler = XmlResponseHandler()

class ClienteHttp(Configuracion):
    def post(self, url, data=None, files=None):
        response = requests.post(f"{self.base_url}{url}", data=data, files=files)
        response.raise_for_status()
        try:
            return self.handler.handleResponse(response)
        except Exception:
            return {'tipoError': 'DATO', 'mensajeError': 'Se produjo un error al intentar leer el XML.'} 
