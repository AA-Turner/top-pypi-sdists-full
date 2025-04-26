"""
Utility metohds that aren't directly related to some sort of software package
or service.
"""
import tarfile
import io
import re
import datetime
import dateutil
import itertools
import logging
import math
import numpy as np
from scipy.stats import shapiro, normaltest
from marshmallow import fields, ValidationError


def format_dt(date_str):
    """
    Setup datetime given date string with or without leading zeros.

    Args:
        date_str (str): date string (e.g., 'YYYY-M-D' or 'YYYY-MM-DD')

    Returns:
        datetime object
    """
    try:
        # Use dateutil.parser to handle different date formats
        return dateutil.parser.parse(date_str)
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD."
        ) from e


class StringOrListField(fields.Field):
    """
    Custom Marshmallow field for handling a field that can be either a single
    string or a list of strings.
    
    Raises:
        ValidationError:
            If the field is neither a string nor a list of strings.
    """
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            return value
        elif (
            isinstance(value, list) and
            all(isinstance(x, str) for x in value)
        ):
            return value
        else:
            raise ValidationError(
                "Field should be either a string or a list of strings.")


def get_date_range(date_0, date_1):
    """
    This method creates a list of dates from d0 to d1.

    Args:
        date_0 (datetime.date): start date
        date_1 (datetime.date): end date

    Returns:
        date range
    """
    return [
        date_0 + datetime.timedelta(days=i)
        for i in range((date_1 - date_0).days + 1)]


def leading_zero(hour):
    """
    This method will generate an hour str with a leading zero.

    Args:
        hour (int|str): hour

    Returns:
        leading zero digit str
    """
    str_hour = str(hour)
    if ((len(str_hour) == 1) and (str_hour != "*")):
        str_hour = "0" + str_hour

    return str_hour


def get_dt_range(dt, days=1, hours=0, weeks=0):
    """
    This method will generate the datetime range between the provided datetime
    and days / hours. Subtract hours / days when negative, otherwise add
    them.

    Args:
        dt (datetime.datetime): input datetime
        days (int): number of days
        hours (int): number of hours

    Returns:
        date range list
    """
    # If both values passed in are 0 return input datetime
    if (days == 0) and (hours == 0) and (weeks == 0):
        logging.error("Both days, hours, and weeks arguments were all 0.")
        return [dt]
    # If hour passed in is the glob character adjust accordingly
    if hours == "*":
        # If days are negative set the dt hour to 23
        if days < 0:
            dt = datetime.datetime(dt.year, dt.month, dt.day, 23)
        # Set hours to 0
        hours = 0
        # Set days to 1 if 0 was passed in
        days = (1 if days == 0 else days)
    # If weeks is setup grab trailing weeks
    if weeks != 0:
        dt_range = [
            dt - datetime.timedelta(weeks=minus_week)
            for minus_week in range(1, weeks + 1)]
    else:
        # Combine days and hours
        total_hours = (24 * days) + hours
        # Get dt range
        if total_hours < 0:
            dt_range = [
                dt - datetime.timedelta(hours=hour)
                for hour in range(abs(total_hours))]
        else:
            dt_range = [
                dt + datetime.timedelta(hours=hour)
                for hour in range(total_hours)]

    return dt_range


def exclude_hours_from_range(dt_range, exclude_hours):
    """
    This method will take a list of strings, convert them to a list of
    integers, then remove all datetimes from the range where the hour
    matches any in the list of integers.

    Args:
        dt_range (list): list of datetimes
        exclude_hours (list): list of strings

    Returns:
        modified list with hours excluded
    """
    hours = []
    # Assemble list of hours
    for arg in exclude_hours:
        # If the type is an int just add it to the list
        if isinstance(arg, int):
            hours.append(arg)
        # Otherwise check if the argument is a string
        elif isinstance(arg, str):
            # If the argument string of digits, cast to int first
            if re.compile(r"[0-9]+").fullmatch(arg):
                hours.append(int(arg))
            # If the argument is a range of digits parse the range and add it
            elif re.compile(r"[0-9]+-[0-9]+").fullmatch(arg):
                start, end = [int(i) for i in arg.split("-")]
                hours += list(range(start, end + 1))
    # Update the dt range to exclude these hours and return
    return [i for i in dt_range if i.hour not in hours]


def create_time_string(total_seconds):
    """
    This method will create a time string given total seconds.

    Args:
        total_seconds (int|str): total time in seconds

    Returns:
        time string
    """
    # If the input is a string cast to an int
    if (
        isinstance(total_seconds, str) and
        re.compile(r"-*[0-9]+").fullmatch(total_seconds)
    ):
        total_seconds = int(total_seconds)
    # If total_seconds is still not an int set it to zero
    if not isinstance(total_seconds, int):
        total_seconds = 0
    # Determine whether total seconds is negative
    is_negative = total_seconds < 0
    # Take the absolute value of total seconds
    total_seconds = abs(total_seconds)
    # Break down the total seconds into minutes and seconds
    minutes = math.floor(total_seconds / 60.0)
    seconds = total_seconds % 60
    # Format the final string
    minutes_str = "{minutes} minute{s}".format(
        minutes=minutes, s="s" * (minutes != 1))
    seconds_str = "{seconds} second{s}".format(
        seconds=seconds, s="s" * (seconds != 1))
    time_str = (
        "-" * is_negative +
        minutes_str * (minutes != 0) +
        " and " * (minutes != 0 and seconds != 0) +
        seconds_str * (not (seconds == 0 and minutes > 0)))

    return time_str


def apply_time_delta(dt, hour, time_delta):
    """
    This method will apply the time delta arguments to the dt and hour
    objects needed for formatting dataset paths.

    Args:
        dt (datetime.datetime): datetime object
        hour (str): either the hour or a glob of all hours
        time_delta (dict): dict with hours and days fields

    Returns:
        new modified datetime and hour objects
    """
    # If hour is glob only consider time delta day arguments
    if hour == "*":
        td = datetime.timedelta(
            **{k: v for k, v in time_delta.items() if k == "days"})
        new_dt = dt - td
        new_hour = hour
    # Otherwise cast hour to int, setup dt, and subtract full time delta
    else:
        td = datetime.timedelta(**time_delta)
        new_dt = datetime.datetime(dt.year, dt.month, dt.day, int(hour)) - td
        new_hour = new_dt.hour

    return new_dt, new_hour


def get_dict_permutations(raw_dict):
    """
    This method will take a raw dictionary and create all unique
    permutations of key value pairs.

    Source: https://codereview.stackexchange.com/questions/171173

    Args:
        raw_dict (dict): raw dictionary

    Returns:
        list of unique key value dict permutations
    """
    # Set default
    dict_permutations = [{}]
    # Check whether input is valid nonempty dictionary
    if isinstance(raw_dict, dict) and (len(raw_dict) > 0):
        # Make sure all values are lists
        dict_of_lists = {}
        for key, value in raw_dict.items():
            if not isinstance(value, list):
                dict_of_lists[key] = [value]
            else:
                dict_of_lists[key] = value
        # Create all unique permutations
        keys, values = zip(*dict_of_lists.items())
        dict_permutations = [
            dict(zip(keys, v)) for v in itertools.product(*values)]

    return dict_permutations


def pooled_stddev(stddevs, sample_sizes):
    """
    This method will calculate the pooled standard deviation across a
    group of samples given each samples standard deviation and size.

    Source: https://www.statisticshowto.com/pooled-standard-deviation/

    Args:
        stddevs (numpy.ndarray): standard deviations of samples
        sample_sizes (numpy.ndarray): samples sizes

    Returns:
        pooled stddev
    """
    # Return null if both arrays are empty or different lengths
    if (
        not(stddevs.any() and sample_sizes.any()) or
        (len(stddevs) != len(sample_sizes))
    ):
        return np.nan
    # Otherwise calculate the pooled standard deviation
    return np.sqrt(np.sum([
        (sample_sizes[i] - 1) * np.power(stddevs[i], 2)
        for i in range(len(sample_sizes))
    ]) / (np.sum(sample_sizes) - len(sample_sizes)))


def test_normal(values, alpha=0.05):
    """
    This method will test whether distributions are guassian.
    TODO: This needs to be flipped

    Args:
        values (np.array):

    Return:
        boolean result
    """
    _, shapiro_p = shapiro(values)
    _, normal_p = normaltest(values)

    return np.all([p < alpha for p in (shapiro_p, normal_p)])


def read_tar_from_bytes(tar_bytes):
    """
    Reads a tar archive from a bytes object and returns a dictionary.
    The dict keys are file names and values are the file content as strings.
    
    Parameters:
        tar_bytes (bytes): The bytes object containing the tar archive.
        
    Returns:
        dict: A dictionary with file names as keys and file content as values.
    """
    file_contents = {}
    # Create a BytesIO object from the bytes
    tar_stream = io.BytesIO(tar_bytes)
    # Open the tar file from the BytesIO stream
    with tarfile.open(fileobj=tar_stream) as tar:
        # Loop over each file in the archive
        for member in tar.getmembers():
            # Make sure it's actually a file (not a directory, etc.)
            if member.isfile():
                # Extract the file object
                f = tar.extractfile(member)
                # Read the file content and decode it to string
                file_contents[member.name] = f.read().decode("latin1")
                
    return file_contents


def write_dict_to_tar_bytes(file_dict):
    """
    Writes a dictionary to a tar archive as a bytes object.
    The dictionary keys are treated as file names, and the values as file content.
    
    Parameters:
        file_dict (dict): A dictionary with file names as keys and file content as values.
        
    Returns:
        bytes: The bytes object containing the tar archive.
    """
    tar_stream = io.BytesIO()
    # Create a tar archive in memory
    with tarfile.open(fileobj=tar_stream, mode='w:gz') as tar:
        for file_name, file_content in file_dict.items():
            # Convert string content to bytes
            file_data = file_content.encode("latin1")
            # Create a TarInfo object for the file
            file_info = tarfile.TarInfo(name=file_name)
            file_info.size = len(file_data)
            # Add the file to the tar archive
            tar.addfile(file_info, io.BytesIO(file_data))
    # Return the byte content of the tar archive
    return tar_stream.getvalue()


def extract_formatting_variables(format_string):
    """
    Extract string formatting variables from a format string.

    Args:
        format_string (str): The format string to extract variables from.

    Returns:
        list: A list of extracted formatting variables.
    """
    # Matches {variable}, {dt.attribute}, and {dt:format}
    pattern = r"{(\w+(?:\.\w+|:[^}]+)?)}"
    variables = re.findall(pattern, format_string)
    # Simplify object references
    simplified_variables = []
    for var in variables:
        if (
            ('.' in var) or (':' in var)
        ):
            obj = var.split('.')[0].split(':')[0]
            simplified_variables.append(obj)
        else:
            simplified_variables.append(var)
    # Remove duplicates
    return list(set(simplified_variables))
