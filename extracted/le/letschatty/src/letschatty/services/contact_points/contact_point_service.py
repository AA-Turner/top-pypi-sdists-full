from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import logging

from letschatty.models.company.assets.contact_point import ContactPoint
from letschatty.models.utils.types.source_types import SourceCheckerType
from letschatty.models.utils.types import StrObjectId
from datetime import datetime
if TYPE_CHECKING:
    from letschatty.models.messages.chatty_messages import ChattyMessage
    from letschatty.models.chat.chat import Chat
    from letschatty.models.analytics.sources import *
    from letschatty.models.analytics.sources.utms.referer_info import RefererInfo

logger = logging.getLogger("logger")
highlights_logger = logging.getLogger("highlights")

class ContactPointService:

    @staticmethod
    def create_matched_from_message_and_source(source: Source, company_id: str,chat: Chat, message: ChattyMessage) -> ContactPoint:
        """
        Contact points that are created directly from a message, for an existing chat.
        For sources with source_checker_method: Literal, referral, similarity.
        """
        topic_id = getattr(source, "topic_id", None)
        return ContactPoint(
            source_id=source.id,
            source_checker_method=source.source_checker,
            topic_id=topic_id,
            company_id=company_id,
            chat_id=chat.identifier,
            message_id=message.id,
            match_timestamp=message.created_at,
            ctwa_clid=message.referral.ctwa_clid,
            new_chat=False,
            matched=True,
            created_at=message.created_at,
            updated_at=message.created_at
            )

    @staticmethod
    def create_unmatched_from_chatty_pixel_referer_info(referer_info: RefererInfo, company_id: str) -> ContactPoint:
        """ We received a ChattyPixel message request, but there's no chat nor message still.
        We create a contact point for it, but it's not matched to a source yet.
        This has the information of the message request such as fbclid, gclid, etc.
        """
        return ContactPoint(
            referer_info=referer_info,
            source_checker_method=SourceCheckerType.SMART_MESSAGES,
            topic_id=referer_info.topic_id,
            created_at=referer_info.timestamp,
            company_id=company_id,
            fb_clid=referer_info.query_params.fbclid,
            gclid=referer_info.query_params.gclid,
            client_ip_address=referer_info.client_ip_address,
            client_user_agent=referer_info.client_user_agent,
            client_external_id=referer_info.client_external_id,
            button_id=referer_info.button_id,
            button_name=referer_info.button_name,
            device_type=referer_info.device_type
            ) #type: ignore

    @staticmethod
    def create_unmatched_from_enviame_whats_app_source(source: Source, company_id: str, timestamp: datetime) -> ContactPoint:
        """ We received a ChattyPixel message request, but there's no chat nor message still.
        We create a contact point for it, but it's not matched to a source yet.
        This has the information of the message request such as fbclid, gclid, etc.
        """
        return ContactPoint(
            source_checker_method=SourceCheckerType.SMART_MESSAGES,
            created_at=timestamp,
            company_id=company_id
            ) #type: ignore

    @staticmethod
    def match_existing_contact_point_with_source_information(contact_point: ContactPoint, source: Source, message: ChattyMessage):
        """ Only for new chats and source_checker_method: Literal, referral, similarity.
        In the case of new chats, the CP is created at the moment the chat is created, so once the message is matched, we need to update the CP with the source and message"""
        contact_point.source_id = source.id
        contact_point.source_checker_method = source.source_checker
        contact_point.topic_id = getattr(source, "topic_id", None)
        contact_point.match_timestamp = message.created_at
        if contact_point.referer_info:
            contact_point.time_from_request_to_match = message.created_at - contact_point.referer_info.timestamp

    @staticmethod
    def update_contact_point_after_referer_info_analysis(contact_point: ContactPoint, source: Source):
        """
        Only for Chatty Pixel Contact Points.
        Still no chat nor message.
        We have the information of the source, which could eventually be matched or not based on the user actually sending the message.
        """
        contact_point.source_id = source.id
        contact_point.source_checker_method = source.source_checker
        contact_point.topic_id = getattr(source, "topic_id", None)

    @staticmethod
    def from_chat(chat: Chat, company_id: str, message: ChattyMessage):
        """
        Only for new chats.
        We just create the contact point, still not matched to a source.
        """
        contact_point = ContactPoint(chat_id=chat.identifier, company_id=company_id, message_id=message.id, ctwa_clid=message.referral.ctwa_clid, new_chat=True) #type: ignore
        return contact_point

    @staticmethod
    def create_contact_point_from_template(chat: Chat, source: TemplateSource, company_id: str, message: ChattyMessage) -> ContactPoint:
        """
        Create the CP for a template sent on a chat, that's either new or existing.
        """
        contact_point = ContactPoint(
            source_id=source.id,
            source_checker_method=source.source_checker,
            chat_id=chat.identifier,
            company_id=company_id,
            message_id=message.id,
            new_chat=False,
            created_at=message.created_at,
            updated_at=message.created_at,
            match_timestamp=message.created_at,
            template_name=source.template_name
            )
        return contact_point

    @staticmethod
    def match_existing_contact_point_with_template_source_for_new_chat(contact_point: ContactPoint, source: TemplateSource, message: ChattyMessage):
        """
        Match an existing contact point with a template source for a new chat.
        """
        contact_point.source_id = source.id
        contact_point.source_checker_method = source.source_checker
        contact_point.template_name = source.template_name
        contact_point.match_timestamp = message.created_at
        contact_point.message_id = message.id


    @staticmethod
    def match_existing_contact_points_created_for_chatty_pixel_message_requests(contact_point: ContactPoint, message:ChattyMessage, chat:Chat, topic_id:StrObjectId) -> ContactPoint:
        """
        Only for Chatty Pixel Contact Points.
        We received the message on WhatsApp, so the Contact Point is matched to the chat.
        """
        contact_point.chat_id = chat.identifier
        contact_point.message_id = message.id
        contact_point.match_timestamp = message.created_at
        contact_point.topic_id = topic_id
        if contact_point.referer_info:
            logger.debug(f"message created at {message.created_at} and referer info timestamp {contact_point.referer_info.timestamp}")
            contact_point.time_from_request_to_match = message.created_at - contact_point.referer_info.timestamp

        return contact_point

