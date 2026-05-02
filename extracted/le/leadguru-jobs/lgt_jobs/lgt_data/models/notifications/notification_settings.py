import copy
from lgt_jobs.lgt_data.models.base import DictionaryModel
from lgt_jobs.lgt_data.models.notifications.notification import (Notification, IncomingMessageNotification,
                                                                 InboxNotification, SourceDeactivationNotification,
                                                                 BillingNotifications, BulkRepliesNotification,
                                                                 BulkReactionsNotification, FollowUpNotification)


class NotificationSettings(DictionaryModel):
    def __init__(self):
        self.incoming_messages: IncomingMessageNotification | None = None
        self.inbox: InboxNotification | None = None
        self.source_deactivation: SourceDeactivationNotification | None = None
        self.billing: BillingNotifications | None = None
        self.bulk_replies: BulkRepliesNotification | None = None
        self.bulk_reactions: BulkReactionsNotification | None = None
        self.follow_ups: FollowUpNotification | None = None
        self.new_leads: bool | None = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model: NotificationSettings = cls()
        model.incoming_messages = IncomingMessageNotification.from_dic(dic.get('incoming_messages'))
        model.inbox = InboxNotification.from_dic(dic.get('inbox'))
        model.source_deactivation = SourceDeactivationNotification.from_dic(dic.get('source_deactivation'))
        model.billing = BillingNotifications.from_dic(dic.get('billing'))
        model.bulk_replies = BulkRepliesNotification.from_dic(dic.get('bulk_replies'))
        model.bulk_reactions = BulkReactionsNotification.from_dic(dic.get('bulk_reactions'))
        model.follow_ups = FollowUpNotification.from_dic(dic.get('follow_ups'))
        model.new_leads = dic.get('new_leads')
        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)

        if result.get('incoming_messages'):
            result['incoming_messages'] = Notification.to_dic(result.get('incoming_messages'))
        if result.get('inbox'):
            result['inbox'] = Notification.to_dic(result.get('inbox'))
        if result.get('source_deactivation'):
            result['source_deactivation'] = Notification.to_dic(result.get('source_deactivation'))
        if result.get('billing'):
            result['billing'] = Notification.to_dic(result.get('billing'))
        if result.get('bulk_replies'):
            result['bulk_replies'] = Notification.to_dic(result.get('bulk_replies'))
        if result.get('bulk_reactions'):
            result['bulk_reactions'] = Notification.to_dic(result.get('bulk_reactions'))
        if result.get('follow_ups'):
            result['follow_ups'] = Notification.to_dic(result.get('follow_ups'))

        return result
