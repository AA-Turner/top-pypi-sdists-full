from __future__ import annotations

import copy
import datetime
import math
import re
from typing import Optional, Tuple, Dict, Union

from seeq.sdk import *
from seeq.spy import _login
from seeq.spy._shared_definition_constants import (
    DURATION_SCALAR_UNITS,
    OFFSET_DIRECTION,
    CAPSULE_SELECTION,
    DEFAULT_DATE_RANGE,
)


# *********************************************************************************************************************
#
# IMPORTANT: This file is a manual mirror of client/packages/webserver/app/src/utilities/sharedDefinitionFunctions.ts.
#
# format_date_range_from_api_output          <-> formatDateRangeFromApiOutput
# _extract_duration_from_formula             <-> extractDurationFromFormula
# _extract_offset_and_direction_from_formula <-> extractOffsetAndDirectionFromFormula
# compute_capsule_offset                     <-> computeCapsuleOffset
# create_date_range_formula                  <-> createDateRangeFormula
#
# Mirrored helpers are documented at their definitions. Keep behavior and tests synchronized on both sides.
#
# The comments quoting TypeScript statements are part of the mirror contract: each one is the source line that the
# Python beneath it reproduces. Update them whenever the TypeScript changes.
#
# *********************************************************************************************************************


# export const formatDateRangeFromApiOutput = (dateRangeOutput: DateRangeOutputV1): DateRange => {
def format_date_range_from_api_output(date_range_output: DateRangeOutputV1) -> dict:
    # IMPORTANT: Mirrors formatDateRangeFromApiOutput() in
    # client/packages/webserver/app/src/utilities/sharedDefinitionFunctions.ts.

    # let formulaFormValid = false;
    formula_form_valid = False
    # const dateRange: any = {};
    # _.defaultsDeep(dateRange, DEFAULT_DATE_RANGE);
    date_range: dict = copy.deepcopy(DEFAULT_DATE_RANGE)
    # _.assign(dateRange, _.pick(dateRangeOutput, ['name', 'id', 'description']));
    date_range.update({'name': date_range_output.name,
                       'id': date_range_output.id,
                       'description': date_range_output.description})
    # noinspection PyUnresolvedReferences
    # _.assign(dateRange.condition, _.pick(dateRangeOutput.condition, ['name', 'id', 'isRedacted']));
    if date_range_output.condition is not None:
        date_range['condition'].update({'name': date_range_output.condition.name,
                                        'id': date_range_output.condition.id,
                                        'isRedacted': date_range_output.condition.is_redacted})
    # noinspection PyUnresolvedReferences
    # _.assign(dateRange.auto, {
    #   enabled: dateRangeOutput.isAutoUpdating,
    # });
    date_range['auto'].update({'enabled': date_range_output.is_auto_updating})
    # dateRange.enabled = dateRangeOutput.isEnabled;
    date_range['enabled'] = date_range_output.is_enabled
    # dateRange.reportId = dateRangeOutput.report?.id;
    date_range['reportId'] = date_range_output.report.id if date_range_output.report is not None else None
    # dateRange.isArchived = dateRangeOutput.isArchived;
    date_range['isArchived'] = date_range_output.is_archived

    #
    # // The backend gives us back ISO8601 timestamps, but expects milliseconds back.
    # if (dateRangeOutput.dateRange?.start) {
    #   dateRange.range.start = moment.utc(dateRangeOutput.dateRange.start).valueOf();
    # }
    if date_range_output.date_range is not None and date_range_output.date_range.start is not None:
        date_range['range']['start'] = int(_login.parse_content_datetime_with_timezone(
            session=None, dt=date_range_output.date_range.start).value / 1_000_000)
    #
    # if (dateRangeOutput.dateRange?.end) {
    #   dateRange.range.end = moment.utc(dateRangeOutput.dateRange.end).valueOf();
    # }
    if date_range_output.date_range is not None and date_range_output.date_range.end is not None:
        date_range['range']['end'] = int(_login.parse_content_datetime_with_timezone(
            session=None, dt=date_range_output.date_range.end).value / 1_000_000)
    #
    # try {
    try:
        # // See .createDateRangeFormula() for expected formula formats
        #
        # // Fixed, no condition
        # if (!dateRangeOutput.condition?.id && dateRangeOutput.formula?.match(/^capsule\(.*\)$/)) {
        if ((date_range_output.condition is None or not date_range_output.condition.id) and
                (date_range_output.formula is not None and re.search(r'^capsule\(.*\)$', date_range_output.formula))):
            # // Nothing additional needs to be extracted from the formula
            # formulaFormValid = true;
            formula_form_valid = True

        # }
        #
        # const setConditionProperties = (
        #   searchStart?: string,
        #   searchEnd?: string,
        #   maxDuration?: string,
        #   columns?: string,
        #   sortBy?: string,
        #   sortAsc?: string,
        # ) => {
        def set_condition_properties(search_start: Optional[str] = None,
                                     search_end: Optional[str] = None,
                                     max_duration: Optional[str] = None,
                                     columns: Optional[str] = None,
                                     sort_by: Optional[str] = None,
                                     sort_asc: Optional[str] = None) -> None:
            # dateRange.condition.range = {
            #   start: toNumber(searchStart),
            #   end: toNumber(searchEnd),
            # };
            date_range['condition']['range'] = {
                'start': _to_number(search_start),
                'end': _to_number(search_end),
            }
            #
            # if (columns) {
            if columns:
                # dateRange.condition.columns = columns.split(',');
                date_range['condition']['columns'] = columns.split(',')
                # dateRange.condition.sortBy = sortBy;
                date_range['condition']['sortBy'] = sort_by
                # dateRange.condition.sortAsc = sortAsc === 'true';
                date_range['condition']['sortAsc'] = sort_asc == 'true'
                # dateRange.condition.isCapsuleFromTable = true;
                date_range['condition']['isCapsuleFromTable'] = True
            # } else {
            else:
                # dateRange.condition.isCapsuleFromTable = false;
                date_range['condition']['isCapsuleFromTable'] = False
            # }
            #
            # if (maxDuration) {
            if max_duration:
                # const maximumDuration = splitDuration(maxDuration);
                maximum_duration = _split_duration(max_duration)
                # if (!maximumDuration) {
                if maximum_duration is None:
                    # throw new Error(`Could not parse ${maxDuration} as a maximum duration`);
                    raise ValueError(f'Could not parse {max_duration} as a maximum duration')
                # }
                #
                # if (!_.includes(DURATION_SCALAR_UNITS, maximumDuration.units)) {
                if maximum_duration['units'] not in DURATION_SCALAR_UNITS:
                    # throw new Error(
                    # `Invalid maximum duration unit ${maximumDuration.units} in ${maxDuration} as a maximum duration`,
                    # );
                    raise ValueError(
                        f'Invalid maximum duration unit {maximum_duration["units"]} in {max_duration} as a maximum '
                        f'duration')
                # }
                #
                # dateRange.condition.maximumDuration = maximumDuration;
                date_range['condition']['maximumDuration'] = maximum_duration

            # }

        # };
        #
        # // auto enabled
        # const setOffsetProperties = (offset = '1') => {
        # A JavaScript default applies when the argument is undefined, whereas an explicit None reaches the body here.
        # Both paths produce a pick of 1 because toNumber(None) is None and the `?? 1` fallback takes over.
        # noinspection PyShadowingNames
        def set_offset_properties(offset: Optional[str] = '1') -> None:
            # const pick = toNumber(offset) ?? 1;
            pick = _to_number(offset)
            pick = pick if pick is not None else 1
            # if (pick === 1) {
            if pick == 1:
                # dateRange.condition.strategy = CAPSULE_SELECTION.STRATEGY.CLOSEST_TO;
                date_range['condition']['strategy'] = CAPSULE_SELECTION.STRATEGY.CLOSEST_TO
                # dateRange.condition.reference = CAPSULE_SELECTION.REFERENCE.START;
                date_range['condition']['reference'] = CAPSULE_SELECTION.REFERENCE.START
                # dateRange.condition.offset = 1;
                date_range['condition']['offset'] = 1
            # } else if (pick > 1) {
            elif pick > 1:
                # dateRange.condition.strategy = CAPSULE_SELECTION.STRATEGY.OFFSET_BY;
                date_range['condition']['strategy'] = CAPSULE_SELECTION.STRATEGY.OFFSET_BY
                # dateRange.condition.reference = CAPSULE_SELECTION.REFERENCE.START;
                date_range['condition']['reference'] = CAPSULE_SELECTION.REFERENCE.START
                # dateRange.condition.offset = pick - 1;
                date_range['condition']['offset'] = pick - 1
            # } else if (pick === -1) {
            elif pick == -1:
                # dateRange.condition.strategy = CAPSULE_SELECTION.STRATEGY.CLOSEST_TO;
                date_range['condition']['strategy'] = CAPSULE_SELECTION.STRATEGY.CLOSEST_TO
                # dateRange.condition.reference = CAPSULE_SELECTION.REFERENCE.END;
                date_range['condition']['reference'] = CAPSULE_SELECTION.REFERENCE.END
                # dateRange.condition.offset = 1;
                date_range['condition']['offset'] = 1
            # } else if (pick < -1) {
            elif pick < -1:
                # dateRange.condition.strategy = CAPSULE_SELECTION.STRATEGY.OFFSET_BY;
                date_range['condition']['strategy'] = CAPSULE_SELECTION.STRATEGY.OFFSET_BY
                # dateRange.condition.reference = CAPSULE_SELECTION.REFERENCE.END;
                date_range['condition']['reference'] = CAPSULE_SELECTION.REFERENCE.END
                # dateRange.condition.offset = Math.abs(pick) - 1;
                date_range['condition']['offset'] = abs(pick) - 1
            # }

        # };
        #
        # if (!dateRange.auto.enabled && !_.includes(dateRangeOutput.formula, 'Offset')) {
        # _.includes() treats a nullish collection as empty rather than throwing, hence the `or ''`.
        if not date_range['auto']['enabled'] and 'Offset' not in (date_range_output.formula or ''):
            # // Fixed, with condition capsule selected from table
            # const fixedMatchPattern =
            #   /^\s*\/\/ searchStart=(.*?)ms\n\s*\/\/ searchEnd=(.*?)ms\n\s*\/\/ columns=(.*?)\n
            #   \s*\/\/ sortBy=(.*?)\n\s*\/\/ sortAsc=(.*?)\n\s* capsule\(.+\)$/m;
            fixed_match_pattern = re.compile(
                r'^\s*// searchStart=(.*?)ms\n\s*// searchEnd=(.*?)ms\n\s*// columns=(.*?)\n\s*// '
                r'sortBy=(.*?)\n\s*// sortAsc=(.*?)\n\s* capsule\(.+\)$', re.MULTILINE)
            # const fixedMatches = dateRangeOutput.formula?.match(fixedMatchPattern);
            fixed_matches = (fixed_match_pattern.search(date_range_output.formula)
                             if date_range_output.formula is not None else None)
            # if (dateRangeOutput.condition?.id && fixedMatches) {
            if (date_range_output.condition is not None and date_range_output.condition.id and
                    fixed_matches is not None):
                # const [_notUsed, parsedStart, parsedEnd, columns, sortBy, sortAsc] = fixedMatches;
                parsed_start, parsed_end, columns, sort_by, sort_asc = fixed_matches.groups()
                # setConditionProperties(parsedStart, parsedEnd, undefined, columns, sortBy, sortAsc);
                set_condition_properties(parsed_start, parsed_end, None, columns, sort_by, sort_asc)
                # formulaFormValid = true;
                formula_form_valid = True
            # }
        # } else if (!dateRange.auto.enabled && dateRangeOutput.formula?.includes('Offset')) {
        elif (not date_range['auto']['enabled'] and date_range_output.formula is not None and 'Offset' in
              date_range_output.formula):
            # // Fixed, with selected relative capsule
            # const fixedConfigMatchPattern =
            #   /^\s*\/\/ searchStart=(.*?)ms\n\s*\/\/ searchEnd=(.*?)ms\n\s*\/\/ capsuleOffset=(.*?)\n
            #   \s*\/\/ maxDuration=(.*?)\n\s*capsule\(.+\)$/m;
            fixed_config_match_pattern = re.compile(
                r'^\s*// searchStart=(.*?)ms\n\s*// searchEnd=(.*?)ms\n\s*// capsuleOffset=(.*?)\n\s*// '
                r'maxDuration=(.*?)\n\s*capsule\(.+\)$', re.MULTILINE)
            # const fixedMatches = dateRangeOutput.formula.match(fixedConfigMatchPattern);
            fixed_matches = fixed_config_match_pattern.search(date_range_output.formula)
            # if (dateRangeOutput.condition?.id && fixedMatches) {
            if (date_range_output.condition is not None and date_range_output.condition.id and
                    fixed_matches is not None):
                # const [_notUsed, parsedStart, parsedEnd, capsuleOffset, parsedMaxDuration] = fixedMatches;
                parsed_start, parsed_end, capsule_offset, parsed_max_duration = fixed_matches.groups()
                # setConditionProperties(parsedStart, parsedEnd, parsedMaxDuration);
                set_condition_properties(parsed_start, parsed_end, parsed_max_duration)
                # setOffsetProperties(capsuleOffset);
                set_offset_properties(capsule_offset)
                # formulaFormValid = true;
                formula_form_valid = True
            # }
        # }
        #
        # // Auto-update with condition
        # const autoConditionMatchPattern =
        #   /^\$condition(.removeLongerThan\(.+?\))?.setCertain\(\).toGroup\(capsule\(.+\)\).pick\((-?[1-9]+[0-9]*)\)$/;
        auto_condition_match_pattern = re.compile(
            r'^\$condition(.removeLongerThan\(.+?\))?.setCertain\(\).toGroup\(capsule\(.+\)\).pick\((-?[1-9]+[0-9]*)\)$'
        )
        # const autoMatches = dateRangeOutput.formula?.match(autoConditionMatchPattern);
        auto_matches = (auto_condition_match_pattern.search(date_range_output.formula)
                        if date_range_output.formula is not None else None)
        # if (dateRangeOutput.condition?.id && autoMatches) {
        if (date_range_output.condition is not None and date_range_output.condition.id and
                auto_matches is not None):
            # // Closest to Start =>  $condition.setCertain().toGroup(capsule(start, end)).pick(1)
            # // Closest to End => $condition.setCertain().toGroup(capsule(start, end)).pick(-1)
            # // Offset by 1 from Start => $condition.setCertain().toGroup(capsule(start, end)).pick(2)
            # // Offset by 2 from Start => $condition.setCertain().toGroup(capsule(start, end)).pick(3)
            # // Offset by 1 from End => $condition.setCertain().toGroup(capsule(start, end)).pick(-2)
            # const parsedPick = dateRangeOutput.formula?.match(/.*\.pick\((-?[1-9]+[0-9]*)\)$/)?.[1];
            pick_match = re.search(r'.*\.pick\((-?[1-9]+[0-9]*)\)$', date_range_output.formula)
            parsed_pick = pick_match.group(1) if pick_match is not None else None
            # const parsedMaximumDuration = dateRangeOutput.formula?.match(/removeLongerThan\((.+?)\)/)?.[1];
            maximum_duration_match = re.search(r'removeLongerThan\((.+?)\)', date_range_output.formula)
            parsed_maximum_duration = maximum_duration_match.group(1) if maximum_duration_match is not None else None
            # setConditionProperties(undefined, undefined, parsedMaximumDuration);
            set_condition_properties(None, None, parsed_maximum_duration)
            # setOffsetProperties(parsedPick);
            set_offset_properties(parsed_pick)
            # formulaFormValid = true;
            formula_form_valid = True
        # }
        #
        # // Auto-update, condition and non-condition
        # if (dateRange.auto.enabled) {
        if date_range['auto']['enabled']:
            # const background = dateRangeOutput.isBackground;
            background = date_range_output.is_background
            # const cronSchedule = dateRangeOutput.cronSchedule;
            cron_schedule = date_range_output.cron_schedule
            # const duration = extractDurationFromFormula(dateRangeOutput.formula as string);
            duration = _extract_duration_from_formula(date_range_output.formula)
            # const offsetAndDirection = extractOffsetAndDirectionFromFormula(dateRangeOutput.formula ?? '');
            offset_and_direction = _extract_offset_and_direction_from_formula(date_range_output.formula or '')
            # const offset = offsetAndDirection[0];
            offset = offset_and_direction[0]
            # const offsetDirection = offsetAndDirection[1];
            offset_direction = offset_and_direction[1]
            #
            # dateRange.auto = {
            date_range['auto'] = {
                # enabled: true,
                'enabled': True,
                # duration,
                'duration': duration,
                # offset,
                'offset': offset,
                # offsetDirection,
                'offsetDirection': offset_direction,
                # background,
                'background': background,
                # cronSchedule,
                'cronSchedule': cron_schedule,
                # };
            }
        # }
    # } catch (e) {
    except Exception:
        # logWarn(e as Error);
        # formulaFormValid = false;
        formula_form_valid = False
    # }
    #
    # if (!formulaFormValid) {
    if not formula_form_valid:
        # logWarn(`Failed to parse date range formula "${dateRangeOutput.formula}" [${dateRangeOutput.id}]`);
        # dateRange.irregularFormula = dateRangeOutput.formula;
        date_range['irregularFormula'] = date_range_output.formula
    # }
    # return dateRange;
    return date_range
    # };


# export const computeCapsuleOffset = (condition: DateRangeCondition): number => {
def compute_capsule_offset(condition: dict) -> Union[int, float]:
    # IMPORTANT: Mirrors computeCapsuleOffset() in
    # client/packages/webserver/app/src/utilities/sharedDefinitionFunctions.ts.

    # const { strategy, reference, offset = 1 } = condition;
    strategy = condition['strategy']
    reference = condition['reference']
    offset = condition.get('offset', 1)
    # const offsetValue = strategy === CAPSULE_SELECTION.STRATEGY.CLOSEST_TO ? 1 : (toNumber(offset) as number) + 1;
    offset_value = 1 if strategy == CAPSULE_SELECTION.STRATEGY.CLOSEST_TO else _to_number(offset) + 1
    # const signValue = reference === CAPSULE_SELECTION.REFERENCE.START ? 1 : -1;
    sign_value = 1 if reference == CAPSULE_SELECTION.REFERENCE.START else -1
    # return offsetValue * signValue;
    return offset_value * sign_value
    # };


# export const createDateRangeFormula = (dateRange: DateRange) => {
def create_date_range_formula(date_range: dict) -> str:
    # IMPORTANT: Mirrors createDateRangeFormula() in
    # client/packages/webserver/app/src/utilities/sharedDefinitionFunctions.ts.

    # // Fixed range, no condition
    # if (!dateRange.auto.enabled && !dateRange.condition?.id) {
    if (not date_range['auto']['enabled'] and
            (date_range['condition'] is None or not date_range['condition'].get('id'))):
        # return `capsule(${dateRange.range.start}ms, ${dateRange.range.end}ms)`;
        return f"capsule({date_range['range']['start']}ms, {date_range['range']['end']}ms)"
    # }

    # const capsuleOffset = computeCapsuleOffset(dateRange.condition as DateRangeCondition);
    capsule_offset = compute_capsule_offset(date_range['condition'])
    # const maximumDuration = dateRange.condition?.maximumDuration
    #   ? `${dateRange.condition.maximumDuration.value}${dateRange.condition.maximumDuration.units}`
    #   : '';
    maximum_duration = (
        f"{date_range['condition']['maximumDuration']['value']}{date_range['condition']['maximumDuration']['units']}"
        if (date_range['condition'] is not None and date_range['condition'].get('maximumDuration') is not None) else '')

    # // Fixed range, condition
    # // For this configuration, we save the search range and other parameters used to find the capsule in a formula
    # // comment, so that we can present it back to the user in the UI when editing the dateRange.
    # if (!dateRange.auto.enabled && dateRange.condition?.id && dateRange.condition.isCapsuleFromTable) {
    if (not date_range['auto']['enabled'] and date_range['condition'].get('id')
            and date_range['condition'].get('isCapsuleFromTable')):
        # return `// searchStart=${dateRange.condition.range.start}ms
        #     // searchEnd=${dateRange.condition.range.end}ms
        #     // columns=${(dateRange.condition.columns ?? []).join(',')}
        #     // sortBy=${dateRange.condition.sortBy}
        #     // sortAsc=${dateRange.condition.sortAsc}
        #     capsule(${dateRange.range.start}ms, ${dateRange.range.end}ms)`;
        # The continuation lines carry the same eight spaces of indentation as the TypeScript template literal, and
        # JavaScript interpolates booleans as 'true'/'false', so sortAsc is lower-cased here.
        return (f"// searchStart={date_range['condition']['range']['start']}ms\n"
                f"        // searchEnd={date_range['condition']['range']['end']}ms\n"
                f"        // columns={','.join(date_range['condition'].get('columns') or [])}\n"
                f"        // sortBy={date_range['condition']['sortBy']}\n"
                f"        // sortAsc={str(date_range['condition']['sortAsc']).lower()}\n"
                f"        capsule({date_range['range']['start']}ms, {date_range['range']['end']}ms)")
    # } else if (!dateRange.auto.enabled && dateRange.condition?.id && !dateRange.condition.isCapsuleFromTable) {
    elif (not date_range['auto']['enabled'] and date_range['condition'].get('id')
          and not date_range['condition'].get('isCapsuleFromTable')):
        # return `// searchStart=${dateRange.condition.range.start}ms
        #     // searchEnd=${dateRange.condition.range.end}ms
        #     // capsuleOffset=${capsuleOffset}
        #     // maxDuration=${maximumDuration}
        #     capsule(${dateRange.range.start}ms, ${dateRange.range.end}ms)`;
        return (f"// searchStart={date_range['condition']['range']['start']}ms\n"
                f"        // searchEnd={date_range['condition']['range']['end']}ms\n"
                f"        // capsuleOffset={capsule_offset}\n"
                f"        // maxDuration={maximum_duration}\n"
                f"        capsule({date_range['range']['start']}ms, {date_range['range']['end']}ms)")
    # }

    # // Auto-update range
    # const sign = dateRange.auto.offsetDirection === OFFSET_DIRECTION.FUTURE ? '+' : '-';
    sign = '+' if date_range['auto']['offsetDirection'] == OFFSET_DIRECTION.FUTURE else '-'
    # const offset = `${dateRange.auto.offset.value}${dateRange.auto.offset.units}`;
    offset = f"{date_range['auto']['offset']['value']}{date_range['auto']['offset']['units']}"
    # const duration = `${dateRange.auto.duration}ms`;
    duration = f"{date_range['auto']['duration']}ms"
    # const rangeFormula = `capsule($now ${sign} ${offset} - ${duration}, $now ${sign} ${offset})`;
    range_formula = f"capsule($now {sign} {offset} - {duration}, $now {sign} {offset})"

    # if (dateRange.condition?.id) {
    if date_range['condition'] is not None and date_range['condition'].get('id'):
        # const maximumDurationSnippet = maximumDuration ? `.removeLongerThan(${maximumDuration})` : '';
        maximum_duration_snippet = f".removeLongerThan({maximum_duration})" if maximum_duration else ''
        # return `$condition${maximumDurationSnippet}.setCertain().toGroup(${rangeFormula}).pick(${capsuleOffset})`;
        return f"$condition{maximum_duration_snippet}.setCertain().toGroup({range_formula}).pick({capsule_offset})"
    # } else {
    else:
        # return rangeFormula;
        return range_formula
    # }
    # };


# export function isNumeric(input: unknown): boolean {
def _is_numeric(input_value: object) -> bool:
    # IMPORTANT: Mirrors isNumeric() in client/packages/webserver/app/src/utilities/numberHelper.utilities.ts.

    # return _.isFinite(input) || (_.isString(input) && !_.isEmpty(input) && /^-?\d*(\.\d+)?$/.test(input));
    # _.isFinite() is false for booleans, which Python would otherwise accept as ints. Python's '$' also matches
    # before a trailing newline, so re.fullmatch() stands in for the anchored JavaScript test.
    if isinstance(input_value, bool):
        return False
    if isinstance(input_value, (int, float)) and math.isfinite(input_value):
        return True
    return (isinstance(input_value, str) and len(input_value) > 0
            and re.fullmatch(r'-?\d*(\.\d+)?', input_value) is not None)
    # }


# export function toNumber(number: unknown): number | undefined {
def _to_number(value: object) -> Optional[Union[int, float]]:
    # IMPORTANT: Mirrors toNumber() in client/packages/webserver/app/src/utilities/numberHelper.utilities.ts.

    # return isNumeric(number) ? _.toNumber(number) : undefined;
    if not _is_numeric(value):
        return None

    try:
        numeric_value = float(value)
    except ValueError:
        # isNumeric() accepts a lone '-', for which _.toNumber() yields NaN rather than throwing.
        return math.nan

    # JavaScript has a single number type. SPy narrows integral values to int so that generated formulas interpolate
    # '1234ms' instead of '1234.0ms'.
    return int(numeric_value) if numeric_value.is_integer() else numeric_value
    # }


# export function splitDuration(durationString: string | undefined): DurationWithUnits | undefined {
def _split_duration(duration_string: object) -> Optional[Dict[str, Union[int, float, str]]]:
    # IMPORTANT: Mirrors splitDuration() in client/packages/utils/src/time/duration.ts.

    # if (typeof durationString !== 'string') {
    if not isinstance(duration_string, str):
        # return undefined;
        return None
    # }
    #
    # // The value and units are intentionally matched independently and unanchored: the first number and the first
    # // run of letters are used wherever they appear (e.g. '5h3m' and 'h5' both yield { value: 5, units: 'h' }).
    # const value = durationString.match(/[-+]?[0-9]*\.?[0-9]+/)?.[0];
    value_match = re.search(r'[-+]?[0-9]*\.?[0-9]+', duration_string)
    # if (!value) {
    if value_match is None:
        # return undefined;
        return None
    # }
    #
    # const units = durationString.match(/[a-zA-Z]+/)?.[0];
    units_match = re.search(r'[a-zA-Z]+', duration_string)
    # if (!units) {
    if units_match is None:
        # return undefined;
        return None
    # }
    #
    # return { value: +value, units };
    # See _to_number() for why integral values are narrowed to int.
    numeric_value = float(value_match.group(0))
    value = int(numeric_value) if numeric_value.is_integer() else numeric_value
    return {'value': value, 'units': units_match.group(0)}
    # }


# export const extractDurationFromFormula = (formula: string): number => {
def _extract_duration_from_formula(formula: str) -> int:
    # IMPORTANT: Mirrors extractDurationFromFormula() in
    # client/packages/webserver/app/src/utilities/sharedDefinitionFunctions.ts.

    # const durationMatch = formula.match(/\$now\s*[+-]\s*(.*?)\s*[+-]\s*([\d.]+[a-z]+),/i)?.[2];
    match = re.search(r'\$now\s*[+-]\s*(.*?)\s*[+-]\s*([\d.]+[a-z]+),', formula, re.IGNORECASE)
    duration_match = match.group(2) if match is not None else None
    # return (parseDuration(durationMatch) as any).valueOf();
    # moment.duration().valueOf() is milliseconds.
    return int(_parse_duration(duration_match).total_seconds() * 1000)
    # };


# // Keys must be the same as the DURATION_PATTERNS translation keys
# const DURATION_CONVERSIONS = {
# Insertion order matters: _.reduce() walks the keys in this order and each unit contributes at most one match.
_DURATION_CONVERSIONS = {
    'MILLISECONDS': 0.001,
    'SECONDS': 1,
    'MINUTES': 60,
    'HOURS': 3600,
    'DAYS': 86400,
    'WEEKS': 604800,
    # // Parse months as 1/12 of a year, so that long durations better align with year lengths
    # MONTHS: moment.duration(1, 'year').asSeconds() / 12,
    'MONTHS': 31536000 / 12,
    'YEARS': 31536000,
}

# The DURATION_PATTERNS entries of client/packages/webserver/app/resources/i18n/en.json. Date-range formulas always
# carry normalized English unit tokens, so SPy mirrors the English translation rather than loading i18next. The
# entries are regular-expression fragments, and the order within each unit is significant because the first pattern
# that matches wins.
_DURATION_PATTERNS = {
    'DAYS': ['day', 'days', 'dy', 'd', 'Day', 'Days', 'Dy', 'D', 'DAY', 'DAYS', 'DY', 'DY_Z', 'DY_Z2'],
    'HOURS': ['hour', 'hours', 'hr', 'h', 'Hour', 'Hours', 'Hr', 'H', 'HOUR', 'HOURS', 'HR', 'HRS', 'HR_Z', 'HR_Z2'],
    'MILLISECONDS': ['millisecond', 'milliseconds', 'ms', 'Millisecond', 'Milliseconds', 'MS', 'MS_Z'],
    'MINUTES': ['minute', 'minutes', 'min', 'mins', 'm(?!s)', 'Minute', 'Minutes', 'Min', 'Mins', 'MIN', 'MINS', 'M',
                'M_Z'],
    'MONTHS': ['month', 'months', 'mon', 'mo', 'mth', 'mths', 'Month', 'Months', 'Mon', 'Mo', 'MONTH', 'MONTHS', 'MTH',
               'MTHS', 'MO_Z', 'MO_Z2', 'MO_Z3', 'MO_Z4', 'MO_Z5', 'MO_Z6', 'MO_Z7'],
    'SECONDS': ['second', 'seconds', 'sec', 's', 'Second', 'Seconds', 'Sec', 'S', 'SECOND', 'SECONDS', 'SEC', 'S_Z',
                'S_Z2'],
    'WEEKS': ['week', 'weeks', 'wk', 'w', 'Week', 'Weeks', 'Wk', 'W', 'WEEK', 'WEEKS', 'WK', 'WKS', 'WK_Z'],
    'YEARS': ['year', 'years', 'yr', 'y', 'Year', 'Years', 'Yr', 'Y', 'YEAR', 'YEARS', 'YR', 'YRS', 'YR_Z'],
}


# export function parseDuration(durationInput: string | undefined): Duration {
def _parse_duration(duration_input: Optional[str]) -> datetime.timedelta:
    # IMPORTANT: Mirrors the behavior used by sharedDefinitionFunctions.ts from parseDuration() in
    # client/packages/webserver/app/src/datetime/dateTime.utilities.ts.

    # const invalidDuration = moment.duration(0);
    invalid_duration = datetime.timedelta(0)
    # if (durationInput === undefined) {
    if duration_input is None:
        # return invalidDuration;
        return invalid_duration
    # }
    # const trimmedInput = _.trim(durationInput);
    trimmed_input = duration_input.strip()
    # if (isNaN(Number(trimmedInput[0]))) {
    # Indexing past the end of an empty string yields undefined in JavaScript, and Number(undefined) is NaN. Only
    # ASCII digits are accepted because Number() rejects the non-ASCII digits that str.isdigit() would allow.
    if not trimmed_input or trimmed_input[0] not in '0123456789':
        # return invalidDuration;
        return invalid_duration
    # }
    #
    # const rawPatterns = i18next.t('DURATION_PATTERNS', { returnObjects: true }) as unknown;
    # const patterns: Record<string, string[]> =
    #   rawPatterns && typeof rawPatterns === 'object' ? (rawPatterns as Record<string, string[]>) : {};
    patterns = _DURATION_PATTERNS
    #
    # const matches: string[] = [];
    matches = []
    # const durationInSeconds: number = _.reduce(
    #   DURATION_CONVERSIONS,
    #   (total, multiplier, key): number => {
    duration_in_seconds = 0
    for key, multiplier in _DURATION_CONVERSIONS.items():
        #     // @ts-ignore Can't figure out how to get the type right here
        #     const patternList = Array.isArray(patterns[key]) ? patterns[key]! : [];
        pattern_list = patterns.get(key) or []
        #     for (const pattern of patternList) {
        for pattern in pattern_list:
            #       const regex = new RegExp(`((\\d+\\.\\d+)|\\d+)\\s?(${pattern}(?=\\s|\\d|$))`, 'gi');
            regex = re.compile(f'((\\d+\\.\\d+)|\\d+)\\s?({pattern}(?=\\s|\\d|$))', re.IGNORECASE)
            #       for (const match of durationInput.matchAll(regex)) {
            matched_unit = False
            for match in regex.finditer(duration_input):
                #         if (!_.includes(matches, match[0])) {
                if match.group(0) not in matches:
                    #           matches.push(match[0]);
                    matches.append(match.group(0))
                    #           return total + parseFloat(match[1]) * multiplier;
                    # Returning from the iteratee stops this unit after its first new match.
                    duration_in_seconds += float(match.group(1)) * multiplier
                    matched_unit = True
                    break
                #         }
            #       }
            if matched_unit:
                break
        #     }
        #
        #     return total;
        #   },
        #   0,
        # );
    #
    # if (_.isEmpty(matches)) {
    if not matches:
        # return invalidDuration;
        return invalid_duration
    # } else {
    else:
        # return moment.duration(durationInSeconds, 'seconds');
        return datetime.timedelta(seconds=duration_in_seconds)
    # }
    # }


# export const extractOffsetAndDirectionFromFormula = (formula = ''): [{ value?: number; units?: string }, string] => {
def _extract_offset_and_direction_from_formula(formula: str = '') -> Tuple[Dict[str, Union[int, float, str]], str]:
    # IMPORTANT: Mirrors extractOffsetAndDirectionFromFormula() in
    # client/packages/webserver/app/src/utilities/sharedDefinitionFunctions.ts.

    # const formulaOffset = formula.match(/[+-](.*?)[-](.*?)(\$now)(.*)/)![4];
    formula_offset = re.search(r'[+-](.*?)[-](.*?)(\$now)(.*)', formula).group(4)
    # const match = formulaOffset.match(/((\d+(?:\.\d+)?)(\w+))/);
    match = re.search(r'((\d+(?:\.\d+)?)(\w+))', formula_offset)
    # const value = toNumber(match![2]);
    value = _to_number(match.group(2))

    # const units = match![3];
    units = match.group(3)
    # const offset = { value, units };
    offset = {'value': value, 'units': units}
    #
    # const offsetDirection = formulaOffset.match(/[+-]/)![0] === '-' ? OFFSET_DIRECTION.PAST : OFFSET_DIRECTION.FUTURE;
    offset_direction = (OFFSET_DIRECTION.PAST if re.search(r'[+-]', formula_offset).group(0) == '-' else
                        OFFSET_DIRECTION.FUTURE)
    #
    # return [offset, offsetDirection];
    return offset, offset_direction
    # };
