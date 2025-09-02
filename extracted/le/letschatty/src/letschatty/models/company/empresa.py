from pydantic import Field, ConfigDict, field_validator, SecretStr, model_validator
from typing import Optional, List, Dict
from ..base_models import ChattyAssetModel
from letschatty.models.channels.channel import WhatsAppClientInfo
from letschatty.models.utils.types import StrObjectId

class EmpresaModel(ChattyAssetModel):
    name: str = Field(description="The name of the company")
    frozen_name: str = Field(description="The frozen name of the company", frozen=True)
    industry: Optional[str] = Field(default = "")
    url: Optional[str] = Field(default = "")
    allowed_origins: list[str] = Field(default_factory=lambda: [])
    company_email: Optional[str] = Field(default = "")
    contributor_count: Optional[str] = Field(default = "")
    purpose_of_use_chatty: Optional[List[str]] = Field(default_factory=lambda: [])
    current_wpp_approach: Optional[str] = Field(default = "")
    main_reason_to_use_chatty: Optional[str] = Field(default = "")
    active: Optional[bool] = Field(default = True)
    friendly_aliases: list[str] = Field(description="The friendly aliases of the company used for the enviamewhats.app links", default_factory=lambda: [])
    terms_of_service_agreement: Optional[bool] = Field(default = False)
    display_phone_number: str = Field(description="The display phone number user's write to", default = "33333333333333", alias="display_phone_number")
    phone_number_id: Optional[str] = Field(description="The phone number id of the company", alias="phone_number_id", default = None)
    business_account_id: Optional[str] = Field(description="The WABA - WhatsApp Business Account id of the company", default = None, alias="bussiness_account_id")
    photo_url: str = Field(default = "")
    meta_token: Optional[str] = Field(default = None, alias="meta_token")
    slack_channels: Dict[str,Dict[str,str]] = Field(default_factory=lambda:{})
    phone_numbers_for_testing: list[str] = Field(default_factory=lambda: [])
    analytics : Optional[bool] = Field(default = True)
    dataset_id: Optional[str] = Field(default = None, description="To notify events to Meta Conversions API")
    hammer_credentials: Optional[Dict[str,str]] = Field(default = None, description="Only usef for hammer propiedades real state agencies")
    continuous_conversation_template_name: Optional[str] = Field(default = None, description="The name of the continuous conversation template")
    default_follow_up_strategy_id: Optional[StrObjectId] = Field(default = None, description="The id of the default follow up strategy")

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_validator("display_phone_number", mode="before")
    def validate_display_phone_number(cls, v):
        if v is None:
            return "33333333333333"
        return v

    @model_validator(mode="before")
    def validate_frozen_name(cls, data: Dict) -> Dict:
        if "frozen_name" not in data:
            data["frozen_name"] = data["name"].replace(" ", "_")
        return data

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        return v

    @property
    def default_follow_up_strategy_id_value(self) -> StrObjectId:
        if self.default_follow_up_strategy_id is None:
            raise ValueError(f"default_follow_up_strategy_id is not set for company {self.name}")
        return self.default_follow_up_strategy_id

    @property
    def active_continuous_conversation_template_name(self) -> str:
        if not self.continuous_conversation_template_name:
            raise ValueError(f"continuous_conversation_template_name is not set for company {self.name}")
        return self.continuous_conversation_template_name

    @property
    def waba_id_value(self) -> str:
        if self.business_account_id is None:
            raise ValueError(f"business_account_id is not set for company {self.name}")
        return self.business_account_id

    @property
    def phone_number_id_value(self) -> str:
        if self.phone_number_id is None:
            raise ValueError(f"phone_number_id is not set for company {self.name}")
        return self.phone_number_id

    @property
    def meta_token_value(self) -> str:
        if self.meta_token is None:
            raise ValueError(f"meta_token is not set for company {self.name}")
        return self.meta_token


    @property
    def whatsapp_channel(self) -> WhatsAppClientInfo:
        if self.active_for_messaging:
            return WhatsAppClientInfo(
                display_phone_number=self.display_phone_number_value,
                business_phone_number_id=self.phone_number_id_value,
                waba_id=self.waba_id_value,
                access_token=SecretStr(self.meta_token_value),
                dataset_id=self.dataset_id
            )
        else:
            raise ValueError(f"Company {self.name} is not active for messaging")

    @property
    def friendly_alias(self):
        return self.friendly_aliases[0]

    @property
    def display_phone_number_value(self):
        if self.display_phone_number is None:
            raise ValueError(f"display_phone_number is not set for company {self.name}")
        return self.display_phone_number

    @property
    def active_for_messaging(self) -> bool:
        try:
            self.meta_token_value
            self.phone_number_id_value
            self.waba_id_value
            self.display_phone_number_value
            return True
        except ValueError:
            return False