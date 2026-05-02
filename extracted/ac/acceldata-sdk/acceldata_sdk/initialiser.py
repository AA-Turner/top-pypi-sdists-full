import logging
import os

logging.basicConfig(level=logging.WARNING)

torch_client_credentials = {
    'url': os.getenv('TORCH_CATALOG_URL', 'https://torch.acceldata.local:5443'),
    'access_key': os.getenv('TORCH_ACCESS_KEY', 'OY2VVIN2N6LJ'),
    'secret_key': os.getenv('TORCH_SECRET_KEY', 'da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
}