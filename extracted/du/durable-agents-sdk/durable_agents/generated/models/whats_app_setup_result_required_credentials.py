from enum import Enum

class WhatsAppSetupResult_required_credentials(str, Enum):
    Access_token = "access_token",
    Phone_number_id = "phone_number_id",

