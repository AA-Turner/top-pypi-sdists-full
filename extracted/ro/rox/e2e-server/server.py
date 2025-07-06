from queue import Queue
import threading
from werkzeug.serving import make_server
from werkzeug import Request, Response

import os
import sys
import json
from datetime import datetime

from rox.server.flags.rox_flag import RoxFlag
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions, NetworkConfigurationsOptions
from datetime import datetime
from rox.core.configuration.configuration_fetched_invoker import ConfigurationFetchedArgs

class Container:
    instance = None

    def __init__(self):
        self.boolDefaultFalse = RoxFlag(False)
        self.boolDefaultTrue = RoxFlag(True)

Container.instance = Container()

class ServerLogger:
    def debug(self, message, ex=None):
        now = datetime.now()
        if ex is None:
            print('date: %s (debug) - %s' % (now, message))
        else:
            print('date: %s (debug) - %s. Exception: %s' % (now, message, ex))

    def error(self, message, ex=None):
        now = datetime.now()
        if ex is None:
            print('date: %s (error) - %s' % (now, message))
        else:
            print('date: %s (error) - %s. Exception: %s' % (now, message, ex))

    def warn(self, message, ex=None):
        now = datetime.now()
        if ex is None:
            print('date: %s (warn) - %s' % (now, message))
        else:
            print('date: %s (warn) - %s. Exception: %s' % (now, message, ex))

def application_handler():
    msgQueue = Queue()

    def config_fetch(o: ConfigurationFetchedArgs):
        now = datetime.now()
        print("date %s: (configFetcher) - applied-from=%s creation-date=%s has-changes=%s error=%s" % (now, o.fetcher_status , o.creation_date , o.has_changes , o.error_details)  )

    @Request.application
    def app(request: Request) -> Response:
        if (request.method == 'GET'):
            if (request.path == '/status-check'):
                return Response("OK", 200)
            else:
                return Response("Not Found", 404)

        if (request.method == 'POST'):
            data = request.get_json()
            action = data['action']
            payload = data.get('payload')
            print(data)
            if action == 'staticFlagIsEnabled':
                result = getattr(Container.instance, payload['flag']).is_enabled(payload['context'])
                contents = json.dumps({ 'result': result })
                return Response(contents, content_type="application/json") 
            elif action == 'registerStaticContainers':
                Rox.register('namespace', Container.instance)
                contents = json.dumps({ 'result': 'done' })
                return Response(contents, content_type="application/json") 
            elif action == 'setCustomPropertyToThrow':
                def raise_(ex):
                    raise ex
                Rox.set_custom_string_property(payload['key'], lambda context: raise_(Exception('error')))
                contents = json.dumps({ 'result': 'done' })
                return Response(contents, content_type="application/json")     
            elif action == 'setCustomStringProperty':
                Rox.set_custom_string_property(payload['key'], payload['value'])
                contents = json.dumps({ 'result': 'done' })
                return Response(contents, content_type="application/json")
            elif action == 'setCustomDateProperty':
                Rox.set_custom_datetime_property(payload['key'], datetime.fromisoformat(payload['value'][0:19]))
                contents = json.dumps({ 'result': 'done' })
                return Response(contents, content_type="application/json")    
            elif action == 'dynamicFlagValue':
                context = payload.get('context')
                flag = None
                if sys.version_info < (3, 0):
                    flag = payload['flag'].encode('utf-8')
                else:
                    flag = payload['flag']
                result = Rox.dynamic_api().value(flag, payload['defaultValue'], [], context)
                contents = json.dumps({ 'result': result })
                return Response(contents, content_type="application/json")    
            elif action == 'dynamicFlagIsEnabled':
                context = payload.get('context')
                flag = payload['flag']
                result = Rox.dynamic_api().is_enabled(flag, payload['defaultValue'], context)
                contents = json.dumps({ 'result': result })
                return Response(contents, content_type="application/json")    
            elif action == 'setupAndAwait':
                print(payload['options'])
                env = 'stam'
                network_config = None
                fetch_interval = None
                options = payload.get('options')
                disable_signature_verification = options.get('disableSignatureVerification')
                if options is not None:
                    fetch_interval = options.get('fetchInterval')
                    env = options.get('env') or env
                    configuration = options.get('configuration')
                if env == 'container':
                    network_config = NetworkConfigurationsOptions(
                        configuration['CD_API_ENDPOINT'],
                        configuration['CD_S3_ENDPOINT'],
                        configuration['SS_API_ENDPOINT'],
                        configuration['SS_S3_ENDPOINT'],
                        configuration['ANALYTICS_ENDPOINT'],
                        configuration['NOTIFICATIONS_ENDPOINT'])
                if env == 'qa':
                    os.environ['ROLLOUT_MODE'] = 'QA'
                if env == 'localhost':
                    os.environ['ROLLOUT_MODE'] = 'LOCAL'
                print("using env: ", env)
                options = RoxOptions(logger=ServerLogger(), 
                                     network_configuration_options=network_config,
                                     fetch_interval=fetch_interval,
                                     disable_signature_verification=disable_signature_verification)
                
                Rox.setup(payload['key'], options).result()
                contents = json.dumps({ 'result': 'done' })
                return Response(contents, content_type="application/json")    
            elif action == 'stop':
                print("stopping SDK")
                Rox.shutdown()
                msgQueue.put("quit") # the message 'quit' has no meaning (it's the return value in msgQueue.get but we don't use it)
                contents = json.dumps({ 'result': 'done' })
                return Response(contents, content_type="application/json")

    port = int(os.environ['PORT'])
    print("starting server on port ", port)

    # Start server
    service = make_server("localhost", port, app)
    sdkServerThread = threading.Thread(target=service.serve_forever)
    sdkServerThread.start()

    # Waiting for a queue message
    msgQueue.get(block=True)

    # Terminate server
    service.shutdown()
    print("server terminated")
    sdkServerThread.join()

if __name__ == "__main__":
    application_handler()
