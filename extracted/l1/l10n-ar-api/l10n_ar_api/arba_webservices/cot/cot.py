# coding=utf-8

from .config import ClienteHttp

class ServicioCotArba(ClienteHttp):
    def __init__(self, user, password, tipo='homologation'):
        super().__init__(user, password, tipo)

    def presentar(self, filepath):
        with open(filepath, "rb") as archivo:
            file = {
                'file': (filepath, archivo, 'text/plain')
            }
            data = {
                "user": self.user,
                "password": self.password,
            }
            return self.post("/TransporteBienes/SeguridadCliente/presentarRemitos.do", files=file, data=data)
        

class CotRegistro(object):
    """
    Clase base para la generación de .txt según el diseño establecido por ARBA 
    https://www.arba.gov.ar/archivos/Publicaciones/nuevodiseniodearchivotxt.pdf
    """

    __slots__ = ['_tipoRegistro']

    def __init__(self, tipoRegistro):
        self._tipoRegistro = tipoRegistro 

    @property
    def tipoRegistro(self):
        return self._tipoRegistro

    def get_line_string(self):

        try:
            line_string = '|'.join(self.get_values())
        except TypeError:
            raise TypeError("La linea esta incompleta o es erronea")

        return line_string


    def get_values(self):
        raise NotImplementedError("Funcion get_registro no implementada para esta clase")


class CotHeader(CotRegistro):

    __slots__ = ['_cuitEmpresa']
     
    def __init__(self):
        super().__init__('01')
        self._cuitEmpresa = None

    @property
    def cuitEmpresa(self):
        return self._cuitEmpresa

    @cuitEmpresa.setter
    def cuitEmpresa(self, cuitEmpresa):
        self._cuitEmpresa = cuitEmpresa

    def get_values(self):
        return [self.tipoRegistro, self.cuitEmpresa]


class CotRemito(CotRegistro):

    __slots__ = ['_fechaEmision', '_codigoUnico', '_fechaSalidaTransporte', '_horaSalidaTransporte', '_sujetoGenerador', '_destinatarioConsumidorFinal',
                 '_destinatarioTipoDocumento', '_destinatarioDocumento', '_destinatarioCuit', '_destinatarioRazonSocial', '_destinatarioTenedor',
                 '_destinoDomicilioCalle', '_destinoDomicilioNumero', '_destinoDomicilioComple','_destinoDomicilioPiso', '_destinoDomicilioDto',
                 '_destinoDomicilioBarrio', '_destinoDomicilioCodigoPostal', '_destinoDomicilioLocalidad', '_destinoDomicilioProvincia', 
                 '_propioDestinoDomicilioCodigo','_entregaDomicilioOrigen', '_origenCuit', '_origenRazonSocial','_emisorTenedor', '_origenDomicilioCalle',
                 '_origenDomicilioNumero', '_origenDomicilioComple', '_origenDomicilioPiso', '_origenDomicilioDto', '_origenDomicilioBarrio',
                 '_origenDomicilioCodigoPostal', '_origenDomicilioLocalidad', '_origenDomicilioProvincia', '_transportistaCuit', '_tipoRecorrido', 
                 '_recorridoLocalidad', '_recorridoCalle', '_recorridoRuta', '_patenteVehiculo', '_patenteAcoplado', '_productoNoTermDev', '_importe']

    def __init__(self):
        super().__init__('02')
        self._fechaEmision = None
        self._codigoUnico = None 
        self._fechaSalidaTransporte = None
        self._horaSalidaTransporte = None
        self._sujetoGenerador = None
        self._destinatarioConsumidorFinal = None
        self._destinatarioTipoDocumento = None
        self._destinatarioDocumento = None
        self._destinatarioCuit = None
        self._destinatarioRazonSocial = None
        self._destinatarioTenedor = None
        self._destinoDomicilioCalle = None
        self._destinoDomicilioNumero = None
        self._destinoDomicilioComple = None
        self._destinoDomicilioPiso = None
        self._destinoDomicilioDto = None
        self._destinoDomicilioBarrio = None
        self._destinoDomicilioCodigoPostal = None
        self._destinoDomicilioLocalidad = None
        self._destinoDomicilioProvincia = None
        self._entregaDomicilioOrigen = None
        self._origenCuit = None
        self._origenRazonSocial = None
        self._emisorTenedor = None
        self._origenDomicilioCalle = None
        self._origenDomicilioNumero = None
        self._origenDomicilioComple = None
        self._origenDomicilioPiso = None
        self._origenDomicilioDto = None
        self._origenDomicilioBarrio = None
        self._origenDomicilioCodigoPostal = None
        self._origenDomicilioLocalidad = None
        self._origenDomicilioProvincia = None
        self._transportistaCuit = None
        self._tipoRecorrido = None
        self._recorridoLocalidad = None
        self._recorridoCalle = None
        self._recorridoRuta = None
        self._patenteVehiculo = None
        self._patenteAcoplado = None
        self._productoNoTermDev = None
        self._importe = None

    @property
    def fechaEmision(self):
        return self._fechaEmision

    @fechaEmision.setter
    def fechaEmision(self, fechaEmision):
        self._fechaEmision = fechaEmision

    @property
    def codigoUnico(self):
        return self._codigoUnico

    @codigoUnico.setter
    def codigoUnico(self, codigoUnico):
        self._codigoUnico = codigoUnico

    @property
    def fechaSalidaTransporte(self):
        return self._fechaSalidaTransporte

    @fechaSalidaTransporte.setter
    def fechaSalidaTransporte(self, fechaSalidaTransporte):
        self._fechaSalidaTransporte = fechaSalidaTransporte

    @property
    def horaSalidaTransporte(self):
        return self._horaSalidaTransporte

    @horaSalidaTransporte.setter
    def horaSalidaTransporte(self, horaSalidaTransporte):
        self._horaSalidaTransporte = horaSalidaTransporte

    @property
    def sujetoGenerador(self):
        return self._sujetoGenerador

    @sujetoGenerador.setter
    def sujetoGenerador(self, sujetoGenerador):
        self._sujetoGenerador = sujetoGenerador

    @property
    def destinatarioConsumidorFinal(self):
        return self._destinatarioConsumidorFinal

    @destinatarioConsumidorFinal.setter
    def destinatarioConsumidorFinal(self, destinatarioConsumidorFinal):
        self._destinatarioConsumidorFinal = destinatarioConsumidorFinal

    @property
    def destinatarioTipoDocumento(self):
        return self._destinatarioTipoDocumento

    @destinatarioTipoDocumento.setter
    def destinatarioTipoDocumento(self, destinatarioTipoDocumento):
        self._destinatarioTipoDocumento = destinatarioTipoDocumento

    @property
    def destinatarioDocumento(self):
        return self._destinatarioDocumento

    @destinatarioDocumento.setter
    def destinatarioDocumento(self, destinatarioDocumento):
        self._destinatarioDocumento = destinatarioDocumento

    @property
    def destinatarioCuit(self):
        return self._destinatarioCuit

    @destinatarioCuit.setter
    def destinatarioCuit(self, destinatarioCuit):
        self._destinatarioCuit = destinatarioCuit

    @property
    def destinatarioRazonSocial(self):
        return self._destinatarioRazonSocial

    @destinatarioRazonSocial.setter
    def destinatarioRazonSocial(self, destinatarioRazonSocial):
        self._destinatarioRazonSocial = destinatarioRazonSocial

    @property
    def destinatarioTenedor(self):
        return self._destinatarioTenedor

    @destinatarioTenedor.setter
    def destinatarioTenedor(self, destinatarioTenedor):
        self._destinatarioTenedor = destinatarioTenedor

    @property
    def destinoDomicilioCalle(self):
        return self._destinoDomicilioCalle

    @destinoDomicilioCalle.setter
    def destinoDomicilioCalle(self, destinoDomicilioCalle):
        self._destinoDomicilioCalle = destinoDomicilioCalle

    @property
    def destinoDomicilioNumero(self):
        return self._destinoDomicilioNumero

    @destinoDomicilioNumero.setter
    def destinoDomicilioNumero(self, destinoDomicilioNumero):
        self._destinoDomicilioNumero = destinoDomicilioNumero

    @property
    def destinoDomicilioComple(self):
        return self._destinoDomicilioComple

    @destinoDomicilioComple.setter
    def destinoDomicilioComple(self, destinoDomicilioComple):
        self._destinoDomicilioComple = destinoDomicilioComple

    @property
    def destinoDomicilioPiso(self):
        return self._destinoDomicilioPiso

    @destinoDomicilioPiso.setter
    def destinoDomicilioPiso(self, destinoDomicilioPiso):
        self._destinoDomicilioPiso = destinoDomicilioPiso

    @property
    def destinoDomicilioDto(self):
        return self._destinoDomicilioDto

    @destinoDomicilioDto.setter
    def destinoDomicilioDto(self, destinoDomicilioDto):
        self._destinoDomicilioDto = destinoDomicilioDto

    @property
    def destinoDomicilioBarrio(self):
        return self._destinoDomicilioBarrio

    @destinoDomicilioBarrio.setter
    def destinoDomicilioBarrio(self, destinoDomicilioBarrio):
        self._destinoDomicilioBarrio = destinoDomicilioBarrio

    @property
    def destinoDomicilioCodigoPostal(self):
        return self._destinoDomicilioCodigoPostal

    @destinoDomicilioCodigoPostal.setter
    def destinoDomicilioCodigoPostal(self, destinoDomicilioCodigoPostal):
        self._destinoDomicilioCodigoPostal = destinoDomicilioCodigoPostal

    @property
    def destinoDomicilioLocalidad(self):
        return self._destinoDomicilioLocalidad

    @destinoDomicilioLocalidad.setter
    def destinoDomicilioLocalidad(self, destinoDomicilioLocalidad):
        self._destinoDomicilioLocalidad = destinoDomicilioLocalidad

    @property
    def destinoDomicilioProvincia(self):
        return self._destinoDomicilioProvincia

    @destinoDomicilioProvincia.setter
    def destinoDomicilioProvincia(self, destinoDomicilioProvincia):
        self._destinoDomicilioProvincia = destinoDomicilioProvincia

    @property
    def propioDestinoDomicilioCodigo(self):
        return self._propioDestinoDomicilioCodigo

    @propioDestinoDomicilioCodigo.setter
    def propioDestinoDomicilioCodigo(self, propioDestinoDomicilioCodigo):
        self._propioDestinoDomicilioCodigo = propioDestinoDomicilioCodigo

    @property
    def entregaDomicilioOrigen(self):
        return self._entregaDomicilioOrigen

    @entregaDomicilioOrigen.setter
    def entregaDomicilioOrigen(self, entregaDomicilioOrigen):
        self._entregaDomicilioOrigen = entregaDomicilioOrigen

    @property
    def origenCuit(self):
        return self._origenCuit

    @origenCuit.setter
    def origenCuit(self, origenCuit):
        self._origenCuit = origenCuit

    @property
    def origenRazonSocial(self):
        return self._origenRazonSocial

    @origenRazonSocial.setter
    def origenRazonSocial(self, origenRazonSocial):
        self._origenRazonSocial = origenRazonSocial

    @property
    def emisorTenedor(self):
        return self._emisorTenedor

    @emisorTenedor.setter
    def emisorTenedor(self, emisorTenedor):
        self._emisorTenedor = emisorTenedor

    @property
    def origenDomicilioCalle(self):
        return self._origenDomicilioCalle

    @origenDomicilioCalle.setter
    def origenDomicilioCalle(self, origenDomicilioCalle):
        self._origenDomicilioCalle = origenDomicilioCalle

    @property
    def origenDomicilioNumero(self):
        return self._origenDomicilioNumero

    @origenDomicilioNumero.setter
    def origenDomicilioNumero(self, origenDomicilioNumero):
        self._origenDomicilioNumero = origenDomicilioNumero

    @property
    def origenDomicilioComple(self):
        return self._origenDomicilioComple

    @origenDomicilioComple.setter
    def origenDomicilioComple(self, origenDomicilioComple):
        self._origenDomicilioComple = origenDomicilioComple

    @property
    def origenDomicilioPiso(self):
        return self._origenDomicilioPiso

    @origenDomicilioPiso.setter
    def origenDomicilioPiso(self, origenDomicilioPiso):
        self._origenDomicilioPiso = origenDomicilioPiso

    @property
    def origenDomicilioDto(self):
        return self._origenDomicilioDto

    @origenDomicilioDto.setter
    def origenDomicilioDto(self, origenDomicilioDto):
        self._origenDomicilioDto = origenDomicilioDto

    @property
    def origenDomicilioBarrio(self):
        return self._origenDomicilioBarrio

    @origenDomicilioBarrio.setter
    def origenDomicilioBarrio(self, origenDomicilioBarrio):
        self._origenDomicilioBarrio = origenDomicilioBarrio

    @property
    def origenDomicilioCodigoPostal(self):
        return self._origenDomicilioCodigoPostal

    @origenDomicilioCodigoPostal.setter
    def origenDomicilioCodigoPostal(self, origenDomicilioCodigoPostal):
        self._origenDomicilioCodigoPostal = origenDomicilioCodigoPostal

    @property
    def origenDomicilioLocalidad(self):
        return self._origenDomicilioLocalidad

    @origenDomicilioLocalidad.setter
    def origenDomicilioLocalidad(self, origenDomicilioLocalidad):
        self._origenDomicilioLocalidad = origenDomicilioLocalidad

    @property
    def origenDomicilioProvincia(self):
        return self._origenDomicilioProvincia

    @origenDomicilioProvincia.setter
    def origenDomicilioProvincia(self, origenDomicilioProvincia):
        self._origenDomicilioProvincia = origenDomicilioProvincia

    @property
    def transportistaCuit(self):
        return self._transportistaCuit

    @transportistaCuit.setter
    def transportistaCuit(self, transportistaCuit):
        self._transportistaCuit = transportistaCuit

    @property
    def tipoRecorrido(self):
        return self._tipoRecorrido

    @tipoRecorrido.setter
    def tipoRecorrido(self, tipoRecorrido):
        self._tipoRecorrido = tipoRecorrido

    @property
    def recorridoLocalidad(self):
        return self._recorridoLocalidad

    @recorridoLocalidad.setter
    def recorridoLocalidad(self, recorridoLocalidad):
        self._recorridoLocalidad = recorridoLocalidad

    @property
    def recorridoCalle(self):
        return self._recorridoCalle

    @recorridoCalle.setter
    def recorridoCalle(self, recorridoCalle):
        self._recorridoCalle = recorridoCalle

    @property
    def recorridoRuta(self):
        return self._recorridoRuta

    @recorridoRuta.setter
    def recorridoRuta(self, recorridoRuta):
        self._recorridoRuta = recorridoRuta

    @property
    def patenteVehiculo(self):
        return self._patenteVehiculo

    @patenteVehiculo.setter
    def patenteVehiculo(self, value):
        self._patenteVehiculo = value

    @property
    def patenteAcoplado(self):
        return self._patenteAcoplado

    @patenteAcoplado.setter
    def patenteAcoplado(self, patenteAcoplado):
        self._patenteAcoplado = patenteAcoplado

    @property
    def productoNoTermDev(self):
        return self._productoNoTermDev

    @productoNoTermDev.setter
    def productoNoTermDev(self, productoNoTermDev):
        self._productoNoTermDev = productoNoTermDev

    @property
    def importe(self):
        return self._importe

    @importe.setter
    def importe(self, importe):
        self._importe = importe

    def get_values(self):
        return [
            self.tipoRegistro,
            self.fechaEmision,
            self.codigoUnico,
            self.fechaSalidaTransporte,
            self.horaSalidaTransporte,
            self.sujetoGenerador,
            self.destinatarioConsumidorFinal,
            self.destinatarioTipoDocumento,
            self.destinatarioDocumento,
            self.destinatarioCuit,
            self.destinatarioRazonSocial,
            self.destinatarioTenedor,
            self.destinoDomicilioCalle,
            self.destinoDomicilioNumero,
            self.destinoDomicilioComple,
            self.destinoDomicilioPiso,
            self.destinoDomicilioDto,
            self.destinoDomicilioBarrio,
            self.destinoDomicilioCodigoPostal,
            self.destinoDomicilioLocalidad,
            self.destinoDomicilioProvincia,
            self.propioDestinoDomicilioCodigo,
            self.entregaDomicilioOrigen,
            self.origenCuit,
            self.origenRazonSocial,
            self.emisorTenedor,
            self.origenDomicilioCalle,
            self.origenDomicilioNumero,
            self.origenDomicilioComple,
            self.origenDomicilioPiso,
            self.origenDomicilioDto,
            self.origenDomicilioBarrio,
            self.origenDomicilioCodigoPostal,
            self.origenDomicilioLocalidad,
            self.origenDomicilioProvincia,
            self.transportistaCuit,
            self.tipoRecorrido,
            self.recorridoLocalidad,
            self.recorridoCalle,
            self.recorridoRuta,
            self.patenteVehiculo,
            self.patenteAcoplado,
            self.productoNoTermDev,
            self.importe
        ]

class CotProducto(CotRegistro):
    __slots__ = ['_codigoUnicoProducto', '_arbaCodigoUnidadMedida', '_cantidad', '_propioCodigoProducto', '_propioDescripcionProducto',
                 '_propioDescripcionUnidadMedida', '_cantidadAjustada']
    def __init__(self):
        super().__init__('03')
        self._codigoUnicoProducto = None
        self._arbaCodigoUnidadMedida = None
        self._cantidad = None
        self._propioCodigoProducto = None
        self._propioDescripcionProducto = None
        self._propioDescripcionUnidadMedida = None
        self._cantidadAjustada = None

    @property
    def codigoUnicoProducto(self):
        return self._codigoUnicoProducto

    @codigoUnicoProducto.setter 
    def codigoUnicoProducto(self, codigoUnicoProducto):
        self._codigoUnicoProducto = codigoUnicoProducto

    @property
    def arbaCodigoUnidadMedida(self):
        return self._arbaCodigoUnidadMedida

    @arbaCodigoUnidadMedida.setter 
    def arbaCodigoUnidadMedida(self, arbaCodigoUnidadMedida):
        self._arbaCodigoUnidadMedida = arbaCodigoUnidadMedida

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        self._cantidad = cantidad

    @property
    def propioCodigoProducto(self):
        return self._propioCodigoProducto

    @propioCodigoProducto.setter 
    def propioCodigoProducto(self, propioCodigoProducto):
        self._propioCodigoProducto = propioCodigoProducto

    @property
    def propioDescripcionProducto(self):
        return self._propioDescripcionProducto

    @propioDescripcionProducto.setter 
    def propioDescripcionProducto(self, propioDescripcionProducto):
        self._propioDescripcionProducto = propioDescripcionProducto[:40]

    @property
    def propioDescripcionUnidadMedida(self):
        return self._propioDescripcionUnidadMedida

    @propioDescripcionUnidadMedida.setter
    def propioDescripcionUnidadMedida(self, propioDescripcionUnidadMedida):
        self._propioDescripcionUnidadMedida = propioDescripcionUnidadMedida

    @property
    def cantidadAjustada(self):
        return self._cantidadAjustada
    
    @cantidadAjustada.setter
    def cantidadAjustada(self, cantidadAjustada):
        self._cantidadAjustada = cantidadAjustada 

    def get_values(self):
        return [
            self.tipoRegistro,
            self.codigoUnicoProducto,
            self.arbaCodigoUnidadMedida,
            self.cantidad,
            self.propioCodigoProducto,
            self.propioDescripcionProducto,
            self.propioDescripcionUnidadMedida,
            self.cantidadAjustada
        ]


class CotFooter(CotRegistro):
    __slots__ = ['_cantidadTotalRemitos']
    def __init__(self):
        super().__init__('04')
        self._cantidadTotalRemitos = None

    @property
    def cantidadTotalRemitos(self):
        return self._cantidadTotalRemitos
    
    @cantidadTotalRemitos.setter
    def cantidadTotalRemitos(self, cantidadTotalRemitos):
        self._cantidadTotalRemitos = cantidadTotalRemitos

    def get_values(self):
        return [
            self.tipoRegistro,
            self.cantidadTotalRemitos
        ]

class GeneradorArchivoCot:
    def __init__(self):
        self.registros = []

    def agregar_registro(self, registro):
        self.registros.append(registro)

    def generar_archivo(self, name=''):
        contenido = ""
        for registro in self.registros:
            contenido += registro.get_line_string() + "\n"
        with open(f'/tmp/{name}.txt', "w") as archivo:
            archivo.write(contenido)
            return archivo 


