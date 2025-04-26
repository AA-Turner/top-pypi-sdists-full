import re
import ipaddress
import pytest
from dataengine.utilities import redact_utils


@pytest.mark.parametrize("test_input", [
    "00:1A:2B:3C:4D:5E",
    "00-1A-2B-3C-4D-5E",
    "a0:b1:c2:d3:e4:f5",
    "A0:B1:C2:D3:E4:F5",
    "A0B1C2D3E4F5"
])
def test_mac_regex_positive_cases(test_input):
    """Test cases that should match the MAC address regex."""
    assert redact_utils.MAC_REGEX.fullmatch(test_input) is not None


@pytest.mark.parametrize("test_input", [
    "00:1A:2B:3C:4D",
    "00-1A-2B-3C",
    "001A2B3C4D",
    "00;1A;2B;3C;4D;5E",
    "A0:B1:C2:D3:E4:G5",
    "A0:B1-C2:D3:E4-F5",
    "20230718-0426",
    "1234567890123"
])
def test_mac_regex_negative_cases(test_input):
    """Test cases that should not match the MAC address regex."""
    assert redact_utils.MAC_REGEX.fullmatch(test_input) is None


@pytest.mark.parametrize("mac_address,expected", [
    # Test with a generated local MAC address
    (redact_utils.generate_random_local_mac(), True),
    # Test with a known local MAC address
    ("01:23:45:67:89:AB", True),
    # Test with a known non-local MAC address
    ("00:23:45:67:89:AB", False),
])
def test_local_mac_regex(mac_address, expected):
    # Check if the MAC address matches the regex
    if expected:
        assert (
            redact_utils.LOCAL_MAC_REGEX.fullmatch(mac_address) is not None,
            f"MAC address {mac_address} did not match the regex")
    else:
        assert (
            redact_utils.LOCAL_MAC_REGEX.fullmatch(mac_address) is None,
            f"MAC address {mac_address} incorrectly matched the regex")


@pytest.mark.parametrize("mac_input, mac_to_match, expected", [
    # Basic tests for matching MAC address in different formats
    ("AA:BB:CC:DD:EE:FF", "AA:BB:CC:DD:EE:FF", True),
    ("AA:BB:CC:DD:EE:FF", "AA-BB-CC-DD-EE-FF", True),
    ("AA:BB:CC:DD:EE:FF", "aabbccddeeff", True),
    
    # Case-insensitivity tests
    ("aa:bb:cc:dd:ee:ff", "AA:BB:CC:DD:EE:FF", True),
    ("AA:BB:CC:DD:EE:FF", "aa:bb:cc:dd:ee:ff", True),
    
    # Tests for invalid inputs
    ("AA:BB:CC:DD:EE:FF", "invalid_mac_address", False),
    ("AA:BB:CC:DD:EE:FF", "AA:BB:CC:DD:EE", False),
    ("AA:BB:CC:DD:EE:FF", "AA:BB:CC:DD:EE:FG", False)
])
def test_generate_mac_regex(mac_input, mac_to_match, expected):
    pattern = redact_utils.generate_mac_regex(mac_input)
    assert bool(pattern.match(mac_to_match)) == expected


@pytest.mark.parametrize("input_word, expected_output", [
    ("1234", "1234"),
    ("0045", "0{0,2}45"),
    ("0000", "0{1,4}"),
    ("0", "0"),
    ("", ""),
    ("abcd", "abcd"),
    ("00ab", "0{0,2}ab")
])
def test_left_pad_zeros(input_word, expected_output):
    assert redact_utils.left_pad_zeros(input_word) == expected_output


def test_generate_alphanumeric_regex_alpha():
    result = redact_utils.generate_alphanumeric_regex("Ab")
    pattern = re.compile(result)
    assert pattern.match("Ab")
    assert pattern.match("aB")
    assert not pattern.match("12")


def test_generate_alphanumeric_regex_digits():
    result = redact_utils.generate_alphanumeric_regex("12")
    pattern = re.compile(result)
    assert pattern.match("12")
    assert not pattern.match("Ab")


def test_generate_alphanumeric_regex_mixed():
    result = redact_utils.generate_alphanumeric_regex("A1")
    pattern = re.compile(result)
    assert pattern.match("A1")
    assert pattern.match("a1")
    assert not pattern.match("B1")


def test_generate_alphanumeric_regex_empty():
    result = redact_utils.generate_alphanumeric_regex("")
    assert result == ""


@pytest.mark.parametrize("input_str, match_str", [
    ("Ab", "Ab"),
    ("Ab", "aB"),
    ("12", "12"),
    ("A1", "A1"),
    ("A1", "a1"),
])
def test_generate_alphanumeric_regex_parametrized(input_str, match_str):
    result = redact_utils.generate_alphanumeric_regex(input_str)
    pattern = re.compile(result)
    assert pattern.match(match_str)


@pytest.mark.parametrize("input_ipv4, test_strings", [
    (
        ipaddress.IPv4Address("192.168.1.1"),
        ["192.168.1.1", "::FFFF:192.168.1.1", "0:0:0:0:0:FFFF:192.168.1.1"]),
    (
        ipaddress.IPv4Address("10.0.0.1"),
        ["10.0.0.1", "::FFFF:10.0.0.1", "0:0:0:0:0:FFFF:10.0.0.1"]),
    (
        ipaddress.IPv4Address("172.16.0.2"),
        ["172.16.0.2", "::FFFF:172.16.0.2", "0:0:0:0:0:FFFF:172.16.0.2"]),
])
def test_generate_ipv4_regex(input_ipv4, test_strings):
    regex_pattern = redact_utils.generate_ipv4_regex(input_ipv4)
    for test_str in test_strings:
        assert regex_pattern.fullmatch(test_str) is not None

# Define test cases with comments
@pytest.mark.parametrize("test_case", [
    # Test full IPv6 address
    {
        "ipv6_address": ipaddress.IPv6Address("2001:0db8:85a3:0000:0000:8a2e:0370:7334"),
        "test_input": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "expected": True},
    # Test compressed IPv6 address
    {
        "ipv6_address": ipaddress.IPv6Address("2001:0db8:85a3:0000:0000:8a2e:0370:7334"),
        "test_input": "2001:0db8:85a3::8a2e:0370:7334",
        "expected": True},
    # Test multiple zeros in IPv6 address
    {
        "ipv6_address": ipaddress.IPv6Address("2001:0db8:0000:0000:0000:0000:0370:7334"),
        "test_input": "2001:0db8:0:0:0:0:370:7334",
        "expected": True}
])
def test_generate_ipv6_regex(test_case):
    ipv6_address = test_case["ipv6_address"]
    test_input = test_case["test_input"]
    expected = test_case["expected"]
    # Generate ipv6 regex
    ipv6_regex = redact_utils.generate_ipv6_regex(ipv6_address)
    assert bool(ipv6_regex.fullmatch(test_input)) == expected


def test_add_colons_to_mac():
    # Test with valid MAC addresses without separators
    mac_without_separator = "0123456789AB"
    mac_with_colon = redact_utils.add_colons_to_mac(mac_without_separator)
    # Check if colons have been added correctly
    assert (
        mac_with_colon == "01:23:45:67:89:AB",
        "Failed to correctly add colons")
    # Check if the format is correct using regex
    assert re.fullmatch(
        r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}",
        mac_with_colon) is not None, "Invalid MAC address format"
    # Test with an invalid MAC address (length not equal to 12)
    invalid_mac = "0123456789A"
    try:
        redact_utils.add_colons_to_mac(invalid_mac)
    except ValueError as e:
        assert (
            str(e) == "Invalid MAC address length",
            "Did not raise correct exception for invalid MAC address")


def test_find_unique_macs_no_macs():
    assert redact_utils.find_unique_macs("No MAC addresses here!") == set()


def test_find_unique_macs_single_mac():
    assert redact_utils.find_unique_macs(
        "Here's a MAC address: 00:1A:2B:3C:4D:5E") == {"00:1A:2B:3C:4D:5E"}


def test_find_unique_macs_multiple_unique_macs():
    assert redact_utils.find_unique_macs(
        "Two MACs: 00:1A:2B:3C:4D:5E and AA:BB:CC:DD:EE:FF"
    ) == {"00:1A:2B:3C:4D:5E", "AA:BB:CC:DD:EE:FF"}


def test_find_unique_macs_duplicate_macs():
    assert redact_utils.find_unique_macs(
        "Duplicate MACs: 00:1A:2B:3C:4D:5E and 00:1A:2B:3C:4D:5E"
    ) == {"00:1A:2B:3C:4D:5E"}


def test_find_unique_macs_duplicate_macs_no_colons():
    assert redact_utils.find_unique_macs(
        "Duplicate MACs: 00:1A:2B:3C:4D:5E and 001A2B3C4D5E"
    ) == {"00:1A:2B:3C:4D:5E"}


def test_find_mac_in_filename():
    assert redact_utils.find_unique_macs(
        "The filename is 001A2B3C4D5E_something.tgz"
    ) == {"00:1A:2B:3C:4D:5E"}


def test_find_unique_macs_mixed_case():
    assert redact_utils.find_unique_macs(
        "Mixed Case: 00:1a:2B:3C:4d:5E and 00:1A:2b:3c:4D:5e"
    ) == {"00:1A:2B:3C:4D:5E"}


def test_find_unique_macs_mixed_separator():
    assert redact_utils.find_unique_macs(
        "00:1a:2B:3C:4d:5E and 00-1a-2B-3C-4d-5E and 001a2B3C4d5E",
    ) == {"00:1A:2B:3C:4D:5E"}


def test_generate_random_mac_type():
    mac = redact_utils.generate_random_mac()
    assert isinstance(mac, str)


def test_generate_random_mac_format():
    mac = redact_utils.generate_random_mac()
    assert bool(redact_utils.MAC_REGEX.match(mac))


def test_generate_random_mac_uniqueness():
    macs = {redact_utils.generate_random_mac() for _ in range(100)}
    assert len(macs) == 100


def test_generate_random_local_mac():
    local_mac_sum = sum([
        True if redact_utils.LOCAL_MAC_REGEX.fullmatch(
            redact_utils.generate_random_local_mac()
        ) else False
        for _ in range(100)])
    assert local_mac_sum == 100


@pytest.mark.parametrize('test_input,expected', [
    # Valid cases
    ('192.168.1.1', True),
    ('0.0.0.0', True),
    ('255.255.255.255', True),
    # Invalid cases
    ('Not an ip address', False),
    ('10.0.0.2.', False),
    ("0.0.0.01", False),
    ("'192.168.1.300'", False)
])
def test_ipv4_regex_fullmatch(test_input, expected):
    assert bool(redact_utils.IPv4_REGEX.fullmatch(test_input)) == expected


@pytest.mark.parametrize('test_text, filter, expected', [
    ('192.168.1.1', False, {ipaddress.IPv4Address('192.168.1.1')}),
    ('0.0.0.0', False, {ipaddress.IPv4Address('0.0.0.0')}),
    ('255.255.255.255', False, {ipaddress.IPv4Address('255.255.255.255')}),
    ('The IP is 10.0.0.2.', False, {ipaddress.IPv4Address('10.0.0.2')}),
    ('Two IPs: 192.168.0.1, 172.16.0.2', False, {
        ipaddress.IPv4Address('172.16.0.2'),
        ipaddress.IPv4Address('192.168.0.1')}),
    ('No IPs here!', False, set()),
    ('.192.168.1.1', False, set()),
    # Last digit is more than 8 bits
    ('192.168.1.300', False, set()),
    # Leading zero in final 8 bits
    ('255.0.0.01', False, set()),
    ('', False, set()),
])
def test_find_unique_ipv4(test_text, filter, expected):
    assert redact_utils.find_unique_ipv4(
        test_text, filter=filter) == expected


@pytest.mark.parametrize('test_input,expected', [
    ('2001:0db8:85a3:0000:0000:8a2e:0370:7334', ['2001:0db8:85a3:0000:0000:8a2e:0370:7334']),
    ('::1', ['::1']),
    ('::', ['::']),
    ('The IPv6 is 2001:0db8:85a3:0000:0000:8a2e:0370:7334.', ['2001:0db8:85a3:0000:0000:8a2e:0370:7334']),
    ('Two IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334, fe80::202:b3ff:fe1e:8329', 
     ['2001:0db8:85a3:0000:0000:8a2e:0370:7334', 'fe80::202:b3ff:fe1e:8329']),
    ('No IPs here!', []),
    ('.2001:0db8:85a3:0000:0000:8a2e:0370:7334', []),
    ('2001:0db8:85a3:0000:0000:8a2e:0370:xyz', []),
    ('', []),
])
def test_ipv6_regex(test_input, expected):
    ipv6_addresses = [
        match[0] for match in redact_utils.IPv6_REGEX.findall(test_input)]
    assert ipv6_addresses == expected


@pytest.mark.parametrize("test_input, expected", [
    # Regular IPv6 and the Loopback address
    (
        'Two IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334, ::1',
        [
            '2001:0DB8:85A3:0000:0000:8A2E:0370:7334',
            '0000:0000:0000:0000:0000:0000:0000:0001'
        ]),
    # Unspecified address
    ('Another IPv6: ::', ['0000:0000:0000:0000:0000:0000:0000:0000']),
    # Two IP with different case
    (
        'IPv6 with different cases: 2001:0db8::ff00:42:8329 and 2001:0DB8::FF00:42:8329',
        ['2001:0DB8:0000:0000:0000:FF00:0042:8329']
    ),
    # No ips in the text
    ('No IPv6 here!', [])
])
def test_find_unique_ipv6_parametrized(test_input, expected):
    result = redact_utils.find_unique_ipv6(test_input)
    assert all(i in expected for i in result), f"For {test_input}, expected {expected} but got {result}"


def test_generate_random_ipv4_type():
    ipv4 = redact_utils.generate_random_ipv4()
    assert isinstance(ipv4, str)


def test_generate_random_ipv4_format():
    ipv4 = redact_utils.generate_random_ipv4()
    assert bool(redact_utils.IPv4_REGEX.match(ipv4))


def test_generate_random_ipv4_uniqueness():
    ipv4_addresses = {redact_utils.generate_random_ipv4() for _ in range(100)}
    assert len(ipv4_addresses) == 100


def test_generate_random_ipv6_type():
    ipv6 = redact_utils.generate_random_ipv6()
    assert isinstance(ipv6, str)


def test_generate_random_ipv6_format():
    ipv6 = redact_utils.generate_random_ipv6()
    assert bool(redact_utils.IPv6_REGEX.match(ipv6))


def test_generate_random_ipv6_uniqueness():
    ipv6_addresses = {redact_utils.generate_random_ipv6() for _ in range(100)}
    assert len(ipv6_addresses) == 100


@pytest.mark.parametrize("compressed, expected", [
    ("1080::8:800:417A", "1080:0000:0000:0000:0000:0008:0800:417A"),
    ("::1", "0000:0000:0000:0000:0000:0000:0000:0001"),
    ("::", "0000:0000:0000:0000:0000:0000:0000:0000"),
    ("2001:db8::ff00:42:8329", "2001:0db8:0000:0000:0000:ff00:0042:8329"),
    ("1:0:0:0:0:0:0:1", "0001:0000:0000:0000:0000:0000:0000:0001"),  # Already in full form
    ("2001:db8:0:0:1:0:0:1", "2001:0db8:0000:0000:0001:0000:0000:0001"),  # Missing leading zeros
])
def test_decompress_ipv6(compressed, expected):
    assert redact_utils.decompress_ipv6(compressed) == expected


def test_redact_text_basic():
    """
    Test basic text redaction with defaults.
    """
    text_list = ["some text with MAC AB:CD:EF:12:34:56 and IP 1.2.3.4"]
    redact_map, redacted_texts = redact_utils.redact_text(text_list)
    assert (
        ("[REDACTED:MAC:1]" in redact_map) and
        (redact_map["[REDACTED:MAC:1]"]["original"] == "AB:CD:EF:12:34:56")
    )
    assert (
        ("[REDACTED:IPv4:1]" in redact_map) and
        (redact_map["[REDACTED:IPv4:1]"][
            "original"] == ipaddress.IPv4Address("1.2.3.4"))
    )
    assert redacted_texts == [
        'some text with MAC [REDACTED:MAC:1] and IP [REDACTED:IPv4:1]']

# Declare these as global function so they can be pickled
def custom_find(text):
    return ['custom']

def custom_regex(match):
    return re.compile('custom')

def test_redact_text_custom():
    """
    Test custom redaction.
    """
    custom_redactions = [("CustomType", custom_find, custom_regex)]
    redact_map, redacted_texts = redact_utils.redact_text(
        ["Replace custom with type"], custom_redactions=custom_redactions)
    assert "[REDACTED:CustomType:1]" in redact_map
    assert redacted_texts == [
        'Replace [REDACTED:CustomType:1] with type']


def test_redact_text_invalid_tuple_length():
    with pytest.raises(ValueError) as excinfo:
        redact_utils.redact_text(
            [], custom_redactions=[("TooShort",)])
    assert "should have exactly 3 elements" in str(excinfo.value)

# Test ValueError for invalid type (non-string)
def test_redact_text_invalid_type():
    with pytest.raises(ValueError) as excinfo:
        redact_utils.redact_text(
            [], custom_redactions=[(123, lambda x: x, lambda x: x)])
    assert "should be a string indicating the redaction type" in str(excinfo.value)

# Test ValueError for non-callable functions
def test_redact_text_non_callable_functions():
    with pytest.raises(ValueError) as excinfo:
        redact_utils.redact_text(
            [], custom_redactions=[("CustomType", "not_a_function", "also_not_a_function")])
    assert "should be callable functions" in str(excinfo.value)
