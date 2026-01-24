import re
def check_first_sentence(message: str) -> bool:

    if 'npc_speak' not in message:
        return False

    message = message.strip()
    if '\n' in message or '\\n' in message:
        return True
    message = re.sub(r'\[.*?\]', '', message)
    message = message.strip()
    fields = message.split(' ')
    if len(fields) >= 10 and any(punct in ' '.join(fields[-1:]) for punct in ['.', '?', '!', '…']):
        return True

    return False





