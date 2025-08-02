from pydantic import BaseModel
from canonmap.connectors.mysql_connector.validators.models import IfExists

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str = None
    first_name: str = None
    last_name: str = None
    role: str = "user"
    is_active: bool = True
    is_superuser: bool = False
    if_exists: IfExists = IfExists.ERROR

class DeleteUserRequest(BaseModel):
    username: str