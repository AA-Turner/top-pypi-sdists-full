import json


def get_obj_memory_size(obj):
    return len(json.dumps(obj))
