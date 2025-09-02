import requests
from lambdatest_sdk_utils.constants import get_smart_ui_server_address
from lambdatest_sdk_utils.logger import get_logger

logger = get_logger('lambdatest_sdk_utils')

def is_smartui_enabled():
    try:
        response = requests.get(f'{get_smart_ui_server_address()}/healthcheck')
        response.raise_for_status()
        return True
    except Exception as e:
        return False
    

def fetch_dom_serializer():
    try:
        response = requests.get(f'{get_smart_ui_server_address()}/domserializer')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        err_resp = e.response.json()
        msg = err_resp.get('data', {}).get('error', 'Unknown error')
        logger.debug(f'fetch DOMSerializer API failed - {msg}')
        raise Exception(f'fetch DOMSerializer failed')
    except Exception as e:
        logger.debug(f'fetch DOMSerializer failed - {e}')
        raise Exception(f'fetch DOMSerializer failed')


def post_snapshot(snapshot,pkg,**kwargs):
    try:
        response = requests.post(f'{get_smart_ui_server_address()}/snapshot', json={
            'snapshot': {
                'dom' : snapshot['dom'],
                'name' : snapshot['name'],
                'url' : snapshot['url'],
                **kwargs
            },
            'testType': pkg
        })    
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        err_resp = e.response.json()
        msg = err_resp.get('data', {}).get('error', 'Unknown error')
        logger.debug(f'Snapshot Error: {msg}')
        raise Exception(f'Snapshot Error')
    except Exception as e:
        logger.debug(f'post snapshot failed : {msg}')
        raise Exception(f'post snapshot failed')


