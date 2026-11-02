from typing import List, Union, Dict, Any
import json
from ....models.messages.meta_message_model.meta_base_notification_json import BaseMetaNotificationJson, NotificationType
from ....models.messages.meta_message_model.meta_message_json import MetaMessageJson
from ....models.messages.meta_message_model.meta_status_json import MetaStatusJson
from ....models.messages.meta_message_model.meta_error_json import MetaErrorJson
from ....models.messages.meta_message_model.meta_echo_json import MetaEchoJson
from ....models.messages.meta_message_model.meta_history_json import MetaHistoryJson
from ....models.messages.meta_message_model.meta_state_sync_json import MetaStateSyncJson
from ....models.messages.meta_message_model.meta_group_json import MetaGroupNotificationJson, MetaGroupLifecycleJson, MetaGroupParticipantsJson
from ....models.utils.custom_exceptions.custom_exceptions import UnknownMetaNotificationType, ImpossibleError

class MetaNotificationFactory:
    @staticmethod
    def _raw_change_field(data: Dict[str, Any]) -> Any:
        """The Change-level `field`, read from the RAW dict without a full model parse."""
        try:
            return data["entry"][0]["changes"][0]["field"]
        except (KeyError, IndexError, TypeError):
            return None

    @staticmethod
    def create(data: Dict[str, Any]) -> Union[MetaMessageJson, MetaStatusJson, MetaErrorJson, MetaEchoJson, MetaHistoryJson, MetaStateSyncJson, MetaGroupNotificationJson, MetaGroupLifecycleJson, MetaGroupParticipantsJson]:
        # WhatsApp Coexistence `history` backfill: route by the authoritative raw `field`
        # BEFORE the strict BaseMetaNotificationJson parse. A history envelope packs many
        # messages and MetaHistoryJson drops a single unparseable one (see its mode='before'
        # validator) so one odd message can't void the whole chunk; the eager strict base
        # parse here would raise for the whole envelope before that leniency can apply. The
        # live/status/error/echo/state_sync paths keep the strict parse below unchanged.
        raw_field = MetaNotificationFactory._raw_change_field(data)
        if raw_field == NotificationType.HISTORY.value:
            return MetaHistoryJson(**data)

        # WhatsApp Groups API: los 4 fields group_* rutean por raw field PRE-parse,
        # igual que history — el Value estricto no los modela y get_notification_type()
        # los mandaría a UNKNOWN → excepción → tormenta SQS. settings/status van al
        # modelo base (api-chatty solo los loguea en v1).
        if raw_field == NotificationType.GROUP_LIFECYCLE_UPDATE.value:
            return MetaGroupLifecycleJson(**data)
        if raw_field == NotificationType.GROUP_PARTICIPANTS_UPDATE.value:
            return MetaGroupParticipantsJson(**data)
        if raw_field in (NotificationType.GROUP_SETTINGS_UPDATE.value, NotificationType.GROUP_STATUS_UPDATE.value):
            return MetaGroupNotificationJson(**data)

        base_notification = BaseMetaNotificationJson(**data)
        notification_type: NotificationType = base_notification.get_notification_type()

        match notification_type:
            case NotificationType.MESSAGES:
                return MetaMessageJson(**data)
            case NotificationType.STATUSES:
                return MetaStatusJson(**data)
            case NotificationType.ERRORS:
                return MetaErrorJson(**data)
            case NotificationType.SMB_MESSAGE_ECHOES: # WhatsApp Coexistence: owner sent from the WhatsApp Business App
                return MetaEchoJson(**data)
            case NotificationType.HISTORY: # WhatsApp Coexistence: chunked backfill of the owner's prior WhatsApp Business App conversations
                return MetaHistoryJson(**data)
            case NotificationType.SMB_APP_STATE_SYNC: # WhatsApp Coexistence: the owner's WhatsApp Business App contacts/state
                return MetaStateSyncJson(**data)
            case NotificationType.UNKNOWN: # Tiene entry, object, changes y values. Pero no es Messages ni Statuses
                raise UnknownMetaNotificationType(message=f"Unknown notification type", json_data=json.dumps(data, indent=4))
            case _: # Es imposible que llegue a este caso
                raise ImpossibleError(f"MetaNotificationFactory logic error")