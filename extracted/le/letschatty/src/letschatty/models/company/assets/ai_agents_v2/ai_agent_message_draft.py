"""
AI Agent Message Draft model.

Wrapper for MessageDraft with AI instructions for adaptation.
Used in launch communications and welcome kits.
"""

from pydantic import BaseModel, Field
from typing import List
from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft


class AIAgentMessageDraft(BaseModel):
    """
    Wrapper for MessageDraft with instructions for AI adaptation.

    Allows multimedia messages (text, image, video, audio, document)
    to be sent with context for AI to adapt them to the conversation.

    Example:
        ```python
        welcome_kit = AIAgentMessageDraft(
            messages=[
                MessageDraft(content=ChattyContentText(body="¡Bienvenido a {{product_name}}!")),
                MessageDraft(content=ChattyContentDocument(url="https://..."))
            ],
            instructions="Personaliza el mensaje usando el nombre del usuario si está disponible."
        )
        ```
    """
    messages: List[MessageDraft] = Field(
        description="List of message drafts to be sent (text, image, video, etc.)"
    )
    instructions: str = Field(
        description="Instructions for AI on how to adapt/personalize these messages"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "content": {
                            "type": "text",
                            "body": "¡Bienvenido a {{product_name}}! Tu link de acceso: {{access_link}}"
                        }
                    },
                    {
                        "content": {
                            "type": "document",
                            "url": "https://example.com/welcome.pdf",
                            "filename": "guia_bienvenida.pdf"
                        }
                    }
                ],
                "instructions": "Personaliza el mensaje de bienvenida según el contexto de la conversación. Usa el nombre del usuario si está disponible."
            }
        }
