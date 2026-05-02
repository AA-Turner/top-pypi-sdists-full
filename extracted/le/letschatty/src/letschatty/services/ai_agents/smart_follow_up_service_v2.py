from typing import List
from letschatty.models.chat.chat import Chat, FlowStateAssignedToChat
from letschatty.models.chat.flow_link_state import StateTrigger
from letschatty.models.company.assets.ai_agents_v2.follow_up_strategy import FollowUpStrategy
from letschatty.models.company.assets.ai_agents_v2.ai_agents_decision_output import SmartFollowUpDecision, SmartFollowUpDecisionAction
from letschatty.services.chat.chat_service import ChatService
from letschatty.models.utils.custom_exceptions import ErrorToMantainSafety, SmartFollowUpStrategyNotSet
from letschatty.models.execution.execution import ExecutionContext
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from letschatty.models.company.assets.flow import FlowPreview
import logging
logger = logging.getLogger("SmartFollowUpService")

class SmartFollowUpService:

    @staticmethod
    def should_send_followup(workflow_link_state: FlowStateAssignedToChat, strategy: FollowUpStrategy) -> bool:
        """Check if we can send another follow-up"""
        return (
            workflow_link_state.total_followups_sent < strategy.maximum_follow_ups_to_be_executed and
            workflow_link_state.consecutive_count < strategy.maximum_consecutive_follow_ups
        )
    @staticmethod
    def reset_sequence(workflow_link_state: FlowStateAssignedToChat):
        """Reset consecutive count when customer responds"""
        workflow_link_state.consecutive_count = 0
        workflow_link_state.execution_attempts = 0
        workflow_link_state.max_consecutive_follow_ups_reached = False

    @staticmethod
    def increment_followup(workflow_link_state: FlowStateAssignedToChat):
        """Called after sending a follow-up"""
        workflow_link_state.total_followups_sent += 1
        workflow_link_state.consecutive_count += 1
        workflow_link_state.execution_attempts = 0
        logger.debug(f"Incremented follow up for workflow link state to {workflow_link_state.consecutive_count} and total follow ups sent to {workflow_link_state.total_followups_sent}")

    @staticmethod
    def update_reached_flags(workflow_link_state: FlowStateAssignedToChat, strategy: FollowUpStrategy) -> None:
        """Set max_total_follow_ups_reached and max_consecutive_follow_ups_reached when limits are reached."""
        if workflow_link_state.total_followups_sent >= strategy.maximum_follow_ups_to_be_executed:
            workflow_link_state.max_total_follow_ups_reached = True
        if workflow_link_state.consecutive_count >= strategy.maximum_consecutive_follow_ups:
            workflow_link_state.max_consecutive_follow_ups_reached = True

    @staticmethod
    def validate_next_call_time_or_default(ai_agent_decision: SmartFollowUpDecision, next_follow_up_number: int, strategy: FollowUpStrategy) -> None:
        """Validate the next call time for the follow up number. If the next call time is not set, we use the default next call time"""
        if ai_agent_decision.next_call_time is not None:
            if ai_agent_decision.next_call_time_value <= datetime.now(ZoneInfo('UTC')):
                raise ErrorToMantainSafety(f"next_call_time must be in the future for POSTPONE_DELTA_TIME action")
        else:
            ai_agent_decision.next_call_time = datetime.now(ZoneInfo('UTC')) + timedelta(minutes=strategy.get_interval_for_followup(next_follow_up_number))

    @staticmethod
    def get_description(workflow_link_state: FlowStateAssignedToChat, strategy: FollowUpStrategy) -> str:
        """Get the description of the follow up strategy"""
        return f"Total de follow ups enviados: {workflow_link_state.total_followups_sent} / {strategy.maximum_follow_ups_to_be_executed}. Descripción: {strategy.instructions_and_goals}"

    @staticmethod
    def get_descriptive_title(workflow_link_state: FlowStateAssignedToChat, strategy: FollowUpStrategy) -> str:
        """Get the descriptive title of the follow up strategy"""
        return f"🤖 Smart Follow Up: {strategy.name} | Ejecutados: {workflow_link_state.consecutive_count} / {strategy.maximum_consecutive_follow_ups}"

    @staticmethod
    def get_follow_up_strategy_info_for_cot(workflow_link_state: FlowStateAssignedToChat, strategy: FollowUpStrategy) -> str:
        """Get the descriptive title of the follow up strategy"""
        return f"\n\nLa estrategia de seguimiento es: {strategy.name} | Se ejecutaron {workflow_link_state.consecutive_count}/{strategy.maximum_consecutive_follow_ups} veces consecutivas y en total se han enviado {workflow_link_state.total_followups_sent}/{strategy.maximum_follow_ups_to_be_executed} seguimientos. \n\n El próximo seguimiento es el #{workflow_link_state.consecutive_count + 1} - configurado para {strategy.get_interval_for_followup(workflow_link_state.consecutive_count + 1)/60} horas. Se hará a las {workflow_link_state.next_call.astimezone(ZoneInfo('UTC')).strftime('%H:%M')} (UTC-0) | {workflow_link_state.next_call.astimezone(ZoneInfo('America/Argentina/Buenos_Aires')).strftime('%H:%M')} (UTC-3)"


    @staticmethod
    def max_consecutive_follow_ups_reached(workflow_link_state: FlowStateAssignedToChat, strategy: FollowUpStrategy, chat: Chat, execution_context: ExecutionContext) -> FlowStateAssignedToChat:
        """Check if the max consecutive follow ups are reached"""
        workflow_link_state.trigger = StateTrigger.CHAT_UPDATE
        workflow_link_state.last_call = datetime.now(ZoneInfo("UTC"))
        return ChatService.update_workflow_link(chat=chat, workflow_id=workflow_link_state.flow_id, workflow_link=workflow_link_state, execution_context=execution_context)

    @staticmethod
    def max_total_follow_ups_reached(workflow_link_state: FlowStateAssignedToChat, flow_preview: FlowPreview, chat: Chat, execution_context: ExecutionContext) -> FlowStateAssignedToChat:
        """Check if the max total follow ups are reached"""
        return ChatService.remove_workflow_link(chat=chat, workflow_id=workflow_link_state.flow_id, flow=flow_preview, execution_context=execution_context)

    @staticmethod
    def update_based_on_decision(chat: Chat, decision: SmartFollowUpDecision, smart_follow_up_state: FlowStateAssignedToChat, flow_preview : FlowPreview, follow_up_strategy: FollowUpStrategy, execution_context: ExecutionContext) -> FlowStateAssignedToChat:
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
            SmartFollowUpService.update_reached_flags(smart_follow_up_state, follow_up_strategy)
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            return ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.SKIP:
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            logger.debug(f"Skipping smart follow up for chat {chat.id} with next call time {decision.next_call_time}")
            return ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.REMOVE:
            logger.debug(f"Removing smart follow up for chat {chat.id}")
            return ChatService.remove_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, flow=flow_preview, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.ESCALATE:
            logger.debug(f"Escalating smart follow up for chat {chat.id}")
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            return ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.POSTPONE_DELTA_TIME:
            logger.debug(f"Postponing smart follow up for chat {chat.id} by delta time {decision.next_call_time_value}")
            SmartFollowUpService.validate_next_call_time_or_default(decision, smart_follow_up_state.consecutive_count + 1, follow_up_strategy)
            smart_follow_up_state.next_call = decision.next_call_time_value
            return ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.POSTPONE_TILL_UPDATE:
            logger.debug(f"Postponing smart follow up for chat {chat.id} till update")
            smart_follow_up_state.trigger = StateTrigger.CHAT_UPDATE
            smart_follow_up_state.last_call = datetime.now(ZoneInfo("UTC"))
            return ChatService.update_workflow_link(chat=chat, workflow_id=smart_follow_up_state.flow_id, workflow_link=smart_follow_up_state, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.MAX_CONSECUTIVE_FOLLOW_UPS_REACHED:
            logger.debug(f"Maximum consecutive follow ups reached for chat {chat.id}")
            smart_follow_up_state.max_consecutive_follow_ups_reached = True
            return SmartFollowUpService.max_consecutive_follow_ups_reached(workflow_link_state=smart_follow_up_state, strategy=follow_up_strategy, chat=chat, execution_context=execution_context)
        elif decision.action == SmartFollowUpDecisionAction.MAX_TOTAL_FOLLOW_UPS_REACHED:
            logger.debug(f"Maximum total follow ups reached for chat {chat.id}")
            smart_follow_up_state.max_total_follow_ups_reached = True
            return SmartFollowUpService.max_total_follow_ups_reached(workflow_link_state=smart_follow_up_state, flow_preview=flow_preview, chat=chat, execution_context=execution_context)
        else:
            raise ValueError(f"Invalid action: {decision.action}")