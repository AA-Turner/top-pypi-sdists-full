import codecs
import traceback
from jira import JIRA
import orjson
from ...utils.json import json_encoder
from .abstract import AbstractEvent
from ...conf import (
    JIRA_API_TOKEN,
    JIRA_USERNAME,
    JIRA_INSTANCE,
    JIRA_PROJECT
)


class Jira(AbstractEvent):
    """Jira.

    Jira Event to create a new Ticket on Error/Exception.
    """
    def __init__(self, *args, **kwargs):
        super(Jira, self).__init__(*args, **kwargs)
        self.program = kwargs.pop("program", None)
        self.task = kwargs.pop("task", None)
        self.issue_type = kwargs.pop("issue_type", 'Bug')
        self._status = kwargs.pop("status", "event")
        self._summary = kwargs.get('summary', 'Error on: ')
        self._assignee = kwargs.get('assignee', {})
        # Initialize Jira Connection
        try:
            self.jira = JIRA(
                server=JIRA_INSTANCE,
                basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN)
            )
        except Exception as err:
            self._logger.error(
                f"Cannot Connect to Jira {err}"
            )
            raise

    async def __call__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', JIRA_PROJECT)
        _message = kwargs.get('message', '')
        task = kwargs.pop("task", None)
        status = kwargs.pop("status", "done")
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        error = kwargs.get('error', None)
        task_id = task.task_id
        if status not in ("error", "failed", "exception", "task error"):
            return True
        # Operar el error
        try:
            stat = task.stats  # getting the stat object:
            stats = stat.to_json()
        except AttributeError:
            stats = []
        description = {}
        if stats:
            # iterate over task stats:
            for stat, value in stats["steps"].items():
                description[stat] = value
        # Create the Jira Ticket:
        desc = orjson.dumps(description, option=orjson.OPT_INDENT_2).decode()
        codereview = codecs.decode(json_encoder(stats['Review']), 'unicode_escape').replace("**", "*")
        desc = f"""
        {{code:json}}
        {desc}
        {{code}}\n\n
        """
        # Capture the stack trace
        stack_trace = traceback.format_exc()
        if stack_trace:
            desc = f"""
            {desc}

            h2. *Error*:\n\n
            {{panel:bgColor=#ffebe6}}\n
            {error}
            \n{{panel}}\n\n

            h2. Stack Trace:\n\n
            {{code:python}}
            {stack_trace}
            {{code}}
            """
        args = {
            'project': project_id,
            'summary': f"{self._summary} {task_name}",
            'description': (
                f"{{color:#FF5630}}[ STATUS: {status.upper()} ]{{color}} \n\n"
                f"{{panel:bgColor=#deebff}}\n*Task*: {task_name}\n{{panel}}\n\n"
                f"{{panel:bgColor=#deebff}}\n*Task_id*: {task_id}\n{{panel}}\n\n"
                f"{{panel:bgColor=#ffebe6}}\n*Message*: {_message}\n{{panel}}\n\n"
                f"h2. *Task Stats*:\n\n"
                f"{desc}"
                f"\n\n----\n\n{{panel:bgColor=#eae6ff}}\nh2. *Code Review*\n\n{codereview}\n\n{{panel}}"
            ),
            'issuetype': {
                'name': self.issue_type
            }
        }
        try:
            new_issue = self.jira.create_issue(**args)
            self._logger.info(
                f"Jira Issue Created: {new_issue}"
            )
            if self._assignee:
                try:
                    new_issue.update(
                        assignee=self._assignee
                    )
                except Exception as err:
                    print('ERROR > ', err)
                    self._logger.warning(
                        f"Error Assigning Jira Issue to {self._assignee}: {err}"
                    )
            return new_issue
        except Exception as err:
            self._logger.error(
                f"Cannot Create Jira Issue {err}"
            )
            raise
