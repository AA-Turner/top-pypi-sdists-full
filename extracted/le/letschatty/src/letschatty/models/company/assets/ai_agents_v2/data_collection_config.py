from pydantic import BaseModel, Field
from typing import List


class DataCollectionFormField(BaseModel):
    """
    Form field reference with required flag.
    """
    field_key: str = Field(description="The field_key of the FormField")
    required: bool = Field(default=False, description="Whether this field is required")


class DataCollectionConfig(BaseModel):
    """
    Configuration for standalone data collection.
    """
    form_fields: List[DataCollectionFormField] = Field(
        default_factory=list,
        description="List of form fields to collect with required status"
    )

    @property
    def has_form_fields(self) -> bool:
        return len(self.form_fields) > 0

    @property
    def is_configured(self) -> bool:
        return self.has_form_fields

    def get_field_keys(self) -> List[str]:
        return [f.field_key for f in self.form_fields]

    def get_required_field_keys(self) -> List[str]:
        return [f.field_key for f in self.form_fields if f.required]
