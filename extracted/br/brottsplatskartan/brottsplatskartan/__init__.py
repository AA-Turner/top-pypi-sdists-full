# coding=utf-8
""" Brottsplatskartan API """

import datetime
import time
from json.decoder import JSONDecodeError
from typing import Union

import requests

AREAS = [
    "Blekinge län", "Dalarnas län", "Gotlands län", "Gävleborgs län",
    "Hallands län", "Jämtlands län", "Jönköpings län", "Kalmar län",
    "Kronobergs län", "Norrbottens län", "Skåne län", "Stockholms län",
    "Södermanlands län", "Uppsala län", "Värmlands län", "Västerbottens län",
    "Västernorrlands län", "Västmanlands län", "Västra Götalands län",
    "Örebro län", "Östergötlands län"
]

ATTRIBUTION = "Information provided by brottsplatskartan.se"
BROTTS_URL = "https://brottsplatskartan.se/api"


class BrottsplatsKartan:  # pylint: disable=too-few-public-methods
    """ Brottsplatskartan API wrapper. """

    def __init__(self, app='bpk', areas=None, longitude=None, latitude=None):
        """ Setup initial brottsplatskartan configuration. """

        self.parameters = {"app": app}
        self.incidents = {}

        if areas:
            for area in areas:
                if area not in AREAS:
                    raise ValueError('not a valid area: {}'.format(area))
            self.url = BROTTS_URL + "/events"
            self.parameters["areas"] = areas
        elif longitude and latitude:
            self.url = BROTTS_URL + "/eventsNearby"
            self.parameters["lat"] = latitude
            self.parameters["lng"] = longitude
        else:
            # Missing parameters. Using default values.
            self.url = BROTTS_URL + "/events"
            self.parameters["areas"] = ["Stockholms län"]

    @staticmethod
    def _get_datetime_as_ymd(date: time.struct_time) -> datetime.datetime:

        datetime_ymd = datetime.datetime(date.tm_year, date.tm_mon,
                                         date.tm_mday)

        return datetime_ymd

    @staticmethod
    def is_ratelimited(requests_response) -> bool:
        """ Check if we have been ratelimited. """
        rate_limited = requests_response.headers.get('x-ratelimit-reset')
        if rate_limited:
            print("You have been rate limited until " + time.strftime(
                '%Y-%m-%d %H:%M:%S%z', time.localtime(int(rate_limited))))
            return True
        return False

    def get_incidents_from_bpk(self, parameters) -> Union[list, bool]:
        """ Make the API calls to get incidents """

        brotts_entries_left = True
        incidents_today = []
        url = self.url

        while brotts_entries_left:

            requests_response = requests.get(url, params=parameters)

            if self.is_ratelimited(requests_response):
                return False

            try:
                requests_response = requests_response.json()
            except JSONDecodeError:
                print("got JSONDecodeError")
                return False

            incidents = requests_response.get("data")
            if not incidents:
                incidents_today = []
                break

            datetime_today = datetime.date.today()
            datetime_today_as_time = time.strptime(str(datetime_today),
                                                   "%Y-%m-%d")
            today_date_ymd = self._get_datetime_as_ymd(datetime_today_as_time)

            for incident in incidents:
                incident_pubdate = incident["pubdate_iso8601"]
                incident_date = time.strptime(incident_pubdate,
                                              "%Y-%m-%dT%H:%M:%S%z")
                incident_date_ymd = self._get_datetime_as_ymd(incident_date)

                if today_date_ymd == incident_date_ymd:
                    incidents_today.append(incident)
                else:
                    brotts_entries_left = False
                    break

            if requests_response.get("links"):
                url = requests_response["links"]["next_page_url"]
            else:
                break

        return incidents_today

    def get_incidents(self) -> Union[list, bool]:
        """ Get today's incidents. """
        areas = self.parameters.get("areas")
        all_incidents = {}
        current_incidents = []
        if areas:
            parameters = {}
            for area in areas:
                parameters["app"] = self.parameters.get("app")
                parameters["area"] = area
                current_incidents = self.get_incidents_from_bpk(parameters)
                all_incidents.update({area: current_incidents})
        else:
            current_incidents = self.get_incidents_from_bpk(self.parameters)
            all_incidents.update({"latlng": current_incidents})
        if current_incidents is False:
            return False

        return all_incidents
