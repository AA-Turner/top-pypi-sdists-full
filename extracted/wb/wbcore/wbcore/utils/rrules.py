import calendar as calendar_reference
from datetime import date

from dateutil import rrule


def convert_rrulestr_to_dict(
    rrule_str: str, dtstart: date | None = None, count: int | None = None, until: date | None = None
) -> dict:
    rule_dict = {
        values[0].lower(): values[1]
        for elt in rrule_str.replace("RRULE:", "").split(";")
        if (values := elt.split("=")) and len(values) == 2
    }
    rule_dict["interval"] = int(rule_dict.get("interval", "1"))
    if setpos_str := rule_dict.get("bysetpos", None):
        rule_dict["bysetpos"] = int(setpos_str)
    if freq := rule_dict.get("freq", None):
        rule_dict["freq"] = getattr(rrule, freq)
    if wkst := rule_dict.get("wkst", None):
        rule_dict["wkst"] = getattr(rrule, wkst)
    if byday := rule_dict.pop("byday", None):
        rule_dict["byweekday"] = [getattr(rrule, day.strip()) for day in byday.split(",")]
    if bymonthday := rule_dict.pop("bymonthday", None):
        rule_dict["bymonthday"] = [int(v) for v in bymonthday.split(",")]
    if dtstart:
        rule_dict["dtstart"] = dtstart
    if count:
        rule_dict["count"] = count
    if until:
        rule_dict["until"] = until
    return rule_dict


def convert_weekday_rrule_to_day_name(wkday: rrule.weekday) -> str:
    week_dict = {_day: _day.weekday for _day in rrule.weekdays}
    if idx := week_dict.get(wkday):
        return calendar_reference.day_name[idx]


def humanize_rrule(rrule_str: rrule) -> str:
    """
    Utility function to humanize a frequence based rrule.

    Args:
        rrule_str: The RRULE object

    Returns:
        A humanized version of the rrule
    """
    if rrule_str._freq is None:
        raise ValueError("We do no support humanization of rrule without frequency yet")
    text = "Every "
    freq = rrule.FREQNAMES[rrule_str._freq]
    if rrule_str._interval and rrule_str._interval != 1:
        text += f"{rrule_str._interval} "
    match freq:
        case "MONTHLY":
            text += "Month "
        case "WEEKLY":
            text += "Week "
        case "DAILY":
            text += "Day "
        case "YEARLY":
            text += "Year "
        case "HOURLY":
            text += "Hour "
        case "MINUTELY":
            text += "Minute "
        case "SECONDLY":
            text += "Second "
    if rrule_str._dtstart:
        text += f"From {rrule_str._dtstart:%Y-%m-%d} "

    max_occurrence_text = []
    if rrule_str._count and rrule_str._count != 1:
        max_occurrence_text.append(f"Max {rrule_str._count} times")
    if rrule_str._until:
        max_occurrence_text.append(f"until {rrule_str._until:%Y-%m-%d}")
    if max_occurrence_text:
        text += f'({"/".join(max_occurrence_text)})'
    return text
