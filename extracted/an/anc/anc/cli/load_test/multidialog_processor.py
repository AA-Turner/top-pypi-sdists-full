import json
from typing import List, Dict, Any, Optional
from anc.data.anc_processor import Processor   

class MultiDialogProcessor(Processor):
    def __init__(self):
        super().__init__()
    
    def transform(self, item: List[Dict[str, str]], is_last_sample: bool = False) -> List[Dict[str, Any]]:
        processed_items = []
        # Extract system message if present
        system_message = None
        for msg in item:
            if msg['role'] == 'system':
                system_message = msg['content']
                break
        
        if system_message is None:
            system_message = ''
        
        # Build dialogue history for all turns
        dialogue = []
        for msg in item:
            if msg['role'] in ['user', 'assistant']:
                dialogue.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # Process each turn in the conversation
        for i in range(len(dialogue)):
            # Only process user messages
            if i % 2 != 0 or dialogue[i]['role'] != 'user':
                continue
                
            # Check if there's a matching assistant response
            if i + 1 >= len(dialogue) or dialogue[i+1]['role'] != 'assistant':
                continue
                
            # Get history up to this point (including current user message)
            history = dialogue[:i+1]
            
            # Format for OpenAI API
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.extend(history)
            
            # Get expected assistant response for output length calculation
            assistant_response = dialogue[i+1]['content']
            # Estimate token length - approximate calculation
            output_len = len(assistant_response.split()) * 2
            
            # Create a prompt in the format expected by vllm OpenAI API
            prompt = {
                "messages": messages
            }
            print(f'output_len: {output_len}, total_turns: {len(dialogue) // 2}')
            processed_item = {
                'prompt': json.dumps(prompt),  # OpenAI API format
                'output_len': output_len,
                'conversation_id': hash(str(item)),  # Unique ID for this conversation
                'turn_index': i // 2,  # Turn number in this conversation
                'total_turns': len(dialogue) // 2  # Total turns in conversation
            }
            processed_items.append(processed_item)
 
        return processed_items
    
    def batch_transform(self, list_of_items: List[List[Dict[str, str]]], is_last_batch: bool = False) -> List[Dict[str, Any]]:
        batch_processed_items = []
        for item in list_of_items:
            batch_processed_items.extend(self.transform(item))
        return batch_processed_items
