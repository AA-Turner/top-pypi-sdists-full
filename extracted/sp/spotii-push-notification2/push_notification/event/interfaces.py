from push_notification.event.models import Event


def emit_event(event_type, object_type, object_id, account_id=None, **kwargs):
    return Event.objects.create(
        event_type=event_type,
        object_type=object_type,
        object_id=object_id,
        account_id=account_id,
        **kwargs,
    )
