from enum import Enum


class ZAMMADARTICLETYPEEnum(str, Enum):
    CHAT = "chat"
    EMAIL = "email"
    FACEBOOK_FEED_COMMENT = "facebook feed comment"
    FACEBOOK_FEED_POST = "facebook feed post"
    FAX = "fax"
    NOTE = "note"
    PHONE = "phone"
    SMS = "sms"
    TELEGRAM_PERSONAL_MESSAGE = "telegram personal-message"
    TWITTER_DIRECT_MESSAGE = "twitter direct-message"
    TWITTER_STATUS = "twitter status"
    WEB = "web"

    def __str__(self) -> str:
        return str(self.value)
