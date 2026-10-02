# -*- coding: utf-8 -*-
from zeep import Client, helpers

from .error import AfipError
from l10n_ar_api.afip_webservices import config

class Wgestimbrefiscal(object):
    def __init__(self, access_token, cuit, tipo_agente, rol, homologation=True, url=None):
        if not url:
            self.url = config.service_urls.get('wstesimbrefiscal_homologation') if homologation\
                else config.service_urls.get('wstesimbrefiscal_production')
        else:
            self.url = url

        self.accessToken = access_token
        self.cuit = cuit
        self.tipo_agente = tipo_agente
        self.rol = rol
        self.argWSAutenticacionEmpresa = self._create_auth_request()

        #details
        self.CuitEmpresa = False
        self.CodigoAduana = False
        self.Destinacion = False

    def fill_details(self, cuitempresa, codigoaduana, destination):
        self.CuitEmpresa = cuitempresa
        self.CodigoAduana = codigoaduana
        self.Destinacion = destination

    def check_webservice_status(self):
        """ Consulta el estado de los webservices de AFIP."""

        res = Client(self.url).service.Dummy()

        if res.Errores != None:
            raise AfipError.parse_error(res)
        if res.Resultado.AppServer != 'OK':
            raise Exception('El servidor de aplicaciones no se encuentra disponible. Intente mas tarde.')
        if res.Resultado.DbServer != 'OK':
            raise Exception('El servidor de base de datos no se encuentra disponible. Intente mas tarde.')
        if res.Resultado.AuthServer != 'OK':
            raise Exception('El servidor de auntenticacion no se encuentra disponible. Intente mas tarde.')


    def _create_auth_request(self):
        argWSAutenticacionEmpresa = {
            'Token': self.accessToken.token,
            'Sign': self.accessToken.sign,
            'CuitEmpresaConectada': self.cuit,
            'TipoAgente': self.tipo_agente,
            'Rol': self.rol,
        }
        return argWSAutenticacionEmpresa

    def retrieve_seals(self, avals):
        sample = [{
            'Item': 1,
            'Subitem': 0,
            'PosicionArancelaria': '8517.12.11',
            'Marca': 'Apple',
            'Modelo': 'iPhone 13 Pro',
            'CodigoGS1': '80898',
            'IdTipoProducto': 1,
            'TimbreTIFE': [
                {'IdentificadorUnico': '010928/00/3890', 'NumeroSerie': 'G7TZL374N81B'},
                {'IdentificadorUnico': '010928/00/38902', 'NumeroSerie': 'G7TZL348N81B'}]
            },{
            'Item': 2,
            'Subitem': 0,
            'PosicionArancelaria': '8517.12.11',
            'Marca': 'Apple',
            'Modelo': 'iPhone 13 Pro MAX',
            'CodigoGS1': '80898',
            'IdTipoProducto': 1,
            'TimbreTIFE': [
                {'IdentificadorUnico': '010928/00/3890', 'NumeroSerie': 'G7TZL374N81B'},
                {'IdentificadorUnico': '010928/00/38902', 'NumeroSerie': 'G7TZL348N81B'}]
            }
        ]

        #print (avals)
        ItemSubitemTIFE = list()
        for vals in avals:
            TimbreTIFE = list()
            _TimbreTIFE = Client(self.url).get_type('ns0:TimbreTIFE')
            for val in vals['TimbreTIFE']:
                TimbreTIFE.append(_TimbreTIFE(
                    IdentificadorUnico=val['IdentificadorUnico'],
                    NumeroSerie=val['NumeroSerie']
                ))

            _ListaTimbres = Client(self.url).get_type('ns0:ArrayOfTimbreTIFE')
            ListaTimbres = _ListaTimbres(
                TimbreTIFE=TimbreTIFE
            )
            _ItemSubitemTIFE = Client(self.url).get_type('ns0:ItemSubitemTIFE')
            ItemSubitemTIFE.append(_ItemSubitemTIFE(
                Item=vals['Item'],
                Subitem=vals['Subitem'],
                PosicionArancelaria=vals['PosicionArancelaria'],
                Marca=vals['Marca'],
                Modelo=vals['Modelo'],
                CodigoGS1=vals['CodigoGS1'],
                IdTipoProducto=vals['IdTipoProducto'],
                ListaTimbres=ListaTimbres
            ))
        self.ItemSubitemTIFE = ItemSubitemTIFE

        _ListaItemsSubitems = Client(self.url).get_type('ns0:ArrayOfItemSubitemTIFE')
        ListaItemsSubitems = _ListaItemsSubitems(
            ItemSubitemTIFE=self.ItemSubitemTIFE
        )
        self.ListaItemsSubitems = ListaItemsSubitems


        _argDestinacionTIFE = Client(self.url).get_type('ns0:DestinacionTIFE')
        argDestinacionTIFE = _argDestinacionTIFE(
            CuitEmpresa=self.CuitEmpresa,
            CodigoAduana=self.CodigoAduana,
            Destinacion=self.Destinacion,
            ListaItemsSubitems=self.ListaItemsSubitems
        )

        #----------DEBUG--------------
        from lxml import etree as ET
        client = Client(self.url)
        node = client.create_message(client.service, 'RegistrarTimbradoFiscalElectDest',
            argWSAutenticacionEmpresa=self.argWSAutenticacionEmpresa,
            argDestinacionTIFE=argDestinacionTIFE)
        tree = ET.ElementTree(node)
        tree.write('/tmp/test.xml', pretty_print=True)



        seals_details = Client(self.url).service.RegistrarTimbradoFiscalElectDest(
            argWSAutenticacionEmpresa=self.argWSAutenticacionEmpresa,
            argDestinacionTIFE=argDestinacionTIFE
        )
        if seals_details.Errores != None:
            raise AfipError().parse_error(seals_details)

        res = helpers.serialize_object(seals_details)
        req = helpers.serialize_object(argDestinacionTIFE)
        return res, req
