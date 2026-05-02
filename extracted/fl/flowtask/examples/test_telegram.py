import asyncio
from jira import JIRA
from navconfig import config
from qw.bots.telegram import (
    TelegramBot,
    types
)


class JiraTicket:
    # JIRA_API_TOKEN, JIRA_USERNAME, JIRA_INSTANCE, JIRA_PROJECT
    def __init__(self, *args, **kwargs):
        self.service = None
        self.api_token = kwargs.get('api_token')
        self.username = kwargs.get('username')
        self.instance = kwargs.get('instance')
        self.project = kwargs.get('project')

    def setup(self):
        args = {"basic_auth": (self.username, self.api_token)}
        self.service = JIRA(self.instance, **args)

    async def comment(self, ticket, comment):
        self.service.add_comment(ticket, comment)

    async def create(self, *args, **kwargs):
        """create.

        Create a new Ticket.
        """
        summary = kwargs.pop("summary", None)
        description = kwargs.pop("description", None)
        args = {
            "project": self.project,
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
        }
        if "issuetype" in kwargs:
            args["issuetype"] = {"name": kwargs["issuetype"]}
        try:
            new_issue = self.service.create_issue(**args)
            print("ISSUE ", new_issue)
            return new_issue
        except Exception as e:
            self._logger.error(f"Error creating Jira Ticket: {e}")
            raise


class JiraBot(TelegramBot):
    def __init__(self, bot_token: str | None = None, **kwargs) -> None:
        super().__init__(bot_token, **kwargs)
        self.jira = JiraTicket(
            api_token=config.get('JIRA_API_TOKEN'),
            username=config.get('JIRA_USERNAME'),
            instance=config.get('JIRA_INSTANCE'),
            project=config.get('JIRA_PROJECT')
        )
        self.jira.setup()

    async def handler_create(self, message: types.Message):
        user = self.user_info(message)
        print('USER > ', user, message)
        summary, description = message.text.split('::')
        ticket = await self.jira.create(
            summary=summary,
            description=description
        )
        await self.get_message(
            message,
            'This is your Jira Ticket ...'
        )

    async def handler_comment(self, message: types.Message):
        user = self.user_info(message)
        print('USER > ', user, message)
        ticket, comment = message.text.split(':')
        await self.jira.comment(ticket, comment)
        await self.get_message(
            message,
            'This is your Jira Ticket ...'
        )

async def main():
    import os
    # SECURITY: Bot token removed from hardcoded values. Use TELEGRAM_BOT_TOKEN environment variable
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    bot = JiraBot(
        bot_token=bot_token
    )
    await bot.run_forever()


if __name__ == '__main__':
    asyncio.run(main())
