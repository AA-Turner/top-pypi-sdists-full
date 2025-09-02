from pydantic import BaseModel
from typing import Optional, List

class Name(BaseModel):
    formatted_name: str
    first_name: str

class Phones(BaseModel):
    phone: str
    wa_id: str
    type: str

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    type: Optional[str] = None

class Email(BaseModel):
    email: str
    type: Optional[str] = None

class FullName(BaseModel):
    formatted_name: str # Full name
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    suffix: Optional[str] = None
    prefix: Optional[str] = None

class Organization(BaseModel):
    company: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None

class Phone(BaseModel):
    phone: str
    type: Optional[str] = None
    wa_id: Optional[str] = None

class Url(BaseModel):
    url: str
    type: Optional[str] = None

class MetaContactContent(BaseModel):
    name: FullName
    phones: Optional[List[Phone]] = None
    addresses: Optional[List[Address]] = None
    birthday: Optional[str] = None
    emails: Optional[List[Email]] = None
    org: Optional[Organization] = None
    urls: Optional[List[Url]] = None
    
    @property
    def phone_number(self) -> Optional[str]:
        """Returns the first phone number that has a valid wa_id"""
        return next((phone.wa_id for phone in self.phones if phone.wa_id), None)
    
    @property
    def full_name(self) -> str:
        """Returns the full name of the contact"""
        return self.name.formatted_name
