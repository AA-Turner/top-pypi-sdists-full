import phonenumbers
from phonenumbers import region_code_for_number
import pycountry
from pycountry.db import Country
from letschatty.models.chat.client import Client, ClientData
from letschatty.models.messages.message_templates.filled_data_from_frontend import FilledTemplateData
class ClientService:

    @staticmethod
    def find_country_with_phone(person_phone: str) -> str:
        """
        Find country name based on phone number.

        Args:
            person_phone (str): Phone number string without '+' prefix

        Returns:
            str: Country name or 'Unknown' if country cannot be determined
        """
        try:
            pn = phonenumbers.parse(f"+{person_phone}")
            country_code = region_code_for_number(pn)
            if not country_code:
                return "Unknown"
            country: Country = pycountry.countries.get(alpha_2=country_code)
            if not country:
                return "Unknown"
            return country.name
        except (phonenumbers.NumberParseException, AttributeError) as error:
            return "Unknown"
