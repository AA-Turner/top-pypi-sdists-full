import builtins
import traceback
## Notify System
from notify import Notify
from notify.providers.email import Email
from notify.providers.slack import Slack
from notify.providers.teams import Teams
from notify.models import (
    Actor,
    Chat,
    Channel,
    TeamsCard,
    TeamsChannel
)
import querysource.utils.functions as qsfunctions
from ....conf import (
    EVENT_CHAT_ID,
    EVENT_CHAT_BOT,
    DEFAULT_RECIPIENT,
    NOTIFY_ON_ERROR,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_HOST,
    ENVIRONMENT,
    SLACK_DEFAULT_CHANNEL,
    SLACK_DEFAULT_CHANNEL_NAME,
    MS_TEAMS_DEFAULT_TEAMS_ID,
    MS_TEAMS_DEFAULT_CHANNEL_ID,
    MS_TEAMS_DEFAULT_CHANNEL_NAME,
)
from ....utils import cPrint, check_empty
from ....exceptions import ConfigError, EventError
from . import functions as alertfunc
from . import colfunctions as colfunc
from ..abstract import AbstractEvent
from ....interfaces.notification import Notification


def recursive_lookup(d, target_key):
    """
    Recursively finds the first dictionary that contains a given key inside a nested dictionary.

    :param d: Dictionary to search
    :param target_key: Key to find ("result" by default)
    :return: The dictionary containing the key, or None if not found
    """
    """
    Recursively finds the first dictionary that contains the given key.

    :param d: Dictionary to search
    :param target_key: Key to find dynamically (e.g., "result" or any other key)
    :return: The dictionary containing the key, or None if not found
    """
    if isinstance(d, dict):
        if target_key in d:
            return d  # Return the entire dictionary that contains the target key
        for _, value in d.items():
            if isinstance(value, dict):  # Recurse into nested dictionaries
                found = recursive_lookup(value, target_key)
                if found is not None:
                    return found
    return None


class Alert(Notification, AbstractEvent):
    def __init__(self, *args, **kwargs):
        # adding checks:
        self.system_checks: list = kwargs.pop("system_checks", [])
        self.result_checks: list = kwargs.pop("result_checks", [])
        self.column_checks: list = kwargs.pop("column_checks", [])
        self.stat_checks: list = kwargs.pop("stat_checks", [])
        self._channel: str = kwargs.pop("channel", NOTIFY_ON_ERROR)
        super().__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        task = kwargs.get("task", None)
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        try:
            stats = task.stats.to_json()
        except AttributeError:
            stats = None

        df = task.resultset()

        errors = []

        if self.system_checks:
            rst = await self.process_checks(self.system_checks, stats, task_name)
            if rst:
                errors += rst

        if self.stat_checks:
            if check_empty(stats):
                self._logger.warning(f"No statistics found for the task {task_name}")
                return None
            steps = stats.get("steps", [])
            rst = await self.stats_checks(self.stat_checks, stats, steps, task_name)
            if rst:
                errors += rst

        if self.result_checks:
            if check_empty(df):
                return None
            data = {
                "num_rows": len(df),
                "num_columns": df.shape[1],
                "shape": df.shape,
                "columns": df.columns.values.tolist()
            }
            rst = await self.process_checks(self.result_checks, data, task_name)
            if rst:
                errors += rst

        if self.column_checks:
            # Get the summary statistics of the DataFrame
            desc = df.describe()
            err = []
            for check in self.column_checks:
                fname, colname, fn, params = self.get_pandas_function(check)
                # Check if the column exists in the DataFrame
                if colname not in df.columns:
                    self._logger.warning(f"Column {colname} not found in DataFrame.")
                    continue
                # execute the function:
                self._logger.debug(f"Exec {fname} with args {params}")
                actual_value, result = fn(df, desc, colname, **params)
                if result is False:
                    # threshold was reached
                    self._logger.error(
                        f"{task_name}: Threshold for {fname} was reached with: {actual_value} on {colname}"
                    )
                    err.append(
                        {
                            "function": fname,
                            "column": colname,
                            "value": actual_value,
                            "expected": params.get("value", "Unknown")
                        }
                    )

        if errors:
            # TODO: send a notification about threshold violation.
            await self.notify(task_name, program, errors, **kwargs)

    def get_pandas_function(self, payload: dict):
        fname = list(payload.keys())[0]
        func = None
        try:
            params = payload[fname]
        except KeyError:
            params = {}
        # Extract the column name from the parameters
        col_name = params.pop("column")
        try:
            func = getattr(colfunc, fname)
        except AttributeError:
            self._logger.warning(f"Function {fname} does not exist on Alert System")
        return fname, col_name, func, params

    def get_function(self, payload: dict):
        """Get the function name, function object and parameters from the payload."""
        fname = list(payload.keys())[0]
        try:
            params = payload[fname]
        except KeyError:
            params = {}
        try:
            func = getattr(alertfunc, fname)
        except AttributeError:
            try:
                func = getattr(qsfunctions, fname)
            except AttributeError:
                try:
                    func = globals()[fname]
                except (KeyError, AttributeError):
                    try:
                        func = getattr(builtins, fname)
                    except AttributeError:
                        func = None
        if not func:
            raise ConfigError(
                f"Function {fname} doesn't exist on Flowtask."
            )
        return fname, func, params

    def exec_function(self, fname, func, data, **kwargs):
        self._logger.debug(f"Exec {fname} with args {kwargs}")
        try:
            return func(data, **kwargs)
        except (TypeError, ValueError) as err:
            self._logger.exception(str(err), exc_info=True, stack_info=True)
            traceback.print_exc()
            return None

    async def process_checks(self, checks, data, task_name):
        errors = []
        for check in checks:
            fname, fn, params = self.get_function(check)
            colname, value, result = self.exec_function(fname, fn, data, **params)
            if result is False:
                # threshold was reached
                self._logger.error(
                    f"{task_name}: Threshold was reached for {fname} {colname} = {value}"
                )
                errors.append(
                    {
                        "function": fname,
                        "column": colname,
                        "value": value,
                        "expected": params.get("value", "Unknown")
                    }
                )
        return errors

    async def stats_checks(self, checks, stats: dict, steps: list, task_name: str):
        errors = []
        for fn in checks:
            result = False
            fname, fn, params = self.get_function(fn)
            if "column" in params:
                # extract the column from stats:
                current_value = stats.get(params["column"], None)
                if current_value is None:
                    self._logger.warning(f"Column {params['column']} not found in stats.")
                    continue
                current_value = stats
            elif 'component' in params:
                component_name = params.pop('component')
                component_dict = stats['steps'].get(component_name, {})
                if component_dict is None:
                    self._logger.warning(f"Component {component_name} not found in stats.")
                    continue
                if not params:
                    self._logger.warning(f"No key provided after 'component' for {component_name}.")
                    continue
                dynamic_key, dyn_value = params.popitem()
                # Recursively find the dictionary containing this key
                result_dict = recursive_lookup(component_dict, dynamic_key)
                if result_dict is None:
                    self._logger.warning(
                        f"No Dict containing '{dynamic_key}' found in {component_name}."
                    )
                    continue
                current_value = result_dict
                params = {
                    "column": dynamic_key,
                    "value": dyn_value
                }
            # Execute the query:
            component, value, result = self.exec_function(fname, fn, current_value, **params)
            if result is False:
                # threshold was reached
                self._logger.error(
                    f"{task_name}: Threshold for {fname} was reached with: {value} on {component}"
                )
                errors.append(
                    {
                        "function": fname,
                        "column": component,
                        "value": value,
                        "expected": params.get("value", "Unknown")
                    }
                )
        return errors

    def getNotify(self, notify, **kwargs):
        if notify == "telegram":
            # defining the Default chat object:
            recipient = Chat(**{"chat_id": EVENT_CHAT_ID, "chat_name": "Navigator"})
            # send notifications to Telegram bot
            args = {"bot_token": EVENT_CHAT_BOT, **kwargs}
            ntf = Notify("telegram", **args)
        elif notify == "slack":
            recipient = Channel(
                channel_id=SLACK_DEFAULT_CHANNEL,
                channel_name=SLACK_DEFAULT_CHANNEL_NAME,
            )
            ntf = Slack()
        elif notify == "email":
            account = {
                "host": EMAIL_HOST,
                "port": EMAIL_PORT,
                "username": EMAIL_USERNAME,
                "password": EMAIL_PASSWORD,
                **kwargs,
            }
            recipient = Actor(**DEFAULT_RECIPIENT)
            ntf = Email(debug=True, **account)
        elif notify == 'teams':
            team_id = kwargs.pop("team_id", MS_TEAMS_DEFAULT_TEAMS_ID)
            recipient = TeamsChannel(
                name=MS_TEAMS_DEFAULT_CHANNEL_NAME,
                team_id=team_id,
                channel_id=MS_TEAMS_DEFAULT_CHANNEL_ID
            )
            ntf = Teams(
                as_user=True,
                team_id=team_id,
            )
        else:
            # Any other Notify Provider:
            recipient = Actor(**DEFAULT_RECIPIENT)
            ntf = Notify(notify, **kwargs)
        return [ntf, recipient]

    async def notify(
        self,
        task_name: str,
        program: str,
        errors: list,
        **kwargs
    ):
        for error in errors:
            fname = error.get("function", "Unknown")
            colname = error.get("column", "Unknown")
            value = error.get("value", "Unknown")
            expected = error.get("expected", "Unknown")
            cPrint(
                "------------"
            )
            cPrint(
                f"- {task_name}: {fname} reached for {colname} with value: {value}, expected: {expected}",
                level='CRITICAL'
            )
            cPrint(
                "------------"
            )
        # Getting a Notify component based on Alert configuration:
        ntf, recipients = self.getNotify(self._channel, **kwargs)
        # build notification message:
        err_info = '\n'.join(
            [
                f"- {error.get('column', 'Unknown')}: {error.get('value', 'Unknown')}"
                for error in errors
            ]
        )
        message = f"🛑 ::{ENVIRONMENT} -  Task {program}.{task_name}, Error on: {err_info}"
        # send the notification:
        args = {"recipient": [recipients], "message": message}
        if self._channel == 'teams':
            channel = recipients
            msg = TeamsCard(
                text=str(message),
                summary=f"Task Summary: {program}.{task_name}",
                title=f"Task {program}.{task_name}",
            )
            async with ntf as conn:
                return await conn.send(
                    recipient=channel,
                    message=msg
                )
        elif ntf.provider_type == "email":
            args["subject"] = message
        elif ntf.provider == "telegram":
            args["disable_notification"] = True
        else:
            args["subject"] = message
        async with ntf as t:
            result = await t.send(**args)
        return result
