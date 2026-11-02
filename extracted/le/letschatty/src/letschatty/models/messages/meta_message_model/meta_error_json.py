from typing import Optional, Dict
from .meta_base_notification_json import BaseMetaNotificationJson
from .schema.values.value_errors import ERROR_CODE_DETAILS

class MetaErrorJson(BaseMetaNotificationJson):
    pass

    def get_error_details(self, code: int) -> Optional[Dict[str, str]]:
        """
        Obtiene los detalles del error basándose en el código de error.
        
        :param code: Código de error entero.
        :return: Diccionario con 'description', 'solution' y 'http_status' si el código existe, de lo contrario None.
        """
        return ERROR_CODE_DETAILS.get(code)

