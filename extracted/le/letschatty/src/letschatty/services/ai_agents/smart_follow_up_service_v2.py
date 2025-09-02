from typing import List
from letschatty.models.chat.chat import Chat
from letschatty.models.chat.flow_link_state import SmartFollowUpState
from letschatty.models.company.assets.ai_agents_v2.follow_up_strategy import FollowUpStrategy
from letschatty.models.company.assets.ai_agents_v2.ai_agents_decision_output import SmartFollowUpDecision, SmartFollowUpDecisionAction
from letschatty.services.chat.chat_service import ChatService
from letschatty.models.utils.custom_exceptions import SmartFollowUpStrategyNotSet
from letschatty.models.execution.execution import ExecutionContext
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from letschatty.models.company.assets.flow import FlowPreview
import logging
logger = logging.getLogger("SmartFollowUpService")

class SmartFollowUpService:

    @staticmethod
    def should_send_followup(workflow_link_state: SmartFollowUpState, strategy: FollowUpStrategy) -> bool:
        """Check if we can send another follow-up"""
        return (
            workflow_link_state.total_followups_sent < strategy.maximum_follow_ups_to_be_executed and
            workflow_link_state.consecutive_count < strategy.maximum_consecutive_follow_ups
        )
    @staticmethod
    def reset_sequence(workflow_link_state: SmartFollowUpState):
        """Reset consecutive count when customer responds"""
        workflow_link_state.consecutive_count = 0

    @staticmethod
    def increment_followup(workflow_link_state: SmartFollowUpState):
        """Called after sending a follow-up"""
        workflow_link_state.total_followups_sent += 1
        workflow_link_state.consecutive_count += 1
        logger.debug(f"Incremented follow up for workflow link state to {workflow_link_state.consecutive_count} and total follow ups sent to {workflow_link_state.total_followups_sent}")

    @staticmethod
    def validate_next_call_time_or_default(ai_agent_decision: SmartFollowUpDecision, next_follow_up_number: int, strategy: FollowUpStrategy) -> None:
        """Validate the next call time for the follow up number. If the next call time is not set, we use the default next call time"""
        if ai_agent_decision.next_call_time is None:
            ai_agent_decision.next_call_time = datetime.now(ZoneInfo('UTC')) + timedelta(minutes=strategy.get_interval_for_followup(next_follow_up_number))

    @staticmethod
    def get_description(workflow_link_state: SmartFollowUpState, strategy: FollowUpStrategy) -> str:
        """Get the description of the follow up strategy"""
        return f"Total de follow ups enviados: {workflow_link_state.total_followups_sent} / {strategy.maximum_follow_ups_to_be_executed}. Descripción: {strategy.instructions_and_goals}"

    @staticmethod
    def get_descriptive_title(workflow_link_state: SmartFollowUpState, strategy: FollowUpStrategy) -> str:
        """Get the descriptive title of the follow up strategy"""
        return f"🤖 Smart Follow Up: {strategy.name} | Ejecutados: {workflow_link_state.consecutive_count} / {strategy.maximum_consecutive_follow_ups}"

    @staticmethod
    def get_follow_up_strategy_info_for_cot(workflow_link_state: SmartFollowUpState, strategy: FollowUpStrategy) -> str:
        """Get the descriptive title of the follow up strategy"""
        return f"\n\nLa estrategia de seguimiento es: {strategy.name} | Se ejecutaron {workflow_link_state.consecutive_count}/{strategy.maximum_consecutive_follow_ups} veces consecutivas y en total se han enviado {workflow_link_state.total_followups_sent}/{strategy.maximum_follow_ups_to_be_executed} seguimientos. \n\n El próximo seguimiento es el #{workflow_link_state.consecutive_count + 1} - configurado para {strategy.get_interval_for_followup(workflow_link_state.consecutive_count + 1)/60} horas. Se hará a las {workflow_link_state.next_call.astimezone(ZoneInfo('UTC')).strftime('%H:%M')} (UTC-0) | {workflow_link_state.next_call.astimezone(ZoneInfo('America/Argentina/Buenos_Aires')).strftime('%H:%M')} (UTC-3)"


    @staticmethod
    def update_based_on_decision(chat: Chat, decision: SmartFollowUpDecision, smart_follow_up_state: SmartFollowUpState, flow_preview : FlowPreview, follow_up_strategy: FollowUpStrategy, execution_context: ExecutionContext) -> None:
        """
        Update the workflow link state based on the decision.
        If the action is SEND or SUGGEST, we increment the followup and update the next call time.
        If the action is SKIP, we update the next call time.
        If the action is REMOVE, we remove the workflow link.

        In any case, we use the ChatService to update the workflow link state in the chat.
        """
        if decision.action == SmartFollowUpDecisionAction.SEND or decision.action == SmartFollowUpDecisionAction.SUGGEST:
            logger.debug(f"Updating smart follow up state based on decision {decision} for chat {chat.id}")
            SmartFollowUpService.increment_followup(smart_follow_up_state)
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.SKIP:
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            logger.debug(f"Skipping smart follow up for chat {chat.id} with next call time {decision.next_call_time}")
            ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.REMOVE:
            logger.debug(f"Removing smart follow up for chat {chat.id}")
            ChatService.remove_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, flow=flow_preview, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.ESCALATE:
            logger.debug(f"Escalating smart follow up for chat {chat.id}")
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        else:
            raise ValueError(f"Invalid action: {decision.action}")