##from abstract_apis import make_request_link
##response= make_request_link('typicaly','get_available_raw_video_list')
##input(response)
from solcatcher_api_calls import *
result = make_solcatcher_api_call('get_latest_row',tableName='logdata')
input(result)
