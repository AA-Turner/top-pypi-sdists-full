"""Module with Address search and validation methods."""
import re
import usaddress
from typing import List
from t_ocr.ocr_tools.models import AddressMatch

us_state_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

_exceptions_list = [
    "zip",
    "code",
    "city",
    "state",
    "address",
    "name",
    "date",
    "sent",
    "to",
    "from",
    "at",
    "the",
    "of",
    "and",
    "or",
    "in",
    "on",
    "for",
    "by",
    "with",
    "as",
    "at",
    "from",
    "into",
    "like",
    "through",
    "after",
    "over",
    "between",
    "out",
    "against",
    "during",
    "without",
    "before",
    "under",
    "around",
    "among",
    "via",
]


class __AddressData:
    def __init__(self, string: str):
        self.data: List[str] = usaddress.parse(string)
        self.address_number = ""
        self.street = ""
        self.street_pre_type = ""
        self.street_name_post_type = ""
        self.street_name_pre_directional = ""
        self.street_name_post_directional = ""
        self.street_post_type = ""
        self.sub_address_type = ""
        self.sub_address_type_id = ""
        self.occupancy_type = ""
        self.occupancy_type_id = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""
        self.address_1 = ""
        self.address_2 = ""
        self.parse_data()
        self.address_1_original_string = ""
        self.address_2_original_string = ""
        self.address_original_string = ""
        self.get_original_strings()

    def get_original_strings(self):

        start_idx = self.get_index("AddressNumber")
        city_idx = self.get_index("PlaceName")
        end_idx = self.get_index("ZipCode")
        if self.is_valid_address_1():
            self.address_1_original_string = " ".join([d[0] for d in self.data[start_idx:city_idx]])
        else:
            self.address_1_original_string = ""
        if self.is_valid_address_2():
            self.address_2_original_string = " ".join([d[0] for d in self.data[start_idx:city_idx]])
        else:
            self.address_2_original_string = ""
        if start_idx and end_idx:
            self.address_original_string = " ".join([d[0] for d in self.data[start_idx : end_idx + 1]])
        else:
            self.address_original_string = " ".join([d[0] for d in self.data])

    def parse_data(self):
        self.address_number = self.get_value("AddressNumber")
        self.street = self.get_all_values("StreetName")
        self.street_name_pre_directional = self.get_value("StreetNamePreDirectional")

        self.street_name_post_directional = self.get_value("StreetNamePostDirectional")

        self.street_pre_type = self.get_all_values("StreetNamePreType")
        self.street_post_type = self.get_value("StreetNamePostType")

        self.sub_address_type = self.get_value("SubaddressType")
        self.sub_address_type_id = self.get_all_values("SubaddressIdentifier")

        self.occupancy_type = self.get_value("OccupancyType")
        self.occupancy_type_id = self.get_all_values("OccupancyIdentifier")
        self.city = self.get_all_values("PlaceName")

        state = self._convert_state_from_ocr(self.get_all_values("StateName"))
        if state and len(state) > 2:
            try:
                self.state = us_state_abbrev[state.title()].upper()
            except KeyError:
                pass
        elif state and len(state) == 2 and state.upper() in us_state_abbrev.values():
            self.state = state.upper()

        self.zip_code = self.get_value("ZipCode")

        self.address_1 = self.address_1_line()
        self.address_2 = self.address_2_line()

    def _convert_state_from_ocr(self, state: str) -> str:
        ocr_compliance = {
            "f1": "FL",
        }
        if state.lower() in ocr_compliance:
            return ocr_compliance[state.lower()]
        return state

    def address_1_line(self) -> str:
        line = (
            f"{self.address_number} {self.street_pre_type} {self.street_name_pre_directional} {self.street} "
            f"{self.street_post_type} {self.street_name_post_directional} {self.sub_address_type} "
            f"{self.sub_address_type_id} {self.occupancy_type} {self.occupancy_type_id}"
        )
        line = re.sub(r"\s+", " ", line).strip()
        return line

    def get_address_1_last_value(self) -> str:
        address_1_keys = [
            "AddressNumber",
            "StreetName",
            "StreetNamePreDirectional",
            "StreetNamePostDirectional",
            "StreetNamePreType",
            "StreetNamePostType",
            "SubaddressType",
            "SubaddressIdentifier",
            "OccupancyType",
            "OccupancyIdentifier",
        ]
        for value, value_key in self.data[::-1]:
            if value_key in address_1_keys:
                return value
        return ""

    def address_2_line(self) -> str:
        line = f"{self.city.title()}, {self.state} {self.zip_code}".strip(" ,")
        line = re.sub(r"\s+", " ", line)
        return line

    def is_valid_address_1(self) -> bool:
        street_exceptions = ["my", "address", "name", "only"]
        for street_word in self.street.split():
            if street_word.lower() in street_exceptions:
                return False

        addr1_values = [self.street, self.address_number]
        if not bool(re.search(r"\d", self.address_number)):
            return False
        if all(addr1_values):
            return True
        return False

    def is_valid_address_2(self) -> bool:
        addr2_values = [self.city, self.state, self.zip_code]
        if any(value.lower() in _exceptions_list for value in [self.city, self.zip_code]):
            return False
        if all(addr2_values):
            return True
        return False

    def is_valid_full_address(self) -> bool:
        if self.is_valid_address_1() and self.is_valid_address_2():
            return True
        return False

    def get_value(self, key: str) -> str:
        for value, value_key in self.data:
            if value_key == key:
                return value.strip(" ,.-")
        return ""

    def get_index(self, key: str) -> int:
        for idx, value_and_key in enumerate(self.data):
            value, value_key = value_and_key
            if value_key == key:
                return idx
        return -1

    def get_all_values(self, key: str) -> str:
        matched_values = []
        for value, value_key in self.data:
            if value_key == key:
                matched_values.append(value.strip(" ,.-"))
        return " ".join(matched_values)


def _try_split_state_and_zip_code(string: str) -> str:
    # Example "12312 Magic Spring Way Bristow VA20136" -> "12312 Magic Spring Way Bristow VA 20136"
    for match in re.findall(r"(?:(?<=\W)|(?<=^))([a-z]{2})(\d{5})(?=\W|$)", string, re.I):
        string = string.replace(f"{match[0]}{match[1]}", f"{match[0]} {match[1]}")
    return string


def __address_data_to_address_match(
    address_string, start, end, address_data: __AddressData, address_1_string: str, address_2_string: str
) -> AddressMatch:
    return AddressMatch(
        string=address_string,
        start=start,
        end=end,
        address_number=address_data.address_number,
        street=address_data.street,
        city=address_data.city,
        state=address_data.state,
        zip_code=address_data.zip_code,
        street_pre_type=address_data.street_pre_type,
        street_post_type=address_data.street_post_type,
        street_pre_directional=address_data.street_name_pre_directional,
        street_post_directional=address_data.street_name_post_directional,
        sub_address_type=address_data.sub_address_type,
        sub_address_type_id=address_data.sub_address_type_id,
        occupancy_type=address_data.occupancy_type,
        occupancy_type_id=address_data.occupancy_type_id,
        address_1_string=address_1_string,
        address_2_string=address_2_string,
    )


def __address_data_to_address_match_multi_line(
    string,
    start,
    end,
    address_data_1: __AddressData,
    address_data_2: __AddressData,
    address_1_string: str,
    address_2_string: str,
) -> AddressMatch:
    return AddressMatch(
        string=string,
        start=start,
        end=end,
        address_number=address_data_1.address_number,
        street=address_data_1.street,
        city=address_data_2.city,
        state=address_data_2.state,
        zip_code=address_data_2.zip_code,
        street_pre_type=address_data_1.street_pre_type,
        street_post_type=address_data_1.street_post_type,
        street_pre_directional=address_data_1.street_name_pre_directional,
        street_post_directional=address_data_1.street_name_post_directional,
        sub_address_type=address_data_1.sub_address_type,
        sub_address_type_id=address_data_1.sub_address_type_id,
        occupancy_type=address_data_1.occupancy_type,
        occupancy_type_id=address_data_1.occupancy_type_id,
        address_1_string=address_1_string,
        address_2_string=address_2_string,
    )


def is_valid_address():
    raise NotImplementedError


def get_valid_addresses(text: str, is_one_line: bool = False, string_range: int = 2) -> List[AddressMatch]:
    """Parse a string and return a list of address matches.
    The method looks for the full address in which the required values are:
        "address_number", "street", "city", "state", "zip_code"

    The method splits the address line into parts:
        - address_number
        - street
        - street_pre_type
        - street_post_type
        - street_pre_directional
        - street_post_directional
        - sub_address_type
        - sub_address_type_id
        - occupancy_type
        - occupancy_type_id
        - city
        - state
        - zip_code

    Args:
        text (str): text from OCR results.
        is_one_line (bool, optional): flag to looks for address line 1 and address line 2 on multiple lines.
        Defaults to False.
        string_range (int, optional): number of lines after line address 1 in which to search for line 2 address.
        Defaults to 2.

    Returns:
        List[AddressMatch]: List of AddressMatch objects.
    """
    address_matches: List[AddressMatch] = []
    row_start_idx = 0
    for idx, row in enumerate(text.split("\n")):
        address_data = __AddressData(row)

        if not address_data.is_valid_full_address():
            address_data = __AddressData(_try_split_state_and_zip_code(row))
        if address_data.is_valid_full_address():
            address_string = row[
                row.index(address_data.address_number) : row.index(address_data.zip_code) + len(address_data.zip_code)
            ]
            start = row_start_idx + row.index(address_string)
            end = start + len(address_string)

            addr_1_last_val = address_data.get_address_1_last_value()
            if addr_1_last_val:
                addr_1_end = address_string.rindex(addr_1_last_val) + len(addr_1_last_val)
            else:
                addr_1_end = len(address_string)
            address_1_string = address_string[:addr_1_end].strip()
            address_2_string = address_string[address_string.index(address_data.city) :].strip()

            address_matches.append(
                __address_data_to_address_match(
                    address_string, start, end, address_data, address_1_string, address_2_string
                )
            )

        row_start_idx += len(row) + 1

    if not is_one_line:
        raw_text = text.split("\n")

        row_start_idx = 0
        for idx, row in enumerate(raw_text):
            address_data_1 = __AddressData(row)
            if address_data_1.is_valid_address_1() and not address_data_1.is_valid_full_address():
                # Search Address 2 in next {string_range} rows
                next_row_start_idx = row_start_idx + len(row) + 1
                for next_row in raw_text[idx + 1 : idx + 1 + string_range]:
                    address_data_2 = __AddressData(next_row)
                    if not address_data_2.is_valid_address_2():
                        address_data_2 = __AddressData(_try_split_state_and_zip_code(row))

                    if address_data_2.is_valid_address_2():
                        addr1_last_val = address_data_1.get_address_1_last_value()
                        if addr1_last_val:
                            end_idx = row.rindex(addr1_last_val) + len(addr1_last_val)
                        else:
                            end_idx = len(row)
                        address_1_string = row[row.index(address_data_1.address_number) : end_idx]
                        address_2_string = next_row[
                            next_row.index(address_data_2.city) : next_row.rindex(address_data_2.zip_code)
                            + len(address_data_2.zip_code)
                        ]

                        start = row_start_idx + row.index(address_1_string)
                        end = next_row_start_idx + next_row.rindex(address_2_string) + len(address_2_string)
                        string = text[start:end]
                        address_matches.append(
                            __address_data_to_address_match_multi_line(
                                string, start, end, address_data_1, address_data_2, address_1_string, address_2_string
                            )
                        )

                    next_row_start_idx += len(next_row) + 1

            row_start_idx += len(row) + 1
    return address_matches
