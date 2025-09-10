from arpakitlib.ar_sqlalchemy_util import get_string_info_from_declarative_base_2

from project.sqlalchemy_db_.sqlalchemy_model.api_key import ApiKeyDBM
from project.sqlalchemy_db_.sqlalchemy_model.common import SimpleDBM
from project.sqlalchemy_db_.sqlalchemy_model.operation import OperationDBM
from project.sqlalchemy_db_.sqlalchemy_model.story_log import StoryLogDBM
from project.sqlalchemy_db_.sqlalchemy_model.user import UserDBM
from project.sqlalchemy_db_.sqlalchemy_model.user_token import UserTokenDBM
from project.sqlalchemy_db_.sqlalchemy_model.verification_code import VerificationCodeDBM

if __name__ == '__main__':
    print(get_string_info_from_declarative_base_2(SimpleDBM))
