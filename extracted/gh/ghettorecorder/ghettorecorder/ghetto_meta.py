"""Extract title information from metadata response.

:methods: meta_get: returns a full path for file dump #
:methods: title_path_build: build the path #
:methods: metadata_request: request one chunk of title info #
:methods: metadata_header_info: write header info to API for other modules to use #
:methods: metadata_icy_info: extract binary meta info from response #
:methods: metadata_get_display_extract: convert to string and clean it
:methods: metadata_get_display_info: pre switch to filter out titles from u unreliable and wrong metadata responses
:methods: remove_special_chars: clean string for writing on OS fs
"""

import os
import ssl
import time
import urllib
import urllib.error
import certifi
from urllib.request import urlopen, Request

import ghettorecorder.ghetto_utils as ghetto_utils

os.environ['SSL_CERT_FILE'] = certifi.where()
context_ssl = ssl.create_default_context(cafile=certifi.where())


class MetaData:
    """Collect Metadata titles. Titles are used as filenames.
    Header information collected as service for 3rd party modules.

    """

    def __init__(self):
        self.title = None
        self.title_path = None
        self.header_info_dict = {}

    def metadata_header_info(self, request, str_radio, request_time, bit_rate):
        """Fill dict with header information to display values/information about radio on html page

        :params: request: icy request
        :params: str_radio: radio
        :params: request_time: time of request duration
        """
        self.header_info_dict = {
            'radio': str_radio,
            'bit_rate': bit_rate,
            'request_time': request_time,
            'content-type': validate_header_data(request.headers['content-type']),
            'icy-name': validate_header_data(request.headers['icy-name']),
            'icy-genre': validate_header_data(request.headers['icy-genre']),
            'icy-url': validate_header_data(request.headers['icy-url']),
        }

    def meta_get(self, url, str_radio, radio_dir, stream_suffix, bit_rate, user_agent):
        """Receive and process metadata. Prone to UrlError Timeout.

        :exception: if metadata corrupt or connection
        :returns: Exception object to deal
        :params: url: url
        :params: str_radio: name of radio
        :params: radio_dir: absolute path to radio dir
        :params: stream_suffix: file suffix of stream
        :params: user_agent: random agent
        :returns: absolute path to file and the title
        :rtype: str
        """
        start_time = time.perf_counter()
        response = metadata_request(url, user_agent)
        request_time = round((time.perf_counter() - start_time) * 1000)
        if not response:
            return

        self.metadata_header_info(response, str_radio, request_time, bit_rate)
        try:
            icy_info = metadata_icy_info(response, str_radio)
            self.title_path, self.title = title_path_build(icy_info, url, radio_dir, stream_suffix)
        except (AttributeError,):  #
            return AttributeError  # minor
        except Exception as e:
            print(f' ---> meta_get() {str_radio}, exception info: {type(e).__name__} , {url} {self.header_info_dict}')


def validate_header_data(value):
    """return either value or empty string for Java or Html
    """
    try:
        return value
    except KeyError:
        return ''


def title_path_build(icy_info, url, radio_dir, stream_suffix):
    """Absolute Path from strings builder.

    :params: icy_info: pre cleaned title string
    :params: url: url
    :params: radio_dir: absolute path to radio dir
    :params: stream_suffix: file suffix of stream
    :rtype: str
    """
    title_raw = metadata_get_display_info(icy_info)
    if title_raw:
        try:
            if title_raw[0] == "'" and title_raw[-1] == "'":
                title_raw = title_raw[1:-1]
            title_blank = ghetto_utils.remove_special_chars(title_raw)
            title = title_blank.strip()
            title_path = os.path.join(radio_dir, title + stream_suffix)
        except Exception as error:
            print(f' ---> title_path_build, exception info: {error} , {url}')
            return False
        return title_path, title


def metadata_request(url, user_agent):
    """ pull the metadata by telling server request.add_header('Icy-MetaData', '1'),
    get binary data block with metadata content

    :params: url: url
    :rtype: response
    """
    request = Request(url)
    request.add_header('Icy-MetaData', '1')
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agent)]  # user agent only wants opener
    urllib.request.install_opener(opener)
    try:
        response = urlopen(request, timeout=15, context=context_ssl)
        return response
    except TimeoutError:
        print('TimeoutError in metadata_request() retry.')
        return False
    except OSError:
        pass  # URLError subclass, short timeout
    except Exception as error:
        print(f'unknown error in metadata_request() {error} exception info: {type(error).__name__} ')
        return False


def metadata_icy_info(request, str_radio):
    """Returns raw byte code metadata from radio.
    Find start byte, convert to int, find out bytes to read, read block of bytes
    return a byte code error message on unknown error.

    :params: request: request
    :params: str_radio: name
    :returns: string of title
    :rtype: bytes
    """
    try:
        icy_meta_int = int(request.headers['icy-metaint'])
        request.read(icy_meta_int)
        start_byte = request.read(1)
        start_int = ord(start_byte)
        num_of_bytes = start_int * 16
        metadata_content = request.read(num_of_bytes)
        return metadata_content
    except Exception as error:
        message = f'metadata_icy_info(), {str_radio}: no or false metadata; {error}'
        print(message)
        # caller expects byte
        return b"StreamTitle='GhettoRecorder module info\n" \
               b"radio returns no or false metadata including title and stream url\n" \
               b"radio service is active on url and port, since I am not crashed, check url part after port\n" \
               b"recording without titles if stream is active at all';StreamUrl='';\x00\x00"


def metadata_get_display_extract(icy_info):
    """ return cleaned up metadata tile

    :params: icy_info: bytes string
    :rtype: str
    """
    # StreamTitle='X-Dream - Panic In Paradise * anima.sknt.ru';StreamUrl='';
    try:
        title_list = icy_info.split(";")
        if not len(title_list) > 1 or title_list is None:
            return  # empty list
        title_list = title_list[0].split("=")
        title = str(title_list[1])
        title = ghetto_utils.remove_special_chars(title)
        if title is not None:
            return title
    except IndexError:
        pass
    except OSError:
        pass
    return


def metadata_get_display_info(icy_info):
    """ extract readable title data to show it on html page

    :params: icy_info: bytes string
    :rtype: decoded str
    """
    # <class 'bytes'> decode to <class 'str'> actually b''
    try:
        title = metadata_get_display_extract(icy_info.decode('utf-8'))
        if not title:
            return
        if title:
            return title
    except AttributeError:
        """AttributeError: Server sends no metadata; bool value instead"""
        return
    except Exception as error:
        print(f' Exception in metadata_get_display_info: {error}')
        return
