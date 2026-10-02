# -*- coding: utf-8 -*-
class AfipError:
    
    @classmethod
    def parse_error(cls, error):
        return Exception("Error {}: {}".format(
            error.Errores.ErrorEjecucion[0].Codigo,
            error.Errores.ErrorEjecucion[0].Descripcion.encode('latin-1')),
        )
