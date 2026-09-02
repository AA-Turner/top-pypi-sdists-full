from .watch import BaseWatcher
from .imap import IMAPWatchdog, ImapWatcher


class TaggedImapWatcher(ImapWatcher):
    def __init__(self, tagged_address: str, *args, **kwargs):
        self.tagged_address = tagged_address
        super(TaggedImapWatcher, self).__init__(*args, **kwargs)

    def process_email(self, email_id, **kwargs):
        # Explicitly mark the email as SEEN
        self.imap_server.store(email_id, "+FLAGS", "\SEEN")
        typ, _ = self.imap_server.fetch(email_id, "(FLAGS)")
        if typ != "OK":
            self._logger.warning(f"Cannot mark email {email_id} as read (SEEN)")
        super(TaggedImapWatcher, self).process_email(email_id, **kwargs)

    def build_search_criteria(self, search_criteria):
        criteria = []
        for key, value in search_criteria.items():
            if value is None:
                criteria.append(key)
            else:
                criteria.append(f'({key} "{value}")')
        criteria.append(f'(TO "{self.tagged_address}") UNSEEN')
        return " ".join(criteria)


class TaggedIMAPWatchdog(IMAPWatchdog):
    def get_tagged_address(self, username: str, tag: str) -> str:
        user, domain = username.split("@")
        return f"{user}+{tag}@{domain}"

    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        tag = kwargs.pop("tag", None)
        if not tag:
            raise ValueError("TAG is required for TaggedIMAPWatchdog")
        credentials = kwargs.pop("credentials", {})
        self.mailbox = kwargs.pop("mailbox", "INBOX")
        interval = kwargs.pop("interval", 10)
        authmech = credentials.pop("authmech", None)
        self.mask_start(**kwargs)
        search = self.processing_search(kwargs.pop("search", {}))
        # TODO: processing with masks the Search criteria:
        self.credentials = self.set_credentials(credentials)
        alias_address = kwargs.pop("alias_address", None)
        if alias_address:
            tagged_address = alias_address
        else:
            tagged_address = self.get_tagged_address(credentials["user"], tag)
        return TaggedImapWatcher(
            **self.credentials,
            mailbox=self.mailbox,
            interval=interval,
            authmech=authmech,
            search=search,
            tagged_address=tagged_address,
            **kwargs,
        )
