"""AWS pagerduty alert Utilities.
This module contains a set of classes used for pagerduty alerts information
"""

import json
import requests


class PagerDutyAlert(object):
    CREATE_INCIDENT = "trigger"
    RESOLVE_INCIDENT = "resolve"
    header = {"Content-Type": "application/json"}

    def __init__(self, routing_key, incident_key, logg=None):
        """
        :param routing_key: Pager Duty routing key
        :param incident_key: Job name as incident key/dedup key
        """
        self.routing_key = routing_key
        self.incident_key = incident_key
        self.__logg = logg

    def trigger_incident(self, chkStatus, details=None, severity=None):
        """
        :param chkStatus: job Status
        :param details: Failure details
        :param severity: Severity of the issue
        :return:
        """
        if chkStatus == 1:
            self.__resolve_incident()
        else:
            self.__create_incident(details, severity)

    def __create_incident(self, details, severity):
        """
            Create new incident (if not already open)
        :param details: Failure details
        :param severity: Severity of the issue
        :return:
        """
        summary = "Failure for [{}]".format(self.incident_key)

        payload = {
            "source": self.incident_key,
            "severity": severity,
            "summary": summary,
            "custom_details": details,
        }

        event = {
            "routing_key": self.routing_key,
            "event_action": self.CREATE_INCIDENT,
            "dedup_key": self.incident_key,
            "payload": payload,
        }

        self.__call_pager_duty(event, self.CREATE_INCIDENT)

    def __resolve_incident(self):
        """
            Resolve open incident (if any)
        :return:
        """
        event = {
            "routing_key": self.routing_key,
            "event_action": self.RESOLVE_INCIDENT,
            "dedup_key": self.incident_key,
        }

        self.__call_pager_duty(event, self.RESOLVE_INCIDENT)

    def __call_pager_duty(self, event, event_action):
        """
        :param event: Event details about the incident.
        :param event_action: Event type
        :return:
        """
        response = requests.post(
            "https://events.pagerduty.com/v2/enqueue",
            data=json.dumps(event),
            headers=self.header,
        )

        if response.json()["status"] == "success":
            self.__log("Incident {}".format(event_action))
        else:
            self.__log(response.text)  # print error message if not successful

    def __log(self, message):
        if self.__logg is not None:
            self.__logg.log(message)
        else:
            print(message)
