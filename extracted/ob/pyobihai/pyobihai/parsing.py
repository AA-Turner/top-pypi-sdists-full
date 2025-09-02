"""Obihai Result Parsers."""

from datetime import datetime, timedelta, timezone
from xml.etree.ElementTree import Element  # nosec


def parse_last_reboot(obj: Element) -> datetime:
    """Get Last Reboot."""

    for exc in obj.findall("./parameter[@name='UpTime']/value"):
        days = exc.attrib.get("current", "").split()[0]
        tstamp = datetime.strptime(exc.attrib.get("current", "").split()[2], "%H:%M:%S")
        now = datetime.now(tz=timezone.utc)
        state = now - timedelta(
            days=float(days),
            hours=tstamp.hour,
            minutes=tstamp.minute,
            seconds=tstamp.second,
            microseconds=now.microsecond,
        )

    return state


def parse_status(name: str, obj: Element) -> str | bool:
    """Get Status for each SIP."""

    for exc in obj.findall("./parameter[@name='Status']/value"):
        if "OBiTALK Service Status" in name:
            return exc.attrib.get("current", "").split()[0]

        state = exc.attrib.get("current", "").split()[0]
        if state != "Service":
            for val in obj.findall("./parameter[@name='CallState']/value"):
                return val.attrib.get("current", "").split()[0]
    return False


def parse_call_direction(lines: str) -> str | bool:
    """Converts call direction result into something human readable."""

    start = lines.find("Number of Active Calls:")
    if start != -1:
        temp_str = lines[start + 24 :]
        end = temp_str.find("</tr>")
        if end != -1:
            call_status = str(temp_str[:end])
            if call_status == "1":
                start = lines.find("Inbound")
                if start != -1:
                    return "Inbound Call"

                start = lines.find("Outbound")
                if start != -1:
                    return "Outbound Call"

    return False
