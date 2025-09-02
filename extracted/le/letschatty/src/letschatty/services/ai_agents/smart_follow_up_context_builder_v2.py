from letschatty.models.chat.chat import Chat
from letschatty.models.chat.flow_link_state import SmartFollowUpState
from letschatty.models.company.assets.ai_agents_v2.follow_up_strategy import FollowUpStrategy
from letschatty.services.ai_agents.context_builder_v2 import ContextBuilder
from letschatty.models.utils.custom_exceptions.custom_exceptions import HumanInterventionRequired, MaximumFollowUpsReached, PostponeFollowUp
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
import logging

logger = logging.getLogger("SmartFollowUpContextBuilder")


class SmartFollowUpContextBuilder(ContextBuilder):

    @staticmethod
    def check_minimum_time_since_last_message(chat: Chat, follow_up_strategy: FollowUpStrategy,smart_follow_up_state: SmartFollowUpState) -> bool:
        expected_interval_minutes = follow_up_strategy.get_interval_for_followup(smart_follow_up_state.consecutive_count)
        last_message_timestamp = chat.last_message_timestamp
        if last_message_timestamp is None:
            raise HumanInterventionRequired("There's no last message in the chat, can't validate the minimum time since last message for the smart follow up")
        time_since_last_message = datetime.now(ZoneInfo('UTC')) - last_message_timestamp
        if time_since_last_message.total_seconds() < expected_interval_minutes * 60:
            raise PostponeFollowUp(time_delta= timedelta(seconds=expected_interval_minutes * 60 - time_since_last_message.total_seconds()), message=f"Se pospuso el Smart Follow Up porque no ha pasado el tiempo mínimo esperado de {expected_interval_minutes/60} horas para el seguimiento #{smart_follow_up_state.consecutive_count}")
        return True

    @staticmethod
    def follow_up_strategy_context(chat_smart_follow_up_assigned: SmartFollowUpState, follow_up_strategy: FollowUpStrategy) -> str:
        if follow_up_strategy.maximum_consecutive_follow_ups == 0:
            raise HumanInterventionRequired("There's a 0 limit for the maximum consecutive follow ups, human intervention is required")
        if follow_up_strategy.maximum_follow_ups_to_be_executed == 0:
            raise HumanInterventionRequired("There's a 0 limit for the total follow ups to be executed, human intervention is required")
        if follow_up_strategy.maximum_consecutive_follow_ups <= chat_smart_follow_up_assigned.consecutive_count:
            raise MaximumFollowUpsReached(message=f"Se alcanzó el máximo de seguimientos consecutivos: {follow_up_strategy.maximum_consecutive_follow_ups}.", area=follow_up_strategy.area_after_reaching_max)
        if follow_up_strategy.maximum_follow_ups_to_be_executed <= chat_smart_follow_up_assigned.total_followups_sent:
            raise MaximumFollowUpsReached(message=f"We've reached the maximum total follow ups to be executed limit of {follow_up_strategy.maximum_follow_ups_to_be_executed}", area=follow_up_strategy.area_after_reaching_max)

        if datetime.now(ZoneInfo('UTC')).weekday() >= 5 and follow_up_strategy.only_on_weekdays:
            days_to_add = 1 if datetime.now(ZoneInfo('UTC')).weekday() == 5 else 2
            raise PostponeFollowUp(time_delta=timedelta(days=days_to_add), message=f"Se pospuso el Smart Follow Up durante {days_to_add} días porque es fin de semana y la configuración del Follow Up Strategy no permite realizar seguimientos en fin de semana")

        context = f"The follow up strategy is: {follow_up_strategy.name}. Your specific instructions and goals are: {follow_up_strategy.instructions_and_goals}"
        context += f"The consecutive follow ups sent are: {chat_smart_follow_up_assigned.consecutive_count} / {follow_up_strategy.maximum_consecutive_follow_ups}"
        context += f"The total follow ups sent are: {chat_smart_follow_up_assigned.total_followups_sent} / {follow_up_strategy.maximum_follow_ups_to_be_executed}"
        context += SmartFollowUpContextBuilder.next_follow_up(chat_smart_follow_up_assigned, follow_up_strategy)
        context += SmartFollowUpContextBuilder.decision_actions_available()
        context += SmartFollowUpContextBuilder.load_training_examples_from_json()
        return context

    @staticmethod
    def next_follow_up(chat_smart_follow_up_assigned: SmartFollowUpState, follow_up_strategy: FollowUpStrategy) -> str:
        next_call = datetime.now(ZoneInfo('UTC')) + timedelta(minutes=follow_up_strategy.get_interval_for_followup(chat_smart_follow_up_assigned.consecutive_count + 1))
        next_interval_minutes = follow_up_strategy.get_interval_for_followup(chat_smart_follow_up_assigned.consecutive_count + 1)
        context = f"As far as the next call, if you decide to send / suggest messages, the standard interval would be: {next_interval_minutes} minutes, so the next call would be: {next_call.isoformat()}. Unless you determine that the situation requires a different interval, in which case you should set the next call time accordingly. If you decide to skip, the next call time up to you based on the context and reason for skipping."
        if follow_up_strategy.only_on_weekdays and next_call.weekday() >= 5:
            context += f"Keep in mind that you are {'supposed' if follow_up_strategy.only_on_weekdays else 'not supposed'} to send messages on weekends."
        return context

    @staticmethod
    def decision_actions_available() -> str:
        decisions = """
        ## DECISION ACTIONS AVAILABLE
        ### SEND
        - Use when: Customer needs gentle nudging, asked question without response, sent proposal/quote
        - **Requirements**: Message must be helpful, contextual, and advance the conversation. Always focus on adding value to the conversation and the client, not just asking for a response. Try to get to know the client better, double click on their interests and needs regarding the product or service asked. If you can, continue the conversation."

        ### SKIP
        - Skip this follow-up cycle but keep the sequence active
        - Use when: Customer indicated they need time ("La semana que viene te confirmo", "Lo veo más tarde cuadno salgo de trabajar")", inappropriate timing.
        - **Set custom next_call time** based on context (e.g., Monday if they "la semana que viene", or a few hours if they "lo veo más tarde")

        ### SUGGEST
        - Recommend follow-up to human agent instead of sending automatically
        - Use when: Either the ai mode is SUGGESTIONS, or if AI mode is COPILOT and you determine that the situation requires human touch, complex negotiation, customer seems frustrated, high-value deal needing personal attention
        - Human will decide whether to send your suggested message or craft their own

        ### REMOVE
        - Completely stop all automatic follow-ups for this chat
        - Use when: Customer explicitly said "don't contact me", conversation naturally concluded (deal closed/lost) and no further follow ups are needed or you've already sent the maximum number of follow ups (total or consecutive)

        """
        return decisions


    @staticmethod
    def load_training_examples_from_json() -> str:
        """
        Loads follow-up training examples from JSON file and formats them into a prompt section.

        Args:
            json_file_path: Path to the JSON file containing training examples

        Returns:
            Formatted string with examples and instructions to focus on reasoning patterns

        Raises:
            FileNotFoundError: If JSON file doesn't exist
            json.JSONDecodeError: If JSON is malformed
        """

        try:
            from .cot_follow_up_examples import follow_up_training_examples
            # Load JSON file
            if not follow_up_training_examples:
                return ""

            # Group examples by action type
            examples_by_action = {
                "send": [],
                "skip": [],
                "suggest": [],
                "remove": []
            }

            for example in follow_up_training_examples:
                title_lower = example.get('title', '').lower()
                if "send" in title_lower:
                    action_type = "send"
                elif "skip" in title_lower:
                    action_type = "skip"
                elif "suggest" in title_lower:
                    action_type = "suggest"
                elif "remove" in title_lower:
                    action_type = "remove"
                else:
                    continue  # Skip examples that don't match action types

                examples_by_action[action_type].append(example)

            # Build training section
            training_section = """
    ## TRAINING EXAMPLES FOR DECISION-MAKING

    **CRITICAL INSTRUCTION:** These examples use GENERIC business scenarios.

    **✅ What to learn:**
    - The REASONING PATTERNS in chain_of_thought sections
    - TIMING considerations and context analysis
    - WHEN to use each action based on situation
    - HOW conversation context affects decisions

    **❌ What NOT to copy:**
    - Specific message wording or content
    - Business details or industry context
    - Exact phrasing (create your own appropriate for THIS business)

    **Your task:** Apply the same decision logic but craft messages using your actual strategy instructions and business context.

    ---

    """

            # Format examples by action type
            for action, action_examples in examples_by_action.items():
                if not action_examples:
                    continue

                training_section += f"### {action.upper()} ACTION EXAMPLES\n\n"

                for example in action_examples:
                    training_section += f"**{example.get('title', 'Untitled Example')}**\n\n"

                    content = example.get('content', [])
                    for element in content:
                        element_type = element.get('type', '')
                        element_content = element.get('content', '')

                        if element_type == "user":
                            training_section += f"👤 Customer: {element_content}\n\n"
                        elif element_type == "ai":
                            training_section += f"🤖 Agent: {element_content}\n\n"
                        elif element_type == "chain_of_thought":
                            training_section += f"🧠 **REASONING:** {element_content}\n\n"

                    training_section += "---\n\n"

            return training_section

        except FileNotFoundError as e:
            # Log the error but don't break the prompt building
            logger.warning(f"Training examples file not found: {e}")
            return ""
        except json.JSONDecodeError as e:
            # Log the error but don't break the prompt building
            logger.warning(f"Invalid JSON in training examples file: {e}")
            return ""
        except Exception as e:
            # Log unexpected errors but don't break the prompt building
            logger.warning(f"Error loading training examples: {e}")
            return ""
