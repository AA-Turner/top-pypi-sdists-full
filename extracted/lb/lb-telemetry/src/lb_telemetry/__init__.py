###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import argparse
import json
import os
import platform
import time
from typing import Optional

import requests
from LbPlatformUtils import inspect
from logzero import logger as logzero

INFLUXDB_LEGAL_TYPES = (bool, int, float, str)


class Logger:
    def __init__(
        self,
        producer="lb-telemetry",
        datasource_id="10459",
        database="monit_production_lb_telemetry",
        send_url="http://monit-metrics.cern.ch:10012/",
    ):
        self.producer = producer
        self.datasource_id = datasource_id
        self.database = database
        self.send_url = send_url

    @staticmethod
    def is_data_valid(data: dict, tags: list) -> bool:
        """Verifies the validity of data for logger usage.

        Logs a meaningful warning in case of invalid data.

        Args:
            data: The data to validate.
            tags: Which data entries are tags (the rest are assumed to be fields).

        Returns:
            Whether the data is valid for logger usage.
        """
        if not data:
            logzero.warning("'data' arg should not be empty")
            return False

        # Ensure all data sent has a legal type
        for value in data.values():
            if not isinstance(value, INFLUXDB_LEGAL_TYPES):
                logzero.warning(
                    f"{value} has type {type(value)} "
                    f"which isn't a type supported by InfluxDB"
                )
                return False

        # Every declared tag should also appear in the data dictionary
        for tag in tags:
            if tag not in data.keys():
                logzero.warning(f"The tag {tag} does not appear in the data dictionary")
                return False

        return True

    @staticmethod
    def get_os_version() -> str:
        system = platform.system()
        if system == "Linux":
            ver_name, ver_num = platform.libc_ver()
            return f"{ver_name} {ver_num}"
        elif system == "Darwin":
            ver_num = platform.mac_ver()[0]
            return ver_num
        elif system == "Windows":
            ver_num = platform.win32_ver()[0]
            return ver_num
        else:
            return "N/A"

    def build_payload(
        self, table: str, data: dict, tags: list[str], include_host_info: bool
    ) -> dict:
        """Builds a payload to be sent to MONIT.

        The payload timestamp is in ms.

        Args:
            table: The name of the calling package and ID for the
                     table the data should be sent to.
            data: The data (tags and fields with their values) to be sent to MONIT.
                  Should not be empty.
            tags: Which data entries are tags (the rest are assumed to be fields).
            include_host_info: Whether information about the caller's system should
                               be included in logging (Python version, OS, etc.)
        """
        if include_host_info:
            host_info = {
                "python": f"{platform.python_implementation()} "
                f"{platform.python_version()}",
                "system": platform.system(),
                "processor": inspect.architecture(),
                "os_version": self.get_os_version(),
            }
        else:
            host_info = {}

        payload = {
            "producer": self.producer,
            "type": table,
            "timestamp": int(time.time() * 1000),
            "idb_tags": tags + list(host_info.keys()),
        }

        return {**payload, **host_info, **data}

    def log_to_monit(
        self, package: str, data: dict, tags: list[str], include_host_info: bool = True
    ) -> Optional[int]:
        """Sends the provided data to MONIT.

        The logged data is accessible via MONIT Grafana.

        Args:
            package: The name of the calling package and ID for the
                     database the data should be sent to.
            data: The data (tags and fields with their values) to be sent to MONIT.
            tags: Which data entries are tags (the rest are assumed to be fields).
            include_host_info: Whether information about the caller's system should
                               be included in logging (Python version, OS, etc.)

        Returns:
            The timestamp of the created log entry.
        """
        if "LBTELEMETRY_ENABLED" not in os.environ:
            return None
        if not Logger.is_data_valid(data, tags):
            return None

        payload = self.build_payload(package, data, tags, include_host_info)

        # Send the data to MONIT
        try:
            response = requests.post(
                self.send_url,
                headers={
                    "Content-Type": "application/json",
                },
                data=json.dumps(payload),
                timeout=5,
            )
        except requests.exceptions.RequestException as e:
            logzero.debug(
                f"An error occurred while logging telemetry "
                f"(this can happen when running from outside "
                f"the CERN network): {e}"
            )
            return None

        if response.status_code != 200:
            logzero.warning(f"Unexpected status code: {response.status_code}")
            logzero.debug(f"Response: {response.text}")
            logzero.debug(f"Payload: {json.dumps(payload)}")
            return None

        return payload["timestamp"]


def lb_telemetry():
    parser = argparse.ArgumentParser(
        usage="lb-telemetry [-h] send json_payload <table> "
        "[--tags tag1 tag2] [--include-host-info]",
        description="Manually send",
    )
    subparsers = parser.add_subparsers(dest="command")

    send_parser = subparsers.add_parser("send", help="Send telemetry data")
    send_parser.add_argument(
        "payload", type=json.loads, help="Telemetry data to send in str JSON format"
    )
    send_parser.add_argument(
        "-t", "--table", type=str, required=True, help="The destination table name"
    )
    send_parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Which payload data are tags (the rest are fields)",
    )
    send_parser.add_argument(
        "--include-host-info",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Include for info about your system to be sent",
    )

    args = parser.parse_args()
    if args.command == "send":
        payload: dict = args.payload
        table: str = args.table
        tags: list[str] = args.tags
        include_host_info: bool = args.include_host_info

        Logger().log_to_monit(
            package=table,
            data=payload,
            tags=tags,
            include_host_info=include_host_info,
        )
