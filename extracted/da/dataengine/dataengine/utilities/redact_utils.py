from typing import List, Callable, Union, Set, Dict, Any
import re
import random
import itertools
import ipaddress
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from multiprocessing import Pool


MAC_REGEX = re.compile(
    # Mac with colons
    r"((?:[0-9A-Fa-f]{2}:{1}){5}[0-9A-Fa-f]{2})|"
    # Mac with dashes
    r"((?:[0-9A-Fa-f]{2}-{1}){5}[0-9A-Fa-f]{2})|"
    # Mac with no colons or dashes
    # Note: This will flag every 12 digit string as a mac because it is
    # technically valid
    r"([0-9A-Fa-f]{12})"
)
LOCAL_MAC_REGEX = re.compile(
    # First octet's second least significant bit must be 1
    r"((?:[0-9a-f][2637AaEeBbFf][:-]?){1}"
    r"([0-9A-Fa-f]{2}[:-]?){4}[0-9A-Fa-f]{2})")
IPv4_REGEX = re.compile(
    r"(?<![.\w])"  # Negative lookbehind
    r"((25[0-5]{1}|2[0-4]{1}[0-9]{1}|1[0-9]{2}|[1-9]{0,1}[0-9]{1}){1}\."
    r"(25[0-5]{1}|2[0-4]{1}[0-9]{1}|1[0-9]{2}|[1-9]{0,1}[0-9]{1}){1}\."
    r"(25[0-5]{1}|2[0-4]{1}[0-9]{1}|1[0-9]{2}|[1-9]{0,1}[0-9]{1}){1}\."
    r"(25[0-5]{1}|2[0-4]{1}[0-9]{1}|1[0-9]{2}|[1-9]{0,1}[0-9]{1}){1})"
    r"(?!\w)"  # Negative lookahead for only word characters
)
# Partial source: https://stackoverflow.com/questions/53497
IPv6_REGEX = re.compile(
    r"(?<![.\w])"  # Negative lookbehind
    r"("  
    r"(([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|"
    r"(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|"
    r"((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|"
    r"(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|"
    r":((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|"
    r"(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|"
    r"((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|"
    r"(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|"
    r"((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|"
    r"(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|"
    r"((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|"
    r"(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|"
    r"((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|"
    r"(:(((:[0-9A-Fa-f]{1,4}){1,7})|"
    r"((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))"
    r")"
    r"(?!\w)"  # Negative lookahead for only word characters
)


def convert_to_hex(decimal):
    """
    Convert to hexadecimal with leading zeros.
    """
    return "{:02x}".format(decimal)


def left_pad_zeros(word: str) -> str:
    """
    Left-pad zeros to a string based on the initial zeros in the input word.

    This function takes a word, counts the number of leading zeros, and
    returns a string that represents the left-padding format to be used for
    similar words.

    Args:
        word (str):
            The input word containing initial zeros and other characters.

    Returns:
        str:
            A string representing the left-padding format, e.g., "0{0,2}".
        
    Examples:
        >>> left_pad_zeros("0045")
        '0{0,2}45'
        
        >>> left_pad_zeros("45")
        '45'
        
        >>> left_pad_zeros("000")
        '0{1,3}'
    """
    if word == "0":
        return word
    elif re.compile("0+").fullmatch(word):
        return f"0{{1,{len(word)}}}"
    zeros = 0
    for i in word:
        if i == "0":
            zeros += 1
        else:
            break
    # Return regex for the word
    if zeros:
        return f"0{{0,{zeros}}}" + word[zeros:]
    else:
        return word


def generate_alphanumeric_regex(alphanumeric_string: str) -> str:
    """
    Generate a regular expression for a given alphanumeric string.

    The function takes an alphanumeric string consisting of alphabetic
    characters and digits, and generates a corresponding regular expression.
    For each alphabetic character, a range consisting of the uppercase and
    lowercase versions is created. Digits are included as-is in the regex.

    Args:
        alphanumeric_string (str):
            The input alphanumeric string consisting of alphabetic characters
            and digits.

    Returns:
        str:
            A regular expression string that can be used to match the given
            alphanumeric string.

    Example:
        >>> generate_alphanumeric_regex("Ab1")
        '[Aa]{1}[Bb]{1}1'
    """
    return "".join(
        f"[{char.upper()}{char.lower()}]{{1}}" if char.isalpha() else char
        for char in alphanumeric_string)


def generate_mac_regex(mac_address: str) -> re.Pattern:
    """
    Generate a regular expression for matching a given MAC address.

    This function takes a MAC address as input, normalizes it by removing
    any colons or dashes, and then generates a regular expression that can
    match the MAC address in various formats (plain, colon-separated, and
    dash-separated).

    Args:
        mac_address (str):
            The input MAC address as a string. It can contain colons or dashes
            as separators.

    Returns:
        re.Pattern:
            A compiled regular expression pattern that can be used to match
            the given MAC address in its various formats.

    Example:
        >>> pattern = generate_mac_regex("AA:BB:CC:DD:EE:FF")
        >>> bool(pattern.match("aabbccddeeff"))
        True
        >>> bool(pattern.match("AA:BB:CC:DD:EE:FF"))
        True
        >>> bool(pattern.match("AA-BB-CC-DD-EE-FF"))
        True
    """
    return re.compile("|".join(
        [mac_address] + [mac_address.replace(":", i) for i in ["-", ""]]),
        re.IGNORECASE)


def generate_ipv4_regex(ipv4_address: ipaddress.IPv4Address) -> re.Pattern:
    """
    Generate a regex pattern to match the given IPv4 address and its
    equivalent IPv6 representations.

    This function takes an IPv4 address, converts it to its IPv6 hexadecimal
    block form, and constructs a regex pattern to match all valid permutations
    of the address.

    Args:
        ipv4_address (ipaddress.IPv4Address): The IPv4 address object

    Returns:
        re.Pattern:
            A regex pattern that matches the IPv4 address and its IPv6
            equivalents.
    """
    ipv4_str = ipv4_address.exploded
    base_str = "(::F{4}:|0{1,4}:0{1,4}:0{1,4}:0{1,4}:0{1,4}:F{4}:){1}"
    # Pull octets from ip address and cast them to hexadecimal
    octets = [
        convert_to_hex(int(decimal)) for decimal in ipv4_str.split(".")]
    # Get last two 16-bit words in final 32 bits of IPv6 Address
    word_1 = left_pad_zeros(generate_alphanumeric_regex("".join(octets[0:2])))
    word_2 = left_pad_zeros(generate_alphanumeric_regex("".join(octets[2:])))
    # Return IPv4 regex that supports all valid permutations
    return re.compile(
        ipv4_str.replace(".", "\\.") + "|" + base_str + "((" +
        ipv4_str.replace(".", "\\.") + ")|(" + ":".join([word_1, word_2]) +
        ")){1}", re.IGNORECASE)


def generate_ipv6_regex(ipv6_address: ipaddress.IPv6Address) -> re.Pattern:
    """
    Generates a regex pattern to match the given a decompressed IPv6 address.
    
    Args:
        ipv6_address (ipaddress.IPv6Address): IPv6 address object.
        
    Returns:
        re.Pattern:
            A compiled regex pattern that can match the IPv6
            address and its compressed forms.
    """
    decompressed_ipv6 = ipv6_address.exploded
    # Split the ip address into 16 bit blocks
    blocks = decompressed_ipv6.split(":")
    # Get the initial permutation
    permutations = [":".join([left_pad_zeros(block) for block in blocks])]
    # Generate zero ranges for ip address
    zero_ranges = []
    in_range = False
    for index, word in enumerate(blocks):
        if (
            (not in_range) and
            (re.compile(r"0{1,4}").fullmatch(word))
        ):
            zero_ranges.append([index])
            in_range = True
        elif (
            (in_range) and
            (not re.compile(r"0{1,4}").fullmatch(word))
        ):
            zero_ranges[-1].append(index)
            in_range = False
    # If the last word is 0 set the final zero range value
    if in_range:
        zero_ranges[-1].append(index)
    # Generate compressed permutations
    # If all the digits are 0 then the compressed format is ::
    if all(char == "0" for char in decompressed_ipv6 if char != ":"):
        permutations.append("::")
    else:
        permutations += [
            ":".join([
                i for i in [
                    left_pad_zeros(word) if not (
                        index >= zero_range[0] and
                        index < zero_range[1]
                    ) else ""
                    if index == (zero_range[1] - 1) else None
                    for index, word in enumerate(blocks)
                ] if i is not None])
            for zero_range in zero_ranges]

    return re.compile("|".join(permutations), re.IGNORECASE)


def add_colons_to_mac(mac):
    """Add colons to a MAC address string.

    Args:
        mac (str):
            A 12-character MAC address string without any separators.

    Returns:
        str:
            The MAC address string with colons added between every two
            characters.

    Raises:
        ValueError: If the length of the input MAC address is not 12.

    Examples:
        >>> add_colons_to_mac("0123456789AB")
        "01:23:45:67:89:AB"

        >>> add_colons_to_mac("A1B2C3D4E5F6")
        "A1:B2:C3:D4:E5:F6"
    """
    if len(mac) != 12:
        raise ValueError("Invalid MAC address length")
    
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))


def find_unique_macs(text: str) -> Set[str]:
    """
    Find and return unique MAC addresses in a given text.

    This function searches for MAC addresses in the text, normalizes them to 
    uppercase and colon-separated format, and then filters out any 12-digit
    numerical sequences that are not valid MAC addresses.

    Args:
        text (str): The text to search for MAC addresses.

    Returns:
        Set[str]: A set of unique MAC addresses found in the text.

    Example:
        >>> find_unique_macs("00:1A:2B:3C:4D:5E and 00-1A-2B-3C-4D-5E")
        {'00:1A:2B:3C:4D:5E'}
    """
    twelve_digit_check = re.compile(r"[0-9]{12}")
    unique_macs = set()
    for match in MAC_REGEX.findall(text):
        mac_str = "".join(match).upper()
        if twelve_digit_check.fullmatch(mac_str):
            continue
        if ":" not in mac_str:
            if "-" in mac_str:
                mac_str = mac_str.replace("-", ":")
            else:
                mac_str = add_colons_to_mac(mac_str)
        unique_macs.add(mac_str)

    return unique_macs


def generate_random_mac():
    """
    Generate a random mac address.

    Returns:
        random mac address
    """
    return ":".join("{:02x}".format(random.randint(0, 255)) for _ in range(6))


def generate_random_local_mac():
    """
    Generate a random local MAC address.

    The function generates a random MAC address and ensures that it is a local
    MAC address by setting the second least significant bit of the first octet
    to 1.

    Returns:
        str:
            A MAC address string in the format "XX:XX:XX:XX:XX:XX", where each
            "XX" is a two-digit hexadecimal number.

    Examples:
        >>> generate_random_local_mac()
        "01:23:45:67:89:AB"

        >>> generate_random_local_mac()
        "1A:2B:3C:4D:5E:6F"
    """
    # Generate a random 8-bit number (0-255)
    first_octet = random.randint(0, 255)
    # Set the second least significant bit to 1
    first_octet |= 2
    # Generate the remaining octets
    mac_address = [first_octet] + [random.randint(0, 255) for _ in range(5)]
    # Convert to hexadecimal and join with colons
    return ':'.join(f'{octet:02x}' for octet in mac_address)


def decompress_ipv6(ipv6_address: str) -> str:
    """
    Decompress a compressed IPv6 address to its full 8-block hexadecimal form.
    
    Given a compressed IPv6 address, this function will expand it into its
    full 8-block representation. Each block in the full form consists of 4
    hexadecimal digits. The function handles the following scenarios:
    
    1. Expands the '::' shorthand to the appropriate number of zero blocks.
    2. Pads existing blocks with leading zeros to ensure 4 digits.
    
    Args:
        ipv6_address (str):
            The compressed IPv6 address to decompress. It can also be an IPv6
            address that's partially compressed or already in full form.
        
    Returns:
        str: The IPv6 address in its full 8-block, 4-digits-per-block form.
    
    Example:
        >>> decompress_ipv6("1080::8:800:417A")
        "1080:0000:0000:0000:0008:0800:417A"
        
        >>> decompress_ipv6("::1")
        "0000:0000:0000:0000:0000:0000:0000:0001"
        
        >>> decompress_ipv6("2001:db8::ff00:42:8329")
        "2001:0db8:0000:0000:0000:ff00:0042:8329"
        
    Notes:
        - The function assumes that the input is a valid IPv6 address.
        - The function does not validate the IPv6 address.
    """
    # Split the IPv6 address by the double colon "::"
    halves = ipv6_address.split("::")
    # If there's no double colon, the address is already in full form
    if len(halves) == 1:
        # Still need to pad with leading zeros for each block
        blocks = ipv6_address.split(":")
        full_blocks = [block.zfill(4) for block in blocks]
        return ":".join(full_blocks)
    # Split each half into its 16-bit blocks
    first_half = halves[0].split(":") if halves[0] else []
    second_half = halves[1].split(":") if halves[1] else []
    # Pad with leading zeros for each block in the halves
    first_half = [block.zfill(4) for block in first_half]
    second_half = [block.zfill(4) for block in second_half]
    # Calculate the number of zero blocks needed for padding
    num_zero_blocks = 8 - (len(first_half) + len(second_half))
    # Create the zero blocks
    zero_blocks = ["0000"] * num_zero_blocks
    # Combine all the blocks to form the full IPv6 address
    full_address_blocks = first_half + zero_blocks + second_half
    # Join the blocks into a full IPv6 address
    full_address = ":".join(full_address_blocks)
    
    return full_address



def find_unique_ipv4(
        text: str, filter: bool = True
    ) -> Set[ipaddress.IPv4Address]:
    """
    Find and return unique IPv4 addresses in a given text.
    
    Args:
        text (str): The text to search for IPv4 addresses.
        filter (bool): Filter loopback, private, and unspecified IP addresses
        
    Returns:
        Set[ipaddress.IPv4Address]:
            A set of unique IPv4 addresses found in the text.
        
    Example:
        >>> find_unique_ipv4("192.168.1.1 and 10.0.0.1 and 192.168.1.1")
        {IPv4Address('192.168.1.1'), IPv4Address('10.0.0.1')}
    """
    unique_ip_addresses = set()
    for match in IPv4_REGEX.findall(text):
        ipv4 = ipaddress.IPv4Address(match[0])
        if (
            filter and (
                ipv4.is_loopback or
                ipv4.is_private or
                ipv4.is_unspecified
            )
        ):
            continue
        unique_ip_addresses.add(ipv4)

    return unique_ip_addresses


def find_unique_ipv6(
        text: str, filter: bool = True
    ) -> Set[ipaddress.IPv6Address]:
    """
    Find and return unique IPv6 addresses in a given text, with optional
    filtering.

    This function identifies IPv6 addresses in the given text, decompresses
    and normalizes them to uppercase. It can also filter out loopback,
    private, and unspecified addresses based on the 'filter' argument.

    Args:
        text (str): The text to search for IPv6 addresses.
        filter (bool, optional):
            Whether to filter out loopback, private, or unspecified addresses.
            Defaults to True.

    Returns:
        Set[ipaddress.IPv6Address]:
            A set of unique IPv6 addresses found in the text.

    Example:
        >>> find_unique_ipv6("::1 and fe80::1 and ::", filter=True)
        {IPv6Address('fe80::1')}
    """
    unique_ip_addresses = set()
    for match in IPv6_REGEX.findall(text):
        # TODO: Remove the if statement once this bug is figured out for 18
        #       octet macs. Make sure ipv6 regex doesn't pick these up
        ip_str = decompress_ipv6(match[0].upper())
        if all(len(j) == 2 for j in ip_str.split(":")):
            continue
        # Can compress this and ipv4 logic after above bug is fixed
        ipv6 = ipaddress.IPv6Address(match[0])
        if (
            filter and (
                ipv6.is_loopback or
                ipv6.is_private or
                ipv6.is_unspecified
            )
        ):
            continue
        unique_ip_addresses.add(ipv6)
    
    return unique_ip_addresses


def generate_random_ipv4():
    """
    Generates a random IPv4 address.
    
    Returns:
        str: A random IPv4 address.
    """
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def generate_random_ipv6():
    """
    Generates a random IPv6 address.
    
    Returns:
        str: A random IPv6 address.
    """
    return ":".join("{:x}".format(random.randint(0, 0xFFFF)) for _ in range(8))


def redact_items_from_text(text, redact_map):
    """
    Redact sensitive information from a given text based on a redaction map.
    
    Args:
        text (str): The original text where redaction needs to be performed.
        redact_map (dict):
            A mapping containing the redaction keys and associated regular
            expressions.

    Returns:
        str: The redacted text.    
    """
    # Make a copy of the original text
    redacted_text = text
    # Redact all full matches from the redaction map
    for redaction_string, values in redact_map.items():
        redacted_text = values["regex"].sub(redaction_string, redacted_text)
    
    return redacted_text


def pooled_redact_text(redact_map, text_list, max_workers=16):
    """
    Perform redaction in parallel on a list of texts using a redaction map.
    
    Args:
        redact_map (dict):
            A mapping containing the redaction keys and associated regular
            expressions.
        text_list (list of str): The list of texts to redact.
        max_workers (int, optional):
            The maximum number of worker processes. Defaults to 16.
    
    Returns:
        list: A list containing the redacted texts.
    """
    with Pool(
        processes=max(1, multiprocessing.cpu_count() - 1)
    ) as executor:
        results = list(executor.starmap(
            redact_items_from_text,
            [(text, redact_map) for text in text_list]))

    return results


def generate_redact_map(
        text_list: List[str], redact_type: str,
        find_function: Callable[[str], Set[Any]],
        regex_function: Callable[[Any], re.Pattern]
    ) -> Dict[str, Dict[str, Union[str, str]]]:
    """
    Generate a redaction map for a list of text items based on specified find
    and regex functions.

    Args:
        text_list (List[str]):
            A list of text items to be processed for redaction.
        redact_type (str):
            A string indicating the type of redaction.
        find_function (Callable[[str], List[str]]):
            A function that takes a string and returns a set of matches.
        regex_function (Callable[[str], str]):
            A function that gives regex pattern that covers all permutations
            of a certain type of string.

    Returns:
        Dict[str, Dict[str, Union[str, str]]]:
            A dictionary containing the redaction mappings. Each key is a
            redaction label and each value is another dictionary containing
            the original match and its regex pattern.
    """
    # Set processes to 1 less than cpu count
    with Pool(
        processes=max(1, multiprocessing.cpu_count() - 1)
    ) as executor:
        results = list(executor.map(find_function, text_list))
    # Get unique matches
    unique_matches = set(itertools.chain.from_iterable(results))
    # Return redact map
    return {
        f"[REDACTED:{redact_type}:{{}}]".format(index + 1): {
            "original": match, "regex": regex_function(match)
        } for index, match in enumerate(unique_matches)}


def redact_text(text_list, custom_redactions=None):
    """
    Perform redaction of MAC addresses, IP addresses, and any custom types on
    a list of text strings.

    This function allows for custom redaction types to be added. Each custom 
    redaction is specified as a tuple containing:
    - A string indicating the type of redaction.
    - A function for finding the substring to redact.
    - A function that generates a regex for the substring.

    Args:
        text_list (list of str):
            The list of texts where redaction needs to be performed.
        custom_redactions (list of tuple, optional):
            Custom redaction types to add.
            Each tuple should contain (type, find_function, regex_function).
            Defaults to None.

    Returns:
        tuple: A tuple containing two elements:
            1. dict:
                A mapping from redaction type to the corresponding redaction
                information.
            2. list: A list of redacted text strings.

    Raises:
        ValueError: If a custom redaction tuple is invalid.
            - Tuple does not have exactly 3 elements.
            - The first element is not a string.
            - The second and third elements are not callable functions.
    """
    # Default redactions
    redaction_args = [
        ("MAC", find_unique_macs, generate_mac_regex),
        ("IPv4", find_unique_ipv4, generate_ipv4_regex),
        ("IPv6", find_unique_ipv6, generate_ipv6_regex)]
    # Add custom redactions if provided
    if custom_redactions:
        for i, custom in enumerate(custom_redactions):
            # Check if tuple has exactly 3 elements
            if len(custom) != 3:
                raise ValueError(
                    f"Custom redaction tuple at index {i} should have exactly"
                    " 3 elements.")
            # Check if the first element is a string
            if not isinstance(custom[0], str):
                raise ValueError(
                    f"The first element of the tuple at index {i} should be a"
                    " string indicating the redaction type.")
            # Check if the second and third elements are callable
            if not callable(custom[1]) or not callable(custom[2]):
                raise ValueError(
                    f"The second and third elements of the tuple at index {i}"
                    " should be callable functions.")
            # Add to existing redactions and update types
            redaction_args.append(custom)
    # Generate redact_map and return redacted texts
    redact_map = {}
    for args in redaction_args:
        redact_map.update(generate_redact_map(text_list, *args))
    
    return redact_map, pooled_redact_text(redact_map, text_list)
