"""A calendar invitation in an email (its .ics, as Google Calendar and Outlook send it), shown
above the email as in Gmail: the event as it is in the user's Google Calendar, what it clashes
with, and Yes, No and Maybe.

Google puts an invitation into the calendar of the address it was sent to by itself. The answer
is given there, and Google tells the organizer, as when answering in Gmail."""

import base64
import binascii
import re
from datetime import date, datetime, timedelta, tzinfo
from typing import Any
from urllib.parse import quote
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from myorb.connections.google_accounts import GoogleAccount, GoogleAccounts
from myorb.plugins.calendar import API, API_NAME, EVENTS_SCOPE, SCOPE, parse_event

RESPONSES = {"accepted": "Yes", "declined": "No", "tentative": "Maybe"}
GUESTS_SHOWN = 6
CLASHES_SHOWN = 3


def decode(data: str) -> str:
    try:
        raw = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
    except (binascii.Error, ValueError):
        return ""
    return raw.decode("utf-8", errors="replace")


def read_ics(text: str) -> dict[str, str]:
    """The invitation's method (REQUEST, CANCEL, REPLY…) and its first event's fields, each by
    its name with the parameters kept apart: {"UID": …, "DTSTART": …, "DTSTART;": "TZID=…"}."""
    fields: dict[str, str] = {}
    in_event = False
    for line in re.sub(r"\r?\n[ \t]", "", text).splitlines():
        name, _, value = line.partition(":")
        key, _, params = name.partition(";")
        key = key.strip().upper()
        if key == "BEGIN" and value.strip().upper() == "VEVENT":
            in_event = True
        elif key == "END" and value.strip().upper() == "VEVENT":
            break
        elif key == "METHOD" and not in_event:
            fields["METHOD"] = value.strip().upper()
        elif in_event and key not in fields:
            fields[key] = value.strip()
            fields[f"{key};"] = params
    return fields


def _text(value: str) -> str:
    return re.sub(r"\\([\\;,nN])", lambda m: "\n" if m[1] in "nN" else m[1], value)


def _address(value: str) -> str:
    return value.removeprefix("mailto:").removeprefix("MAILTO:").strip()


def ics_time(value: str, params: str, timezone: tzinfo) -> datetime | date | None:
    """A DTSTART or DTEND: a date, a time in UTC or in a named time zone. Outlook's own zone
    names ("Central Europe Standard Time") are not known here: None, and the time is left out."""
    if re.fullmatch(r"\d{8}", value):
        return date(int(value[:4]), int(value[4:6]), int(value[6:]))
    match = re.fullmatch(r"(\d{8}T\d{6})(Z?)", value)
    if not match:
        return None
    moment = datetime.strptime(match[1], "%Y%m%dT%H%M%S")
    if match[2]:
        return moment.replace(tzinfo=ZoneInfo("UTC")).astimezone(timezone)
    zone = re.search(r"TZID=\"?([^\";:]+)", params)
    try:
        return moment.replace(tzinfo=ZoneInfo(zone[1])).astimezone(timezone) if zone else None
    except (ZoneInfoNotFoundError, ValueError):
        return None


def when(start: datetime | date | None, end: datetime | date | None, all_day: bool) -> str:
    """ "Thu 5 Nov · 14:00–15:00", "Thu 5 Nov", "Thu 5 – Sat 7 Nov"."""
    if start is None:
        return ""
    day = start.strftime("%a %-d %b")
    if all_day:
        last = end - timedelta(days=1) if isinstance(end, date) else None
        if last is None or last <= start:
            return day
        return f"{start.strftime('%a %-d')} – {last.strftime('%a %-d %b')}"
    if not isinstance(start, datetime):
        return day
    if not isinstance(end, datetime):
        return f"{day} · {start:%H:%M}"
    if end.date() == start.date():
        return f"{day} · {start:%H:%M}–{end:%H:%M}"
    return f"{day} {start:%H:%M} – {end.strftime('%a %-d %b')} {end:%H:%M}"


def _events_url(event_id: str = "") -> str:
    url = f"{API}/calendars/primary/events"
    return f"{url}/{quote(event_id, safe='')}" if event_id else url


def _pick(items: list[dict[str, Any]], fields: dict[str, str]) -> dict[str, Any] | None:
    """The event of the invitation among those Google keeps under its UID: the series, or the
    one changed day of it the invitation is about."""
    if not items:
        return None
    if fields.get("RECURRENCE-ID"):
        day = fields["RECURRENCE-ID"][:8]
        changed = [i for i in items if i.get("recurringEventId")]
        for item in changed:
            original = item.get("originalStartTime", {})
            if (original.get("dateTime") or original.get("date") or "").replace("-", "")[:8] == day:
                return item
        if len(changed) == 1:
            return changed[0]
    return next((i for i in items if not i.get("recurringEventId")), items[0])


async def _clashes(
    google: GoogleAccounts, account: GoogleAccount, event: dict[str, Any], timezone: tzinfo
) -> list[str]:
    """Other events in the calendar at the same time, as Gmail's "Possible conflict"."""
    start, end = event["start"], event["end"]
    params = {
        "timeMin": start.isoformat(),
        "timeMax": end.isoformat(),
        "singleEvents": "true",
        "maxResults": 20,
    }
    found = await google.get_json(account, _events_url(), API_NAME, params)
    titles = []
    for item in found.get("items", []):
        if item.get("id") == event["id"] or item.get("recurringEventId") == event["id"]:
            continue
        other = parse_event(item, {"primary": True}, timezone)
        if other and not other["all_day"] and not other["free"]:
            titles.append(other["title"])
    return titles[:CLASHES_SHOWN]


async def invitation(
    google: GoogleAccounts, account: GoogleAccount, ics: str, timezone: tzinfo
) -> dict[str, Any] | None:
    """What the card shows, or None when the email holds no invitation (an answer to one the
    user sent, say). Without the calendar, or with the event not in it, the card has what the
    .ics says and no answers."""
    fields = read_ics(ics)
    method = fields.get("METHOD", "REQUEST")
    if method not in ("REQUEST", "CANCEL") or not fields.get("UID"):
        return None
    start = ics_time(fields.get("DTSTART", ""), fields.get("DTSTART;", ""), timezone)
    end = ics_time(fields.get("DTEND", ""), fields.get("DTEND;", ""), timezone)
    card: dict[str, Any] = {
        "title": _text(fields.get("SUMMARY", "")) or "(No title)",
        "when": when(start, end, isinstance(start, date) and not isinstance(start, datetime)),
        "organizer": _address(fields.get("ORGANIZER", "")),
        "guests": [],
        "more_guests": 0,
        "cancelled": method == "CANCEL",
        "clashes": [],
        "response": None,
        "event_id": "",
        "url": "",
        "can_answer": False,
        "needs_permission": False,
    }
    if SCOPE not in account.scopes and EVENTS_SCOPE not in account.scopes:
        return card
    found = await google.get_json(account, _events_url(), API_NAME, {"iCalUID": fields["UID"]})
    event = _pick(found.get("items", []), fields)
    if event is None:
        return card
    cancelled = card["cancelled"] or event.get("status") == "cancelled"
    attendees = event.get("attendees", [])
    me = next((a for a in attendees if a.get("self")), None)
    organizer = event.get("organizer") or {}
    guests = [
        a.get("email", "")
        for a in attendees
        if not a.get("self") and not a.get("organizer") and not a.get("resource")
    ]
    card.update(
        title=event.get("summary") or card["title"],
        organizer=organizer.get("email") or card["organizer"],
        guests=guests[:GUESTS_SHOWN],
        more_guests=max(0, len(guests) - GUESTS_SHOWN),
        cancelled=cancelled,
        url=event.get("htmlLink", ""),
        event_id=event.get("id", ""),
        response=me.get("responseStatus") if me else None,
    )
    parsed = None if cancelled else parse_event(event, {"primary": True}, timezone)
    if parsed:
        card["when"] = when(parsed["start"], parsed["end"], parsed["all_day"])
        if not parsed["all_day"]:
            card["clashes"] = await _clashes(
                google, account, {**parsed, "id": event["id"]}, timezone
            )
    answerable = me is not None and not me.get("organizer") and not cancelled
    card["can_answer"] = answerable and EVENTS_SCOPE in account.scopes
    card["needs_permission"] = answerable and EVENTS_SCOPE not in account.scopes
    return card


async def answer(
    google: GoogleAccounts, account: GoogleAccount, event_id: str, response: str
) -> None:
    """Yes, No or Maybe, in the user's calendar; Google tells the organizer."""
    if response not in RESPONSES:
        raise ValueError("Answer Yes, No or Maybe.")
    event = await google.get_json(account, _events_url(event_id), API_NAME)
    attendees = event.get("attendees", [])
    if not any(a.get("self") and not a.get("organizer") for a in attendees):
        raise ValueError("This event is not an invitation to you.")
    answered = [{**a, "responseStatus": response} if a.get("self") else a for a in attendees]
    await google.request_json(
        account,
        "PATCH",
        _events_url(event_id),
        API_NAME,
        params={"sendUpdates": "all"},
        json={"attendees": answered},
    )
