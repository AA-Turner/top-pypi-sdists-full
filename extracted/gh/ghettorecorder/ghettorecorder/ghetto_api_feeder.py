
import ghettorecorder.ghetto_procenv as procenv
from ghettorecorder.ghetto_api import ghettoApi


def ghetto_info_dump_get():
    """Dump all active radios info to Ghetto API.
    procenv uses *eval* via queue to get data.

    A list of header properties dicts is used to update info API subclass.

    :methods: ghetto_api_feed
    """
    rad_lst = [radio for radio in ghettoApi.radio_inst_dict.keys()]
    if len(rad_lst):
        api_item_lst = list(map(lambda rad: procenv.radio_attribute_get(radio=rad, attribute='info_dump_dct'), rad_lst))
        ghetto_api_feed(api_item_lst)


def ghetto_api_feed(api_item_lst):
    """Set key and value for API, info subclass.
    """
    for dct in api_item_lst:
        try:
            radio = dct['radio']
            ghettoApi.info.icy_url[radio] = dct['icy-url']
            ghettoApi.info.icy_name[radio] = dct['icy-name']
            ghettoApi.info.bit_rate[radio] = dct['bit_rate']
            ghettoApi.info.request_time[radio] = dct['request_time']
            ghettoApi.info.content_type[radio] = dct['content-type']
            ghettoApi.info.current_title_dict[radio] = dct['new_title']
        except KeyError:
            pass
        try:
            radio = dct['radio']
            ghettoApi.info.runs_meta[radio] = dct['runs_meta']
            ghettoApi.info.runs_record[radio] = dct['runs_record']
            ghettoApi.info.runs_listen[radio] = dct['runs_listen']
        except KeyError:
            pass
