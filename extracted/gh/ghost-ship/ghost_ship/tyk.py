from pymongo import MongoClient
from os import environ
import logging, requests, time
from ghost_ship import exception

MONGO_URL = environ['TYK_MONGO_URL']
CONSUL_ADDR = environ['CONSUL_ADDR']
TYK_ADDR = environ['TYK_ADDR']
TYK_TOKEN = environ['TYK_TOKEN']
TYK_DB_NAME = environ.get('TYK_DB_NAME', 'tyk_analytics')

mong = MongoClient(MONGO_URL)
db = mong[TYK_DB_NAME]

def reload(service_name, state):
  logging.info('Waiting 10s before reload...')
  query_endpoint = CONSUL_ADDR + '/v1/health/service/%s?passing&tag=%s' % (service_name, state)
  condition = {"proxy.service_discovery.query_endpoint": {"$regex": "http(.)*%s(.)*" % service_name}}
  logging.debug('Tyk update condition')
  logging.debug(condition)
  for item in db.tyk_apis.find(condition):
    logging.debug(item)

  if db.tyk_apis.find(condition).count():
    logging.info('Update %s discovery to: %s' % (service_name, query_endpoint))
    db.tyk_apis.update_many(condition, {
      "$set": {
        "proxy.service_discovery.query_endpoint": query_endpoint 
      }
    })
    logging.info('Reload tyk')
    if not reload_tyk():
      raise exception.TykReloadFailed('Reload Tyk fail cmnr!!!')
    logging.info('Reload signal has been sent to tyk, waiting 30s...')
    time.sleep(30)
  else:
    raise exception.TykServiceNotFound('Tyk service: %s is not found' % service_name)

def reload_tyk():
  url = TYK_ADDR + '/tyk/reload/group'
  headers = {
    "X-Tyk-Authorization": TYK_TOKEN
  }
  resp = requests.get(url, headers=headers)
  return resp.status_code == 200
