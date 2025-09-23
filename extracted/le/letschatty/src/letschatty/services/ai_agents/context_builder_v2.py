from letschatty.models.chat.chat import Chat
from letschatty.models.company.assets.ai_agents_v2.chat_example import ChatExample
from typing import List
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from letschatty.models.company.assets.ai_agents_v2.chain_of_thought_in_chat import ChainOfThoughtInChatTrigger
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode
from letschatty.models.company.assets.ai_agents_v2.faq import FAQ
from letschatty.models.company.assets.ai_agents_v2.context_item import ContextItem
from letschatty.services.filter_criteria_service import FilterCriteriaService
from letschatty.models.company.empresa import EmpresaModel
from datetime import datetime
from zoneinfo import ZoneInfo

class ContextBuilder:

    @staticmethod
    def chain_of_thought_instructions_and_final_prompt(trigger: ChainOfThoughtInChatTrigger) -> str:
        context = """
        You are to always provide a summary of your chain of thought so the business has a better understanding of the reasoning.
        Keep the summary short. As simple as possible. 1-2 sentences. And come up with a title as a preview of the chain of thought.
        Make a check list of the unbreakable rules and confirm that you're following them. This is PRIVATE INFORMATION and only meant for the CHAIN OF THOUGHT, never mention it to the user.
        """
        return context

    @staticmethod
    def common_prompt(agent: ChattyAIAgent, mode_in_chat: ChattyAIMode, company_info:EmpresaModel) -> str:
        context = f"You are a WhatsApp AI Agent {agent.name} [comment: your agent id is {agent.id}] for the company {company_info.name}."
        context += f"In order of relevance, the most important knowleadge base are the chat examples, they have both the information, reasoning, and expected answer for each case. Then you can use both contexts and fast answers to write / enrich your answer to suit the user's question. But always prioritize the chat examples. Last but not least, once you have your answer, ALWAYS check each unbreakable rule is being followed. If you can't follow them and answer at the same time, escalate to a human."
        context += f"\nThe current time is {datetime.now(ZoneInfo('UTC')).strftime('%Y-%m-%d %H:%M:%S')} (UTC-0)"
        context += f"\nHere's your desired behavior and personality: {agent.personality}"
        context += f"\nYour answers should be in the same lenguage as the user's messages. Default lenguage is Spanish."
        context += f"\nYour overall general objective is: {agent.general_objective}"
        context += f"\nAs for the format of your answer: We want you to be as human as possible. When the answer requires it for redability, split it into max 3 messages that make sense. You are also to use line breaks inside each message to make it more readable."
        context += f"\n\n{ChattyAIMode.get_context_for_mode(mode_in_chat)}"
        return context

    @staticmethod
    def contexts_prompt(contexts: List[ContextItem]) -> str:
        context = "This is your knowleadge base, feel free to use it to answer the user's question."
        for context_item in contexts:
            context += f"\n\n{context_item.name}: {context_item.content}"
        return context

    @staticmethod
    def faqs_prompt(faqs: List[FAQ]) -> str:
        context = f"\n\nHere are the FAQ:"
        for faq_index, faq in enumerate(faqs):
            context += f"\n{faq_index + 1}. user: {faq.question}\nAI: {faq.answer}"
        return context

    @staticmethod
    def examples_prompt(examples: List[ChatExample]) -> str:
        context = f"\n\nThis is the MOST IMPORTANT part of your knowledge base. It includes examples of real interactions with users, and the reasoning you should do to answer the user's question. If there's an example that matches the user's question, mantain the exact same reasoning and answer if possible (maybe you need to add some details to the example to fit the user's question)."
        for example_index, example in enumerate(examples):
            context += f"\n{example_index + 1}. {example.name}\n"
            for element in example.content:
                context += f"\n{element.type.value}: {element.content}"
        return context

    @staticmethod
    def unbreakable_rules_prompt(agent: ChattyAIAgent) -> str:
        context = f"\n\nHere are the unbreakable rules you must follow at all times. You can't break them under any circumstances:"
        context += "\nALWAYS prioritize the user experience. If the user is asking for a specific information, you should provide it as long as its within your scope, and then smoothly resume the desired conversation workflow."
        context += "\nNEVER talk about a subject other than the specified in your objective / contexts / prompt. If asked about something else, politely say that that's not within your scope and resume the desired conversation workflow."
        context += "\nNEVER ask the user for information that you already have."
        context += "\nDo not ask for the user phone number, you're already talking through WhatsApp."
        context += "\nNEVER repeat the same information unless the user asks for it. If you think the user is asking for the same information, try to sumarize it and ask if that suits their needs. If not, offer them to escalate the question to a human and call the human_handover tool."
        for rule in agent.unbreakable_rules:
            context += f"\n{rule}"
        return context

    @staticmethod
    def control_triggers_prompt(agent: ChattyAIAgent) -> str:
        context = f"\n\nHere are the control triggers you must follow. If you identify any of these situations:"
        for trigger in agent.control_triggers:
            context += f"\n{trigger}"
        context += "If you escalate, send a message to the user explaining that we'll answer their question as soon as possible. Always prioritize the escalation message the company has set for this situation if any."
        return context

    @staticmethod
    def chain_of_thought_prompt(agent: ChattyAIAgent, mode_in_chat: ChattyAIMode, trigger: ChainOfThoughtInChatTrigger) -> str:
        context = f"\n\nRemember that {mode_in_chat.value} mode."
        context += f"Remember to follow each unbreakable rule:\n- {'\n- '.join(agent.unbreakable_rules)}"
        context += f"\n\n{ContextBuilder.chain_of_thought_instructions_and_final_prompt(trigger)}"
        return context