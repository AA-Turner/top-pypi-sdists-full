from enum import Enum

from pydantic import BaseModel

from .policy import Policy

class DataClassificationCategoryId(Enum):
    """
    The normalized identifier of the data classification category.
    """
    Unknown: int = 0
    Personal: int = 1 # Any Personally Identifiable Information (PII), Electronic Personal
                      # Health Information (ePHI), or similarly personal information.
                      # E.g., full name, home address, date of birth, etc.
    Governmental: int = 2 # Any sensitive government identification number related to a
                          # person or other classified material. E.g., Passport numbers,
                          # driver license numbers, business identification, taxation
                          # identifiers, etc.
    Financial: int = 3 # Any financially-related sensitive information or Cardholder
                       # Data (CHD). E.g., banking account numbers, credit card numbers,
                       # International Banking Account Numbers (IBAN), SWIFT codes, etc.
    Business: int = 4 # Any business-specific sensitive data such as intellectual property,
                      # trademarks, copyrights, human resource data, Board of Directors
                      # meeting minutes, and similar.
    Military_And_Law_Enforcement: int = 5 # Any mission-specific sensitive data for military,
                                          # law enforcement, or other government agencies such
                                          # as specifically classified data, weapon systems
                                          # information, or other planning data.
    Security: int = 6 # Any sensitive security-related data such as passwords, passkeys,
                      # IP addresses, API keys, credentials and similar secrets. E.g.,
                      # AWS Access Secret Key, SaaS API Keys, user passwords, database
                      # credentials, etc.
    Other: int = 99

class DataClassification(BaseModel):
    """
    The Data Classification object includes information about data classification
    levels and data category types.
    """

    # Recommended:
    category_id: DataClassificationCategoryId | None = None # The normalized identifier of the data
                                                            # classification category.
    confidentiality_id: int | None = None

    # Optional:
    category: str | None = None # The name of the data classification category that data matched into,
                                # e.g. Financial, Personal, Governmental, etc.
    confidentiality: str | None = None
    policy: Policy | None = None # Details about the data policy that governs data handling and
                                 # security measures related to classification.
