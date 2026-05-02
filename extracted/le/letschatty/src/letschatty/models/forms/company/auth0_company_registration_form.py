from pydantic import BaseModel, Field
from typing import List

class Auth0CompanyRegistrationForm(BaseModel):
    user_name: str
    user_email: str
    company_name: str = Field(description="The name of the company", default=None)
    industry: str = Field(description="The industry of the company", default=None)
    url: str = Field(description="The url of the company", default=None)
    company_email: str = Field(description="The email of the company", default=None)
    contributor_count: str = Field(description="The contributor count of the company", default=None)
    purpose_of_use_chatty: List[str] = Field(description="The purpose of use chatty of the company", default=None)
    current_wpp_approach: str = Field(description="The current wpp approach of the company", default=None)
    main_reason_to_use_chatty: str = Field(description="The main reason to use chatty of the company", default=None)
    terms_of_service_agreement: bool = Field(description="The terms of service agreement of the company", default=None)
    alias: str = Field(description="The alias of the company", default=None)

