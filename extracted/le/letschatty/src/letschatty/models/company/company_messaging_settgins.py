from pydantic import Field, BaseModel, model_validator
from typing import List, Optional
from enum import StrEnum
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode
from letschatty.models.company.home_widget import HomeWidget

class ProductsInfoLevel(StrEnum):
    """Products info level"""
    NAME = "name"
    DESCRIPTION = "description"
    ALL = "all"

class MessagingSettings(BaseModel):
    """Messaging settings for the company"""
    good_quality_score_definition: Optional[str] = Field(default=None, description="The definition of a good quality score")
    products_info_level : ProductsInfoLevel = Field(default=ProductsInfoLevel.NAME, description="Whether to include all products info in the prompt or just the name / description")
    ai_god_mode : Optional[ChattyAIMode] = Field(default=None, description="The mode of the ai god - null if not active")
    whatsapp_apb_mode : bool = Field(default=False, description="Whether to use the whatsapp apb mode")
    is_coexistence: bool = Field(default=False, description="WhatsApp Coexistence: number shared between Business App and Cloud API")
    is_chattyless: bool = Field(default=False, description="Chattyless tier: coexistence-native, AI-led company. CINTIA routes captured references to supervised probation.")
    signup_origin: Optional[str] = Field(
        default=None,
        description=(
            "Where the company SIGNED UP, stamped once at creation and never rewritten. "
            "'chattyless' = came through the WhatsApp free-report funnel "
            "(whatsapp.letschatty.com); 'standard' = anywhere else. "
            "Deliberately a free string, NOT an enum: new origins (mcp, mobile, partner) "
            "then cost a value in the Auth0 Action instead of a letschatty release. "
            "Distinct from is_chattyless, which is a MUTABLE commercial tier the backoffice "
            "overwrites on every plan save — so a company that converts to a paid plan keeps "
            "its origin here and loses it there."
        ),
    )
    billing_claim_code: Optional[str] = Field(
        default=None,
        description=(
            "Billing claim code, stamped once at signup and never rewritten — the sibling "
            "of signup_origin above. Carried by the signup link "
            "(app.letschatty.com/?codigo=...), forwarded by the Auth0 Action into "
            "company_workspace/create, sanitized there (canonical form: 8 uppercase chars, "
            "ambiguity-free alphabet), and REDEEMED downstream by the billing "
            "COMPANY_CREATED consumer, which links the newborn company to the pay-first "
            "contract that issued the code. Declared here so it rides the COMPANY_CREATED "
            "event (which serializes the whole company model); a raw $set would survive in "
            "Mongo but never reach the event. Single-use enforcement lives in billing, not "
            "here. Spec: lambdas docs/superpowers/specs/2026-08-29-vinculacion-por-codigo-design.md"
        ),
    )
    home_config : Optional[dict[str, bool]] = Field(default=None, description="The config for the home page")
    home_por_rol: Optional[dict[str, List[HomeWidget]]] = Field(default=None, description="Inicio de arranque por rol (claves: valores de UserRole)")
    tagger_instructions: Optional[str] = Field(default=None, description="The instructions for the tagger when using the tagger ai agent")
    allow_unconfigured_additional_fields: bool = Field(
        default=False,
        description="If true, tagger may collect and persist non-configured additional_fields keys"
    )
    tagger_funnel_assignment_enabled: bool = Field(
        default=False,
        description="If true, tagger will attempt to assign funnels to chats that have no funnel yet"
    )
    hide_chats: bool = Field(
        default=False,
        description="Do not expose conversations in the frontend — for companies exclusively on WhatsApp Business App that need extra privacy"
    )
    is_executive_chatty: bool = Field(
        default=False,
        description="Executive Chatty: the owner interacts only via WhatsApp nudges, not the Chatty inbox. Forces hide_chats so chats/previews are suppressed in the frontend."
    )
    is_transient_for_lead_magnet: bool = Field(
        default=False,
        description="Lead-magnet ephemeral company: parse + emit coexistence history to Redshift, "
                    "but never persist chats/messages to Mongo and never emit live-message events."
    )
    self_assign_chats_enabled: bool = Field(
        default=True,
        description="Whether employees can self-assign a batch of prioritized waiting chats via the "
                    "'Asignarme chats' button. Default True to preserve existing behavior; company "
                    "admins can disable it from the configuration page for the whole team."
    )
    agents_can_see_unassigned_chats: bool = Field(
        default=True,
        description="Whether restricted users (plain agents — those without "
                    "`can_see_all_agents_chats`) can see chats that have NO agent assigned. "
                    "Default True, which is the historical behavior: an agent sees their own "
                    "chats plus every free one. Set to False and an agent only ever sees the "
                    "chats assigned to them — 'Esperando agente' goes empty for them and chats "
                    "have to reach them by assignment (manual, auto-assign or 'Asignarme chats'). "
                    "Has no effect on super_agent / overviewer / admin / owner / mega-admin, on "
                    "copilots and integrations, or on APB companies, where assignment is "
                    "machinery and not ownership."
    )

    @model_validator(mode='after')
    def executive_chatty_forces_hide_chats(self) -> "MessagingSettings":
        """Executive Chatty companies never use the inbox — the owner only receives
        WhatsApp nudges. So is_executive_chatty forces hide_chats, reusing the existing
        chat/preview suppression guards rather than introducing a parallel mechanism."""
        if self.is_executive_chatty:
            self.hide_chats = True
        return self
