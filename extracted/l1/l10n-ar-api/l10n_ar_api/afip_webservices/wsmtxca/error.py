# -*- coding: utf-8 -*-


class AfipError:

    @classmethod
    def parse_error(cls, response):
        """ Arma una excepcion legible a partir del arrayErrores devuelto por WSMTXCA.

        WSMTXCA devuelve los errores en response.arrayErrores.codigoDescripcion, una lista de
        elementos con los campos codigo y descripcion.
        """
        errores = response.arrayErrores.codigoDescripcion
        codigo = errores[0].codigo
        descripcion = errores[0].descripcion
        if isinstance(descripcion, bytes):
            descripcion = descripcion.decode('latin-1')
        return Exception("Error {}: {}".format(codigo, descripcion))
