from portkey_ai import Portkey
from typing import Dict, List, Optional
import random
import asyncio
import time
import sys
import tiktoken
import json

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

def get_token_count(text: str) -> int:
    """
    Get the number of tokens in a text string using tiktoken.
    
    Args:
        text (str): The input text to count tokens for
        
    Returns:
        int: Number of tokens in the text
    """
    try:
        encoding = tiktoken.encoding_for_model("gpt-4o")
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception as e:
        logger.debug(f"Error counting tokens: {str(e)}")
        return 0

def truncate_messages(messages: List[Dict[str, str]], max_tokens: int) -> List[Dict[str, str]]:
    """
    Truncate conversation history to fit within token limit while preserving system prompts.
    Preserves system messages and most recent messages.
    
    Args:
        messages: List of message dictionaries
        max_tokens: Maximum allowed tokens
        
    Returns:
        Truncated message list
    """
    # Separate system messages and other messages
    system_messages = [msg for msg in messages if msg['role'] == 'system']
    other_messages = [msg for msg in messages if msg['role'] != 'system']
    
    system_tokens = sum(get_token_count(json.dumps(msg)) for msg in system_messages)
    remaining_tokens = max_tokens - system_tokens
    
    truncated_messages = system_messages.copy()
    total_tokens = system_tokens
    
    # Add most recent non-system messages that fit
    for msg in reversed(other_messages):
        msg_text = json.dumps(msg)
        tokens = get_token_count(msg_text)
        
        if total_tokens + tokens <= max_tokens:
            truncated_messages.append(msg)
            total_tokens += tokens
            
    # Sort messages back to original order
    truncated_messages.sort(key=lambda x: messages.index(x))
    return truncated_messages

def split_message(message: Dict[str, str], max_tokens: int) -> List[Dict[str, str]]:
    """
    Split a large message into smaller chunks within token limit.
    Preserves message role and splits on sentence boundaries when possible.
    
    Args:
        message: Message dictionary to split
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of message chunks
    """
    content = message['content']
    role = message['role']
    
    # Don't split system messages
    if role == 'system':
        return [message]
        
    chunks = []
    current_chunk = ''
    current_tokens = 0
    
    # Split on sentences when possible
    sentences = content.replace('\n', '. ').split('. ')
    
    for sentence in sentences:
        sentence = sentence.strip() + '. '
        sentence_tokens = get_token_count(sentence)
        
        if current_tokens + sentence_tokens > max_tokens:
            if current_chunk:
                # Ensure the role alternates between user and assistant
                if len(chunks) > 0 and chunks[-1]['role'] == role:
                    role = 'assistant' if role == 'user' else 'user'
                
                chunks.append({
                    'role': role,
                    'content': current_chunk.strip()
                })
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            current_chunk += sentence
            current_tokens += sentence_tokens
            
    if current_chunk:
        # Ensure the role alternates between user and assistant
        if len(chunks) > 0 and chunks[-1]['role'] == role:
            role = 'assistant' if role == 'user' else 'user'
        
        chunks.append({
            'role': role,
            'content': current_chunk.strip()
        })
        
    return chunks

class TokenController:
    """Manages token counts and message processing while preserving message quality"""
    
    # Define context windows and max completion tokens for different models
    MODEL_LIMITS = {
        # Azure Models
        "azure1": {
            "context_window": 200000,
            "max_completion": 100000
        },
        "azure2": {
            "context_window": 1047576,
            "max_completion": 32768
        },
        "azureMini1": {
            "context_window": 128000,
            "max_completion": 16384
        },
        "azureMini2": {
            "context_window": 128000,
            "max_completion": 16384
        },
        # Bedrock Models
        "bedrock2": {
            "context_window": 200000,
            "max_completion": 4096
        },
        "bedrock3": {
            "context_window": 200000,
            "max_completion": 4096
        },
        "bedrocllama2": {
            "context_window": 128000,
            "max_completion": 4096
        },
        "bedrochaiku2": {
            "context_window": 200000,
            "max_completion": 4096
        },
        # Gemini Models
        "geminiflash": {
            "context_window": 1048576,
            "max_completion": 65536
        },
        "geminipro": {
            "context_window": 1048576,
            "max_completion": 65536
        }
    }
    
    @classmethod
    def get_model_limits(cls, model_type: str) -> tuple:
        """Get context window and max completion tokens for a model type"""
        limits = cls.MODEL_LIMITS.get(model_type, {
            "context_window": 128000,  # Default values
            "max_completion": 4096
        })
        return limits["context_window"], limits["max_completion"]

    @classmethod
    async def process_messages(cls, messages: List[Dict[str, str]], 
                             max_completion_tokens: int,
                             model_type: str = "bedrock2") -> List[Dict[str, str]]:
        """
        Process messages to fit within token limits while maintaining quality.
        Preserves system messages and recent context.
        
        Args:
            messages: Input messages
            max_completion_tokens: Maximum completion tokens
            model_type: Specific model being used (azure1, bedrock2, geminipro, etc.)
            
        Returns:
            Processed messages list
        """
        # Check if messages is empty or None
        if not messages:
            logger.warning("Received empty messages list, adding a default user message")
            messages = [{"role": "user", "content": "Hello"}]
            
        # Get model-specific limits
        context_window, default_max_completion = cls.get_model_limits(model_type)
        
        # Use provided max_completion_tokens or default
        max_completion = max_completion_tokens or default_max_completion
        
        # Reserve tokens for completion
        max_context_tokens = context_window - max_completion
        
        # Count total tokens
        total_tokens = sum(get_token_count(json.dumps(msg)) for msg in messages)
        
        if total_tokens <= max_context_tokens:
            return messages
            
        # First try truncating while preserving system messages
        truncated = truncate_messages(messages, max_context_tokens)
        if len(truncated) > 0:
            return truncated
            
        # If still too large, split non-system messages only
        last_msg = messages[-1]
        if last_msg['role'] != 'system':
            history = messages[:-1]
            history_tokens = sum(get_token_count(json.dumps(msg)) for msg in history)
            remaining_tokens = max_context_tokens - history_tokens
            
            chunks = split_message(last_msg, remaining_tokens)
            result = history + chunks
            
            # Ensure we never return an empty message list
            if not result:
                logger.warning("Message processing resulted in empty list, adding default message")
                return [{"role": "user", "content": "Hello"}]
            return result
        
        # Fallback to ensure we never return an empty list
        if not messages:
            logger.warning("No messages could be processed, adding default message")
            return [{"role": "user", "content": "Hello"}]
            
        return messages

class BaseModel:
    def __init__(self, api_key: str, virtual_key: str, config_id: str):
        try:
            # Remove any additional arguments and only pass the required ones
            self.portkey = Portkey(
                api_key=api_key,
                virtual_key=virtual_key,
                config=config_id
            )
        except Exception as e:
            logger.debug(f"Failed to initialize Portkey: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        raise NotImplementedError

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        raise NotImplementedError

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        raise NotImplementedError
    

class AzureModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 16384
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel coding_prompt failed: {str(e)}")
            raise

    async def arch_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for arch_prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 16384
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel arch_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 16384
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using AzureModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_tokens": 16384,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel stream_prompt failed: {str(e)}")
            raise

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using AzureModel for arch_stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_tokens": 16384,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel arch_stream_prompt failed: {str(e)}")
            raise

class Azure2Model(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_completion_tokens": 100000
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel coding_prompt failed: {str(e)}")
            raise

    async def arch_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for arch_prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_completion_tokens": 100000
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel arch_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_completion_tokens": 100000
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using AzureModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_completion_tokens": 100000,
                "stream": True
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel stream_prompt failed: {str(e)}")
            raise

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using AzureModel for arch_stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 16384)
            common_params = {
                "messages": processed_messages,
                "max_completion_tokens": 100000,
                "stream": True
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel arch_stream_prompt failed: {str(e)}")
            raise


class BedrockModel3(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 4096,
                "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel coding_prompt failed: {str(e)}")
            raise

    async def arch_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for arch_prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 4096,
                "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel arch_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 4096,
                "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"    
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 4096,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel stream_prompt failed: {str(e)}")
            raise

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel for arch_stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 4096,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel arch_stream_prompt failed: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, model: str):
        try:
            return self.portkey.images.generate(
                prompt=prompt,
                model=model
            )
        except Exception as e:
            logger.debug(f"BedrockModel generate_image failed: {str(e)}")
            raise

class BedrockModel2(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel2 for prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 4096,
                "model": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 coding_prompt failed: {str(e)}")
            raise

    async def arch_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel2 for arch_prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 4096,
                "model": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 arch_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel2 for prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 4096,
                "model": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel2 for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 4096,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 stream_prompt failed: {str(e)}")
            raise

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel2 for arch_stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 4096, "claude")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 4096,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 arch_stream_prompt failed: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, model: str):
        try:
            return self.portkey.images.generate(
                prompt=prompt,
                model=model
            )
        except Exception as e:
            logger.debug(f"BedrockModel2 generate_image failed: {str(e)}")
            raise

class GeminiFlashModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_flash")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 65536,
                "model": "gemini-2.5-flash-preview-04-17"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel coding_prompt failed: {str(e)}")
            raise

    async def arch_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using GeminiModel for arch_prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_flash")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1, 
                "max_tokens": 65536,
                "model": "gemini-2.5-flash-preview-04-17" 
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel arch_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using GeminiModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_flash")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 65536,
                "model": "gemini-2.5-flash-preview-04-17"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using GeminiModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_flash")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 65536,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "gemini-2.5-flash-preview-04-17"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.error(f"GeminiModel stream_prompt failed: {str(e)}")
            raise

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using GeminiModel for arch_stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_flash")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 65536,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "gemini-2.5-flash-preview-04-17"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel arch_stream_prompt failed: {str(e)}")
            raise

class GeminiProModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_pro")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 65536,
                "model": "gemini-2.5-pro-preview-03-25"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel coding_prompt failed: {str(e)}")
            raise

    async def arch_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using GeminiModel for arch_prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_pro")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 65536,
                "model": "gemini-2.5-pro-preview-03-25"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel arch_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using GeminiModel for prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_pro")
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": 65536,
                "model": "gemini-2.5-pro-preview-03-25"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using GeminiModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_pro")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 65536,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "gemini-2.5-pro-preview-03-25"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.error(f"GeminiModel stream_prompt failed: {str(e)}")
            raise

    async def arch_stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using GeminiModel for arch_stream_prompt")
            processed_messages = await TokenController.process_messages(messages, 65536, "gemini_pro")
            common_params = {
                "messages": processed_messages,
                "max_tokens": 65536,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "gemini-2.5-pro-preview-03-25"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel arch_stream_prompt failed: {str(e)}")
            raise

class DalleModel(BaseModel):
    def generate_image(self, prompt: str, size: str = "1024x1024"):
        try:
            logger.debug("Using DALL-E 3 for image generation")
            return self.portkey.images.generate(prompt=prompt, size=size)
        except Exception as e:
            logger.debug(f"DalleModel generate_image failed: {str(e)}")
            raise

class AIGateway:
    _instance = None

    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure1": "azure-569680",
        "azure2": "azure-5b6bdd",
        "bedrock2": "bedrock-1c7d76",
        "bedrock3": "bedrock-1c7d76",
        "gemini_flash": "gemini-a826eb",
        "gemini_pro": "gemini-a826eb",
        "dalle3_1": "dalle3-34c86a",
        "dalle3_2": "dalle3-ea9815"
    }
    ARCH_STEAM_WEIGHTS = {
        "gemini_pro": 0.9,
        "azure1": 0.1,
    }

    MODEL_WEIGHTS = {
       "gemini_flash": 0.5,
       "azure1": 0.3,
       "gemini_pro": 0.2,
    }

    STREAM_MODEL_WEIGHTS = {
       "gemini_flash": 0.5,
       "azure1": 0.3,
       "gemini_pro": 0.2,
    }

    STREAM_EXPLAINER_MODEL_WEIGHTS = {
       "gemini_flash": 0.5,
       "azure1": 0.3,
       "gemini_pro": 0.2,
    }

    Architect_MODEL_WEIGHTS = {
       "gemini_pro": 0.7,
       "azure1": 0.3,
    }

    CODING_MODEL_WEIGHTS = {
       "bedrock3": 0.4,
       "bedrock2": 0.3,
       "azure1": 0.2,
       "gemini_pro": 0.1,
    }

    FREE_IMAGE_MODEL_WEIGHTS = {
        "dalle3_1": 0.167,
        "dalle3_2": 0.167,
        "sdxl": 0.167,
        "sdxl2": 0.167,
        "stable_core": 0.166,
        "stable_core2": 0.166,
    }

    PRO_IMAGE_MODEL_WEIGHTS = {
        "sd": 0.25,
        "sd2": 0.25,
        "stable_ultra": 0.25,
        "stable_ultra2": 0.25,
        "dalle3_1": 0.05,
        "dalle3_2": 0.05,
    }
    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(AIGateway, cls).__new__(cls)
                
                # Initialize Azure models
                cls._instance.azure1_model = AzureModel(cls.API_KEY, cls.VIRTUAL_KEYS["azure1"], cls.CONFIG_ID)
                cls._instance.azure2_model = Azure2Model(cls.API_KEY, cls.VIRTUAL_KEYS["azure2"], cls.CONFIG_ID)
                
                cls._instance.bedrock2_model = BedrockModel2(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock2"], cls.CONFIG_ID)
                cls._instance.bedrock3_model = BedrockModel3(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock3"], cls.CONFIG_ID)
                
                # Initialize Gemini models
                cls._instance.geminiflash_model = GeminiFlashModel(cls.API_KEY, cls.VIRTUAL_KEYS["gemini_flash"], cls.CONFIG_ID)
                cls._instance.geminipro_model = GeminiProModel(cls.API_KEY, cls.VIRTUAL_KEYS["gemini_pro"], cls.CONFIG_ID)
                
                # Initialize DALL-E models
                cls._instance.dalle3_1_model = DalleModel(cls.API_KEY, cls.VIRTUAL_KEYS["dalle3_1"], cls.CONFIG_ID)
                cls._instance.dalle3_2_model = DalleModel(cls.API_KEY, cls.VIRTUAL_KEYS["dalle3_2"], cls.CONFIG_ID)
                
                cls._instance.model_usage_count = {}
                logger.debug("AIGateway initialized with all models")
            except Exception as e:
                logger.error(f"Failed to initialize AI models: {str(e)}")
                raise
        return cls._instance


    def _select_model(self, weights, exclude=None, messages=None):
        try:
            # If messages contain images, exclude gemini from available models

            for model in weights:
                if model not in self.model_usage_count:
                    self.model_usage_count[model] = 0

            total_usage = sum(self.model_usage_count[model] for model in weights)
            if total_usage == 0:
                available_models = [model for model in weights if model not in (exclude or set())]
                if not available_models:
                    logger.error("No available models to choose from")
                    raise ValueError("No available models to choose from")
                
                weights_list = [(model, weights[model]) for model in available_models]
                selected_model = random.choices(
                    population=[m[0] for m in weights_list],
                    weights=[m[1] for m in weights_list],
                    k=1
                )[0]
            else:
                available_models = [model for model in weights if model not in (exclude or set())]
                if not available_models:
                    logger.error("No available models to choose from")
                    raise ValueError("No available models to choose from")
                
                ratio_diffs = []
                for model in available_models:
                    current_ratio = self.model_usage_count[model] / total_usage
                    target_ratio = weights[model] / sum(weights[m] for m in available_models)
                    ratio_diffs.append((model, target_ratio - current_ratio))
                
                selected_model = max(ratio_diffs, key=lambda x: x[1])[0]

            self.model_usage_count[selected_model] += 1
            
            logger.debug(f"Selected model: {selected_model} (usage count: {self.model_usage_count[selected_model]})")
            return selected_model
            
        except Exception as e:
            logger.error(f"Error in model selection: {str(e)}")
            raise

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting prompt method")
        tried_models = set()
        while len(tried_models) < len(self.MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model\n")
                # Fix the model attribute name mapping
                if model_type == "gemini_pro":
                    model = self.geminipro_model
                elif model_type == "gemini_flash":
                    model = self.geminiflash_model
                else:
                    model = getattr(self, f"{model_type}_model")
                completion = await model.prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model")
                return completion
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.error(f"Rate limit exceeded for {model_type} model: {str(e)}")
                else:
                    logger.error(f"Error in prompting {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond")
        raise Exception("All models failed to respond")
    
    async def arch_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting arch_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.Architect_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.Architect_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for architecture\n")
                # Fix the model attribute name mapping
                if model_type == "gemini_pro":
                    model = self.geminipro_model
                elif model_type == "gemini_flash":
                    model = self.geminiflash_model
                else:
                    model = getattr(self, f"{model_type}_model")
                completion = await model.arch_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model for architecture")
                return completion
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.error(f"Rate limit exceeded for {model_type} model in arch_prompt: {str(e)}")
                else:
                    logger.error(f"Error in arch_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond for arch_prompt")
        raise Exception("All models failed to respond for arch_prompt")
    
    async def coding_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0, 
                    ) -> Dict:
        tried_models = set()
        while len(tried_models) < len(self.CODING_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.CODING_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model\n")
                # Fix the model attribute name mapping
                if model_type == "gemini_pro":
                    model = self.geminipro_model
                elif model_type == "gemini_flash":
                    model = self.geminiflash_model
                else:
                    model = getattr(self, f"{model_type}_model")
                completion = await model.coding_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model")
                return completion
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.error(f"Rate limit exceeded for {model_type} model in coding_prompt: {str(e)}")
                else:
                    logger.error(f"Error in coding_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)

        logger.error("All models failed to respond in coding_prompt")
        raise Exception("All models failed to respond")

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Starting stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.STREAM_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.STREAM_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for streaming\n")
                # Fix the model attribute name mapping
                if model_type == "gemini_pro":
                    model = self.geminipro_model
                elif model_type == "gemini_flash":
                    model = self.geminiflash_model
                else:
                    model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received streaming response from {model_type} model")
                
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        final_response += content
                        sys.stdout.buffer.write(content.encode('utf-8'))
                        sys.stdout.flush()
                print()
                return final_response
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.error(f"Rate limit exceeded for {model_type} model in stream_prompt: {str(e)}")
                else:
                    logger.error(f"Error in stream_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)

        logger.error("All models failed to respond for stream prompt")
        raise Exception("All models failed to respond")

    
    async def explainer_stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting explainer_stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.STREAM_EXPLAINER_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.STREAM_EXPLAINER_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for streaming\n")
                # Fix the model attribute name mapping
                if model_type == "gemini_pro":
                    model = self.geminipro_model
                elif model_type == "gemini_flash":
                    model = self.geminiflash_model
                else:
                    model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        final_response += content
                        sys.stdout.buffer.write(content.encode('utf-8'))
                        sys.stdout.flush()
                print()
                return final_response
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.error(f"Rate limit exceeded for {model_type} model in explainer_stream_prompt: {str(e)}")
                else:
                    logger.error(f"Error in explainer_stream_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond for explainer stream prompt")
        raise Exception("All models failed to respond")
    
    async def arch_stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting arch_stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.ARCH_STEAM_WEIGHTS):
            try:
                model_type = self._select_model(self.ARCH_STEAM_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for streaming\n")
                # Fix the model attribute name mapping
                if model_type == "gemini_pro":
                    model = self.geminipro_model
                elif model_type == "gemini_flash":
                    model = self.geminiflash_model
                else:
                    model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.arch_stream_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received streaming response from {model_type} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        final_response += content
                        sys.stdout.buffer.write(content.encode('utf-8'))
                        sys.stdout.flush()
                print()
                return final_response
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.error(f"Rate limit exceeded for {model_type} model in arch_stream_prompt: {str(e)}")
                else:
                    logger.error(f"Error in arch_stream_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond for arch stream prompt")
        raise Exception("All models failed to respond")


    def generate_image(self, prompt: str, size: str = "1024x1024", tier: str = "Free"):
        logger.debug("Starting image generation")
        tried_models = set()
        
        if tier == "Free":
            weights_to_try = [self.FREE_IMAGE_MODEL_WEIGHTS]
        else:
            pro_weights = self.PRO_IMAGE_MODEL_WEIGHTS.copy()
            free_weights = {k: v for k, v in self.FREE_IMAGE_MODEL_WEIGHTS.items() 
                          if k not in pro_weights}
            weights_to_try = [pro_weights, free_weights]
            
        for current_weights in weights_to_try:
            while len(tried_models) < len(current_weights):
                try:
                    model_type = self._select_model(current_weights, exclude=tried_models)
                    if model_type.startswith("dalle3"):
                        model = getattr(self, f"{model_type}_model")
                        return model.generate_image(prompt, size)
                    elif model_type == "sdxl":
                        return self.bedrock2_model.generate_image(prompt, model="stability.stable-diffusion-xl-v1")
                    elif model_type == "sd":
                        return self.bedrock2_model.generate_image(prompt, model="stability.sd3-large-v1:0")
                    elif model_type == "stable_ultra":
                        return self.bedrock2_model.generate_image(prompt, model="stability.stable-image-ultra-v1:0")
                    elif model_type == "stable_core":
                        return self.bedrock2_model.generate_image(prompt, model="stability.stable-image-core-v1:0")
                except Exception as e:
                    logger.error(f"Failed to generate image with {model_type}: {str(e)}")
                    tried_models.add(model_type)
                    time.sleep(1)
                    continue

        logger.error("All image generation models failed")
        raise Exception("All image generation models failed")
