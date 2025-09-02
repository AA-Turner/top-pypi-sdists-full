from enum import StrEnum

class ChattyAIMode(StrEnum):
    """AI mode for the AI agent"""
    AUTONOMOUS = "autonomous"
    SUGGESTIONS = "suggestions"
    COPILOT = "copilot"
    OFF = "off"

    @classmethod
    def is_implemented(cls, mode: 'ChattyAIMode') -> bool:
        return mode in [cls.AUTONOMOUS, cls.OFF]

    @classmethod
    def get_description(cls, mode: 'ChattyAIMode') -> str:
        return {
            cls.AUTONOMOUS: "El agente de IA tendrá la autonomía de conversar en tiempo real con el usuario, respetando sus instrucciones y las reglas establecidas.",
            cls.SUGGESTIONS: "El agente de IA sugerirá sólo hará sugerencias de respuestas y seguimientos, pero no enviará mensajes ni interactuará de forma directa con el usuario.",
            cls.COPILOT: "El agente de IA hará sugerencias de respuestas y seguimientos, y responderá de forma directa únicamente aquellas preguntas especificadas en el contexto del agente, en la sección de preguntas frecuentes (FAQ).",
            cls.OFF: "El agente de IA estará inactivo. No responderá al usuario ni hará sugerencias."
        }[mode]

    @classmethod
    def get_context_for_mode(cls, mode: 'ChattyAIMode') -> str:
        intro = "Your mode is set to " + mode.value + ". Here are the rules you need to follow:"
        mode_description = {
            cls.AUTONOMOUS: "Only answer based on the context and rules provided. Do not improvise or make up information. If you can't handle the question, call human_handover tool to ask for help.",
            cls.SUGGESTIONS: "You're only going to be making suggestions, you won't have the chat assigned to yourself nor be interacting directly with the user. Always include the 'suggest' mode in your output for the messages you want to send.",
            cls.COPILOT: "You're in a COPILOT mode, so you'll be making suggestions on general inquires, and answer only questions specified in the FAQ section. So, for answers which you're creating based on the context, you'll be making a suggestions, and need to add the 'suggestion' subtype in each message. When asked about a question included in the FAQ, you're allowed to adapt the answer to the user's question, but you're not allowed to improvise or make up information, and you'll set the 'text' subtype in the messages.",
            cls.OFF: ""
        }[mode]
        return intro + "\n\n" + mode_description
