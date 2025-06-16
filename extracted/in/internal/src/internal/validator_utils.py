import re

from .exception.app_exception import PlateNoFormatException, VinLengthOrFormatException, PhoneFormatException, \
    DateFormatException, EMailFormatException
from .utils import sanitize_plate_no


def verify_and_sanitize_plate_no(value: str, is_require: bool = False):
    if is_require and not value:
        raise PlateNoFormatException()

    if value:
        if not re.match(r'^[A-Za-z0-9]{6,7}$', value):
            raise PlateNoFormatException()
    return sanitize_plate_no(value)


def verify_vin(value: str, is_require: bool = False):
    if is_require and not value:
        raise VinLengthOrFormatException()

    if value:
        if not re.match(r'^(?:[A-Za-z0-9]{7}|[A-Za-z0-9]{10}|[A-Za-z0-9]{17})$', value):
            raise VinLengthOrFormatException()


def verify_phone(value: str, is_require: bool = False):
    if is_require and not value:
        raise PhoneFormatException()

    if value:
        if not re.match(r'^09\d{8}$', value):
            raise PhoneFormatException()


def verify_date(value: str, is_require: bool = False):
    if is_require and not value:
        raise DateFormatException()

    if value:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise DateFormatException()


def verify_mail(value: str, is_require: bool = False):
    if is_require and not value:
        raise EMailFormatException()

    if value:
        if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', value):
            raise EMailFormatException()
