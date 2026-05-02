from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, List, TYPE_CHECKING
from zoneinfo import ZoneInfo

from letschatty.models.company.assets.users.user import CurrentChatAPBMode
from .chat_service import AlreadyCompleted, ChatService

if TYPE_CHECKING:
    from letschatty.models.company.assets.users.user import User
    from letschatty.models.chat.chat import Chat
    from letschatty.models.execution.execution import ExecutionContext

import logging
logger = logging.getLogger("WhatsappAPBModeService")
class WhatsappAPBModeService:

    @staticmethod
    def is_it_current_chat_renewal(chat_to_assign: Chat, agent_in_chat_to_assign: Optional[User], agent_getting_chat: Optional[User], current_chat_assigned: Optional[Chat], execution_context: ExecutionContext) -> bool:
        """
        Check if the current chat is just a renewal, meaning its the same chat and the same agent.
        """
        if agent_in_chat_to_assign is None or agent_getting_chat is None or current_chat_assigned is None or chat_to_assign is None:
            return False

        if chat_to_assign.is_chat_assigned_to_agent(agent_getting_chat.id):
            WhatsappAPBModeService.renew_current_chat_apb_mode(agent=agent_in_chat_to_assign, chat=current_chat_assigned)
            logger.debug(f"The chat {chat_to_assign.id} is a renewal of the current chat assigned to the agent {agent_in_chat_to_assign.name} with id {agent_in_chat_to_assign.id}")
            return True
        else:
            return False

    @staticmethod
    def get_chat_apb_mode(chat_to_assign: Chat, agent_in_chat_to_assign: Optional[User], agent_getting_chat: User, current_chat_assigned: Optional[Chat], execution_context: ExecutionContext) -> Chat:
        """
        Get the apb mode for the chat.
        If the chat is not assigned to an agent, assign it to the agent_getting_chat and populate the user current chat apb mode.
        if the chat is assigned to an agent, check if the last activity of the current agent is older than 15 seconds, if so, assign it to the agent_getting_chat and populate the user current chat apb mode.
        """
        if WhatsappAPBModeService.is_it_current_chat_renewal(chat_to_assign=chat_to_assign, agent_in_chat_to_assign=agent_in_chat_to_assign, agent_getting_chat=agent_getting_chat, current_chat_assigned=current_chat_assigned, execution_context=execution_context):
            return chat_to_assign
        if agent_in_chat_to_assign is not None and chat_to_assign.is_chat_assigned_to_agent(agent_in_chat_to_assign.id):
            #chat is assigned to an agent (not the same as the agent getting the chat)
            logger.debug(f"The chat {chat_to_assign.id} is assigned to an agent (not the same as the agent getting the chat) {agent_in_chat_to_assign.name} with id {agent_in_chat_to_assign.id}")
            if WhatsappAPBModeService.is_chat_available_after_lazy_update_chat_agent_apb_mode(current_chat_assigned=chat_to_assign, current_agent=agent_in_chat_to_assign, execution_context=execution_context):
                return WhatsappAPBModeService.assign_chat_apb_mode(chat=chat_to_assign, agent_getting_chat=agent_getting_chat, current_chat_assigned=current_chat_assigned, execution_context=execution_context)
            else:
                #Chat is not available to be assigned to the agent getting the chat, so it's not available to be assigned to the agent getting the chat
                return chat_to_assign
        else:
            #chat is not assigned to an agent
            return WhatsappAPBModeService.assign_chat_apb_mode(chat=chat_to_assign, agent_getting_chat=agent_getting_chat, current_chat_assigned=current_chat_assigned, execution_context=execution_context)

    @staticmethod
    def is_chat_available_after_lazy_update_chat_agent_apb_mode(current_chat_assigned: Chat, current_agent: User, execution_context: ExecutionContext) -> bool:
        """
        Lazy update the chat agent apb mode.
        If the last activity of the current agent is older than 15 seconds, update the chat agent apb mode.
        """
        if current_agent.current_chat_apb_mode and current_agent.current_chat_apb_mode.last_activity + timedelta(seconds=15) < datetime.now(tz=ZoneInfo("UTC")):
            try:
                ChatService.desassign_chat(current_chat_assigned, execution_context, current_agent)
            except AlreadyCompleted as e:
                pass
            logger.debug(f"The chat {current_chat_assigned.id} is available to be assigned to the agent {current_agent.name} with id {current_agent.id} because the last activity of the current agent is older than 15 seconds")
            return True
        else:
            #Still didn't expire, so it's not available to be assigned to the agent getting the chat
            logger.debug(f"The chat {current_chat_assigned.id} is not available to be assigned to the agent {current_agent.name} with id {current_agent.id} because the last activity of the current agent is not older than 15 seconds")
            return False

    @staticmethod
    def assign_chat_apb_mode(chat: Chat, agent_getting_chat: User, current_chat_assigned: Optional[Chat], execution_context: ExecutionContext) -> Chat:
        """
        Assign the apb mode to the chat.
        """
        if current_chat_assigned is not None:
            ChatService.desassign_chat(current_chat_assigned, execution_context, agent_getting_chat)

        if agent_getting_chat.is_mega_admin:
            #mega admin is not affected by the apb mode
            return chat
        ChatService.assign_chat(chat, agent_getting_chat, execution_context, current_agent=None)
        agent_getting_chat.current_chat_apb_mode = CurrentChatAPBMode.for_chat_id(chat.id)
        return chat

    @staticmethod
    def renew_current_chat_apb_mode(agent: User, chat: Chat) -> Chat:
        """
        Renew the current chat apb mode for the agent.
        """
        agent.current_chat_apb_mode = CurrentChatAPBMode.for_chat_id(chat.id)
        return chat