"""Network module for GhettoRecorder.

:methods: load_url: exec request
:methods: stream_filetype_url: get file suffix of the stream from content-type
:methods: content_type_get: Content-Type of response
:methods: suffix_from_content_type_get: file suffix from content-type
:methods: bit_rate_get: bit rate from header
:methods: calc_buffer_size: buf size to write optimal to fs blocks
:methods: pls_m3u_resolve_url: resolve playlist url
:methods: playlist_m3u: extract first available server from playlist
:methods: resolve_playlist: return first url from a playlist
"""
import io
import ssl
import urllib
import certifi
from urllib.request import urlopen, Request

import ghettorecorder.ghetto_header_mp3 as ghetto_header_mp3
import ghettorecorder.ghetto_header_aac as ghetto_header_aac

context_ssl = ssl.create_default_context(cafile=certifi.where())


def load_url(url, user_agent=None):
    """Get server response.
    The place of hope and ''interesting behaviour''.

    :params: url: url
    :exception: Timeout recursive call
    :return: http server response
    :rtype: http response
    """
    request = Request(url)
    opener = urllib.request.build_opener()
    if user_agent:
        opener.addheaders = [('User-agent', user_agent)]
    urllib.request.install_opener(opener)

    try:
        response = urlopen(request, timeout=15, context=context_ssl)
    except TimeoutError:
        print('TimeoutError in load_url().')
        return False
    except Exception as error:
        print(f'unknown error in load_url() {error}')
        return False

    return response


def stream_filetype_url(response, str_radio):
    """Get file suffix of the stream from content-type,
    not called if the server failed before.

    :params: response: http response
    :params: str_radio: name
    :returns: stream suffix
    :rtype: str
    """
    content_type = response.getheader('Content-Type')
    stream_suffix = suffix_from_content_type_get(content_type)
    try:
        if not stream_suffix:
            print(f"\n---> error {str_radio}: record(), no content-type {stream_suffix}"
                  f"\nServer alive but wrong endpoint\nCheck URL! - Exit")
            return
    except TypeError as error:
        print(f"\n---> error {str_radio}: record(), no content-type {error} - Exit")
        return
    return stream_suffix


def content_type_get(response):
    """Content-Type of response.
    Bugfix for Chrome browsers

    :params: response: http response
    :returns: Content-Type
    :rtype: str
    """
    if 'aacp' in response.getheader('Content-Type'):
        return 'audio/aac'  # fix chromium, download instead of play
    # print(response.headers)
    return response.getheader('Content-Type')


def suffix_from_content_type_get(content_type):
    """Translate content-type to file suffix.

    :params: content_type: content_type
    :returns: stream suffix
    :rtype: str
    """
    stream_suffix = ''
    if content_type == 'audio/aacp' or content_type == 'application/aacp':
        stream_suffix = '.aacp'
    if content_type == 'audio/aac':
        stream_suffix = '.aac'
    if content_type == 'audio/ogg' or content_type == 'application/ogg':
        stream_suffix = '.ogg'
    if content_type == 'audio/mpeg':
        stream_suffix = '.mp3'
    if content_type == 'audio/x-mpegurl' or content_type == 'text/html':
        stream_suffix = '.m3u'
    # application/x-winamp-playlist , audio/scpls , audio/x-scpls ,  audio/x-mpegurl
    return stream_suffix


def bit_rate_get(chunk, suffix):
    """Get bitrate from stream to adapt buffer size for writing and listen queue.

    :exception: stream is not mp3 or aac; has wrong content-type
    :rtype: False
    :params: chunk: to scan for bitrate
    :params: suffix: stream file extension
    :return: bit rate value
    :rtype: int
    """
    try:
        if 'mp3' in suffix:
            mp3H = ghetto_header_mp3.Mp3Header(chunk)
            bitrate = mp3H.bitrate_get()
            return int(bitrate) if bitrate else None
        elif 'aac' in suffix:
            bitrate = ghetto_header_aac.bit_rate_get(chunk)
            return int(bitrate) if bitrate else None
        else:
            raise Exception('---> no bitrate from stream')
    except Exception as ex:
        print(ex)
        return False


def calc_buffer_size(bitrate):
    """Bitrate from file chunk header.
    buf_size = (bitrate * 1_000) / 8
    - Avoid digital noise, delays and connection breaks in Browser.

    :params: bitrate: bitrate
    :return: buffer size for reading Http response chunks
    :rtype: int
    """
    if bitrate <= 80:
        stream_chunk_size = io.DEFAULT_BUFFER_SIZE
    elif (bitrate > 80) and (bitrate <= 160):
        stream_chunk_size = io.DEFAULT_BUFFER_SIZE * 2
    elif (bitrate > 160) and (bitrate <= 240):
        stream_chunk_size = io.DEFAULT_BUFFER_SIZE * 3
    else:
        stream_chunk_size = io.DEFAULT_BUFFER_SIZE * 4  # 8KB * x; HQ audio 320kB/s
    return int(stream_chunk_size)


def pls_m3u_resolve_url(url):
    """Return URL, if input url was a play list.
    - 'http://metafiles.gl-systemhaus.de/hr/hr3_2.m3u' to 'http://dispatcher.rndfnk.com/hr/hr3/live/mp3/128/stream.mp3'

    :params: url: url
    :returns: true url of server or does nothing
    :rtype: str
    """
    if url[-4:] == '.m3u' or url[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
        resolved_url = playlist_m3u(url)
        return resolved_url
    else:
        return url


def playlist_m3u(url):
    """We know it is a playlist.
    Return the first server.

    :exception: server not ready
    :rtype: False
    :params: url: url
    :returns: true url of server
    :rtype: str
    """
    try:
        response = load_url(url)
    except Exception as ex:
        print(ex)
        return False

    playlist_file = response.read().decode('utf-8')
    m3u_lines = playlist_file.split("\n")
    for row_url in m3u_lines:
        if row_url[0:4].lower() == 'http':
            return row_url
