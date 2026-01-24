"""Module with ocr tools models."""
import re
from datetime import datetime, time, date


class _Match:
    def __init__(self, string: str, start: int, end: int):
        self.string: str = string
        self.start: int = start
        self.end: int = end

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class DateMatch(_Match):
    """DateMatch object."""

    def __init__(self, string: str, date_time: datetime, start: int, end: int):
        """Create a DateMatch object."""
        super().__init__(string, start, end)
        self.date_time: date = date_time.date()


class TimeMatch(_Match):
    """TimeMatch object."""

    def __init__(self, string: str, date_time: datetime, start: int, end: int):
        """Create a TimeMatch object."""
        super().__init__(string, start, end)
        self.time: time = date_time.timetz()


class DateTimeMatch(_Match):
    """DateTimeMatch object."""

    def __init__(self, string: str, date_time: datetime, start: int, end: int):
        """Create a DateTimeMatch object."""
        super().__init__(string, start, end)
        self.date_time: datetime = date_time


class EmailMatch(_Match):
    """EmailMatch object."""

    def __init__(self, string: str, start: int, end: int):
        """Create a EmailMatch object."""
        super().__init__(string, start, end)


class AmountMatch(_Match):
    """AmountMatch object."""

    def __init__(self, string: str, number: int or float, start: int, end: int):
        """Create a AmountMatch object."""
        super().__init__(string, start, end)
        self.number: int or float = number

    def __repr__(self):
        """Represent object."""
        return str(self.number)


class AddressMatch(_Match):
    """AddressMatch class object to represent Address object with street, city, state, zip and county fields."""

    def __init__(
        self,
        string: str,
        start: int,
        end: int,
        address_number: str,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        street_pre_type: str = "",
        street_post_type: str = "",
        street_pre_directional: str = "",
        street_post_directional: str = "",
        sub_address_type: str = "",
        sub_address_type_id: str = "",
        occupancy_type: str = "",
        occupancy_type_id: str = "",
        address_1_string: str = "",
        address_2_string: str = "",
    ):
        """Initialize the object with the given address .

        Args:
            string (str): raw address value from page.
            start (int): start index for raw address value
            end (int): end index for raw address value
            address_number (str): parsed address number value from raw address value.
            street (str): parsed street value from raw address value.
            city (str): parsed city value from raw address value.
            state (str): parsed state value from raw address value.
            zip_code (str): parsed zip-code value from raw address value.
            street_pre_type (str): parsed street pre type value from raw address value.
            street_post_type (str): parsed street post type value from raw address value.
            street_pre_directional (str): parsed street pre directional value from raw address value.
            street_post_directional (str): parsed street post directional value from raw address value.
            sub_address_type (str): parsed sub address type value from raw address value.
            sub_address_type_id (str): parsed sub address type id value from raw address value.
            occupancy_type (str): parsed occupancy type value from raw address value.
            occupancy_type_id (str): parsed occupancy type id value from raw address value.
            address_1_string (str): parsed address 1 string value from raw address value.
            address_2_string (str): parsed address 2 string value from raw address value.
        """
        super().__init__(string, start, end)
        self.address_number = address_number
        self.street = street
        self.street_pre_type = street_pre_type
        self.street_post_type = street_post_type
        self.street_pre_directional = street_pre_directional
        self.street_post_directional = street_post_directional
        self.sub_address_type = sub_address_type
        self.sub_address_type_id = sub_address_type_id
        self.occupancy_type = occupancy_type
        self.occupancy_type_id = occupancy_type_id
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.address_1_formatted = self.formatted_address_line_1()
        self.address_2_formatted = self.formatted_address_line_2()
        self.full_address_formatted = f"{self.address_1_formatted} {self.address_2_formatted}".strip()
        self.address_1_string = address_1_string
        self.address_2_string = address_2_string

    def formatted_address_line_1(self) -> str:
        if len(self.street_pre_directional) == 2:
            self.street_pre_directional = self.street_pre_directional.upper()
        else:
            self.street_pre_directional = self.street_pre_directional.title()

        if len(self.street_post_directional) == 2:
            self.street_post_directional = self.street_post_directional.upper()
        else:
            self.street_post_directional = self.street_post_directional.title()

        line = (
            f"{self.address_number.title()} {self.street_pre_type.title()} {self.street_pre_directional} "
            f"{self.street.title()} "
            f"{self.street_post_type.title()} {self.street_post_directional} "
            f"{self.sub_address_type.title()} "
            f"{self.sub_address_type_id.title()} {self.occupancy_type.title()} {self.occupancy_type_id.title()}"
        )
        line = re.sub(r"\s+", " ", line).strip()
        return line

    def formatted_address_line_2(self) -> str:
        line = f"{self.city.title()}, {self.state.upper()} {self.zip_code}".strip(" ,")
        line = re.sub(r"\s+", " ", line)
        return line


# class AddressMatch(_Match):
#     """AddressMatch class object to represent Address object with street, city, state, zip and county fields."""
#
#     def __init__(
#         self, string: str, street: str, city: str, state: str, zip_code: str, county: str, start: int, end: int
#     ):
#         """Initialize the object with the given address .
#
#         Args:
#             string (str): raw address value from page.
#             street (str): parsed street value from raw address value.
#             city (str): parsed city value from raw address value.
#             state (str): parsed state value from raw address value.
#             zip_code (str): parsed zip-code value from raw address value.
#             county (str): parsed county value from raw address value.
#             start (int): start index for raw address value
#             end (int): end index for raw address value
#         """
#         super().__init__(string, start, end)
#         # 123 Sample street
#         self.street = street
#         # New York, NY 10000
#         # New York
#         self.city = city
#         # NY; NEW YORK
#         self.state = state
#         # 10000; 12345-1234
#         self.zip = zip_code
#         # WAYNE-MI
#         self.county = county
#
#     def __str__(self) -> str:
#         """Return the string representation of the AddressMatch class.
#
#         Returns:
#             str: string representation of the AddressMatch class.
#         """
#         return f"""string: '{self.string}' at position ({self.start} - {self.end})
# street: '{self.street}', city: '{self.city}', county: '{self.county}',
# state: '{self.state}', zip: '{self.zip}'"""
