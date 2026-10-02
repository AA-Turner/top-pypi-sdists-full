# -*- coding: utf-8 -*-


class AfipServiceError(Exception):
    """Error devuelto por un servicio de ARCA con codigo y mensaje."""

    def __init__(self, code, message):
        self.code = code
        self.afip_message = message
        super().__init__("Error {}: {}".format(code, message))


class AfipError:

    @classmethod
    def parse_error(cls, error):
        code = error.Errors.Err[0].Code
        msg = error.Errors.Err[0].Msg
        if isinstance(msg, bytes):
            msg = msg.decode('latin-1')
        return AfipServiceError(code, msg)

    @classmethod
    def parse_errors(cls, error):
        """Parsea todos los errores del response, no solo el primero."""
        errors = []
        for err in error.Errors.Err:
            msg = err.Msg
            if isinstance(msg, bytes):
                msg = msg.decode('latin-1')
            errors.append(AfipServiceError(err.Code, msg))
        return errors
