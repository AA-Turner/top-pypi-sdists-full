from letschatty.models.messages.message_templates.chatty_template_campaign import TemplateCampaign
from letschatty.models.messages.message_templates.raw_meta_template import WhatsappTemplate
from letschatty.models.messages.message_templates.required_for_frontend_templates import RequiredTemplateParameter
from letschatty.models.messages.message_templates.filled_data_from_frontend import FilledTemplateData, FilledRecipientParameter, TemplateOrigin
from letschatty.models.messages.message_templates.recipient_of_template_campaign import RecipientOfTemplateCampaign
from typing import List
import logging

logger = logging.getLogger("TemplateCampaignService")

class TemplateCampaignService:

    @staticmethod
    def _validate_template_campaign_parameters(recipients : List[RecipientOfTemplateCampaign], whatsapp_template : WhatsappTemplate) -> None:
        recipient_example = recipients[0]
        recipient_params = set([parameter.id for parameter in recipient_example.parameters])
        expected_parameters = RequiredTemplateParameter.from_whatsapp_template(whatsapp_template)
        expected_parameters_keys = set([parameter.id for parameter in expected_parameters])
        if not expected_parameters_keys.issubset(recipient_params):
            raise ValueError(f"Missing parameters: {expected_parameters_keys - recipient_params}")

    @staticmethod
    def _instantiate_recipient(recipient_dict : dict, whatsapp_template : WhatsappTemplate) -> RecipientOfTemplateCampaign:
        expected_parameters = RequiredTemplateParameter.from_whatsapp_template(whatsapp_template)
        logger.debug(f"Expected parameters: {expected_parameters}")
        recipient_parameters = FilledRecipientParameter.from_required_template_parameters_and_recipient_dict(expected_parameters, recipient_dict)
        recipient_dict["parameters"] = recipient_parameters
        return RecipientOfTemplateCampaign(**recipient_dict)

    @staticmethod
    def validate_and_instantiate_recipients_in_campaign(whatsapp_template : WhatsappTemplate,template_campaign_dict : dict,recipients_dict : List[dict]) -> TemplateCampaign:
        recipients = [TemplateCampaignService._instantiate_recipient(recipient_dict=recipient_dict, whatsapp_template=whatsapp_template) for recipient_dict in recipients_dict]
        if recipients[0].is_example_recipient:
            logger.debug("Example recipient found in campaign creation. Removing it.")
            recipients = recipients[1:]
        if len(recipients) == 0:
            raise ValueError("Recipients are required to create a campaign")
        logger.debug(f"Recipients: {recipients}")
        TemplateCampaignService._validate_template_campaign_parameters(recipients, whatsapp_template)
        template_campaign_dict["recipients"] = recipients
        template_campaign = TemplateCampaign(**template_campaign_dict)
        return template_campaign

    @staticmethod
    def build_template_data_for_recipient(recipient : RecipientOfTemplateCampaign, template_campaign : TemplateCampaign) -> FilledTemplateData:
        return FilledTemplateData(
            template_name=template_campaign.template_name,
            area=template_campaign.area,
            assign_to_agent=template_campaign.assign_to_agent,
            phone_number=recipient.phone_number,
            new_contact_name=recipient.new_contact_name,
            parameters=recipient.parameters,
            tags=template_campaign.tags,
            products=template_campaign.products,
            flow=template_campaign.flow,
            description=template_campaign.description,
            forced_send=template_campaign.forced_send,
            campaign_name=template_campaign.name,
            campaign_id=template_campaign.id,
            origin=TemplateOrigin.FROM_CAMPAIGN
        )

    @staticmethod
    def instantiate_template_campaign(template_campaign_dict : dict) -> TemplateCampaign:
        return TemplateCampaign(**template_campaign_dict)