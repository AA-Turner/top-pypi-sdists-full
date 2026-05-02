from ...conf import (
    ZAMMAD_INSTANCE,
    ZAMMAD_TOKEN,
    ZAMMAD_DEFAULT_CUSTOMER,
    ZAMMAD_DEFAULT_GROUP,
)
from ...exceptions import ActionError
from .ticket import AbstractTicket
from .rest import AbstractREST


class Zammad(AbstractTicket, AbstractREST):
    """Zammad.

    Managing Tickets using Zammad.
    """

    auth_type = "apikey"
    token_type = "Bearer"
    article_base = {"type": "note", "internal": False}
    data_format: str = "raw"

    def __init__(self, *args, **kwargs):
        super(Zammad, self).__init__(*args, **kwargs)
        self.auth = {"apikey": ZAMMAD_TOKEN}

    async def close(self):
        pass

    async def open(self):
        pass

    async def create(self, hook, *args, **kwargs):
        """create.

        Create a new Ticket.
        """
        self.url = f"{ZAMMAD_INSTANCE}api/v1/tickets"
        self.method = "post"
        group = kwargs.pop("group", ZAMMAD_DEFAULT_GROUP)
        title = kwargs.pop("title", None)
        customer = kwargs.pop("customer", ZAMMAD_DEFAULT_CUSTOMER)
        article = kwargs.pop("article")
        article = {**self.article_base, **article}
        data = {
            "title": title,
            "group": group,
            "customer": customer,
            "article": article,
        }
        try:
            result, _ = await self.request(self.url, self.method, data=data)
            return result
        except Exception as e:
            raise ActionError(f"Error creating Zammad Ticket: {e}") from e
