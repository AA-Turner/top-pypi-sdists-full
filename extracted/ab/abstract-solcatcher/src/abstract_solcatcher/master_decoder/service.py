from .src import *

def decode_event(data,**kwargs):
    ENV = get_decoder_env()
    event = kwargs.get("event")
    discriminator = kwargs.get("discriminator")
    signature=kwargs.get("signature")
    program_id=kwargs.get("program_id")
    return ENV.decode(
        data,
        signature=signature,
        program_id=program_id,
        discriminator=discriminator,
        event=event
        )
    
