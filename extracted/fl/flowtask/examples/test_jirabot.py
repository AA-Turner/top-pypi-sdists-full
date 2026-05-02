from flowtask.services.bots.telegram import TelegramBot
from flowtask.services.jira import JiraActions
from aiogram import types
import asyncio
from asyncdb import AsyncDB
from querysource.conf import default_dsn
from flowtask.conf import TELEGRAM_JIRA_BOT_TOKEN

class JiraBot(TelegramBot):
    def __init__(self, bot_token: str | None = None, **kwargs) -> None:
        super().__init__(bot_token, **kwargs)
        self.jira = JiraActions(
            'https://trocglobal.atlassian.net',
            'wcabrera@mobileinsight.com',
            'ATATT3xFfGF0FqA_86I0WnqyAt0U9kBwpScs0WeA3VBMUDq3eKmlWJGp5CZhFwbWlMt8z5HOgbsfBUxNaxBIrGnweAIoMEmO2oydJAc55X2ZzS2GK4I1W_2LUDaG1U3dBepS15KHYVRL3KZ2vIOttBzscPR7xTHKOnKFGCPaSHGoJIUXOnsRLjE=FB035771'
        )
    
    
    async def get_jira_instance(self, message: types.Message, address: str = False):
        user = self.user_info(message)
        user_id = user[0]['user_id']
        db = AsyncDB('pg', dsn=default_dsn)
        result = None
        async with await db.connection() as conn:
            qry = f"""SELECT a.user_id, a.uid, a.account, a.address
                FROM auth.user_accounts a 
                INNER JOIN auth.user_accounts c ON c.user_id = a.user_id AND c.provider = 'telegram' and c.uid = '{user_id}' 
                WHERE a.provider = 'Jira'"""
            result, error = await conn.queryrow(qry)
            if not error:
                jira = JiraActions(
                    result['address'],
                    result['uid'],
                    result['account']['api_token']
                )
                if not address:
                    return jira
                else:
                    return jira, result['address']

    async def handler_create(self, message: types.Message):
        try:
            split_message = message.text.replace('/create ', '').split('::')
            project_key, summary, description = split_message[:3]
            issue_type = split_message[3] if len(split_message) > 3 else "Bug"
        except ValueError:
            msg = '''At least 3 values are expected but less has been received, you should send the command as follows\n
<code>/create NAV::Test Issue::Issue Description::Bug</code>\n
or\n
<code>/create NAV::Test Issue::Issue Description</code>'''
            await self.send_message(message, msg)
            return

        try:
            jira = await self.get_jira_instance(message)
            issue = jira.create_issue(
                project_key = project_key,
                summary = summary,
                description = description,
                issue_type = issue_type)
            result = f'Created issue {issue.key}'
        except Exception as err:
            result = f'Error: {str(err)}'
        await self.send_message(message, result)


    async def handler_comment(self, message: types.Message):
        try:
            split_message = message.text.replace('/comment ', '').split('::')
            issue_key, comment = split_message[:2]
        except ValueError:
            msg = '''At least 2 values are expected but less has been received, you should send the command as follows\n
<code>/comment NAV-0000::Comment on Issue</code>'''
            await self.send_message(message, msg)
            return

        try:
            jira = await self.get_jira_instance(message)
            issue = jira.add_comment(issue_key, comment)
            result = f'Added comment in issue {issue_key}'
        except Exception as err:
            result = f'Error: {str(err)}'
        await self.send_message(message, result)


    async def handler_transition(self, message: types.Message):
        try:
            split_message = message.text.replace('/transition ', '').split('::')
            issue_key, transition_name = split_message[:2]
            comment = split_message[2] if len(split_message) > 3 else None
        except ValueError:
            msg = '''At least 3 values are expected but less has been received, you should send the command as follows\n
<code>/transition NAV-0000::To Do::Transition Comment</code>\n
or\n
<code>/transition NAV-0000::To Do</code>'''
            await self.send_message(message, msg)
            return

        try:
            jira = await self.get_jira_instance(message)
            issue = jira.transition_issue(issue_key, transition_name, comment)
            result = f'Status changed in issue {issue_key}'
        except Exception as err:
            result = f'Error: {str(err)}'
        await self.send_message(message, result)


    async def handler_assign(self, message: types.Message):
        try:
            split_message = message.text.replace('/assign ', '').split('::')
            issue_key, assignee = split_message[:2]
        except ValueError:
            msg = '''At least 2 values are expected but less has been received, you should send the command as follows\n
<code>/assign NAV-0000::user@domain.com</code>'''
            await self.send_message(message, msg)
            return

        try:
            jira = await self.get_jira_instance(message)
            issue = jira.assign_issue(issue_key, assignee)
            result = f'Assigned changed in issue {issue_key}'
        except Exception as err:
            result = f'Error: {issue_key}'
        await self.send_message(message, result)


    async def handler_worklog(self, message: types.Message):
        try:
            split_message = message.text.replace('/worklog ', '').split('::')
            issue_key, time_spent = split_message[:2]
            comment = split_message[2] if len(split_message) > 2 else None
            started = split_message[3] if len(split_message) > 3 else None
        except ValueError:
            msg = '''At least 2 values are expected but less has been received, you should send the command as follows\n
<code>/worklog NAV-0000::2h::Issue Comment::2024-08-01T09:00:00</code>\n
or\n
<code>/worklog NAV-0000::2h::Issue Comment</code>
or\n
<code>/worklog NAV-0000::2h</code>'''
            await self.send_message(message, msg)
            return

        try:
            jira = await self.get_jira_instance(message)
            issue = jira.add_worklog(issue_key, time_spent, comment, started)
            result = f'Worklog changed in issue {issue_key}'
        except Exception as err:
            result = f'Error: {str(err)}'
        await self.send_message(message, result)


    async def handler_issues(self, message: types.Message):
        try:
            jira, address = await self.get_jira_instance(message, True)
            result = jira.list_issues()
            msg = ''
            for issue in result:
                msg += f'- <a href="{address}browse/{issue.key}">{issue.key}</a>: {issue.fields.summary} [{issue.fields.status}]\n'
                print(msg)
        except Exception as err:
            msg = f'Error-: {str(err)}'
        await self.send_message(message, msg)


    async def handler_transitions(self, message: types.Message):
        ticket = message.text.replace('/transitions', '').strip()
        if ticket == '':
            msg = '''At least 2 values are expected but less has been received, you should send the command as follows\n\n<code>/transitions NAV-0000</code>'''
            await self.send_message(message, msg)
            return

        try:
            jira = await self.get_jira_instance(message)
            list = jira.list_transitions(ticket)
            result = f'Valid transitions for {ticket}:\n- '
            result += '\n- '.join(list)
        except Exception as err:
            result = f'Error: {str(err)}'
        await self.send_message(message, result)


async def main():
    bot = JiraBot(
        bot_token=TELEGRAM_JIRA_BOT_TOKEN
    )
    await bot.run_forever()


if __name__ == '__main__':
    asyncio.run(main())