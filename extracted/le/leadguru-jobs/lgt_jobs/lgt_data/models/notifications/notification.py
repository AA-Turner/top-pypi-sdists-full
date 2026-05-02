from datetime import datetime, UTC, timedelta

from lgt_jobs.env import portal_url
from lgt_jobs.lgt_data.enums import NotificationType
from lgt_jobs.lgt_data.models.base import DictionaryModel
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.post.post import Post
from lgt_jobs.lgt_data.models.user_leads.extended_user_lead import ExtendedUserLeadModel
from lgt_jobs.lgt_data.models.user_leads.user_lead import UserLeadModel


class Notification(DictionaryModel):
    def __init__(self):
        self.enabled: bool = True
        self.type: NotificationType = NotificationType.INSTANTLY
        self.day: int | None = None
        self.hour: int | None = None
        self.minute: int | None = None
        self.last_notification: datetime | None = None
        self.need_to_notify: bool = False
        self.attributes: list = []

    @property
    def need_to_notify_now(self) -> bool:
        if not self.enabled or not self.need_to_notify:
            return False

        now = datetime.now(UTC)
        current_week_day = datetime.isoweekday(now)
        if self.last_notification:
            self.last_notification = self.last_notification.replace(tzinfo=UTC)

        if (self.type == NotificationType.UNREAD_FOR_FEW_MINUTES
                and self.last_notification and (now.minute - self.minute <= self.last_notification.minute)):
            return False

        if self.type == NotificationType.ONCE_A_WEEK and current_week_day != self.day:
            return False

        if ((self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK)
                and (now.hour != self.hour or now.minute < self.minute)):
            return False

        if ((self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK)
                and self.last_notification and self.last_notification > now - timedelta(hours=1)):
            return False

        return True

    @staticmethod
    def need_to_notify_week_before(date: datetime) -> bool:
        return datetime.now(UTC) < (date + timedelta(7))

    @staticmethod
    def get_name(user) -> str:
        if user.get('name'):
            return user['name']
        elif user.get('display_name'):
            return user['display_name']
        elif user.get('real_name'):
            return user['real_name']
        return ''


class IncomingMessageNotification(Notification):
    other_leads_text = ' and other leads.'

    name_html_item = '''
        <div style="display: inline-block; padding-left: 2px;  line-height: 32px" class="lead_names">
            <img alt="Lead Photo" src="$$USER_IMAGE$$" width="24" height="24"
                    style="background-color: #FFFFFE !important; display: inline-block; vertical-align: top; width: 24px; 
                    max-width: 24px; min-width: 24px; font-family: 'Outfit', Helvetica, Arial, sans-serif; color: #FFFFFE; 
                    border-radius: 50% !important; font-size: 16px;" border="0">
                    <span style="font-weight: 600;">$$USER_NAME$$</span>
        </div>
        '''
    view_message_html_item = '''
        <td align="right" class="pr-text-dark" style="width: 100%">
            <a href="$$VIEW_MESSAGE_URL$$" target="_blank"style="color: #3579F6; font-family: 'Outfit', Helvetica, Arial, 
            sans-serif; font-size: 14px; font-weight: 500; line-height: 20px; text-decoration: none; 
            display: inline-block;">View message <img alt="View message" src="{{ IMAGE_ARROW_BLUE.src }}" width="16" 
            height="16" style="display: inline-block; vertical-align: middle; width: 16px; max-width: 16px; 
            min-width: 16px; margin: 0 -1px 4px 7px" border="0"></a> 
        </td>'''
    unread_message_html_item = '''
        <tr>
                                                <td bgcolor="#FFFFFE" align="left" style="padding-top: 16px;"
                                                    class="pr-bg-dark pr-text-dark">
                                                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                        <tr>
                                                            <td bgcolor="#FFFFFE" align="left"
                                                                class="pr-bg-dark pr-text-dark"
                                                                style="font-family: 'Outfit', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 20px;">
                                                                <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                                                       style="border-collapse: separate !important;">
                                                                    <tr>
                                                                        <td align="center" bgcolor="#FFFFFE" style="border-radius: 50% !important;">
                                                                            <img alt="Lead Photo" src="$$USER_IMAGE$$" width="24"
                                                                                 height="24"
                                                                                 style="display: inline-block; vertical-align: middle; width: 24px; max-width: 24px; min-width: 24px; font-family: 'Outfit', Helvetica, Arial, sans-serif; color: #FFFFFE; border-radius: 50% !important; font-size: 16px;"
                                                                                 border="0">
                                                                        </td>
                                                                        <td align="center"
                                                                            class="pr-text-dark"
                                                                            style="white-space: nowrap; font-family: 'Outfit', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; line-height: 20px; padding-left: 4px">
                                                                            $$USER_NAME$$
                                                                        </td>
                                                                        $$VIEW_MESSAGE_BUTTON$$  
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>

                                                        <tr>
                                                            <td align="left" style="padding-top: 8px">
                                                                <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                                                       style="border-collapse: separate !important;">
                                                                    <tr>
                                                                        <td align="left" bgcolor="#F6F6F8"
                                                                            class="sec-bg-dark pr-text-dark"
                                                                            style="color: #262730; font-family: 'Outfit', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 20px; padding: 12px; border-radius: 0 12px 12px 12px !important; background-color: #F6F6F8">
                                                                            $$MESSAGE_TEXT$$
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
        '''

    @staticmethod
    def get_button_name() -> str:
        return 'Go to Chat'

    @staticmethod
    def get_chat_url(users: list, messages: list):
        if len(users) > 1:
            return f'{portal_url}/feed?chat=true'
        else:
            return IncomingMessageNotification.get_button_url(users[0], messages[0]['bot']['source']['source_id'])

    @staticmethod
    def get_button_url(sender_id: str, source_id: str) -> str:
        return f'{portal_url}/feed?senderId={sender_id}&sourceId={source_id}'

    def get_subject_text(self, users: list) -> str:
        if self.type == NotificationType.INSTANTLY or self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            return 'New message from your lead'
        elif len(users) > 1:
            return 'Unread messages from your lead'
        return 'Unread message from your lead'

    def create_title(self, user_ids: list[str], users: list):
        title = ""
        for user_id in user_ids[:3]:
            user = [user for user in users if user_id == user['sender_id']][0]
            photo = (user.get('images') or {}).get('image_72', '{{ IMAGE_PERSON.src }}')
            name = self.get_name(user)
            item = self.name_html_item.replace('$$USER_NAME$$', name)
            item = item.replace('$$USER_IMAGE$$', photo)
            title += item

        if len(user_ids) > 3:
            title += self.other_leads_text

        return f"You have unread messages from {title}" if len(users) > 1 else f"You have unread message from {title}"

    def create_unread_messages_list(self, messages: list):
        unread_messages = ""
        for message in messages[:3]:
            name = self.get_name(message['user'])
            photo = (message['user'].get('images') or {}).get('image_72', '{{ IMAGE_PERSON.src }}')
            item = self.unread_message_html_item.replace('$$USER_NAME$$', name)
            item = item.replace('$$USER_IMAGE$$', photo)
            item = item.replace('$$MESSAGE_TEXT$$', message['text'])
            view_message_button = ""
            if len(messages) > 1:
                view_message_button = (
                    self.view_message_html_item.replace('$$VIEW_MESSAGE_URL$$',
                                                        self.get_button_url(message['sender_id'],
                                                                            message['bot']['source']['source_id'])))
            item = item.replace('$$VIEW_MESSAGE_BUTTON$$', view_message_button)

            unread_messages += item
        return unread_messages


class InboxNotification(Notification):
    name_html_item = '''
            <div style="display: inline-block; padding-left: 2px; line-height: 32px" class="lead_names">
                <img alt="Lead Photo" src="$$USER_IMAGE$$" width="24" height="24"
                        style="background-color: #FFFFFE !important; display: inline-block; vertical-align: top; width: 24px; 
                        max-width: 24px; min-width: 24px; font-family: 'Outfit', Helvetica, Arial, sans-serif; color: #FFFFFE; 
                        border-radius: 50% !important; font-size: 16px;" border="0">
                        <span style="font-weight: 600;">$$USER_NAME$$</span>
            </div>
            '''
    new_request_html_item = '''
        <tr>
                                                <td bgcolor="#FFFFFE" align="left" style="padding-top: 16px;"
                                                    class="pr-bg-dark pr-text-dark">
                                                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                        <tr>
                                                            <td bgcolor="#FFFFFE" align="left"
                                                                class="pr-bg-dark pr-text-dark"
                                                                style="font-family: 'Outfit', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 20px;">
                                                                <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                                                       style="border-collapse: separate !important;">
                                                                    <tr>
                                                                        <td align="center" bgcolor="#FFFFFE" style="border-radius: 50% !important;">
                                                                            <img alt="Lead Photo" src="$$USER_IMAGE$$" width="24"
                                                                                 height="24"
                                                                                 style="display: inline-block; vertical-align: middle; width: 24px; max-width: 24px; min-width: 24px; font-family: 'Outfit', Helvetica, Arial, sans-serif; color: #FFFFFE; border-radius: 50% !important; font-size: 16px;"
                                                                                 border="0">
                                                                        </td>
                                                                        <td align="center"
                                                                            class="pr-text-dark"
                                                                            style="white-space: nowrap; font-family: 'Outfit', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; line-height: 20px; padding-left: 4px">
                                                                            $$USER_NAME$$
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>

                                                        <tr>
                                                            <td align="left" style="padding-top: 8px">
                                                                <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                                                       style="border-collapse: separate !important;">
                                                                    <tr>
                                                                        <td align="left" bgcolor="#F6F6F8"
                                                                            class="sec-bg-dark pr-text-dark"
                                                                            style="color: #262730; font-family: 'Outfit', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 20px; padding: 12px; border-radius: 0 12px 12px 12px !important; background-color: #F6F6F8">
                                                                            $$REQUEST_TEXT$$
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
        '''

    @staticmethod
    def get_button_name(users: list):
        return 'View message requests' if len(users) > 1 else 'View message request'

    @staticmethod
    def get_chat_url():
        return f'{portal_url}/feed?requests=true'

    @staticmethod
    def get_subject_text(users: list) -> str:
        return 'New message requests on Leadguru' if len(users) > 1 else 'New message request on Leadguru'

    def create_title(self, user_ids: list[str], users: list):
        title = ""
        for user_id in user_ids[:3]:
            user = [user for user in users if user_id == user['sender_id']][0]
            photo = (user.get('images') or {}).get('image_72', '{{ IMAGE_PERSON.src }}')
            name = self.get_name(user)
            item = self.name_html_item.replace('$$USER_NAME$$', name)
            item = item.replace('$$USER_IMAGE$$', photo)
            title += item

        return f"New message requests from {title}" if len(users) > 1 else f"New message request from {title}"

    def create_new_requests_list(self, requests: list):
        new_requests = ""
        for request in requests[:3]:
            name = self.get_name(request['user'])
            photo = (request['user'].get('images') or {}).get('image_72', '{{ IMAGE_PERSON.src }}')
            item = self.new_request_html_item.replace('$$USER_NAME$$', name)
            item = item.replace('$$USER_IMAGE$$', photo)
            item = item.replace('$$REQUEST_TEXT$$', request['text'])
            new_requests += item
        return new_requests


class SourceDeactivationNotification(Notification):
    @staticmethod
    def get_button_name() -> str:
        return 'Show community'

    @staticmethod
    def get_button_url() -> str:
        return f'{portal_url}/communities?inactive=true'

    @staticmethod
    def get_subject_text() -> str:
        return 'Inactivation of Community on Leadguru'

    @staticmethod
    def get_notification_text(bots: list[DedicatedBotModel]):
        names = [server.name for bot in bots for server in bot.servers]
        match len(bots):
            case 1:
                return f'{names[-1]} became inactive on Leadguru.'
            case 2 | 3:
                return f'{", ".join(names)} became inactive on Leadguru.'
            case _:
                return f'{", ".join(names[:3])} and other became inactive on Leadguru.'


class BulkRepliesNotification(Notification):

    @staticmethod
    def get_button_name() -> str:
        return 'View post'

    @staticmethod
    def get_button_url(post: Post) -> str:
        return f'{portal_url}/bulk-post/form/{post.id}'

    def get_subject_text(self, post: Post) -> str:
        replied_messages = [message.id for message in post.messages if message.id in self.attributes]
        if len(replied_messages) > 1:
            return 'New replies to your bulk post'
        return 'New reply to your bulk post'

    @staticmethod
    def get_notification_text(post: Post):
        if len(post.messages) <= 1:
            source_name = post.messages[0].server_name
            channel_name = post.messages[0].channel_name
            return f'You have new reply in #{channel_name} from {source_name.capitalize()} to your {post.title} post.'

        channels = set([message.channel_id for message in post.messages])
        sources = set([message.server_id for message in post.messages])
        return (f'You have new replies in {len(channels)} from {len(sources)} communities '
                f'to your {post.title} post.')


class BulkReactionsNotification(Notification):

    @staticmethod
    def get_button_name() -> str:
        return 'View post'

    @staticmethod
    def get_button_url(post: Post) -> str:
        return f'{portal_url}/bulk-post/form/{post.id}'

    @staticmethod
    def get_subject_text() -> str:
        return 'People are reacting to your post'

    @staticmethod
    def get_notification_text(post: Post):
        if len(post.messages) <= 1:
            source_name = post.messages[0].server_name
            channel_name = post.messages[0].channel_name
            return (f'You have new reaction in <b>{source_name}/#{channel_name}</b> '
                    f'to your <span style="font-weight: 600; color: #3579F6">{post.title}</span> post.')

        channels = set([message.channel_id for message in post.messages])
        sources = set([message.server_id for message in post.messages])
        return (f'You have new reactions in <b>{len(channels)}</b> from <b>{len(sources)}</b> communities '
                f'to your <span style="font-weight: 600; color: #3579F6">{post.title}</span> post.')


class FollowUpNotification(Notification):

    @property
    def need_to_notify_now(self) -> bool:
        allowed_types = [NotificationType.ONCE_A_DAY, NotificationType.ONCE_A_DAY,
                         NotificationType.UNREAD_FOR_FEW_MINUTES]
        if not self.enabled or self.type not in allowed_types:
            return False

        now = datetime.now(UTC)
        if self.last_notification:
            self.last_notification = self.last_notification.replace(tzinfo=UTC)

        if (self.type == NotificationType.ONCE_A_DAY and self.last_notification
                and (self.last_notification.day == now.day or self.hour != now.hour)):
            return False

        if (self.type == NotificationType.ONCE_A_WEEK and self.last_notification
                and (self.last_notification.day == now.day or (now.hour != self.hour or now.day != self.day))):
            return False

        return True

    def has_not_notified_leads(self, actual: list[UserLeadModel]) -> bool:
        if self.type == NotificationType.UNREAD_FOR_FEW_MINUTES and self.last_notification:
            self.last_notification = self.last_notification.replace(tzinfo=UTC)
            not_notified_leads = [lead for lead in actual if lead.followup_date.replace(tzinfo=UTC) >
                                  (self.last_notification + timedelta(minutes=self.minute))]
            return bool(not_notified_leads)

        return True

    @staticmethod
    def get_button_name(actual: list[UserLeadModel]) -> str:
        if len(actual) > 1:
            return 'View calendar'
        return 'Send message'

    def get_button_url(self, actual: list[UserLeadModel]) -> str:
        if len(actual) > 1:
            if self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
                return f'{portal_url}/dashboard/calendar?view=day'
            return f'{portal_url}/dashboard/calendar?view=week'
        return f'{portal_url}/feed?senderId={actual[0].message.sender_id}&sourceId={actual[0].message.source.source_id}'

    def get_subject_text(self, actual: list[UserLeadModel]) -> str:
        subject_text = 'You have planned follow-ups' if len(actual) > 1 else 'You have planned follow-up'

        if self.type == NotificationType.ONCE_A_DAY:
            return f'{subject_text} for today'
        elif self.type == NotificationType.ONCE_A_WEEK:
            return f'{subject_text} for this week'
        elif self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            return f'{subject_text} for today in {self.minute} minutes'

        return subject_text

    def get_notification_text(self, actual: list[ExtendedUserLeadModel], overdue: list[ExtendedUserLeadModel]) -> str:
        notification_text = ''
        names = [lead.contact.real_name for lead in actual]
        if self.type == NotificationType.ONCE_A_DAY:
            match len(actual):
                case 1:
                    notification_text = f'You have planned to send follow-up today to {names[0]}.'
                case 2 | 3:
                    notification_text = f'You have planned to send follow-up today to {", ".join(names)}.'
                case _:
                    notification_text = (f'You have planned to send follow-up today to {", ".join(names[:3])} '
                                         f'and {len(names) - 3} other leads.')
        elif self.type == NotificationType.ONCE_A_WEEK:
            match len(actual):
                case 1:
                    notification_text = f'You have planned to send follow-up to {names[0]} this week.'
                case 2 | 3:
                    notification_text = f'You have planned to send follow-up to {", ".join(names)} this week.'
                case _:
                    notification_text = (f'You have planned to send follow-up to {", ".join(names[:3])} '
                                         f'and {len(names) - 3} other leads this week.')
        elif self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            match len(actual):
                case 1:
                    notification_text = (f'You have planned to send follow-up today in '
                                         f'{self.minute} minutes to {names[0]}.')
                case 2 | 3:
                    notification_text = (f'You have planned to send follow-up today in '
                                         f'{self.minute} minutes to {", ".join(names)}.')
                case _:
                    notification_text = (f'You have planned to send follow-up today in '
                                         f'{self.minute} minutes to {", ".join(names[:3])} '
                                         f'and {len(names) - 3} other leads.')

        return f'{notification_text} Plus you have {len(overdue)} overdue follow-ups.' if overdue else notification_text


class BillingNotifications(Notification):
    pass
