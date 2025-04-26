import json

def get_auth(path):

    with open(path, 'r') as f:
        config = json.load(f)

    if isinstance(config, str):
        config = eval(config)

    return config