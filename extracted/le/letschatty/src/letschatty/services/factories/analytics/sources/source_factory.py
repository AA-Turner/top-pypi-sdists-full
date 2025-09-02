from __future__ import annotations
from typing import Dict, Type, TYPE_CHECKING
import logging

from .....models.analytics.sources import WhatsAppDefaultSource, TopicDefaultSource, PureAd, Source, TemplateSource, OtherSource
from .....models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation
from .....models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIMode
from .....models.utils.types.identifier import StrObjectId
from .....models.utils.types.source_types import SourceType, SourceCheckerType
from .helpers import SourceFactoryHelpers
from datetime import datetime
from zoneinfo import ZoneInfo
import traceback

from bson import ObjectId

if TYPE_CHECKING:
    from .....models.messages import ChattyMessage
    from .....models.analytics.smart_messages.topic import Topic

logger = logging.getLogger(__name__)

class SourceFactory:

    @staticmethod
    def instantiate_source(source_data: dict) -> Source:
        """Instantiate a source from a dictionary.
        1) from mongo
        2) from a request (if its new, it creates the id for posterior mongo insertion)
        """
        source_type = source_data.get("type")
        try:
            source_class : Source = SourceFactoryHelpers.source_type_to_class(source_type) #type: ignore
            return source_class(**source_data) #type: ignore
        except Exception as e:
            logger.error(f"Error creating source of type {source_type}: {str(e)} {source_data}")
            logger.error(traceback.format_exc())
            raise e

    @staticmethod
    def create_whatsapp_default_source(company_id: str) -> WhatsAppDefaultSource:
        return WhatsAppDefaultSource(
            company_id=company_id,
            created_at=datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.now(ZoneInfo("UTC")),
            )

    @staticmethod
    def create_topic_default_source(topic: Topic, company_id: str, whatsapp_default_source: WhatsAppDefaultSource) -> TopicDefaultSource:
        return TopicDefaultSource(
            topic_id=topic.id,
            name = f"{topic.name} Topic Default Source",
            _id = topic.default_source_id,
            description= "Message matched the Topic but there was no direct source to attribute it to.",
            created_at=topic.created_at,
            updated_at=topic.updated_at,
            company_id=company_id,
            flow=whatsapp_default_source.flow,
            tags=whatsapp_default_source.tags,
            products=whatsapp_default_source.products,
            chatty_ai_agent_config=whatsapp_default_source.chatty_ai_agent_config
            )

    @staticmethod
    def create_new_pure_ad_not_loaded(message: ChattyMessage, company_id: str, whatsapp_default_source: WhatsAppDefaultSource) -> PureAd:
        body = message.referral.body
        headline = message.referral.headline
        source_url = message.referral.source_url
        ad_id = message.referral.source_id
        name_for_ad = f"Nuevo Anuncio de Meta {ad_id} {headline}"
        description = f"Se creó el anuncio ya que no estaba cargado como fuente de origen. \n Info: {source_url} - {body}"

        source_data = {
            "name": name_for_ad,
            "type": SourceType.PURE_AD,
            "ad_id": ad_id,
            "flow": whatsapp_default_source.flow,
            "tags": whatsapp_default_source.tags,
            "products": whatsapp_default_source.products,
            "chatty_ai_agent_config": whatsapp_default_source.chatty_ai_agent_config,
            "description": description,
            "trackeable": True,
            "meta_ad_url": message.referral.source_url,
            "meta_source_type": message.referral.source_type,
            "meta_body": message.referral.body,
            "meta_headline": message.referral.headline,
            "meta_media_type": message.referral.media_type,
            "meta_thumbnail_url": message.referral.thumbnail_url,
            "meta_image_url": message.referral.image_url,
            "meta_video_url": message.referral.video_url,
            "company_id": company_id
            }

        return SourceFactory.instantiate_source(source_data) #type: ignore

    @staticmethod
    def create_new_impure_ad(message: ChattyMessage, company_id: str, whatsapp_default_source: WhatsAppDefaultSource) -> PureAd:
        source_data = {
            "name": f"Anuncio Meta Impuro - {message.referral.source_url}",
            "type": SourceType.PURE_AD,
            "ad_id": "provisional_ad_id" + str(ObjectId()),
            "description": f"El anuncio es impuro porque sólo contiene la url del anuncio (falta el ad_id): {message.referral.source_url}",
            "trackeable": True,
            "meta_ad_url":message.referral.source_url.strip(),
            "flow": whatsapp_default_source.flow,
            "tags": whatsapp_default_source.tags,
            "products": whatsapp_default_source.products,
            "chatty_ai_agent_config": whatsapp_default_source.chatty_ai_agent_config,
            "company_id": company_id
        }
        return SourceFactory.instantiate_source(source_data) #type: ignore

    @staticmethod
    def create_source_from_template(template_name: str, company_id: str) -> TemplateSource:
        return TemplateSource(
            company_id=company_id,
            created_at=datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.now(ZoneInfo("UTC")),
            name=f"Template '{template_name}'",
            description=f"Template '{template_name}'",
            trackeable=True,
            template_name=template_name
            )

    @staticmethod
    def create_literal_source_for_ai_agent_test(company_id: StrObjectId, ai_agent_name: str, chatty_ai_agent_id: StrObjectId, trigger: str) -> OtherSource:
        return OtherSource(
            company_id=company_id,
            created_at=datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.now(ZoneInfo("UTC")),
            name=f"Chatty AI Test {ai_agent_name}",
            description=f"This is a default source for the Chatty AI Agent {ai_agent_name}",
            trackeable=False,
            trigger=trigger,
            source_checker=SourceCheckerType.LITERAL,
            chatty_ai_agent_config=ChattyAIConfigForAutomation(
                agent_id=chatty_ai_agent_id,
                mode=ChattyAIMode.AUTONOMOUS,
                only_for_new_chats=False
            ),
        )