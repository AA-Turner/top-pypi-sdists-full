from .schema import *
from .imports import *
def decode_metaDatas(encoded_data):
    metadata_struct = Struct(
        "name" / Bytes(32),
        "symbol" / Bytes(14),
        "uri" / Bytes(72),
    )
    # Decode the Base64 data
    decoded_data = base64.b64decode(encoded_data)
    # Parse the data
    parsed_metadata = metadata_struct.parse(decoded_data)
    # Convert bytes to strings where appropriate
    name = parsed_metadata.name.strip()[16:]
    symbol = parsed_metadata.symbol.strip()[3:]
    uri = parsed_metadata.uri.strip()[4:]
    return {"name":str(name.decode('utf-8')),"symbol":symbol.decode('utf-8'),"uri":uri.decode('utf-8')}
