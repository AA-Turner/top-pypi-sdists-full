"""What a hosted arm hands Core's prompt executor reaches the chat relay."""
from hugpy_core.relay import internal


def test_an_image_beside_the_prompt_reaches_the_relay_in_its_user_turn(monkeypatch):
    sent = {}

    def chat(body, *, caller):
        sent.update(body)
        return {'choices': [{'message': {'content': 'a red square'}}], 'model': body['model']}, 200

    monkeypatch.setattr(internal, 'chat', chat)
    result = internal.execute_prompt(
        caller='media', task='image-text-to-text', model_key='vision-model',
        messages=[{'role': 'system', 'content': 'Describe images.'}, {'role': 'user', 'content': 'What is this?'}],
        images=['data:image/png;base64,AAAA'], max_new_tokens=64)

    assert result['ok'] and result['text'] == 'a red square'
    assert 'images' not in sent                      # the relay forwards messages, not side fields
    assert sent['messages'][0] == {'role': 'system', 'content': 'Describe images.'}
    assert sent['messages'][-1] == {'role': 'user', 'content': [
        {'type': 'text', 'text': 'What is this?'},
        {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,AAAA'}}]}
    assert sent['max_tokens'] == 64
