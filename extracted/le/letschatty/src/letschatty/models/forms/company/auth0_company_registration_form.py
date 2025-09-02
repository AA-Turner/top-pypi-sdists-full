from pydantic import BaseModel
from typing import List

class Auth0CompanyRegistrationForm(BaseModel):
    user_name: str
    user_email: str
    company_name: str
    industry: str
    url: str
    company_email: str
    contributor_count: str
    purpose_of_use_chatty: List[str]
    current_wpp_approach: str
    main_reason_to_use_chatty: str
    terms_of_service_agreement: bool
    alias: str

