import json
import uuid
from lambdatest_sdk_utils import is_smartui_enabled,fetch_dom_serializer,post_snapshot,get_snapshot_status
from lambdatest_sdk_utils import setup_logger,get_logger


def smartui_snapshot(driver, name,options={}):
    # setting up logger
    setup_logger()
    logger = get_logger('lambdatest-selenium-driver')

    if not name:
        raise Exception('The `snapshotName` argument is required.')
    if is_smartui_enabled() is False: 
        raise Exception("Cannot find SmartUI server.")
    
    try:
        resp = fetch_dom_serializer()
        driver.execute_script(resp['data']['dom'])

        # Get the sessionId from the driver
        session_id = driver.session_id
        if session_id:
            options['sessionId'] = session_id  # Append sessionId to options

        # Serialize and capture the DOM
        dom = driver.execute_script(
            f"""
            return {{
                dom: SmartUIDOM.serialize({json.dumps(options)}),
                url: document.URL
            }}
            """
        )

        # Post the dom to smartui endpoint
        dom['name'] = name
        if 'sync' in options and options['sync'] is True:
            options['contextId'] = str(uuid.uuid4())
            res = post_snapshot(dom,'lambdatest-selenium-driver',options=options)

            if res and res.get('data') and res['data'].get('warnings') and len(res['data']['warnings']) != 0:
                for warning in res['data']['warnings']:
                    logger.warn(warning)

            logger.info(f'Snapshot captured {name}')
            timeout= 600
            if 'timeout' in options and options['timeout'] is not None:
                timeout = options['timeout']
            if timeout > 900 or timeout < 30:
                timeout=600
                logger.warn("Timeout value is not valid, allowed range is 30-900 seconds. Defaulting to 600 seconds.")
            return get_snapshot_status(name,options['contextId'],timeout)
        else:
            res = post_snapshot(dom,'lambdatest-selenium-driver',options=options)

            if res and res.get('data') and res['data'].get('warnings') and len(res['data']['warnings']) != 0:
                for warning in res['data']['warnings']:
                    logger.warn(warning)

            logger.info(f'Snapshot captured {name}')
    except Exception as e:
        logger.error(f'SmartUI snapshot failed  "${name}"')
        logger.error(e)