from typing import List, Union, Dict, Any
import json
from ....models.messages.meta_message_model.meta_base_notification_json import BaseMetaNotificationJson, NotificationType
from ....models.messages.meta_message_model.meta_message_json import MetaMessageJson
from ....models.messages.meta_message_model.meta_status_json import MetaStatusJson
from ....models.messages.meta_message_model.meta_error_json import MetaErrorJson
from ....models.utils.custom_exceptions.custom_exceptions import UnknownMetaNotificationType, ImpossibleError

class MetaNotificationFactory:
    @staticmethod
    def create(data: Dict[str, Any]) -> Union[MetaMessageJson, MetaStatusJson, MetaErrorJson]:
        base_notification = BaseMetaNotificationJson(**data) 
        notification_type: NotificationType = base_notification.get_notification_type()
        
        match notification_type:
            case NotificationType.MESSAGES:
                return MetaMessageJson(**data)
            case NotificationType.STATUSES:
                return MetaStatusJson(**data)
            case NotificationType.ERRORS: 
                return MetaErrorJson(**data)
            case NotificationType.UNKNOWN: # Tiene entry, object, changes y values. Pero no es Messages ni Statuses
                raise UnknownMetaNotificationType(message=f"Unknown notification type", json_data=json.dumps(data, indent=4))
            case _: # Es imposible que llegue a este caso
                raise ImpossibleError(f"MetaNotificationFactory logic error")