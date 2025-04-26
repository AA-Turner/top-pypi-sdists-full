import uuid


def random_filename(extension):
    return f'{str(uuid.uuid4())}.{extension}'

def random_dirname():
    return str(uuid.uuid4())

def chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:(i+size)]
