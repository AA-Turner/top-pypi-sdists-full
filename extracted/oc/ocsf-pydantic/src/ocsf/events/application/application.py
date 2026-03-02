from ocsf.events.base import BaseEvent, CategoryId

class Application(BaseEvent):
    category_uid: CategoryId = CategoryId.Application_Activity
