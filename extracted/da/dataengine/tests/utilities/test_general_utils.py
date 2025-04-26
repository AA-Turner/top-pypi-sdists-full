import datetime
import tarfile
import io
import pytest
import numpy as np
from dataengine.utilities import general_utils


def test_get_date_range():
    # Test when date_0 and date_1 are the same
    date_0 = date_1 = datetime.date(2021, 1, 1)
    assert general_utils.get_date_range(date_0, date_1) == [
        datetime.date(2021, 1, 1)]
    # Test when date_1 is later than date_0
    date_0 = datetime.date(2021, 1, 1)
    date_1 = datetime.date(2021, 1, 3)
    assert general_utils.get_date_range(date_0, date_1) == [
        datetime.date(2021, 1, 1), datetime.date(2021, 1, 2),
        datetime.date(2021, 1, 3)]
    # Test when date_0 is later than date_1
    date_0 = datetime.date(2021, 1, 3)
    date_1 = datetime.date(2021, 1, 1)
    assert general_utils.get_date_range(date_0, date_1) == []


def test_leading_zero():
    # Test when hour is a single-digit integer
    assert general_utils.leading_zero(1) == "01"
    assert general_utils.leading_zero(9) == "09"
    # Test when hour is a two-digit integer
    assert general_utils.leading_zero(10) == "10"
    assert general_utils.leading_zero(23) == "23"
    # Test when hour is a single-digit string
    assert general_utils.leading_zero('1') == "01"
    assert general_utils.leading_zero('9') == "09"
    # Test when hour is a two-digit string
    assert general_utils.leading_zero('10') == "10"
    assert general_utils.leading_zero('23') == "23"
    # Test when hour is the special character "*"
    assert general_utils.leading_zero('*') == "*"


def test_get_dt_range():
    # Test 1: Default parameters (1 day forward)
    dt = datetime.datetime(2022, 1, 1, 0, 0)
    assert general_utils.get_dt_range(dt) == [
        dt + datetime.timedelta(hours=i) for i in range(24)]
    # Test 2: days specified
    assert general_utils.get_dt_range(dt, days=2) == [
        dt + datetime.timedelta(hours=i) for i in range(48)]
    # Test 3: hours specified
    assert general_utils.get_dt_range(dt, days=0, hours=3) == [
        dt + datetime.timedelta(hours=i) for i in range(3)]
    # Test 4: days and hours specified
    assert general_utils.get_dt_range(dt, days=1, hours=1) == [
        dt + datetime.timedelta(hours=i) for i in range(25)]
    # Test 5: weeks specified
    assert general_utils.get_dt_range(dt, weeks=1) == [
        dt - datetime.timedelta(weeks=i) for i in range(1, 2)]
    # Test 6: Negative days
    assert general_utils.get_dt_range(dt, days=-1) == [
        dt - datetime.timedelta(hours=i) for i in range(24)]
    # Test 7: Negative hours
    assert general_utils.get_dt_range(dt, days=0, hours=-3) == [
        dt - datetime.timedelta(hours=i) for i in range(3)]
    # Test 8: Hours set to "*"
    dt = datetime.datetime(2022, 1, 1, 0, 0)
    assert general_utils.get_dt_range(dt, days=0, hours="*") == [
        datetime.datetime(2022, 1, 1, i, 0) for i in range(24)]
    # Test 9: Both days, hours, and weeks set to 0
    assert general_utils.get_dt_range(dt, days=0, hours=0, weeks=0) == [dt]


def test_exclude_hours_from_range():
    dt = datetime.datetime(2022, 1, 1, 0, 0)
    dt_range = [dt + datetime.timedelta(hours=i) for i in range(24)]
    # Test 1: Empty dt_range
    assert general_utils.exclude_hours_from_range([], ["1"]) == []
    # Test 2: Empty exclude_hours
    assert general_utils.exclude_hours_from_range(dt_range, []) == dt_range
    # Test 3: Single digits in exclude_hours
    assert general_utils.exclude_hours_from_range(dt_range, ["1", "2"]) == [
        dt + datetime.timedelta(hours=i) for i in range(24) if i not in [1, 2]]
    # Test 4: Ranges in exclude_hours
    assert general_utils.exclude_hours_from_range(dt_range, ["1-3"]) == [
        dt + datetime.timedelta(hours=i) for i in range(24)
        if i not in [1, 2, 3]]
    # Test 5: Mixed single digits and ranges in exclude_hours
    assert general_utils.exclude_hours_from_range(dt_range, ["1", "3-5"]) == [
        dt + datetime.timedelta(hours=i) for i in range(24)
        if i not in [1, 3, 4, 5]]
    # Test 6: Exclude all hours
    assert general_utils.exclude_hours_from_range(dt_range, ["0-23"]) == []


def test_create_time_string():
    # Test 1: Zero total time
    assert general_utils.create_time_string(0) == "0 seconds"
    # Test 2: Less than 60 seconds
    assert general_utils.create_time_string(30) == "30 seconds"
    # Test 3: Exactly 60 seconds
    assert general_utils.create_time_string(60) == "1 minute"
    # Test 4: More than 60 seconds but less than 120
    assert general_utils.create_time_string(90) == "1 minute and 30 seconds"
    # Test 5: More than 120 seconds
    assert general_utils.create_time_string(150) == "2 minutes and 30 seconds"
    # Test 6: Negative total time
    assert general_utils.create_time_string(-30) == "-30 seconds"
    # Test 7: Total time as a string
    assert general_utils.create_time_string("150") == "2 minutes and 30 seconds"
    # Test 8: Invalid string input
    assert general_utils.create_time_string("invalid") == "0 seconds"
    # Test 9: Invalid type input
    assert general_utils.create_time_string([150]) == "0 seconds"


def test_apply_time_delta():
    base_dt = datetime.datetime(2023, 9, 16, 12, 0, 0)
    # Test 1: When hour is a glob "*"
    new_dt, new_hour = general_utils.apply_time_delta(
        base_dt, "*", {"days": 1, "hours": 2})
    assert new_dt == datetime.datetime(2023, 9, 15, 12, 0, 0)
    assert new_hour == "*"
    # Test 2: When hour is a specific hour
    new_dt, new_hour = general_utils.apply_time_delta(
        base_dt, "15", {"days": 1, "hours": 2})
    assert new_dt == datetime.datetime(2023, 9, 15, 13, 0, 0)
    assert new_hour == 13
    # Test 3: When time_delta only contains "days"
    new_dt, new_hour = general_utils.apply_time_delta(
        base_dt, "15", {"days": 1})
    assert new_dt == datetime.datetime(2023, 9, 15, 15, 0, 0)
    assert new_hour == 15
    # Test 4: When time_delta only contains "hours"
    new_dt, new_hour = general_utils.apply_time_delta(
        base_dt, "15", {"hours": 1})
    assert new_dt == datetime.datetime(2023, 9, 16, 14, 0, 0)
    assert new_hour == 14
    # Test 5: When time_delta contains both "days" and "hours"
    new_dt, new_hour = general_utils.apply_time_delta(
        base_dt, "15", {"days": 1, "hours": 1})
    assert new_dt == datetime.datetime(2023, 9, 15, 14, 0, 0)
    assert new_hour == 14



def test_get_dict_permutations():
    # Test 1: When input dictionary is empty
    assert general_utils.get_dict_permutations({}) == [{}]
    # Test 2: When input dictionary has keys but all values are empty lists
    assert general_utils.get_dict_permutations({"a": [], "b": []}) == []
    # Test 3: When input dictionary contains single-value lists
    assert general_utils.get_dict_permutations(
        {"a": [1], "b": [2]}) == [{"a": 1, "b": 2}]
    # Test 4: When input dictionary contains multi-value lists
    assert general_utils.get_dict_permutations(
        {"a": [1, 2], "b": [3, 4]}) == [
            {"a": 1, "b": 3},
            {"a": 1, "b": 4},
            {"a": 2, "b": 3},
            {"a": 2, "b": 4}]
    # Test 5: When input dictionary contains a mix of single and multi-value lists
    assert general_utils.get_dict_permutations({"a": [1], "b": [3, 4]}) == [
        {"a": 1, "b": 3},
        {"a": 1, "b": 4}]
    # Test 6: When input dictionary contains non-list values
    assert general_utils.get_dict_permutations(
        {"a": 1, "b": 2}) == [{"a": 1, "b": 2}]


def test_pooled_stddev():
    # Test 1: When both stddevs and sample_sizes are empty arrays
    assert np.isnan(general_utils.pooled_stddev(np.array([]), np.array([])))
    # Test 2: When stddevs and sample_sizes have different lengths
    assert np.isnan(
        general_utils.pooled_stddev(np.array([1.0, 2.0]), np.array([10])))
    # Test 3: When stddevs and sample_sizes have same length and sample_sizes
    # include elements less than 2
    assert np.isclose(
        general_utils.pooled_stddev(np.array([1.0, 2.0]), np.array([1, 10])),
        np.sqrt((0 * 1 + 9 * 4) / (1 + 10 - 2)),
        atol=1e-9)
    # Test 4: When stddevs and sample_sizes have same length and all elements
    # in sample_sizes are at least 2
    assert np.isclose(
        general_utils.pooled_stddev(np.array([2.0, 3.0]), np.array([4, 5])),
        np.sqrt((3 * 4 + 4 * 9) / (4 + 5 - 2)),
        atol=1e-9)


def test_read_tar_from_bytes():
    # Create a tar archive in memory with some test files
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        file_data1 = "Hello, world!".encode('utf-8')
        file_data2 = "Python is awesome.".encode('utf-8')
        file1 = tarfile.TarInfo(name='file1.txt')
        file1.size = len(file_data1)
        file2 = tarfile.TarInfo(name='file2.txt')
        file2.size = len(file_data2)
        tar.addfile(file1, io.BytesIO(file_data1))
        tar.addfile(file2, io.BytesIO(file_data2))
    # Get the byte content of the tar archive
    tar_bytes = tar_stream.getvalue()
    # Call the function to read the tar archive
    result = general_utils.read_tar_from_bytes(tar_bytes)
    # Check that the function correctly reads the files in the tar archive
    assert result['file1.txt'] == 'Hello, world!'
    assert result['file2.txt'] == 'Python is awesome.'


def test_write_dict_to_tar_bytes():
    # Create a dictionary with file names and contents
    file_dict = {
        'file1.txt': 'Hello, world!',
        'file2.txt': 'Python is awesome.'
    }
    # Call the function to write the dictionary to a tar archive
    tar_bytes = general_utils.write_dict_to_tar_bytes(file_dict)
    # Read the tar archive using the read_tar_from_bytes function
    result = general_utils.read_tar_from_bytes(tar_bytes)
    # Check that the function correctly writes the files to the tar archive
    assert result['file1.txt'] == 'Hello, world!'
    assert result['file2.txt'] == 'Python is awesome.'
