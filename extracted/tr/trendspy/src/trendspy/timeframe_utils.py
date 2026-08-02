__all__ = ['convert_timeframe', 'timeframe_to_timedelta', 'verify_consistent_timeframes']

import re
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from typing import Any
from .utils import ensure_list
# Regular expression pattern to validate date strings in the format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH'
VALID_DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}(T\d{2})?$'

# Set of fixed timeframes supported by an external API
FIXED_TIMEFRAMES = {'now 1-H', 'now 4-H', 'now 1-d', 'now 7-d', 'today 1-m', 'today 3-m', 'today 5-y', 'today 12-m', 'all'}

# Date format strings for standard and datetime with hour formats
DATE_FORMAT = "%Y-%m-%d"
DATE_T_FORMAT = "%Y-%m-%dT%H"

# Regular expression pattern to validate offset strings like '10-d', '5-H', etc.
OFFSET_PATTERN = r'\d+[-]?[Hdmy]$'

# Mapping of units (H, d, m, y) to relativedelta arguments
UNIT_MAP = {'H': 'hours', 'd': 'days', 'm': 'months', 'y': 'years'}


def _is_valid_date(date_str):
	# Checks if the given string matches the valid date pattern
	return bool(re.match(VALID_DATE_PATTERN, date_str))


def _is_valid_format(offset_str):
	# Checks if the given string matches the valid offset pattern
	return bool(re.match(OFFSET_PATTERN, offset_str))


def _extract_time_parts(offset_str):
	# Extracts numerical value and unit (H, d, m, y) from the offset string
	match = re.search(r'(\d+)[-]?([Hdmy]+)', offset_str)
	if match:
		return int(match.group(1)), match.group(2)
	return None


def _decode_trend_datetime(date_str):
	# Parses the date string into a datetime object based on whether it includes time ('T' character)
	return datetime.strptime(date_str, DATE_T_FORMAT) if 'T' in date_str else datetime.strptime(date_str, DATE_FORMAT)


def _process_two_dates(date_part_1, date_part_2):
	isT1 = 'T' in date_part_1
	isT2 = 'T' in date_part_2
	if (not isT1) and (not isT2):
		return f'{date_part_1} {date_part_2}'

	# Processes two date parts and returns the formatted result
	date_1 = _decode_trend_datetime(date_part_1)
	date_2 = _decode_trend_datetime(date_part_2)

	# Adjust date formatting if only one of the dates includes hour information
	if (isT1) and (not isT2):
		date_2 += timedelta(days=1)
		date_2 = date_2.replace(hour=0)
	elif (not isT1) and (isT2):
		date_1 = date_1.replace(hour=0)

	# Ensure the difference between dates does not exceed 7 days when time information is included
	if ('T' in date_part_1 or 'T' in date_part_2) and abs((date_1 - date_2).days) > 7:
		raise ValueError(f'Date difference cannot exceed 7 days for format with hours: {date_part_1} {date_part_2}')

	# Return the formatted result with both dates including hours
	return f'{date_1.strftime(DATE_T_FORMAT)} {date_2.strftime(DATE_T_FORMAT)}'


def _process_date_with_offset(date_part_1, offset_part):
	# Processes a date part with an offset to calculate the resulting timeframe
	date_1 = _decode_trend_datetime(date_part_1)
	count, unit = _extract_time_parts(offset_part)

	# Calculate the offset using relativedelta
	raw_diff = relativedelta(**{UNIT_MAP[unit]: count})
	if unit in {'m', 'y'}:
		# Special handling for months and years: adjust based on the current UTC date
		now = datetime.now(timezone.utc)
		end_date = now - raw_diff
		raw_diff = now - end_date

	# Raise an error if the offset exceeds 7 days for formats that include time
	if 'T' in date_part_1 and ((unit == 'd' and count > 7) or (unit == 'H' and count > 7 * 24)):
		raise ValueError(f'Offset cannot exceed 7 days for format with time: {date_part_1} {offset_part}. Use YYYY-MM-DD format or "today".')

	# Determine the appropriate date format based on the unit (hours/days or months/years)
	date_format = DATE_T_FORMAT if 'T' in date_part_1 else DATE_FORMAT
	return f'{(date_1 - raw_diff).strftime(date_format)} {date_1.strftime(date_format)}'


def convert_timeframe(timeframe, convert_fixed_timeframes_to_dates=False):
	"""
	Converts timeframe strings to Google Trends format.

	Supports multiple formats:
	1. Fixed timeframes ('now 1-H', 'today 12-m', etc.)
	2. Date ranges ('2024-01-01 2024-12-31')
	3. Date with offset ('2024-03-25 5-m')
	4. Hour-specific ranges ('2024-03-25T12 2024-03-25T15')

	Parameters:
		timeframe (str): Input timeframe string
		convert_fixed_timeframes_to_dates (bool): Convert fixed timeframes to dates

	Returns:
		str: Converted timeframe string in Google Trends format

	Raises:
		ValueError: If timeframe format is invalid
	"""
	# If the timeframe is in the fixed set and conversion is not requested, return as is
	if (timeframe in FIXED_TIMEFRAMES) and (not convert_fixed_timeframes_to_dates):
		return timeframe
	
	# Replace 'now' and 'today' with the current datetime in the appropriate format
	utc_now = datetime.now(timezone.utc)
	if convert_fixed_timeframes_to_dates and timeframe=='all':
		return '2024-01-01 {}'.format(utc_now.strftime(DATE_FORMAT))

	timeframe = timeframe.replace('now', utc_now.strftime(DATE_T_FORMAT)).replace('today', utc_now.strftime(DATE_FORMAT))

	# Split the timeframe into two parts
	parts = timeframe.split()
	if len(parts) != 2:
		raise ValueError(f"Invalid timeframe format: {timeframe}. Expected format: '<date> <offset>' or '<date> <date>'.")

	date_part_1, date_part_2 = parts

	# Process the timeframe based on its parts
	if _is_valid_date(date_part_1):
		if _is_valid_date(date_part_2):
			# Process if both parts are valid dates
			return _process_two_dates(date_part_1, date_part_2)
		elif _is_valid_format(date_part_2):
			# Process if the second part is a valid offset
			return _process_date_with_offset(date_part_1, date_part_2)

	raise ValueError(f'Could not process timeframe: {timeframe}')

def timeframe_to_timedelta(timeframe):
	result = convert_timeframe(timeframe, convert_fixed_timeframes_to_dates=True)
	date_1, date_2 = result.split()
	datetime_1 = _decode_trend_datetime(date_1)
	datetime_2 = _decode_trend_datetime(date_2)
	return (datetime_2 - datetime_1)

def verify_consistent_timeframes(timeframes):
	"""
	Verifies that all timeframes have consistent resolution.

	Google Trends requires all timeframes in a request to have the same
	data resolution (e.g., hourly, daily, weekly).

	Parameters:
		timeframes (list): List of timeframe strings

	Returns:
		bool: True if timeframes are consistent

	Raises:
		ValueError: If timeframes have different resolutions
	"""
	if isinstance(timeframes, str):
		return True

	timedeltas = list(map(timeframe_to_timedelta, timeframes))
	if all(td == timedeltas[0] for td in timedeltas):
		return True
	else:
		raise ValueError(f"Inconsistent timeframes detected: {[str(td) for td in timedeltas]}")

# Define the mapping between time range, resolution, and its range
def get_resolution_and_range(timeframe):
	delta = timeframe_to_timedelta(timeframe)
	if delta < timedelta(hours=5):
		return "1 minute", "delta < 5 hours"
	elif delta < timedelta(hours=36):
		return "8 minutes", "5 hours <= delta < 36 hours"
	elif delta < timedelta(hours=72):
		return "16 minutes", "36 hours <= delta < 72 hours"
	elif delta < timedelta(days=8):
		return "1 hour", "72 hours <= delta < 8 days"
	elif delta < timedelta(days=270):
		return "1 day", "8 days <= delta < 270 days"
	elif delta < timedelta(days=1900):
		return "1 week", "270 days <= delta < 1900 days"
	else:
		return "1 month", "delta >= 1900 days"

# Function to check if all timeframes have the same resolution
def check_timeframe_resolution(timeframes):
	timeframes = ensure_list(timeframes)
	resolutions = list(map(get_resolution_and_range, timeframes))

	# Extract only resolutions (without ranges) to check if they are the same
	resolution_values = [r[0] for r in resolutions]

	# Check if all resolutions are the same
	deltas = [timeframe_to_timedelta(timeframe) for timeframe in timeframes]
	if len(set(resolution_values)) > 1:
		# If there are differences, output an error message with details
		error_message = "Error: Different resolutions detected for the timeframes:\n"
		for timeframe, delta, (resolution, time_range) in zip(timeframes, deltas, resolutions):
			error_message += (
				f"Timeframe: {timeframe}, Delta: {delta}, "
				f"Resolution: {resolution} (based on range: {time_range})\n"
			)
		raise ValueError(error_message)
	
	min_delta, min_timeframe = min(zip(deltas, timeframes))
	max_delta, max_timeframe = max(zip(deltas, timeframes))
	
	if max_delta >= min_delta * 2:
		raise ValueError(
			f"Error: The maximum delta {max_delta} (from timeframe {max_timeframe}) "
			f"should be less than twice the minimum delta {min_delta} (from timeframe {min_timeframe})."
		)