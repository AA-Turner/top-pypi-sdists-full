from ocsf.events.base import BaseEvent, CategoryId

from ocsf.objects.device import Device

from ocsf.objects.actor import Actor


class SystemActivity(BaseEvent):
    """
    The System Activity event is a generic event that defines a set of attributes
    available in the system activity events. As a generic event, it could be used to
    log events that are not otherwise defined by the System Activity category.
    """

    category_uid: CategoryId = CategoryId.System_Activity

    actor: Actor
    device: Device

