from zeep.cache import SqliteCache

# Tiempo de vida de la cache de WSDL de zeep, en segundos. Los WSDL de AFIP/ARCA son
# estables (cambian muy esporadicamente), por lo que cacheamos el documento en disco para
# evitar descargarlo y parsearlo desde los servidores de AFIP en cada instanciacion del cliente.
WSDL_CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 dias


def get_wsdl_cache(timeout=WSDL_CACHE_TIMEOUT, path=None):
    """ Devuelve una cache SQLite para los WSDL de zeep.

    Por defecto los clientes NO cachean (mantienen el comportamiento historico); es el
    consumidor quien debe construir la cache con este helper y pasarla via wsdl_cache.

    :param timeout: vigencia de la cache en segundos
    :param path: ruta del archivo SQLite; None usa el tempdir del sistema
    """
    return SqliteCache(path=path, timeout=timeout)


authorization_urls = dict(
    homologation='https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl',
    production='https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl',
)

service_urls = dict(
    wstesimbrefiscal_homologation='https://wsaduhomoext.afip.gob.ar/diav2/wgestimbrefiscalelectronico/wgestimbrefiscalelectronico.asmx?WSDL',
    wstesimbrefiscal_production='https://wswadu.afip.gob.ar/DIAV2/wgestimbrefiscalelectronico/wgestimbrefiscalelectronico.asmx?WSDL',
    wsct_homologation='https://fwshomo.afip.gov.ar/wsct/CTService?WSDL',
    wsct_production='https://serviciosjava.afip.gob.ar/wsct/CTService?WSDL',
    wsmtxca_homologation='https://fwshomo.afip.gov.ar/wsmtxca/services/MTXCAService?wsdl',
    wsmtxca_production='https://serviciosjava.afip.gob.ar/wsmtxca/services/MTXCAService?wsdl',
    wsbfev1_homologation='https://wswhomo.afip.gov.ar/wsbfev1/service.asmx?WSDL',
    wsbfev1_production='https://servicios1.afip.gov.ar/wsbfev1/service.asmx?WSDL',
    wsfev1_homologation='https://wswhomo.afip.gov.ar/wsfev1/service.asmx?wsdl',
    wsfev1_production='https://servicios1.afip.gov.ar/wsfev1/service.asmx?wsdl',
    wsfexv1_homologation='https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?wsdl',
    wsfexv1_production='https://servicios1.afip.gov.ar/wsfexv1/service.asmx?wsdl',
    ws_sr_padron_a5_homologation='https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL',
    ws_sr_padron_a5_production='https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL',
)
