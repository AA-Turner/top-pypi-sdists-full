# -*- coding: utf-8 -*-
class AfipError:
    
    @classmethod
    def parse_error(cls, error):
        return Exception("Error {}: {}".format(
            error.arrayErrores.codigoDescripcion[0].codigo,
            error.arrayErrores.codigoDescripcion[0].descripcion.encode('utf-8')),
        )
