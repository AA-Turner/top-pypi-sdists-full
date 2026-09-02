"""
Date/time utility functions for Observational Memory.
Pure functions for formatting relative timestamps and annotating observations.

Mirrors: packages/memory/src/processors/observational-memory/date-utils.ts
"""

import re
from datetime import datetime, timedelta
from typing import Optional


def format_relative_time(date: datetime, current_date: datetime) -> str:
    """Format a relative time string like '5 days ago', '2 weeks ago', 'today', etc."""
    diff = current_date - date
    diff_days = diff.days

    if diff_days < 0:
        future_days = abs(diff_days)
        if future_days == 1: return "tomorrow"
        if future_days < 7: return f"in {future_days} days"
        if future_days < 14: return "in 1 week"
        if future_days < 30: return f"in {future_days // 7} weeks"
        if future_days < 60: return "in 1 month"
        if future_days < 365: return f"in {future_days // 30} months"
        years = future_days // 365
        return f"in {years} year{'s' if years > 1 else ''}"

    if diff_days == 0: return "today"
    if diff_days == 1: return "yesterday"
    if diff_days < 7: return f"{diff_days} days ago"
    if diff_days < 14: return "1 week ago"
    if diff_days < 30: return f"{diff_days // 7} weeks ago"
    if diff_days < 60: return "1 month ago"
    if diff_days < 365: return f"{diff_days // 30} months ago"
    years = diff_days // 365
    return f"{years} year{'s' if years > 1 else ''} ago"


def format_gap_between_dates(prev_date: datetime, curr_date: datetime) -> Optional[str]:
    """Format the gap between two dates as a human-readable string."""
    diff = curr_date - prev_date
    diff_days = diff.days

    if diff_days <= 1:
        return None
    elif diff_days < 7:
        return f"[{diff_days} days later]"
    elif diff_days < 14:
        return "[1 week later]"
    elif diff_days < 30:
        return f"[{diff_days // 7} weeks later]"
    elif diff_days < 60:
        return "[1 month later]"
    else:
        return f"[{diff_days // 30} months later]"


def parse_date_from_content(date_content: str) -> Optional[datetime]:
    """
    Parses a date string like 'May 30, 2023', 'May 27-28, 2023', 'late April 2023', etc.
    """
    # Simple date format: "May 30, 2023"
    simple_match = re.search(r'([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})', date_content)
    if simple_match:
        try:
            return datetime.strptime(simple_match.group(0).replace(",", ""), "%B %d %Y")
        except ValueError:
            pass

    # Range format: "May 27-28, 2023" - use first date
    range_match = re.search(r'([A-Z][a-z]+)\s+(\d{1,2})-\d{1,2},?\s+(\d{4})', date_content)
    if range_match:
        date_str = f"{range_match.group(1)} {range_match.group(2)} {range_match.group(3)}"
        try:
            return datetime.strptime(date_str, "%B %d %Y")
        except ValueError:
            pass

    # Vague format: "late April 2023"
    vague_match = re.search(r'(late|early|mid)[- ]?(?:to[- ]?(?:late|early|mid)[- ]?)?([A-Z][a-z]+)\s+(\d{4})', date_content, re.IGNORECASE)
    if vague_match:
        modifier = vague_match.group(1).lower()
        month = vague_match.group(2)
        year = vague_match.group(3)
        day = 15
        if modifier == "early": day = 7
        if modifier == "late": day = 23
        try:
            return datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
        except ValueError:
            pass

    # Cross-month range: "April to May 2023"
    cross_match = re.search(r'([A-Z][a-z]+)\s+to\s+(?:early\s+)?([A-Z][a-z]+)\s+(\d{4})', date_content, re.IGNORECASE)
    if cross_match:
        month = cross_match.group(2)
        year = cross_match.group(3)
        try:
            return datetime.strptime(f"{month} 1 {year}", "%B %d %Y")
        except ValueError:
            pass

    return None


def is_future_intent_observation(line: str) -> bool:
    """Detects if an observation line indicates future intent."""
    patterns = [
        r'\bwill\s+(?:be\s+)?(?:\w+ing|\w+)\b',
        r'\bplans?\s+to\b',
        r'\bplanning\s+to\b',
        r'\blooking\s+forward\s+to\b',
        r'\bgoing\s+to\b',
        r'\bintends?\s+to\b',
        r'\bwants?\s+to\b',
        r'\bneeds?\s+to\b',
        r'\babout\s+to\b',
    ]
    combined = re.compile('|'.join(patterns), re.IGNORECASE)
    return bool(combined.search(line))


def expand_inline_estimated_dates(observations: str, current_date: datetime) -> str:
    """Expand inline estimated dates with relative time."""
    pattern = re.compile(r'\((estimated|meaning)\s+([^)]+\d{4})\)', re.IGNORECASE)

    def replacer(match):
        prefix = match.group(1)
        date_content = match.group(2)
        target_date = parse_date_from_content(date_content)
        
        if target_date:
            relative = format_relative_time(target_date, current_date)
            # Find the line before this match
            offset = match.start()
            line_start = observations.rfind('\n', 0, offset) + 1
            line_before_date = observations[line_start:offset]
            
            is_past = target_date < current_date
            is_future_intent = is_future_intent_observation(line_before_date)
            
            if is_past and is_future_intent:
                return f"({prefix} {date_content} - {relative}, likely already happened)"
            return f"({prefix} {date_content} - {relative})"
        return match.group(0)

    return pattern.sub(replacer, observations)


def add_relative_time_to_observations(observations: str, current_date: datetime) -> str:
    """
    Add relative time annotations to observations.
    Transforms 'Date: May 15, 2023' headers to 'Date: May 15, 2023 (5 days ago)'
    and expands inline estimated dates.
    """
    with_inline_dates = expand_inline_estimated_dates(observations, current_date)
    
    date_header_regex = re.compile(r'^(Date:\s*)([A-Z][a-z]+ \d{1,2}, \d{4})$', re.MULTILINE)
    
    dates = []
    for match in date_header_regex.finditer(with_inline_dates):
        date_str = match.group(2)
        try:
            parsed = datetime.strptime(date_str, "%B %d, %Y")
            dates.append({
                "index": match.start(),
                "date": parsed,
                "match": match.group(0),
                "prefix": match.group(1),
                "date_str": date_str
            })
        except ValueError:
            pass

    if not dates:
        return with_inline_dates

    result = []
    last_index = 0
    
    for i, curr in enumerate(dates):
        prev = dates[i-1] if i > 0 else None
        
        result.append(with_inline_dates[last_index:curr["index"]])
        
        if prev:
            gap = format_gap_between_dates(prev["date"], curr["date"])
            if gap:
                result.append(f"\n{gap}\n\n")
        
        relative = format_relative_time(curr["date"], current_date)
        result.append(f'{curr["prefix"]}{curr["date_str"]} ({relative})')
        
        last_index = curr["index"] + len(curr["match"])
        
    result.append(with_inline_dates[last_index:])
    
    return "".join(result)
