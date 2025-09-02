import logging
import re
from datetime import datetime, timezone
from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv4Interface,
    AddressValueError,
    IPv6Address,
    IPv6Network,
    IPv6Interface,
    ip_network,
)
from json import JSONDecodeError, loads
from typing import Union, Optional
from urllib.parse import urljoin
from uuid import UUID

import macaddress
from dateutil import parser
from httpx import Response, Timeout, Proxy, HTTPStatusError
from httpx._types import URLTypes
from pydantic import InstanceOf
from pytz import BaseTzInfo, utc

logger = logging.getLogger("ipfabric")

LAST_ID, PREV_ID, LASTLOCKED_ID = "$last", "$prev", "$lastLocked"
VALID_REFS_DICT = {
    LAST_ID.lower(): LAST_ID,
    PREV_ID.lower(): PREV_ID,
    LASTLOCKED_ID.lower(): LASTLOCKED_ID,
}
VALID_REFS = [LAST_ID, PREV_ID, LASTLOCKED_ID]
VALID_IP = Union[IPv4Address, IPv4Network, IPv4Interface]
VALID_IPv6 = Union[IPv6Address, IPv6Network, IPv6Interface]
SLUG = re.compile(r"^[a-zA-Z0-9_\-.#:]*$")

ProxyTypes = Union[None, URLTypes, InstanceOf[Proxy]]
TimeoutTypes = Union[
    Optional[float], tuple[Optional[float], Optional[float], Optional[float], Optional[float]], Timeout, None
]


def valid_snapshot(snapshot: Union[None, str], init: bool = False) -> str:
    if snapshot is None:
        return snapshot
    elif isinstance(snapshot, UUID):
        return str(snapshot).lower()
    elif snapshot.lower() in VALID_REFS_DICT:
        return VALID_REFS_DICT[snapshot.lower()]
    elif re.match(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", snapshot.lower()):
        return snapshot.lower()
    else:
        msg = "'IPF_SNAPSHOT' env variable or 'snapshot_id' argument" if init else "Snapshot ID"
        raise ValueError(f"{msg} '{snapshot}' is not valid, must be a UUID or one of {VALID_REFS}.")


def format_error_message(response: Response) -> str:
    msg = response.json()
    message = ""
    for idx, error in enumerate(msg.get("errors", [])):
        message += f"\nError {idx} Message: '{error['message']}"
        if error["field"]:
            message += f"\nError {idx} Field: {error['field']}"
            try:
                if error["field"][0] == "columns":
                    column = (
                        loads(response.url.params["columns"])[error["field"][1]]
                        if response.url.params
                        else loads(response.request.content)["columns"][error["field"][1]]
                    )
                    message += f"\nError {idx} Invalid Column Name: '{column}'"
            except (KeyError, IndexError, JSONDecodeError):
                pass
    return message


def raise_for_status(response: Response) -> Response:
    """
    Raise the `HTTPStatusError` if one occurred.
    """
    request = response._request

    if request is None:
        raise RuntimeError("Cannot call `raise_for_status` as the request instance has not been set on this response.")
    if response.is_success:
        return response

    error_type = {
        1: "Informational response",
        3: "Redirect response",
        4: "Client error",
        5: "Server error",
    }.get(response.status_code // 100, "Invalid status code")
    url = urljoin(str(response.url), response.url.path)
    query = f"\nQuery: '{response.url.query}'" if response.url.query else ""

    if response.has_redirect_location:
        message = (
            f"{error_type} '{response.status_code} {response.reason_phrase}' for url '{url}'{query}"
            f"\nRedirect location: '{response.headers['location']}'"
        )
    else:
        try:
            msg = response.json()
            message = (
                f"{error_type} '{response.status_code} {response.reason_phrase}' for url '{url}'{query}"
                f"\n{msg['code']}: {msg['message']}"
            )
            message += format_error_message(response)
        except (JSONDecodeError, TypeError, KeyError):
            message = f"{error_type} '{response.status_code} {response.reason_phrase}' for url '{url}'{query}"

    raise HTTPStatusError(message, request=request, response=response)


def valid_slug(name: str):
    if not SLUG.match(name):
        raise ValueError(f"{name} is not a valid slug/name and must match regex {SLUG.pattern}.")
    return name


def validate_ip_network(
    ip: Union[str, VALID_IP, VALID_IPv6],
    max_size: Optional[int] = None,
    max_v6_size: Optional[int] = None,
    ipv6: bool = False,
) -> Union[IPv4Network, IPv6Network]:
    try:
        ip = ip_network(ip, strict=False)
    except AddressValueError:
        raise ValueError(f'IP "{ip}" not a valid IPv4/6 Address or Network.')

    if ip.version == 6 and not ipv6:
        raise ValueError(f"IP {ip} is IPv6 and IPv6 is not supported.")
    if ip.version == 4 and max_size and ip.prefixlen < max_size:
        raise ValueError(f"Network {ip} is larger than the maximum allowed prefix length of {max_size}.")
    if ip.version == 6 and max_v6_size and ip.prefixlen < max_v6_size:
        raise ValueError(f"Network {ip} is larger than the maximum allowed prefix length of {max_v6_size}.")
    return ip


def validate_ip_network_str(
    ip: Union[str, IPv4Address, IPv4Network, IPv4Interface],
    max_size: Optional[int] = None,
    max_v6_size: Optional[int] = None,
    ipv6: bool = False,
) -> str:
    return str(validate_ip_network(ip, max_size, max_v6_size, ipv6))


def create_filter(client, url, filters=None, sn=None) -> tuple:
    all_columns = client.get_columns(url)
    if not any([_ in ["sn", "localSn"] for _ in all_columns]):
        raise KeyError(f'Column "sn" or "localSn" not found in "{url}" table.')
    f = {"sn": ["eq", sn]} if "sn" in all_columns else {"localSn": ["eq", sn]}
    if filters:
        f = {"and": [f, filters]}
    return all_columns, f


class MAC(macaddress.MAC):
    formats = ("xxxx.xxxx.xxxx",) + macaddress.MAC.formats


def convert_timestamp(
    ts: int, ts_format: str = "datetime", milliseconds: bool = True, tzinfo: BaseTzInfo = utc
) -> datetime:
    """Converts IP Fabric timestamp in milliseconds to a formatted time

    Args:
        ts: int: Timestamp in milliseconds (IP Fabric's returned format)
        ts_format: str: Default datetime, can be ['datetime', 'iso', 'ziso', 'date']
        milliseconds: bool: Default True to return milliseconds, False returns seconds
        tzinfo: pytz object: Default utc
    Returns:
        date time object in the requested format
    """
    dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).astimezone(tzinfo)
    if ts_format == "datetime":
        return dt
    elif ts_format == "iso":
        return dt.isoformat(timespec="milliseconds" if milliseconds else "seconds")
    elif ts_format == "ziso":
        return dt.isoformat(timespec="milliseconds" if milliseconds else "seconds").replace("+00:00", "Z")
    elif ts_format == "date":
        return dt.date()
    else:
        raise SyntaxError(f"{ts_format} is not one of ['datetime', 'iso', 'ziso', 'date'].")


def date_parser(timestamp: Union[int, str]) -> datetime:
    return (
        datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if isinstance(timestamp, int)
        else parser.parse(timestamp).replace(tzinfo=timezone.utc)
    )


def parse_mac(mac_address) -> Union[str, list, None]:
    """Takes any format MAC address and return IP Fabric format.

    Args:
        mac_address: Union[str, list]: String or list of MAC address
    Returns:
        String or list of MAC address
    """

    def mac_format(mac):
        try:
            return str(MAC(mac.strip())).lower()
        except ValueError:
            logger.warning(f"{mac.strip()} is not a valid mac.")
            return None

    if isinstance(mac_address, str):
        return mac_format(mac_address)
    elif isinstance(mac_address, list):
        parsed = list()
        for m in mac_address:
            if not m:
                continue
            mac = mac_format(m)
            if mac:
                parsed.append(mac)

        return parsed
    return None


TIMEZONES = {
    "africa/abidjan": "Africa/Abidjan",
    "africa/accra": "Africa/Accra",
    "africa/addis_ababa": "Africa/Addis_Ababa",
    "africa/algiers": "Africa/Algiers",
    "africa/asmara": "Africa/Asmara",
    "africa/bamako": "Africa/Bamako",
    "africa/bangui": "Africa/Bangui",
    "africa/banjul": "Africa/Banjul",
    "africa/bissau": "Africa/Bissau",
    "africa/blantyre": "Africa/Blantyre",
    "africa/brazzaville": "Africa/Brazzaville",
    "africa/bujumbura": "Africa/Bujumbura",
    "africa/cairo": "Africa/Cairo",
    "africa/casablanca": "Africa/Casablanca",
    "africa/ceuta": "Africa/Ceuta",
    "africa/conakry": "Africa/Conakry",
    "africa/dakar": "Africa/Dakar",
    "africa/dar_es_salaam": "Africa/Dar_es_Salaam",
    "africa/djibouti": "Africa/Djibouti",
    "africa/douala": "Africa/Douala",
    "africa/el_aaiun": "Africa/El_Aaiun",
    "africa/freetown": "Africa/Freetown",
    "africa/gaborone": "Africa/Gaborone",
    "africa/harare": "Africa/Harare",
    "africa/johannesburg": "Africa/Johannesburg",
    "africa/juba": "Africa/Juba",
    "africa/kampala": "Africa/Kampala",
    "africa/khartoum": "Africa/Khartoum",
    "africa/kigali": "Africa/Kigali",
    "africa/kinshasa": "Africa/Kinshasa",
    "africa/lagos": "Africa/Lagos",
    "africa/libreville": "Africa/Libreville",
    "africa/lome": "Africa/Lome",
    "africa/luanda": "Africa/Luanda",
    "africa/lubumbashi": "Africa/Lubumbashi",
    "africa/lusaka": "Africa/Lusaka",
    "africa/malabo": "Africa/Malabo",
    "africa/maputo": "Africa/Maputo",
    "africa/maseru": "Africa/Maseru",
    "africa/mbabane": "Africa/Mbabane",
    "africa/mogadishu": "Africa/Mogadishu",
    "africa/monrovia": "Africa/Monrovia",
    "africa/nairobi": "Africa/Nairobi",
    "africa/ndjamena": "Africa/Ndjamena",
    "africa/niamey": "Africa/Niamey",
    "africa/nouakchott": "Africa/Nouakchott",
    "africa/ouagadougou": "Africa/Ouagadougou",
    "africa/porto-novo": "Africa/Porto-Novo",
    "africa/sao_tome": "Africa/Sao_Tome",
    "africa/tripoli": "Africa/Tripoli",
    "africa/tunis": "Africa/Tunis",
    "africa/windhoek": "Africa/Windhoek",
    "america/adak": "America/Adak",
    "america/anchorage": "America/Anchorage",
    "america/anguilla": "America/Anguilla",
    "america/antigua": "America/Antigua",
    "america/araguaina": "America/Araguaina",
    "america/argentina/buenos_aires": "America/Argentina/Buenos_Aires",
    "america/argentina/catamarca": "America/Argentina/Catamarca",
    "america/argentina/cordoba": "America/Argentina/Cordoba",
    "america/argentina/jujuy": "America/Argentina/Jujuy",
    "america/argentina/la_rioja": "America/Argentina/La_Rioja",
    "america/argentina/mendoza": "America/Argentina/Mendoza",
    "america/argentina/rio_gallegos": "America/Argentina/Rio_Gallegos",
    "america/argentina/salta": "America/Argentina/Salta",
    "america/argentina/san_juan": "America/Argentina/San_Juan",
    "america/argentina/san_luis": "America/Argentina/San_Luis",
    "america/argentina/tucuman": "America/Argentina/Tucuman",
    "america/argentina/ushuaia": "America/Argentina/Ushuaia",
    "america/aruba": "America/Aruba",
    "america/asuncion": "America/Asuncion",
    "america/atikokan": "America/Atikokan",
    "america/bahia": "America/Bahia",
    "america/bahia_banderas": "America/Bahia_Banderas",
    "america/barbados": "America/Barbados",
    "america/belem": "America/Belem",
    "america/belize": "America/Belize",
    "america/blanc-sablon": "America/Blanc-Sablon",
    "america/boa_vista": "America/Boa_Vista",
    "america/bogota": "America/Bogota",
    "america/boise": "America/Boise",
    "america/cambridge_bay": "America/Cambridge_Bay",
    "america/campo_grande": "America/Campo_Grande",
    "america/cancun": "America/Cancun",
    "america/caracas": "America/Caracas",
    "america/cayenne": "America/Cayenne",
    "america/cayman": "America/Cayman",
    "america/chicago": "America/Chicago",
    "america/chihuahua": "America/Chihuahua",
    "america/costa_rica": "America/Costa_Rica",
    "america/creston": "America/Creston",
    "america/cuiaba": "America/Cuiaba",
    "america/curacao": "America/Curacao",
    "america/danmarkshavn": "America/Danmarkshavn",
    "america/dawson": "America/Dawson",
    "america/dawson_creek": "America/Dawson_Creek",
    "america/denver": "America/Denver",
    "america/detroit": "America/Detroit",
    "america/dominica": "America/Dominica",
    "america/edmonton": "America/Edmonton",
    "america/eirunepe": "America/Eirunepe",
    "america/el_salvador": "America/El_Salvador",
    "america/fort_nelson": "America/Fort_Nelson",
    "america/fortaleza": "America/Fortaleza",
    "america/glace_bay": "America/Glace_Bay",
    "america/goose_bay": "America/Goose_Bay",
    "america/grand_turk": "America/Grand_Turk",
    "america/grenada": "America/Grenada",
    "america/guadeloupe": "America/Guadeloupe",
    "america/guatemala": "America/Guatemala",
    "america/guayaquil": "America/Guayaquil",
    "america/guyana": "America/Guyana",
    "america/halifax": "America/Halifax",
    "america/havana": "America/Havana",
    "america/hermosillo": "America/Hermosillo",
    "america/indiana/indianapolis": "America/Indiana/Indianapolis",
    "america/indiana/knox": "America/Indiana/Knox",
    "america/indiana/marengo": "America/Indiana/Marengo",
    "america/indiana/petersburg": "America/Indiana/Petersburg",
    "america/indiana/tell_city": "America/Indiana/Tell_City",
    "america/indiana/vevay": "America/Indiana/Vevay",
    "america/indiana/vincennes": "America/Indiana/Vincennes",
    "america/indiana/winamac": "America/Indiana/Winamac",
    "america/inuvik": "America/Inuvik",
    "america/iqaluit": "America/Iqaluit",
    "america/jamaica": "America/Jamaica",
    "america/juneau": "America/Juneau",
    "america/kentucky/louisville": "America/Kentucky/Louisville",
    "america/kentucky/monticello": "America/Kentucky/Monticello",
    "america/kralendijk": "America/Kralendijk",
    "america/la_paz": "America/La_Paz",
    "america/lima": "America/Lima",
    "america/los_angeles": "America/Los_Angeles",
    "america/lower_princes": "America/Lower_Princes",
    "america/maceio": "America/Maceio",
    "america/managua": "America/Managua",
    "america/manaus": "America/Manaus",
    "america/marigot": "America/Marigot",
    "america/martinique": "America/Martinique",
    "america/matamoros": "America/Matamoros",
    "america/mazatlan": "America/Mazatlan",
    "america/menominee": "America/Menominee",
    "america/merida": "America/Merida",
    "america/metlakatla": "America/Metlakatla",
    "america/mexico_city": "America/Mexico_City",
    "america/miquelon": "America/Miquelon",
    "america/moncton": "America/Moncton",
    "america/monterrey": "America/Monterrey",
    "america/montevideo": "America/Montevideo",
    "america/montserrat": "America/Montserrat",
    "america/nassau": "America/Nassau",
    "america/new_york": "America/New_York",
    "america/nipigon": "America/Nipigon",
    "america/nome": "America/Nome",
    "america/noronha": "America/Noronha",
    "america/north_dakota/beulah": "America/North_Dakota/Beulah",
    "america/north_dakota/center": "America/North_Dakota/Center",
    "america/north_dakota/new_salem": "America/North_Dakota/New_Salem",
    "america/nuuk": "America/Nuuk",
    "america/ojinaga": "America/Ojinaga",
    "america/panama": "America/Panama",
    "america/pangnirtung": "America/Pangnirtung",
    "america/paramaribo": "America/Paramaribo",
    "america/phoenix": "America/Phoenix",
    "america/port-au-prince": "America/Port-au-Prince",
    "america/port_of_spain": "America/Port_of_Spain",
    "america/porto_velho": "America/Porto_Velho",
    "america/puerto_rico": "America/Puerto_Rico",
    "america/punta_arenas": "America/Punta_Arenas",
    "america/rainy_river": "America/Rainy_River",
    "america/rankin_inlet": "America/Rankin_Inlet",
    "america/recife": "America/Recife",
    "america/regina": "America/Regina",
    "america/resolute": "America/Resolute",
    "america/rio_branco": "America/Rio_Branco",
    "america/santarem": "America/Santarem",
    "america/santiago": "America/Santiago",
    "america/santo_domingo": "America/Santo_Domingo",
    "america/sao_paulo": "America/Sao_Paulo",
    "america/scoresbysund": "America/Scoresbysund",
    "america/sitka": "America/Sitka",
    "america/st_barthelemy": "America/St_Barthelemy",
    "america/st_johns": "America/St_Johns",
    "america/st_kitts": "America/St_Kitts",
    "america/st_lucia": "America/St_Lucia",
    "america/st_thomas": "America/St_Thomas",
    "america/st_vincent": "America/St_Vincent",
    "america/swift_current": "America/Swift_Current",
    "america/tegucigalpa": "America/Tegucigalpa",
    "america/thule": "America/Thule",
    "america/thunder_bay": "America/Thunder_Bay",
    "america/tijuana": "America/Tijuana",
    "america/toronto": "America/Toronto",
    "america/tortola": "America/Tortola",
    "america/vancouver": "America/Vancouver",
    "america/whitehorse": "America/Whitehorse",
    "america/winnipeg": "America/Winnipeg",
    "america/yakutat": "America/Yakutat",
    "america/yellowknife": "America/Yellowknife",
    "antarctica/casey": "Antarctica/Casey",
    "antarctica/davis": "Antarctica/Davis",
    "antarctica/dumontdurville": "Antarctica/DumontDUrville",
    "antarctica/macquarie": "Antarctica/Macquarie",
    "antarctica/mawson": "Antarctica/Mawson",
    "antarctica/mcmurdo": "Antarctica/McMurdo",
    "antarctica/palmer": "Antarctica/Palmer",
    "antarctica/rothera": "Antarctica/Rothera",
    "antarctica/syowa": "Antarctica/Syowa",
    "antarctica/troll": "Antarctica/Troll",
    "antarctica/vostok": "Antarctica/Vostok",
    "arctic/longyearbyen": "Arctic/Longyearbyen",
    "asia/aden": "Asia/Aden",
    "asia/almaty": "Asia/Almaty",
    "asia/amman": "Asia/Amman",
    "asia/anadyr": "Asia/Anadyr",
    "asia/aqtau": "Asia/Aqtau",
    "asia/aqtobe": "Asia/Aqtobe",
    "asia/ashgabat": "Asia/Ashgabat",
    "asia/atyrau": "Asia/Atyrau",
    "asia/baghdad": "Asia/Baghdad",
    "asia/bahrain": "Asia/Bahrain",
    "asia/baku": "Asia/Baku",
    "asia/bangkok": "Asia/Bangkok",
    "asia/barnaul": "Asia/Barnaul",
    "asia/beirut": "Asia/Beirut",
    "asia/bishkek": "Asia/Bishkek",
    "asia/brunei": "Asia/Brunei",
    "asia/chita": "Asia/Chita",
    "asia/choibalsan": "Asia/Choibalsan",
    "asia/colombo": "Asia/Colombo",
    "asia/damascus": "Asia/Damascus",
    "asia/dhaka": "Asia/Dhaka",
    "asia/dili": "Asia/Dili",
    "asia/dubai": "Asia/Dubai",
    "asia/dushanbe": "Asia/Dushanbe",
    "asia/famagusta": "Asia/Famagusta",
    "asia/gaza": "Asia/Gaza",
    "asia/hebron": "Asia/Hebron",
    "asia/ho_chi_minh": "Asia/Ho_Chi_Minh",
    "asia/hong_kong": "Asia/Hong_Kong",
    "asia/hovd": "Asia/Hovd",
    "asia/irkutsk": "Asia/Irkutsk",
    "asia/jakarta": "Asia/Jakarta",
    "asia/jayapura": "Asia/Jayapura",
    "asia/jerusalem": "Asia/Jerusalem",
    "asia/kabul": "Asia/Kabul",
    "asia/kamchatka": "Asia/Kamchatka",
    "asia/karachi": "Asia/Karachi",
    "asia/kathmandu": "Asia/Kathmandu",
    "asia/khandyga": "Asia/Khandyga",
    "asia/kolkata": "Asia/Kolkata",
    "asia/krasnoyarsk": "Asia/Krasnoyarsk",
    "asia/kuala_lumpur": "Asia/Kuala_Lumpur",
    "asia/kuching": "Asia/Kuching",
    "asia/kuwait": "Asia/Kuwait",
    "asia/macau": "Asia/Macau",
    "asia/magadan": "Asia/Magadan",
    "asia/makassar": "Asia/Makassar",
    "asia/manila": "Asia/Manila",
    "asia/muscat": "Asia/Muscat",
    "asia/nicosia": "Asia/Nicosia",
    "asia/novokuznetsk": "Asia/Novokuznetsk",
    "asia/novosibirsk": "Asia/Novosibirsk",
    "asia/omsk": "Asia/Omsk",
    "asia/oral": "Asia/Oral",
    "asia/phnom_penh": "Asia/Phnom_Penh",
    "asia/pontianak": "Asia/Pontianak",
    "asia/pyongyang": "Asia/Pyongyang",
    "asia/qatar": "Asia/Qatar",
    "asia/qostanay": "Asia/Qostanay",
    "asia/qyzylorda": "Asia/Qyzylorda",
    "asia/riyadh": "Asia/Riyadh",
    "asia/sakhalin": "Asia/Sakhalin",
    "asia/samarkand": "Asia/Samarkand",
    "asia/seoul": "Asia/Seoul",
    "asia/shanghai": "Asia/Shanghai",
    "asia/singapore": "Asia/Singapore",
    "asia/srednekolymsk": "Asia/Srednekolymsk",
    "asia/taipei": "Asia/Taipei",
    "asia/tashkent": "Asia/Tashkent",
    "asia/tbilisi": "Asia/Tbilisi",
    "asia/tehran": "Asia/Tehran",
    "asia/thimphu": "Asia/Thimphu",
    "asia/tokyo": "Asia/Tokyo",
    "asia/tomsk": "Asia/Tomsk",
    "asia/ulaanbaatar": "Asia/Ulaanbaatar",
    "asia/urumqi": "Asia/Urumqi",
    "asia/ust-nera": "Asia/Ust-Nera",
    "asia/vientiane": "Asia/Vientiane",
    "asia/vladivostok": "Asia/Vladivostok",
    "asia/yakutsk": "Asia/Yakutsk",
    "asia/yangon": "Asia/Yangon",
    "asia/yekaterinburg": "Asia/Yekaterinburg",
    "asia/yerevan": "Asia/Yerevan",
    "atlantic/azores": "Atlantic/Azores",
    "atlantic/bermuda": "Atlantic/Bermuda",
    "atlantic/canary": "Atlantic/Canary",
    "atlantic/cape_verde": "Atlantic/Cape_Verde",
    "atlantic/faroe": "Atlantic/Faroe",
    "atlantic/madeira": "Atlantic/Madeira",
    "atlantic/reykjavik": "Atlantic/Reykjavik",
    "atlantic/south_georgia": "Atlantic/South_Georgia",
    "atlantic/st_helena": "Atlantic/St_Helena",
    "atlantic/stanley": "Atlantic/Stanley",
    "australia/adelaide": "Australia/Adelaide",
    "australia/brisbane": "Australia/Brisbane",
    "australia/broken_hill": "Australia/Broken_Hill",
    "australia/darwin": "Australia/Darwin",
    "australia/eucla": "Australia/Eucla",
    "australia/hobart": "Australia/Hobart",
    "australia/lindeman": "Australia/Lindeman",
    "australia/lord_howe": "Australia/Lord_Howe",
    "australia/melbourne": "Australia/Melbourne",
    "australia/perth": "Australia/Perth",
    "australia/sydney": "Australia/Sydney",
    "europe/amsterdam": "Europe/Amsterdam",
    "europe/andorra": "Europe/Andorra",
    "europe/astrakhan": "Europe/Astrakhan",
    "europe/athens": "Europe/Athens",
    "europe/belgrade": "Europe/Belgrade",
    "europe/berlin": "Europe/Berlin",
    "europe/bratislava": "Europe/Bratislava",
    "europe/brussels": "Europe/Brussels",
    "europe/bucharest": "Europe/Bucharest",
    "europe/budapest": "Europe/Budapest",
    "europe/busingen": "Europe/Busingen",
    "europe/chisinau": "Europe/Chisinau",
    "europe/copenhagen": "Europe/Copenhagen",
    "europe/dublin": "Europe/Dublin",
    "europe/gibraltar": "Europe/Gibraltar",
    "europe/guernsey": "Europe/Guernsey",
    "europe/helsinki": "Europe/Helsinki",
    "europe/isle_of_man": "Europe/Isle_of_Man",
    "europe/istanbul": "Europe/Istanbul",
    "europe/jersey": "Europe/Jersey",
    "europe/kaliningrad": "Europe/Kaliningrad",
    "europe/kiev": "Europe/Kiev",
    "europe/kirov": "Europe/Kirov",
    "europe/lisbon": "Europe/Lisbon",
    "europe/ljubljana": "Europe/Ljubljana",
    "europe/london": "Europe/London",
    "europe/luxembourg": "Europe/Luxembourg",
    "europe/madrid": "Europe/Madrid",
    "europe/malta": "Europe/Malta",
    "europe/mariehamn": "Europe/Mariehamn",
    "europe/minsk": "Europe/Minsk",
    "europe/monaco": "Europe/Monaco",
    "europe/moscow": "Europe/Moscow",
    "europe/oslo": "Europe/Oslo",
    "europe/paris": "Europe/Paris",
    "europe/podgorica": "Europe/Podgorica",
    "europe/prague": "Europe/Prague",
    "europe/riga": "Europe/Riga",
    "europe/rome": "Europe/Rome",
    "europe/samara": "Europe/Samara",
    "europe/san_marino": "Europe/San_Marino",
    "europe/sarajevo": "Europe/Sarajevo",
    "europe/saratov": "Europe/Saratov",
    "europe/simferopol": "Europe/Simferopol",
    "europe/skopje": "Europe/Skopje",
    "europe/sofia": "Europe/Sofia",
    "europe/stockholm": "Europe/Stockholm",
    "europe/tallinn": "Europe/Tallinn",
    "europe/tirane": "Europe/Tirane",
    "europe/ulyanovsk": "Europe/Ulyanovsk",
    "europe/uzhgorod": "Europe/Uzhgorod",
    "europe/vaduz": "Europe/Vaduz",
    "europe/vatican": "Europe/Vatican",
    "europe/vienna": "Europe/Vienna",
    "europe/vilnius": "Europe/Vilnius",
    "europe/volgograd": "Europe/Volgograd",
    "europe/warsaw": "Europe/Warsaw",
    "europe/zagreb": "Europe/Zagreb",
    "europe/zaporozhye": "Europe/Zaporozhye",
    "europe/zurich": "Europe/Zurich",
    "indian/antananarivo": "Indian/Antananarivo",
    "indian/chagos": "Indian/Chagos",
    "indian/christmas": "Indian/Christmas",
    "indian/cocos": "Indian/Cocos",
    "indian/comoro": "Indian/Comoro",
    "indian/kerguelen": "Indian/Kerguelen",
    "indian/mahe": "Indian/Mahe",
    "indian/maldives": "Indian/Maldives",
    "indian/mauritius": "Indian/Mauritius",
    "indian/mayotte": "Indian/Mayotte",
    "indian/reunion": "Indian/Reunion",
    "pacific/apia": "Pacific/Apia",
    "pacific/auckland": "Pacific/Auckland",
    "pacific/bougainville": "Pacific/Bougainville",
    "pacific/chatham": "Pacific/Chatham",
    "pacific/chuuk": "Pacific/Chuuk",
    "pacific/easter": "Pacific/Easter",
    "pacific/efate": "Pacific/Efate",
    "pacific/enderbury": "Pacific/Enderbury",
    "pacific/fakaofo": "Pacific/Fakaofo",
    "pacific/fiji": "Pacific/Fiji",
    "pacific/funafuti": "Pacific/Funafuti",
    "pacific/galapagos": "Pacific/Galapagos",
    "pacific/gambier": "Pacific/Gambier",
    "pacific/guadalcanal": "Pacific/Guadalcanal",
    "pacific/guam": "Pacific/Guam",
    "pacific/honolulu": "Pacific/Honolulu",
    "pacific/kiritimati": "Pacific/Kiritimati",
    "pacific/kosrae": "Pacific/Kosrae",
    "pacific/kwajalein": "Pacific/Kwajalein",
    "pacific/majuro": "Pacific/Majuro",
    "pacific/marquesas": "Pacific/Marquesas",
    "pacific/midway": "Pacific/Midway",
    "pacific/nauru": "Pacific/Nauru",
    "pacific/niue": "Pacific/Niue",
    "pacific/norfolk": "Pacific/Norfolk",
    "pacific/noumea": "Pacific/Noumea",
    "pacific/pago_pago": "Pacific/Pago_Pago",
    "pacific/palau": "Pacific/Palau",
    "pacific/pitcairn": "Pacific/Pitcairn",
    "pacific/pohnpei": "Pacific/Pohnpei",
    "pacific/port_moresby": "Pacific/Port_Moresby",
    "pacific/rarotonga": "Pacific/Rarotonga",
    "pacific/saipan": "Pacific/Saipan",
    "pacific/tahiti": "Pacific/Tahiti",
    "pacific/tarawa": "Pacific/Tarawa",
    "pacific/tongatapu": "Pacific/Tongatapu",
    "pacific/wake": "Pacific/Wake",
    "pacific/wallis": "Pacific/Wallis",
    "utc": "UTC",
}
