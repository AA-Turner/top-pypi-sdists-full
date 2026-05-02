from __future__ import annotations
from typing import Dict, Any
from ....models.company.assets import ChattyFastAnswer

class ChattyFastAnswersFactory:
    
    @staticmethod
    def create(chatty_fast_answer_data : Dict[str, Any]) -> ChattyFastAnswer:
        """This method is used to create a ChattyFastAnswer from scratch"""
        return ChattyFastAnswer(**chatty_fast_answer_data)