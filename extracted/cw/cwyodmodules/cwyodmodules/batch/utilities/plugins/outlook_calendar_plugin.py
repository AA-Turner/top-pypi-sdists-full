import requests
import datetime
from semantic_kernel.functions import kernel_function
from ..tools.text_processing_tool import TextProcessingTool
from ...utilities.helpers.env_helper import EnvHelper

from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class OutlookCalendarPlugin:
    def __init__(self, question: str, chat_history: list[dict], user_info: dict):
        self.question = question
        self.chat_history = chat_history
        self.user_info = user_info
        self.env_helper = EnvHelper()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def _get_access_token(self) -> str:
        logger.info("Retrieving access token from user info")
        access_token = self.user_info.get("access_token", None)
        if isinstance(access_token, str):
            logger.info("User access token %s", access_token[:5])
        else:
            logger.info("User access token array created")
        return access_token

    @kernel_function(name="get_calendar_events", description="Get upcoming Outlook calendar events, appointments, metings, etc.")
    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def get_calendar_events(self, days: int = 1) -> str:
        language = self.env_helper.AZURE_MAIN_CHAT_LANGUAGE
        logger.info("Method get_calendar_events of OutlookCalendarPlugin started")
        try:
            logger.info("Retrieving access token for calendar events")
            token = self._get_access_token()
        except Exception as e:
            answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text=f"Authentication error: {str(e)}",
                operation="Explain the user in his language {language} that you failed to get calendar appointment due to an error.",
            )
            return answer
        headers = {"Authorization": f"Bearer {token}"}
        now = datetime.datetime.utcnow().isoformat() + "Z"
        end = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + "Z"
        url = f"https://graph.microsoft.com/v1.0/me/calendarview?startDateTime={now}&endDateTime={end}"
        resp = requests.get(url, headers=headers)
        logger.info("Calendar get results: %s", resp.text[0:120])
        if resp.status_code != 200:
            answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text=f"Failed to fetch events: {resp.text[0:120]}",
                operation=f"Explain the user in his language {language} that you failed to fetch calendar events due to an error.",
            )
            return answer
        events = resp.json().get("value", [])
        if not events:
            answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text="No events found.",
                operation=f"Explain the user in his language {language} that no events were found in the calendar.",
            )
            return answer
        events_text = "\n".join([f"{e.get('subject', 'No subject')} at {e.get('start', {}).get('dateTime', 'Unknown time')}" for e in events])
        answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text=events_text,
                operation=f"Summarize the calendar schedule in the user's {language}.",
            )
        return answer

    @kernel_function(name="schedule_appointment", description="Schedule a new Outlook calendar appointment, meeting, etc.")
    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def schedule_appointment(self, subject: str, start_time: str, end_time: str) -> str:
        logger.info("Method schedule_appointment of OutlookCalendarPlugin started")
        language = self.env_helper.AZURE_MAIN_CHAT_LANGUAGE
        try:
            token = self._get_access_token()
        except Exception as e:
            answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text=f"Failed to schedule appointment: {str(e)}",
                operation=f"Explain the user in his language {language} that you failed to schedule a calendar appointment due to an error.",
            )
            return answer
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url = "https://graph.microsoft.com/v1.0/me/events"
        event = {
            "subject": subject,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
        }
        resp = requests.post(url, headers=headers, json=event)
        logger.info("Calendar set results: %s", resp.text[0:120])
        if resp.status_code == 201:
            answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text="Appointment scheduled successfully.",
                operation=f"Explain to the user in his language {language} that the appointment was scheduled successfully. And summarize the appointment details. And all appointments shortly before and after the scheduled appointment.",
            )
            return answer
        else:
            answer = TextProcessingTool().answer_question(
                question=self.question,
                chat_history=self.chat_history,
                text=f"Failed to schedule appointment: {resp.text[0:120]}",
                operation=f"Explain to the user in his language {language} that the appointment scheduling failed.",
            )
            return answer