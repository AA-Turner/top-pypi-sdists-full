from arpakitlib.ar_sqladmin_util import get_string_info_from_model_view
from project.sqladmin_.model_view.api_key import ApiKeyMV
from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.model_view.operation import OperationMV
from project.sqladmin_.model_view.story_log import StoryLogMV
from project.sqladmin_.model_view.user import UserMV
from project.sqladmin_.model_view.user_token import UserTokenMV
from project.sqladmin_.model_view.verification_code import VerificationCodeMV

if __name__ == '__main__':
    print(get_string_info_from_model_view(class_=SimpleMV))
