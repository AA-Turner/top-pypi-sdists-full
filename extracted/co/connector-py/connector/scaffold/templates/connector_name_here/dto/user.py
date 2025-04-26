from connector.generated import CreatableAccount
from pydantic import Field


# TODO: add/remove fields required to create account
class CreateAccount(CreatableAccount):
    email: str = Field(default=None, description="The email address for the new account")
