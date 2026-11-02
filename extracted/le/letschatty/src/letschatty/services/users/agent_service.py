from letschatty.models.chat.chat import Chat
from letschatty.models.company.users.user import User
from typing import Optional

class AgentService:

    @staticmethod
    def chat_assignment(chat:Chat, agent:User, executor:User, current_agent:Optional[User] = None):
        pass