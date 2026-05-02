"""Module to operate the radio instances.

changes for android
search in files for "ANDROID_STORAGE"
"""
import os
import time


import ghettorecorder.ghetto_net as net
from ghettorecorder.__init__ import GhettoRecorder  # without __init__ broken !? [Baustelle]
from ghettorecorder.ghetto_api import ghettoApi

dir_name = os.path.dirname(__file__)

if 'ANDROID_STORAGE' not in os.environ:
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
else:
    import queue


class ProcEnv:
    def __init__(self):
        self.trash_bin = None  # supress useless msg
        self.instance_start_dict = {}  # radio instances collector


procenv = ProcEnv()


def radio_instances_get():
    """Return list of radio instances.
    We can connect to the Queues for communication.

    :returns: list of running radio instances
    """
    r_lst = [radio for radio in ghettoApi.radio_inst_dict.keys()]
    return r_lst


def del_radio_instance(radio):
    """
    | Cancel radio instance.
    | cancel_join_thread(), no graceful shutdown of queue
    """

    inst_dct = ghettoApi.radio_inst_dict
    if radio not in inst_dct.keys():
        return
    try:
        radio_run_cmd(radio=radio, cmd='self.cancel()')
        q_lst = [inst_dct[radio].com_in, inst_dct[radio].com_out, inst_dct[radio].audio_out]
        for q in q_lst:
            while not q.empty():
                q.get()
            try:
                q.cancel_join_thread()
            except AttributeError:  # Android use queue.Queue, cancel_join_thread avail
                pass

        del ghettoApi.radio_inst_dict[radio]

    except Exception as e:
        print('Exception: del_radio_instance ', radio, e)
    print(f'[removed] {radio} from dictionary ')


def radio_instance_create(radio, url, **kwargs):
    """Start radio if not exist.

    | Message Queues, com ports, creator of instance (we) attach the queue to instance

    :params: com_in: = mp.Queue(maxsize=1) (radio, [str 'eval' or 'exec'], str 'command') e.g. 'radio_attribute_get'
    :params: com_out: = mp.Queue(maxsize=1) result tuple (radio, 'eval', result)  result can be error
    :params: audio_out: = mp.Queue(maxsize=1) port to connect a server, audio data is same as written to disk

    :params: radio: radio
    :params: url: url
    :params: kwargs: config, blacklist, path variables
    :returns: True if instance was created or is running
    """
    if radio in ghettoApi.radio_inst_dict.keys():  # runs already
        return True

    resp = net.load_url(url)  # open connection and forget,; reverse in '__main__.get_sound' we release connection
    if not resp:
        print(f'NO connection for instance: {radio} ')
        return False

    radio, url = radio, url
    meta, record, listen, base_dir = True, True, True, dir_name
    if len(kwargs):
        base_dir = kwargs['radios_parent_dir']
        meta, record, listen = kwargs['runs_meta'], kwargs['runs_record'], kwargs['runs_listen']

    dct = ghettoApi.radio_inst_dict
    dct[radio] = GhettoRecorder(radio, url)
    dct[radio].radio_base_dir = base_dir
    dct[radio].runs_meta = meta
    dct[radio].runs_record = record
    dct[radio].runs_listen = listen
    if 'ANDROID_STORAGE' not in os.environ:
        dct[radio].com_in = mp.Queue(maxsize=1)  # radio must share one com_in q with others, if mp per CPU is up
        dct[radio].com_out = mp.Queue(maxsize=1)  # com_out dito
        dct[radio].audio_out = mp.Queue(maxsize=1)  # audio_out dito
    else:
        dct[radio].com_in = queue.Queue(maxsize=1)
        dct[radio].com_out = queue.Queue(maxsize=1)
        dct[radio].audio_out = queue.Queue(maxsize=1)
    dct[radio].start()
    return True


def radio_wait_online(radio):
    """Ask instance for ready status."""
    in_ = ghettoApi.radio_inst_dict[radio].com_in
    out_ = ghettoApi.radio_inst_dict[radio].com_out
    start = time.perf_counter()
    timeout = 15
    while 1:  # minimize wait time
        msg = (radio, 'eval', 'getattr(self, "init_done")')  # tuple
        in_.put(msg)
        done = out_.get()[2]  # tuple
        if done or round((time.perf_counter() - start)) >= timeout:
            break
        time.sleep(.2)


def radio_control_qs_get(radio):
    """
    | Queues to process eval, exec commands in multiprocessor instances.
    | Basic check if radio instance is available.

    :params: radio: instance to connect control queues
    :returns: tuple of control queues in and out put
    """
    if radio not in ghettoApi.radio_inst_dict.keys():
        return None, None
    radio_wait_online(radio)
    in_ = ghettoApi.radio_inst_dict[radio].com_in
    out_ = ghettoApi.radio_inst_dict[radio].com_out
    return in_, out_


def radio_attribute_get(radio=None, attribute=None):
    """Eval request of instance.

    :params: radio: name of instance
    :params: attribute: string of attribute name
    """
    in_, out_ = radio_control_qs_get(radio)
    if in_ and out_:
        msg = (radio, 'eval', 'getattr(self, "' + attribute + '")')  # tuple
        in_.put(msg)
        return out_.get()[2]  # tuple


def radio_attribute_set(radio=None, attribute=None, value=None):
    """Set only instance Attribute values here.

    :params: radio: name of instance
    :params: attribute: string of attribute name
    :params: attribute: string of attribute value
    """
    in_, out_ = radio_control_qs_get(radio)
    if in_ and out_:
        in_.put((radio, 'exec', 'setattr(self, "' + attribute + '", ' + value + ')'))
        procenv.trash_bin = out_.get()[2]  # useless msg, just see it was done


def radio_run_cmd(radio=None, cmd=None):
    """Run one or multiple commands string in the radio instance.

    :params: radio: instance of a radio
    :params: cmd: string of python statement
    """
    in_, out_ = radio_control_qs_get(radio)
    if in_ and out_:
        in_.put((radio, 'exec', cmd))
        procenv.trash_bin = out_.get()[2]  # useless msg, just see it was done


def user_display_dict_get(radio):
    """Give user overview. Where are files, header info, which recorder is running."""
    user_display_dct = {'title': None,
                        'bit_rate': None,
                        'radio_dir': None,
                        'content': None,
                        'radio_name': radio,
                        'recorder': None}

    if radio not in ghettoApi.radio_inst_dict.keys():
        return user_display_dct

    content_type, bit_rate, new_title, radio_dir = "content_type", "bit_rate", "new_title", "radio_dir"
    user_display_dct = {'title': radio_attribute_get(radio=radio, attribute=new_title),
                        'bit_rate': radio_attribute_get(radio=radio, attribute=bit_rate),
                        'radio_dir': radio_attribute_get(radio=radio, attribute=radio_dir),
                        'content': radio_attribute_get(radio=radio, attribute=content_type),
                        'radio_name': radio,
                        'recorder': None}
    return user_display_dct
