"""Modules use the attributes to communicate with other modules.
"""


class GhettoApi:
    """Container. lol
    3rd party module for exposing some useful variables (to Terminal or Flask).

    __init__

    :params: radio_inst_dict: store & config radio instances, ghettoApi.radio_inst_dict[radio] = GhR(radio, url)
    :params: measure_dict: {'radio,elem': txt} response header values for UI
    :params: audio_stream_queue_dict: {'radio,audio': queue_data} queue buffer to web srv to html audio element
    :params: audio_stream_suffix_dict: {'radio_name,audio': '.mp3'} file extension of audio_stream_queue_dict data
    :params: audio_stream_content_type_dict: {'radio1,audio': audio/mpeg, 'radio2,audio': audio/aac} for Flask
    :params: current_title_dict: {'radio_name': song_title}
    :params: error_dict: error messages for Web server, can send it to Frontend and write messages to Html UI
    :params: recorder_new_title_dict: new title, compare it with all_blacklists_dict and write file or not
    :params: all_blacklists_dict: stores all lists of all radios from fs json or db in a memory dict
    :params: stop_blacklist_writer: stop writer thread
    :params: skipped_in_session_dict: shows effects of record blacklisting per session
    :params: blacklist_dir: path to record blacklist json dict
    :params: blacklist_name: name of record blacklist file
    :params: blacklist_enable: [GLOBAL] section of ini config, enables it for all radios
    :params: config_dir: absolute path to ini config file
    :params: config_name: name of ini config file
    :params: radio_parent: name of radio parent dir (example 'RADIOS')
    :params: save_to_dir: [GLOBAL] section of ini config full path, remote save files, overrides default path
    :params: radio_err_count_dict: {'radio_name': 42} reveal connection errors, useful to count in a timeframe
    :params: feature_mgr_dict: feature manager instances
    """

    def __init__(self):
        """Here is no __private_var. No setter, getter needed. Dict init must not be 'None'"""
        # dict to store radio instances
        self.radio_inst_dict = {}

        # grouped attributes container
        self.audio = self.Audio()
        self.blacklist = self.BlackList()
        self.err = self.Err()
        self.info = self.Info()
        self.path = self.Path()
        self.feature = self.Feature()

    class Audio:
        def __init__(self):
            self.audio_simple_http_queue_dict = {}
            self.audio_stream_queue_dict = {}
            self.audio_stream_suffix_dict = {}
            self.audio_stream_content_type_dict = {}

    class BlackList:
        # keep it simple for mp, queue updates process local inherited api (dead) dicts, instance think all is ok
        def __init__(self):
            self.blacklist_dir = ""
            self.blacklist_name = ""
            self.blacklist_enable = False  # input instance if multiprocessing, recorder must know
            self.all_blacklists_dict = {}  # input instance, bl json radio list
            self.stop_blacklist_writer = False
            self.skipped_in_session_dict = {}
            self.recorder_new_title_dict = {}  # output instance

    class Err:
        def __init__(self):
            self.error_dict = {}
            self.radio_err_count_dict = {}

    class Info:
        """Dicts are incompatible with GhettoRecorder < v3.
        Previous version used ghetto_measure_dict[name + ',suffix'] style in one dict.
        """
        def __init__(self):
            self.bit_rate = {}
            self.request_time = {}
            self.content_type = {}
            self.icy_name = {}
            self.icy_genre = {}
            self.icy_url = {}
            self.current_title_dict = {}
            self.runs_meta = {}  # update from instance {'bar': True}
            self.runs_record = {}
            self.runs_listen = {}

    class Path:
        def __init__(self):
            self.config_dir = ""
            self.config_name = ""
            self.radio_parent = ""
            self.save_to_dir = ""

    class Feature:
        def __init__(self):
            self.feature_mgr_dict = {}


ghettoApi = GhettoApi()
