from __future__ import annotations

import logging
import re
from difflib import SequenceMatcher
from pathlib import Path

from contributors_txt.create_content import (
    Alias,
    Person,
    get_teams,
    line_for_person,
    person_should_be_shown,
    persons_from_shortlog,
)


def similar(a_string: str, another_string: str) -> float:
    return SequenceMatcher(None, a_string, another_string).ratio()


def update_content(
    output: Path | str,
    aliases: list[Alias],
    shortlog_output: str,
    configuration_file: str,
) -> str:
    result: str = ""
    header: str = f"""\
# This file is autocompleted by 'contributors-txt',
# using the configuration in '{configuration_file}'.
# Do not add new persons manually and only add information without
# using '-' as the line first character.
# Please verify that your change are stable if you modify manually.

"""
    persons = persons_from_shortlog(aliases, shortlog_output)
    with open(output, encoding="utf8") as f:
        current_output = f.read()
    result = update_teams(
        current_output if header in current_output else header + current_output,
        persons,
    )
    return result


def update_teams(current_result: str, persons: dict[str, Person]) -> str:
    teams = get_teams(persons, exclude_standard=False)
    if not teams:
        return current_result
    current_result = add_email_if_missing(current_result, teams)
    check_no_email(current_result)
    # current_result = order_by_commit(current_result, teams)
    if current_result[-1] != "\n":
        current_result += "\n"
    return current_result


def check_no_email(current_result: str) -> None:
    for part in current_result.split("\n-"):
        if all(c not in part for c in [">", "<", "@"]):
            logging.warning("There's no email in %s", part)


def order_by_commit(current_result: str, teams: dict[str, list[Person]]) -> str:
    new_teams: list[str] = []
    team_boundary = get_team_boundary(current_result, list(teams.keys()))
    for team_name, team_members in teams.items():
        new_teams.append(
            order_by_commit_in_team(
                current_result, team_boundary, team_members, team_name
            )
        )
    return "".join(new_teams)


def order_by_commit_in_team(
    current_result: str,
    team_boundary: dict[str, tuple[int, int]],
    team_members: list[Person],
    team_name: str,
) -> str:
    # pylint: disable=too-many-locals
    logging.debug("Updating team %s", team_name)
    begin, end = team_boundary[team_name]
    new_team: list[str] = []
    existing_persons = current_result[begin:end].split("\n-")
    logging.debug(existing_persons[0])
    consumed: list[int] = []
    for _, team_member in enumerate(team_members):
        if not person_should_be_shown(team_member):
            continue
        # logging.debug(f"Finding the content for %s", repr(team_member))
        person_found = False
        person_found_by_name = False
        for i, existing_person in enumerate(existing_persons):
            if team_member.mail and team_member.mail in existing_person:
                # logging.debug(f"Placing {team_member.name}: {existing_person}")
                # if person_found:
                #     raise RuntimeError(
                #         f"{team_member.mail} is duplicated {existing_person}!"
                #     )
                person_found = add_person(
                    consumed, existing_person, i, new_team, person_found
                )
            if team_member.name in existing_person and team_member.mail is None:
                if similar(team_member.name, existing_person) >= 0.9:
                    logging.info(
                        "Found %s by name and it's really close.", repr(team_member)
                    )
                    person_found = add_person(
                        consumed, existing_person, i, new_team, person_found
                    )
                else:
                    # The name is not sufficient
                    logging.warning(
                        "Found %s in '%s' but not sure if it's really them (no mail),"
                        " please check",
                        repr(team_member),
                        existing_person,
                    )
                    person_found_by_name = True
        if not person_found and not person_found_by_name:
            logging.debug("Could not find %s in %s !", team_member, team_name)
            # new_team.insert(team_index, f" {team_member}")
    for i, person_not_found in enumerate(existing_persons):
        if i not in consumed:
            logging.debug("%s, '%s' was not consumed.", i, person_not_found)
            new_team.insert(i, person_not_found)
    return "\n-".join(new_team)


def add_person(
    consumed: list[int],
    existing_person: str,
    i: int,
    new_team: list[str],
    person_found: bool,
) -> bool:
    new_team.append(existing_person)
    person_found = True
    consumed.append(i)
    return person_found


def add_email_if_missing(current_result: str, teams: dict[str, list[Person]]) -> str:
    new_teams: list[str] = []
    team_boundary = get_team_boundary(current_result, list(teams.keys()))
    being_header, end_header = team_boundary["Header"]
    new_teams.append(current_result[being_header:end_header])
    for team_name in sorted(team_boundary, key=team_boundary.get):  # type: ignore[arg-type]
        if team_name == "Header":
            continue
        begin, end = team_boundary[team_name]
        new_team = str(current_result[begin:end])
        if team_name not in teams:
            # Section exists in file but has no committers (e.g. Co-Author),
            # pass through unchanged
            new_teams.append(new_team)
            continue
        team_members = teams[team_name]
        logging.debug("Updating team %s", team_name)
        section_slice = current_result[begin:end]
        for team_member in team_members:
            if not person_should_be_shown(team_member):
                continue
            if team_member.name in section_slice:
                new_team = _add_email_to_existing(
                    current_result, new_team, team_member, team_name,
                    section_slice,
                )
            elif team_member.mail is not None and team_member.mail in current_result:
                base_message = (
                    f"'{team_member}' already exists in the file at "
                    f"{current_result.find(team_member.mail)} "
                    f"({team_boundary}) but is not in the proper section, "
                    f"it should be '{team_name}', please fix manually. Did "
                    "you consider uniformizing the name ? :\n"
                )
                raise RuntimeError(
                    team_member.get_template(base_message) + "}\n"
                )
            elif team_member.mail:
                new_team = _insert_person_by_commits(
                    new_team, team_member, team_members
                )
            else:
                logging.warning(
                    "'%s' was not treated as there's no email.", team_member
                )
        new_teams.append(new_team)
    return "".join(new_teams)


def _add_email_to_existing(
    current_result: str,
    new_team: str,
    team_member: Person,
    team_name: str,
    section_slice: str,
) -> str:
    if team_member.mail and team_member.mail in section_slice:
        check_for_duplication(current_result, team_member)
        return new_team
    if not team_member.mail:
        return new_team
    if team_member.name.find(" ") != -1:
        logging.debug("For %s in %s: Adding email", team_member, team_name)
        return new_team.replace(
            team_member.name, f"{team_member.name} {team_member.mail}"
        )
    logging.debug(
        "For %s, there's only a one word name not replacing "
        "anything but it exists.",
        repr(team_member),
    )
    return new_team


def _insert_person_by_commits(
    section_text: str, new_person: Person, team_members: list[Person]
) -> str:
    """Insert a new person into a section, ordered by number of commits."""
    new_line = line_for_person(new_person)
    lines = section_text.split("\n")
    person_entries = _find_person_entries(lines, team_members)
    insert_pos = _find_insert_position(lines, person_entries, new_person)
    lines.insert(insert_pos, new_line.rstrip("\n"))
    return "\n".join(lines)


def _find_person_entries(
    lines: list[str], team_members: list[Person]
) -> list[tuple[int, int]]:
    """Return (line_index, commit_count) for person lines matched to team members."""
    entries: list[tuple[int, int]] = []
    for i, line in enumerate(lines):
        if not line.startswith("- "):
            continue
        for tm in team_members:
            if tm.mail and tm.mail in line:
                entries.append((i, tm.number_of_commits))
                break
    return entries


def _find_insert_position(
    lines: list[str],
    person_entries: list[tuple[int, int]],
    new_person: Person,
) -> int:
    """Find the line index where a new person should be inserted."""
    if not person_entries:
        return _fallback_insert_position(lines)

    # After the last matched person with >= commits
    insert_after_idx = None
    for line_idx, commits in person_entries:
        if commits >= new_person.number_of_commits:
            insert_after_idx = line_idx

    if insert_after_idx is None:
        # More commits than all matched entries, insert before first matched
        return person_entries[0][0]
    return _end_of_person_entry(lines, insert_after_idx)


def _fallback_insert_position(lines: list[str]) -> int:
    """Find insert position when no matched person entries exist."""
    last_person_idx = None
    for i, line in enumerate(lines):
        if line.startswith("- "):
            last_person_idx = i
    if last_person_idx is not None:
        return _end_of_person_entry(lines, last_person_idx)
    # No person entries at all, append before trailing whitespace
    pos = len(lines)
    while pos > 0 and lines[pos - 1].strip() == "":
        pos -= 1
    return pos


def _end_of_person_entry(lines: list[str], person_line_idx: int) -> int:
    """Return the line index after a person entry and its continuation lines."""
    pos = person_line_idx + 1
    while pos < len(lines) and lines[pos] and not lines[pos].startswith("- "):
        pos += 1
    return pos


def check_for_duplication(current_result: str, team_member: Person) -> None:
    assert team_member.mail
    if current_result.count(team_member.mail) != 1:
        raise RuntimeError(f"{team_member} is duplicated")
    name_count = current_result.count(team_member.name)
    name_in_email = team_member.name in team_member.mail
    if (name_count > 1 and not name_in_email) or (name_count > 2 and name_in_email):
        logging.info(
            "It's possible that %s is duplicated, please check by yourself",
            team_member,
        )


def get_team_boundary(
    current_result: str, teams: list[str]
) -> dict[str, tuple[int, int]]:
    teams_boundary: dict[str, tuple[int, int]] = {"Header": (0, 0)}
    for team in teams:
        teams_boundary[team] = current_result.find(team), 0
    # Also detect section headers in the file that aren't in the teams dict
    # (e.g. "Co-Author" sections with no committers in the shortlog)
    for match in re.finditer(r"^(.+)\n-{2,}$", current_result, re.MULTILINE):
        section_name = match.group(1)
        if section_name not in teams_boundary:
            teams_boundary[section_name] = match.start(), 0
    ordered_teams = sorted(teams_boundary, key=teams_boundary.get)  # type: ignore[arg-type]
    for i, team in enumerate(ordered_teams):
        begin = teams_boundary[team][0]
        if i == len(ordered_teams) - 1:
            end = len(current_result)
        else:
            end = teams_boundary[ordered_teams[i + 1]][0]
        teams_boundary[team] = (begin, end)
    return teams_boundary
