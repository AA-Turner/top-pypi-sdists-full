from typing import Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from bson.objectid import ObjectId

from ....models.company.empresa import EmpresaModel
from ....models.company.assets.users.user import User
from ....models.forms.company.auth0_company_registration_form import Auth0CompanyRegistrationForm

import logging
logger = logging.getLogger(__name__)

class EmpresaFactory:
    """
    Factory in charge of creating Empresa objects
    """
    @staticmethod
    def from_auth0_registration_form(auht0_form:Auth0CompanyRegistrationForm):

        return EmpresaModel(
            _id = str(ObjectId()),
            created_at = datetime.now(ZoneInfo("UTC")),
            updated_at = datetime.now(ZoneInfo("UTC")),
            name = auht0_form.company_name,
            industry = auht0_form.industry,
            url = auht0_form.url,
            company_email = auht0_form.company_email,
            contributor_count = auht0_form.contributor_count,
            purpose_of_use_chatty = auht0_form.purpose_of_use_chatty,
            current_wpp_approach = auht0_form.current_wpp_approach,
            main_reason_to_use_chatty = auht0_form.main_reason_to_use_chatty,
            terms_of_service_agreement = auht0_form.terms_of_service_agreement,
            friendly_aliases = [auht0_form.alias],
            allowed_origins = [auht0_form.url],
            frozen_name = auht0_form.company_name
        )

    @staticmethod
    def from_json(empresa_json:dict) -> EmpresaModel:
        try:
            return EmpresaModel(**empresa_json)
        except Exception as e:
            logger.error(f"Error creating EmpresaModel from json: {e} {empresa_json}")
            raise e
