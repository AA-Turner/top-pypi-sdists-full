from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Any, ClassVar, List
from letschatty.models.base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
import re


class FormFieldPreview(ChattyAssetPreview):
    """Preview model for FormField - used in list views"""
    field_key: str = Field(description="Unique key identifier for the field")
    is_system_field: bool = Field(default=False, description="True if this is a system/standard field")
    question_example: Optional[str] = Field(default=None, description="Example question for AI")
    description: Optional[str] = Field(default=None, description="Description of the field")


class FormField(CompanyAssetModel):
    """
    Company asset for data collection fields.
    AI handles all validation - no regex or type constraints.

    System fields (is_system_field=True) are standard fields that map directly
    to Client model properties (name, email, phone, document_id, external_id).

    When a system field is customized, a document is created in this same collection
    with is_system_field=True and the same field_key as the base system field.
    The field_key serves as the unique identifier for system field customizations.

    field_key is FROZEN after creation - it cannot be changed.
    """
    name: str = Field(description="Display name of the field (e.g., 'Email', 'Budget')")
    field_key: str = Field(description="Unique key identifier for the field (e.g., 'email', 'budget'). Only letters, numbers, and underscores allowed. Frozen after creation.")
    description: str = Field(
        default="",
        description="Description of what information this field aims to collect"
    )
    question_example: Optional[str] = Field(
        default=None,
        description="Example of how AI should ask for this information"
    )
    is_system_field: bool = Field(
        default=False,
        description="True if this is a system/standard field (cannot be deleted)"
    )

    @field_validator('field_key', mode='before')
    @classmethod
    def normalize_field_key(cls, v: str) -> str:
        """
        Normalize field_key to only contain lowercase letters, numbers, and underscores.
        - Converts to lowercase
        - Replaces spaces and hyphens with underscores
        - Removes any other special characters
        - Strips leading/trailing whitespace
        """
        if not v:
            raise ValueError("field_key cannot be empty")

        # Convert to lowercase and strip whitespace
        normalized = v.lower().strip()

        # Replace spaces and hyphens with underscores
        normalized = normalized.replace(' ', '_').replace('-', '_')

        # Remove any character that's not a letter, number, or underscore
        normalized = re.sub(r'[^a-z0-9_]', '', normalized)

        # Remove consecutive underscores
        normalized = re.sub(r'_+', '_', normalized)

        # Remove leading/trailing underscores
        normalized = normalized.strip('_')

        if not normalized:
            raise ValueError("field_key must contain at least one letter or number")

        return normalized

    # Preview class for API responses
    preview_class: ClassVar[type[FormFieldPreview]] = FormFieldPreview

    @classmethod
    def example_email(cls) -> dict:
        """Example email field"""
        return {
            "name": "Email",
            "field_key": "email",
            "description": "Customer's email address for communication",
            "question_example": "Could you share your email so I can send you more information?",
            "required": True
        }

    @classmethod
    def example_budget(cls) -> dict:
        """Example budget field"""
        return {
            "name": "Budget",
            "field_key": "budget",
            "description": "Customer's budget allocation for the project",
            "question_example": "What's your budget range for this project?"
        }


class SystemFormFields:
    """
    Standard system fields available for all companies.
    These map directly to Client model properties.

    field_key is the unique identifier for system fields.
    """

    # System field keys (used as identifiers)
    SYSTEM_KEYS = ["name", "email", "phone", "document_id", "external_id"]

    @classmethod
    def get_all(cls) -> List[dict]:
        """Get all system form fields as dicts (for API responses)"""
        return [
            cls.name_field(),
            cls.email_field(),
            cls.phone_field(),
            cls.document_id_field(),
            cls.external_id_field(),
        ]

    @classmethod
    def get_all_keys(cls) -> List[str]:
        """Get all system field keys"""
        return cls.SYSTEM_KEYS

    @classmethod
    def is_system_field_key(cls, field_key: str) -> bool:
        """Check if a field_key belongs to a system field"""
        return field_key in cls.SYSTEM_KEYS

    @classmethod
    def get_by_key(cls, field_key: str) -> Optional[dict]:
        """Get a system field by its field_key"""
        fields_map = {
            "name": cls.name_field(),
            "email": cls.email_field(),
            "phone": cls.phone_field(),
            "document_id": cls.document_id_field(),
            "external_id": cls.external_id_field(),
        }
        return fields_map.get(field_key)

    @classmethod
    def name_field(cls) -> dict:
        """Standard name field"""
        return {
            "field_key": "name",
            "name": "Nombre",
            "description": "Nombre del cliente",
            "question_example": "¿Cuál es tu nombre?",
            "is_system_field": True,
            "deleted_at": None
        }

    @classmethod
    def email_field(cls) -> dict:
        """Standard email field"""
        return {
            "field_key": "email",
            "name": "Email",
            "description": "Dirección de correo electrónico del cliente",
            "question_example": "¿Podrías compartirme tu email para enviarte más información?",
            "is_system_field": True,
            "deleted_at": None
        }

    @classmethod
    def phone_field(cls) -> dict:
        """Standard phone field"""
        return {
            "field_key": "phone",
            "name": "Teléfono",
            "description": "Número de teléfono del cliente",
            "question_example": "¿Cuál es tu número de teléfono?",
            "is_system_field": True,
            "deleted_at": None
        }

    @classmethod
    def document_id_field(cls) -> dict:
        """Standard document ID field (DNI/ID)"""
        return {
            "field_key": "document_id",
            "name": "DNI / Documento",
            "description": "Número de documento de identidad del cliente",
            "question_example": "¿Cuál es tu número de DNI o documento?",
            "is_system_field": True,
            "deleted_at": None
        }

    @classmethod
    def external_id_field(cls) -> dict:
        """Standard external/CRM ID field"""
        return {
            "field_key": "external_id",
            "name": "ID Externo / CRM",
            "description": "Identificador externo del cliente en CRM u otro sistema",
            "question_example": "¿Tienes un número de cliente o código de referencia?",
            "is_system_field": True,
            "deleted_at": None
        }


class CollectedData(BaseModel):
    """
    Data collected from customer during conversation.
    AI validates format - we just store strings.
    """
    name: Optional[str] = Field(default=None, description="Customer's name")
    email: Optional[str] = Field(default=None, description="Customer's email address")
    phone: Optional[str] = Field(default=None, description="Customer's phone number")
    document_id: Optional[str] = Field(
        default=None,
        alias="dni",
        description="Customer's DNI/ID number"
    )
    external_id: Optional[str] = Field(
        default=None,
        description="Customer's external CRM/reference ID"
    )

    # Generic key-value store for any other collected fields
    additional_fields: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional collected fields as key-value pairs"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


    @classmethod
    def example(cls) -> dict:
        """Example collected data"""
        return {
            "name": "Juan Perez",
            "email": "customer@example.com",
            "phone": "+5491123456789",
            "dni": "12345678",
            "external_id": "crm_9981",
            "additional_fields": {
                "budget": "10000-50000",
                "timeline": "this_month",
                "company_size": "25"
            }
        }

    @classmethod
    def get_json_schema_property(cls) -> dict:
        """Returns JSON schema for OpenAI structured output"""
        return {
            "type": "object",
            "properties": {
                "name": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": "Customer's name if provided"
                },
                "email": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": "Customer's email address if provided"
                },
                "phone": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": "Customer's phone number if provided"
                },
                "dni": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": "Customer's DNI/ID number if provided"
                },
                "external_id": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": "Customer's external CRM/reference ID if provided"
                },
                "additional_fields": {
                    "type": "object",
                    "additionalProperties": True,
                    "description": "Other collected fields as key-value pairs (e.g., budget, timeline)"
                }
            },
            "required": ["name", "email", "phone", "dni", "external_id", "additional_fields"],
            "additionalProperties": False
        }
