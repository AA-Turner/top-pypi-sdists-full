/* Generated file - do not edit. */
/* See doc/docstrings/ *.rst. */

#include "pycurl.h"

PYCURL_INTERNAL const char curl_doc[] = "Curl() -> New Curl object\n\
\n\
Creates a new :ref:`curlobject` which corresponds to a\n\
``CURL`` handle in libcurl. Curl objects automatically set\n\
CURLOPT_VERBOSE to 0, CURLOPT_NOPROGRESS to 1, provide a default\n\
CURLOPT_USERAGENT and setup CURLOPT_ERRORBUFFER to point to a\n\
private error buffer.\n\
\n\
Implicitly calls :py:func:`pycurl.global_init` if the latter has not yet been called.\n\
\n\
The ``Curl`` object can be used as a context manager. Exiting the\n\
context calls ``close()``.\n\
\n\
Example::\n\
\n\
    with pycurl.Curl() as c:\n\
        # perform operations";

PYCURL_INTERNAL const char curl_close_doc[] = "close() -> None\n\
\n\
Close handle and end curl session.\n\
\n\
Corresponds to `curl_easy_cleanup`_ in libcurl. This method is\n\
automatically called by pycurl when a Curl object no longer has any\n\
references to it, but can also be called explicitly.\n\
\n\
.. _curl_easy_cleanup:\n\
    https://curl.haxx.se/libcurl/c/curl_easy_cleanup.html";

PYCURL_INTERNAL const char curl_closed_doc[] = "closed() -> bool\n\
\n\
Return ``True`` if the ``Curl`` object was already closed, ``False`` otherwise.";

PYCURL_INTERNAL const char curl_duphandle_doc[] = "duphandle() -> Curl\n\
\n\
Clone a curl handle. This function will return a new curl handle,\n\
a duplicate, using all the options previously set in the input curl handle.\n\
Both handles can subsequently be used independently.\n\
\n\
The new handle will not inherit any state information, no connections,\n\
no SSL sessions and no cookies. It also will not inherit any share object\n\
states or options (it will be made as if SHARE was unset).\n\
\n\
When ``MIMEPOST`` includes parts configured with ``CurlMimePart.data_cb()``,\n\
libcurl duplicates callback userdata pointers into the duplicated handle.\n\
Design callback state (especially any ``free`` hook side effects) so that\n\
multiple handle instances can release it safely.\n\
See also `curl_mime_data_cb`_ in libcurl.\n\
\n\
Corresponds to `curl_easy_duphandle`_ in libcurl.\n\
\n\
Example usage::\n\
\n\
    import pycurl\n\
    curl = pycurl.Curl()\n\
    curl.setopt(pycurl.URL, \"https://python.org\")\n\
    dup = curl.duphandle()\n\
    curl.perform()\n\
    dup.perform()\n\
\n\
.. _curl_easy_duphandle:\n\
    https://curl.se/libcurl/c/curl_easy_duphandle.html\n\
\n\
.. _curl_mime_data_cb:\n\
    https://curl.se/libcurl/c/curl_mime_data_cb.html";

PYCURL_INTERNAL const char curl_errstr_doc[] = "errstr() -> string\n\
\n\
Return the internal libcurl error buffer of this handle as a string.\n\
\n\
Return value is a ``str`` instance. Error buffer data is decoded using\n\
Python's default encoding at the time of the call. If this decoding fails,\n\
``UnicodeDecodeError`` is raised. Use :ref:`errstr_raw <errstr_raw>` to\n\
retrieve the error buffer as a byte string in this case.";

PYCURL_INTERNAL const char curl_errstr_raw_doc[] = "errstr_raw() -> byte string\n\
\n\
Return the internal libcurl error buffer of this handle as a byte string.\n\
\n\
Return value is a ``bytes`` instance. Unlike :ref:`errstr <errstr>`,\n\
``errstr_raw`` allows reading libcurl error buffer when its contents is not\n\
valid in Python's default encoding.\n\
\n\
*Added in version 7.43.0.2.*";

PYCURL_INTERNAL const char curl_getinfo_doc[] = "getinfo(option) -> Result\n\
\n\
Extract and return information from a curl session,\n\
decoding string data in Python's default encoding at the time of the call.\n\
Corresponds to `curl_easy_getinfo`_ in libcurl.\n\
The ``getinfo`` method should not be called unless\n\
``perform`` has been called and finished.\n\
\n\
*option* is a constant corresponding to one of the\n\
``CURLINFO_*`` constants in libcurl. Most option constant names match\n\
the respective ``CURLINFO_*`` constant names with the ``CURLINFO_`` prefix\n\
removed, for example ``CURLINFO_CONTENT_TYPE`` is accessible as\n\
``pycurl.CONTENT_TYPE``. Exceptions to this rule are as follows:\n\
\n\
- ``CURLINFO_FILETIME`` is mapped as ``pycurl.INFO_FILETIME``\n\
- ``CURLINFO_COOKIELIST`` is mapped as ``pycurl.INFO_COOKIELIST``\n\
- ``CURLINFO_CERTINFO`` is mapped as ``pycurl.INFO_CERTINFO``\n\
- ``CURLINFO_RTSP_CLIENT_CSEQ`` is mapped as ``pycurl.INFO_RTSP_CLIENT_CSEQ``\n\
- ``CURLINFO_RTSP_CSEQ_RECV`` is mapped as ``pycurl.INFO_RTSP_CSEQ_RECV``\n\
- ``CURLINFO_RTSP_SERVER_CSEQ`` is mapped as ``pycurl.INFO_RTSP_SERVER_CSEQ``\n\
- ``CURLINFO_RTSP_SESSION_ID`` is mapped as ``pycurl.INFO_RTSP_SESSION_ID``\n\
\n\
The type of return value depends on the option, as follows:\n\
\n\
- Options documented by libcurl to return an integer value return a\n\
  Python ``int``.\n\
- Options documented by libcurl to return a floating point value\n\
  return a Python ``float``.\n\
- Options documented by libcurl to return a string value\n\
  return a Python ``str``.\n\
  The data returned by libcurl is decoded using the\n\
  default string encoding at the time of the call.\n\
  If the data cannot be decoded using the default encoding, ``UnicodeDecodeError``\n\
  is raised. Use :ref:`getinfo_raw <getinfo_raw>`\n\
  to retrieve the data as ``bytes`` in these\n\
  cases.\n\
- ``SSL_ENGINES`` and ``INFO_COOKIELIST`` return a list of strings.\n\
  The same encoding caveats apply; use :ref:`getinfo_raw <getinfo_raw>`\n\
  to retrieve the\n\
  data as a list of byte strings.\n\
- ``INFO_CERTINFO`` returns a list with one element\n\
  per certificate in the chain, starting with the leaf; each element is a\n\
  sequence of *(key, value)* tuples where both ``key`` and ``value`` are\n\
  strings. String encoding caveats apply; use :ref:`getinfo_raw <getinfo_raw>`\n\
  to retrieve\n\
  certificate data as byte strings.\n\
- For libcurl versions >= 7.45.0, ``CURLINFO_LASTSOCKET`` is aliased to\n\
  ``CURLINFO_ACTIVESOCKET`` to avoid unreliable results on some platforms.\n\
\n\
Example usage::\n\
\n\
    import pycurl\n\
    c = pycurl.Curl()\n\
    c.setopt(pycurl.OPT_CERTINFO, 1)\n\
    c.setopt(pycurl.URL, \"https://python.org\")\n\
    c.setopt(pycurl.FOLLOWLOCATION, 1)\n\
    c.perform()\n\
    print(c.getinfo(pycurl.HTTP_CODE))\n\
    # --> 200\n\
    print(c.getinfo(pycurl.EFFECTIVE_URL))\n\
    # --> \"https://www.python.org/\"\n\
    certinfo = c.getinfo(pycurl.INFO_CERTINFO)\n\
    print(certinfo)\n\
    # --> [(('Subject', 'C = AU, ST = Some-State, O = PycURL test suite,\n\
             CN = localhost'), ('Issuer', 'C = AU, ST = Some-State,\n\
             O = PycURL test suite, OU = localhost, CN = localhost'),\n\
            ('Version', '0'), ...)]\n\
\n\
\n\
Raises pycurl.error exception upon failure.\n\
\n\
.. _curl_easy_getinfo:\n\
    https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html";

PYCURL_INTERNAL const char curl_getinfo_raw_doc[] = "getinfo_raw(option) -> Result\n\
\n\
Extract and return information from a curl session,\n\
returning string data as byte strings.\n\
Corresponds to `curl_easy_getinfo`_ in libcurl.\n\
The ``getinfo_raw`` method should not be called unless\n\
``perform`` has been called and finished.\n\
\n\
*option* is a constant corresponding to one of the\n\
``CURLINFO_*`` constants in libcurl. Most option constant names match\n\
the respective ``CURLINFO_*`` constant names with the ``CURLINFO_`` prefix\n\
removed, for example ``CURLINFO_CONTENT_TYPE`` is accessible as\n\
``pycurl.CONTENT_TYPE``. Exceptions to this rule are as follows:\n\
\n\
- ``CURLINFO_FILETIME`` is mapped as ``pycurl.INFO_FILETIME``\n\
- ``CURLINFO_COOKIELIST`` is mapped as ``pycurl.INFO_COOKIELIST``\n\
- ``CURLINFO_CERTINFO`` is mapped as ``pycurl.INFO_CERTINFO``\n\
- ``CURLINFO_RTSP_CLIENT_CSEQ`` is mapped as ``pycurl.INFO_RTSP_CLIENT_CSEQ``\n\
- ``CURLINFO_RTSP_CSEQ_RECV`` is mapped as ``pycurl.INFO_RTSP_CSEQ_RECV``\n\
- ``CURLINFO_RTSP_SERVER_CSEQ`` is mapped as ``pycurl.INFO_RTSP_SERVER_CSEQ``\n\
- ``CURLINFO_RTSP_SESSION_ID`` is mapped as ``pycurl.INFO_RTSP_SESSION_ID``\n\
\n\
The type of return value depends on the option, as follows:\n\
\n\
- Options documented by libcurl to return an integer value return a\n\
  Python ``int``.\n\
- Options documented by libcurl to return a floating point value\n\
  return a Python ``float``.\n\
- Options documented by libcurl to return a string value\n\
  return a Python ``bytes`` instance.\n\
  The string contains whatever data libcurl returned.\n\
  Use :ref:`getinfo <getinfo>` to retrieve this data as a Unicode string.\n\
- ``SSL_ENGINES`` and ``INFO_COOKIELIST`` return a list of byte strings.\n\
  The same encoding caveats apply; use :ref:`getinfo <getinfo>` to retrieve the\n\
  data as a list of potentially Unicode strings.\n\
- ``INFO_CERTINFO`` returns a list with one element\n\
  per certificate in the chain, starting with the leaf; each element is a\n\
  sequence of *(key, value)* tuples where both ``key`` and ``value`` are\n\
  byte strings. String encoding caveats apply; use :ref:`getinfo <getinfo>`\n\
  to retrieve\n\
  certificate data as potentially Unicode strings.\n\
\n\
Example usage::\n\
\n\
    import pycurl\n\
    c = pycurl.Curl()\n\
    c.setopt(pycurl.OPT_CERTINFO, 1)\n\
    c.setopt(pycurl.URL, \"https://python.org\")\n\
    c.setopt(pycurl.FOLLOWLOCATION, 1)\n\
    c.perform()\n\
    print(c.getinfo_raw(pycurl.HTTP_CODE))\n\
    # --> 200\n\
    print(c.getinfo_raw(pycurl.EFFECTIVE_URL))\n\
    # --> b\"https://www.python.org/\"\n\
    certinfo = c.getinfo_raw(pycurl.INFO_CERTINFO)\n\
    print(certinfo)\n\
    # --> [((b'Subject', b'C = AU, ST = Some-State, O = PycURL test suite,\n\
             CN = localhost'), (b'Issuer', b'C = AU, ST = Some-State,\n\
             O = PycURL test suite, OU = localhost, CN = localhost'),\n\
            (b'Version', b'0'), ...)]\n\
\n\
\n\
Raises pycurl.error exception upon failure.\n\
\n\
*Added in version 7.43.0.2.*\n\
\n\
.. _curl_easy_getinfo:\n\
    https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html";

PYCURL_INTERNAL const char curl_multi_doc[] = "multi() -> CurlMulti | None\n\
\n\
Return the ``CurlMulti`` object this ``Curl`` handle currently belongs to,\n\
or ``None`` if it is not part of any ``CurlMulti``.";

PYCURL_INTERNAL const char curl_pause_doc[] = "pause(bitmask=PAUSE_ALL) -> None\n\
\n\
Pause or unpause a curl handle. ``bitmask`` defaults to ``PAUSE_ALL``.\n\
Pass a value such as ``PAUSE_RECV``, ``PAUSE_SEND``, or ``PAUSE_CONT`` to\n\
override.\n\
\n\
Corresponds to `curl_easy_pause`_ in libcurl. The argument should be\n\
derived from the ``PAUSE_RECV``, ``PAUSE_SEND``, ``PAUSE_ALL`` and\n\
``PAUSE_CONT`` constants.\n\
\n\
Raises pycurl.error exception upon failure.\n\
\n\
.. _curl_easy_pause: https://curl.haxx.se/libcurl/c/curl_easy_pause.html";

PYCURL_INTERNAL const char curl_perform_doc[] = "perform() -> None\n\
\n\
Perform a file transfer.\n\
\n\
Corresponds to `curl_easy_perform`_ in libcurl.\n\
\n\
Raises pycurl.error exception upon failure.\n\
\n\
.. _curl_easy_perform:\n\
    https://curl.haxx.se/libcurl/c/curl_easy_perform.html";

PYCURL_INTERNAL const char curl_perform_rb_doc[] = "perform_rb() -> response_body\n\
\n\
Perform a file transfer and return response body as a byte string.\n\
\n\
This method arranges for response body to be saved in a BytesIO\n\
instance, then invokes :ref:`perform <perform>`\n\
to perform the file transfer, then returns the value of the BytesIO\n\
instance which is a ``bytes`` instance. Errors during transfer raise\n\
``pycurl.error`` exceptions just like in :ref:`perform <perform>`.\n\
\n\
Use :ref:`perform_rs <perform_rs>` to retrieve response body as a ``str``.\n\
\n\
Raises ``pycurl.error`` exception upon failure.\n\
\n\
*Added in version 7.43.0.2.*";

PYCURL_INTERNAL const char curl_perform_rs_doc[] = "perform_rs() -> response_body\n\
\n\
Perform a file transfer and return response body as a string.\n\
\n\
This method arranges for response body to be saved in a BytesIO\n\
instance, then invokes :ref:`perform <perform>`\n\
to perform the file transfer, then decodes the response body in Python's\n\
default encoding and returns the decoded body as a Unicode string\n\
(``str`` instance). *Note:* decoding happens after the transfer finishes,\n\
thus an encoding error implies the transfer/network operation succeeded.\n\
\n\
Any transfer errors raise ``pycurl.error`` exception,\n\
just like in :ref:`perform <perform>`.\n\
\n\
Use :ref:`perform_rb <perform_rb>` to retrieve response body as a byte\n\
string (``bytes`` instance) without attempting to decode it.\n\
\n\
Raises ``pycurl.error`` exception upon failure.\n\
\n\
*Added in version 7.43.0.2.*";

PYCURL_INTERNAL const char curl_recv_doc[] = "recv(buffersize) -> data\n\
\n\
Receive data from a connection established with ``CONNECT_ONLY``.\n\
\n\
Receive up to *buffersize* bytes and return them as a ``bytes`` object.\n\
A returned empty ``bytes`` object indicates that the peer has closed the\n\
connection.\n\
\n\
Raises ``ValueError`` if *buffersize* is negative.\n\
\n\
Corresponds to `curl_easy_recv`_ in libcurl.\n\
\n\
Because the underlying socket is used in non-blocking mode internally,\n\
this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``\n\
when libcurl returns ``CURLE_AGAIN``.\n\
\n\
Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.\n\
\n\
.. _curl_easy_recv: https://curl.se/libcurl/c/curl_easy_recv.html";

PYCURL_INTERNAL const char curl_recv_into_doc[] = "recv_into(buffer[, nbytes]) -> nbytes\n\
\n\
Receive data from a connection established with ``CONNECT_ONLY`` into\n\
*buffer*.\n\
\n\
*buffer* must be a writable bytes-like object.\n\
\n\
If *nbytes* is ``0`` (the default), receive up to ``len(buffer)`` bytes.\n\
Otherwise, receive up to *nbytes* bytes. Returns the number of bytes\n\
received.\n\
\n\
Raises ``ValueError`` if *nbytes* is negative or larger than ``len(buffer)``.\n\
\n\
Corresponds to `curl_easy_recv`_ in libcurl.\n\
\n\
Because the underlying socket is used in non-blocking mode internally,\n\
this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``\n\
when libcurl returns ``CURLE_AGAIN``.\n\
\n\
Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.\n\
\n\
.. _curl_easy_recv: https://curl.se/libcurl/c/curl_easy_recv.html";

PYCURL_INTERNAL const char curl_reset_doc[] = "reset() -> None\n\
\n\
Reset all options set on curl handle to default values, but preserves\n\
live connections, session ID cache, DNS cache, cookies, and shares.\n\
\n\
Corresponds to `curl_easy_reset`_ in libcurl.\n\
\n\
.. _curl_easy_reset: https://curl.haxx.se/libcurl/c/curl_easy_reset.html";

PYCURL_INTERNAL const char curl_send_doc[] = "send(bytes) -> count\n\
\n\
Send data over a connection established with ``CONNECT_ONLY``.\n\
\n\
*data* may be any bytes-like object.\n\
\n\
Returns the number of bytes sent. If fewer than ``len(data)`` bytes are sent,\n\
the remaining data should be sent in a subsequent call.\n\
\n\
Corresponds to `curl_easy_send`_ in libcurl.\n\
\n\
Because the underlying socket is used in non-blocking mode internally,\n\
this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``\n\
when libcurl returns ``CURLE_AGAIN``.\n\
\n\
Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.\n\
\n\
.. _curl_easy_send: https://curl.se/libcurl/c/curl_easy_send.html";

PYCURL_INTERNAL const char curl_set_ca_certs_doc[] = "set_ca_certs() -> None\n\
\n\
Load ca certs from provided unicode string.\n\
\n\
Note that certificates will be added only when cURL starts new connection.";

PYCURL_INTERNAL const char curl_setopt_doc[] = "setopt(option, value) -> None\n\
\n\
Set curl session option. Corresponds to `curl_easy_setopt`_ in libcurl.\n\
\n\
*option* specifies which option to set. PycURL defines constants\n\
corresponding to ``CURLOPT_*`` constants in libcurl, except that\n\
the ``CURLOPT_`` prefix is removed. For example, ``CURLOPT_URL`` is\n\
exposed in PycURL as ``pycurl.URL``, with some exceptions as detailed below.\n\
For convenience, ``CURLOPT_*``\n\
constants are also exposed on the Curl objects themselves::\n\
\n\
    import pycurl\n\
    c = pycurl.Curl()\n\
    c.setopt(pycurl.URL, \"http://www.python.org/\")\n\
    # Same as:\n\
    c.setopt(c.URL, \"http://www.python.org/\")\n\
\n\
The following are exceptions to option constant naming convention:\n\
\n\
- ``CURLOPT_FILETIME`` is mapped as ``pycurl.OPT_FILETIME``\n\
- ``CURLOPT_CERTINFO`` is mapped as ``pycurl.OPT_CERTINFO``\n\
- ``CURLOPT_COOKIELIST`` is mapped as ``pycurl.COOKIELIST``\n\
  and, as of PycURL 7.43.0.2, also as ``pycurl.OPT_COOKIELIST``\n\
- ``CURLOPT_RTSP_CLIENT_CSEQ`` is mapped as ``pycurl.OPT_RTSP_CLIENT_CSEQ``\n\
- ``CURLOPT_RTSP_REQUEST`` is mapped as ``pycurl.OPT_RTSP_REQUEST``\n\
- ``CURLOPT_RTSP_SERVER_CSEQ`` is mapped as ``pycurl.OPT_RTSP_SERVER_CSEQ``\n\
- ``CURLOPT_RTSP_SESSION_ID`` is mapped as ``pycurl.OPT_RTSP_SESSION_ID``\n\
- ``CURLOPT_RTSP_STREAM_URI`` is mapped as ``pycurl.OPT_RTSP_STREAM_URI``\n\
- ``CURLOPT_RTSP_TRANSPORT`` is mapped as ``pycurl.OPT_RTSP_TRANSPORT``\n\
\n\
*value* specifies the value to set the option to. Different options accept\n\
values of different types:\n\
\n\
- Options specified by `curl_easy_setopt`_ as accepting ``1`` or an\n\
  integer value accept Python integers and booleans::\n\
\n\
    c.setopt(pycurl.FOLLOWLOCATION, True)\n\
    c.setopt(pycurl.FOLLOWLOCATION, 1)\n\
\n\
- Options specified as accepting strings by ``curl_easy_setopt`` accept\n\
  ``bytes`` and ``str`` with ASCII code points only.\n\
  For more information, please refer to :ref:`unicode`. Example::\n\
\n\
    c.setopt(pycurl.URL, \"http://www.python.org/\")\n\
    c.setopt(pycurl.URL, b\"http://www.python.org/\")\n\
\n\
- ``HTTP200ALIASES``, ``HTTPHEADER``, ``POSTQUOTE``, ``PREQUOTE``,\n\
  ``PROXYHEADER`` and\n\
  ``QUOTE`` accept a list or tuple of strings. The same rules apply to these\n\
  strings as do to string option values. Example::\n\
\n\
    c.setopt(pycurl.HTTPHEADER, [\"Accept:\"])\n\
    c.setopt(pycurl.HTTPHEADER, (\"Accept:\",))\n\
\n\
- ``READDATA`` accepts a file object or any Python object which has\n\
  a ``read`` method. ``READDATA`` is emulated in PycURL via ``READFUNCTION``.\n\
  The file should generally be opened in binary mode. Example::\n\
\n\
    f = open('file.txt', 'rb')\n\
    c.setopt(c.READDATA, f)\n\
\n\
- ``WRITEDATA`` and ``WRITEHEADER`` accept a file object or any Python\n\
  object which has a ``write`` method. ``WRITEDATA`` is emulated in PycURL\n\
  via ``WRITEFUNCTION``.\n\
  The file should generally be opened in binary mode. Example::\n\
\n\
    f = open('/dev/null', 'wb')\n\
    c.setopt(c.WRITEDATA, f)\n\
\n\
- ``*FUNCTION`` options accept a function. Supported callbacks are documented\n\
  in :ref:`callbacks`. Example::\n\
\n\
    import io\n\
    b = io.BytesIO()\n\
    c.setopt(pycurl.WRITEFUNCTION, b.write)\n\
\n\
- ``SHARE`` option accepts a :ref:`curlshareobject`.\n\
\n\
- ``STDERR`` option is not currently supported.\n\
\n\
It is possible to set integer options - and only them - that PycURL does\n\
not know about by using the numeric value of the option constant directly.\n\
For example, ``pycurl.VERBOSE`` has the value 42, and may be set as follows::\n\
\n\
    c.setopt(42, 1)\n\
\n\
*setopt* can reset some options to their default value, performing the job of\n\
:py:meth:`pycurl.Curl.unsetopt`, if ``None`` is passed\n\
for the option value. The following two calls are equivalent::\n\
\n\
    c.setopt(c.URL, None)\n\
    c.unsetopt(c.URL)\n\
\n\
Raises TypeError when the option value is not of a type accepted by the\n\
respective option, and pycurl.error exception when libcurl rejects the\n\
option or its value.\n\
\n\
.. _curl_easy_setopt: https://curl.haxx.se/libcurl/c/curl_easy_setopt.html";

PYCURL_INTERNAL const char curl_setopt_string_doc[] = "setopt_string(option, value) -> None\n\
\n\
Set curl session option to a string value.\n\
\n\
This method allows setting string options that are not officially supported\n\
by PycURL, for example because they did not exist when the version of PycURL\n\
being used was released.\n\
:py:meth:`pycurl.Curl.setopt` should be used for setting options that\n\
PycURL knows about.\n\
\n\
**Warning:** No checking is performed that *option* does, in fact,\n\
expect a string value. Using this method incorrectly can crash the program\n\
and may lead to a security vulnerability.\n\
Furthermore, it is on the application to ensure that the *value* object\n\
does not get garbage collected while libcurl is using it.\n\
libcurl copies most string options but not all; one option whose value\n\
is not copied by libcurl is `CURLOPT_POSTFIELDS`_.\n\
\n\
*option* would generally need to be given as an integer literal rather than\n\
a symbolic constant.\n\
\n\
*value* can be a binary string or a Unicode string using ASCII code points,\n\
same as with string options given to PycURL elsewhere.\n\
\n\
Example setting URL via ``setopt_string``::\n\
\n\
    import pycurl\n\
    c = pycurl.Curl()\n\
    c.setopt_string(10002, \"http://www.python.org/\")\n\
\n\
.. _CURLOPT_POSTFIELDS: https://curl.haxx.se/libcurl/c/CURLOPT_POSTFIELDS.html";

PYCURL_INTERNAL const char curl_share_doc[] = "share() -> CurlShare | None\n\
\n\
Return the ``CurlShare`` object that this ``Curl`` handle is currently\n\
associated with, or ``None`` if it is not part of any ``CurlShare``.";

PYCURL_INTERNAL const char curl_unpause_doc[] = "unpause() -> None\n\
\n\
Unpause a curl handle.\n\
\n\
Equivalent to ``pause(PAUSE_CONT)``.\n\
\n\
Corresponds to `curl_easy_pause`_ in libcurl.\n\
\n\
Raises pycurl.error exception upon failure.\n\
\n\
.. _curl_easy_pause: https://curl.haxx.se/libcurl/c/curl_easy_pause.html";

PYCURL_INTERNAL const char curl_unsetopt_doc[] = "unsetopt(option) -> None\n\
\n\
Reset curl session option to its default value.\n\
\n\
Only some curl options may be reset via this method.\n\
\n\
libcurl does not provide a general way to reset a single option to its default value;\n\
:py:meth:`pycurl.Curl.reset` resets all options to their default values,\n\
otherwise :py:meth:`pycurl.Curl.setopt` must be called with whatever value\n\
is the default. For convenience, PycURL provides this unsetopt method\n\
to reset some of the options to their default values.\n\
\n\
Raises pycurl.error exception on failure.\n\
\n\
``c.unsetopt(option)`` is equivalent to ``c.setopt(option, None)``.";

PYCURL_INTERNAL const char curl_ws_close_doc[] = "ws_close(code=None, reason=None, encoding='utf-8') -> count\n\
\n\
Send a WebSocket close frame. In detached mode this requires\n\
``CONNECT_ONLY=2``; inside an active ``WRITEFUNCTION`` callback it may\n\
also be used to send a blocking reply.\n\
\n\
Builds an RFC 6455 §5.5.1 close payload — an optional 2-byte big-endian\n\
status *code* followed by an optional UTF-8 *reason* — and sends it as\n\
a ``WS_CLOSE`` control frame. Prefer this over\n\
``ws_send(bytes, WS_CLOSE)``: the payload format is non-obvious.\n\
\n\
*code* is the WebSocket close status code. Omitted (``None``) sends an\n\
empty close payload. When specified, must be a valid wire code per RFC\n\
6455 §7.4.1: ``1000`` (normal), ``1001`` (going away), ``1002``, ``1003``,\n\
``1007``-``1014``, or a private-use value in ``3000..4999``. Codes\n\
``1004``, ``1005``, ``1006``, ``1015`` are RFC-forbidden to send and\n\
rejected.\n\
\n\
*reason* may be a ``str`` or any bytes-like object. ``str`` is encoded\n\
with *encoding* (UTF-8 by default). The resulting bytes must be valid\n\
UTF-8 on the wire; invalid UTF-8 raises ``UnicodeDecodeError``,\n\
non-encodable input raises ``UnicodeEncodeError``. ``reason`` without\n\
``code`` raises ``ValueError``. The combined payload (2-byte code +\n\
reason) must not exceed 125 bytes (RFC 6455 §5.5).\n\
\n\
Returns the number of bytes accepted by libcurl.\n\
\n\
Same blocking / non-blocking semantics as :py:meth:`ws_send`. Calls\n\
from other threads while ``perform()`` is running are rejected.\n\
\n\
Corresponds to `curl_ws_send`_ with ``CURLWS_CLOSE``. Requires libcurl\n\
7.86.0 or later. Raises ``pycurl.error`` for libcurl failures other\n\
than ``CURLE_AGAIN``.\n\
\n\
.. _curl_ws_send: https://curl.se/libcurl/c/curl_ws_send.html";

PYCURL_INTERNAL const char curl_ws_meta_doc[] = "ws_meta() -> WsFrame or None\n\
\n\
Return a snapshot of the current WebSocket frame's metadata.\n\
\n\
This is a callback-context helper. It is intended to be called from\n\
inside an active ``WRITEFUNCTION`` callback on a WebSocket transfer,\n\
where it returns a ``WsFrame`` namedtuple with the metadata of the\n\
chunk currently being delivered.\n\
\n\
Outside that context — including when used in detached mode\n\
(``CONNECT_ONLY=2``), after ``perform()`` has returned, or on a\n\
non-WebSocket transfer — libcurl's ``curl_ws_meta()`` returns ``NULL``\n\
and PycURL maps that ``NULL`` to Python ``None``. No exception is\n\
raised; callers can use ``if c.ws_meta() is None`` to probe context\n\
validity.\n\
\n\
In detached mode, prefer the metadata returned directly by\n\
``ws_recv()`` / ``ws_recv_into()`` rather than a separate ``ws_meta()``\n\
call.\n\
\n\
Corresponds to `curl_ws_meta`_ in libcurl. Requires libcurl 7.86.0 or\n\
later.\n\
\n\
.. _curl_ws_meta: https://curl.se/libcurl/c/curl_ws_meta.html";

PYCURL_INTERNAL const char curl_ws_recv_doc[] = "ws_recv(buffersize) -> (data, meta)\n\
\n\
Receive a WebSocket frame chunk on a connection established with\n\
``CONNECT_ONLY=2``.\n\
\n\
Receive up to *buffersize* bytes. Returns a 2-tuple ``(data, meta)``\n\
where *data* is a ``bytes`` object containing the received payload chunk\n\
and *meta* is a ``WsFrame`` namedtuple carrying the per-frame metadata\n\
returned by libcurl for this call (``age``, ``flags``, ``offset``,\n\
``bytesleft``, ``len``).\n\
\n\
A single call may return only part of a frame's payload: check\n\
``meta.bytesleft`` to decide whether to loop. Reassembly of fragmented\n\
messages is the caller's responsibility.\n\
\n\
A *buffersize* of ``0`` performs a zero-length ``curl_ws_recv`` call.\n\
This returns ``(b\"\", meta)`` so callers can inspect frame metadata\n\
without consuming payload bytes. Frames with empty payload are consumed\n\
by this action.\n\
\n\
Raises ``ValueError`` if *buffersize* is negative.\n\
\n\
Corresponds to `curl_ws_recv`_ in libcurl. Requires libcurl 7.86.0 or\n\
later.\n\
\n\
Because the underlying socket is used in non-blocking mode internally,\n\
this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``\n\
when libcurl returns ``CURLE_AGAIN``.\n\
\n\
Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.\n\
\n\
.. _curl_ws_recv: https://curl.se/libcurl/c/curl_ws_recv.html";

PYCURL_INTERNAL const char curl_ws_recv_into_doc[] = "ws_recv_into(buffer[, nbytes]) -> (nbytes, meta)\n\
\n\
Receive a WebSocket frame chunk on a connection established with\n\
``CONNECT_ONLY=2`` into a caller-owned writable *buffer*.\n\
\n\
*buffer* must be a writable bytes-like object (e.g. ``bytearray``,\n\
``memoryview``, ``array.array``).\n\
\n\
If *nbytes* is ``0`` (the default), receive up to ``len(buffer)`` bytes.\n\
Otherwise, receive up to *nbytes* bytes.\n\
\n\
Returns a 2-tuple ``(nbytes, meta)`` where *nbytes* is the number of\n\
bytes written into *buffer* and *meta* is a ``WsFrame`` namedtuple with\n\
the per-frame metadata returned by libcurl for this call.\n\
\n\
Raises ``ValueError`` if *nbytes* is negative or larger than\n\
``len(buffer)``.\n\
\n\
If *buffer* has length ``0``, this performs a zero-length\n\
``curl_ws_recv`` call and returns ``(0, meta)`` so callers can inspect\n\
frame metadata without consuming payload bytes. Frames with empty\n\
payload are consumed by this action.\n\
\n\
Corresponds to `curl_ws_recv`_ in libcurl. Requires libcurl 7.86.0 or\n\
later.\n\
\n\
Because the underlying socket is used in non-blocking mode internally,\n\
this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``\n\
when libcurl returns ``CURLE_AGAIN``.\n\
\n\
Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.\n\
\n\
.. _curl_ws_recv: https://curl.se/libcurl/c/curl_ws_recv.html";

PYCURL_INTERNAL const char curl_ws_send_doc[] = "ws_send(data, flags=None, fragsize=0, encoding='utf-8') -> count\n\
\n\
Send a WebSocket frame. In detached mode this requires ``CONNECT_ONLY=2``;\n\
inside an active ``WRITEFUNCTION`` callback it may also be used to send\n\
a blocking reply.\n\
\n\
*data* may be a ``str`` or any bytes-like object. ``str`` is encoded\n\
with *encoding* (UTF-8 by default); characters that are not\n\
representable in *encoding* raise ``UnicodeEncodeError``. Passing\n\
``None`` raises ``TypeError`` — use ``b\"\"`` for an empty payload.\n\
\n\
*flags* is a bitmask built from the frame-type constants ``WS_TEXT``,\n\
``WS_BINARY``, ``WS_CONT``, ``WS_CLOSE``, ``WS_PING``, ``WS_PONG``. When\n\
``flags`` is omitted (``None``), the frame type is inferred: ``str`` ->\n\
``WS_TEXT``, bytes-like -> ``WS_BINARY``. Explicit flags win. ``str`` +\n\
``WS_BINARY`` and ``str`` + ``WS_CLOSE`` raise ``TypeError`` (use\n\
:py:meth:`ws_close` for close frames, or pass bytes-like data).\n\
\n\
*fragsize* maps to ``curl_ws_send``'s ``fragsize`` parameter; ``0``\n\
means \"whole message\". ``WS_OFFSET`` is the companion flag for\n\
multi-call fragmented sends; see the libcurl docs for the rules.\n\
\n\
Returns the number of bytes accepted by libcurl.\n\
\n\
Raises ``BlockingIOError`` (``errno=EAGAIN``) in detached mode when\n\
libcurl returns ``CURLE_AGAIN``. Inside a ``WRITEFUNCTION`` callback\n\
libcurl treats the call as blocking and returns only once the frame has\n\
been fully sent; ``BlockingIOError`` does not apply. Calls from other\n\
threads while ``perform()`` is running are rejected.\n\
\n\
Corresponds to `curl_ws_send`_ in libcurl. Requires libcurl 7.86.0 or\n\
later. Raises ``pycurl.error`` for libcurl failures other than\n\
``CURLE_AGAIN``.\n\
\n\
.. _curl_ws_send: https://curl.se/libcurl/c/curl_ws_send.html";

PYCURL_INTERNAL const char multi_doc[] = "CurlMulti(close_handles=False) -> New CurlMulti object\n\
\n\
Creates a new :ref:`curlmultiobject` which corresponds to\n\
a ``CURLM`` handle in libcurl.\n\
\n\
The ``CurlMulti`` object can be used as a context manager. Exiting the\n\
context calls ``close()``.\n\
\n\
Example::\n\
\n\
    with pycurl.CurlMulti(close_handles=True) as m:\n\
        m.add_handle(curl)\n\
        # perform multi operations\n\
    # easy handles have been removed and closed\n\
\n\
:param bool close_handles:\n\
    If ``False`` (default), easy handles added to the multi handle\n\
    are removed from the multi handle when ``close()`` is called\n\
    or when exiting the context manager, but remain open and must\n\
    be managed by the caller.\n\
\n\
    If ``True``, easy handles are removed from the multi handle when\n\
    ``close()`` is called or when exiting the context manager, and\n\
    are then automatically closed.\n\
\n\
    In all cases, easy handles are not closed when they are removed\n\
    individually from the multi handle.";

PYCURL_INTERNAL const char multi_add_handle_doc[] = "add_handle(Curl object) -> None\n\
\n\
Corresponds to `curl_multi_add_handle`_ in libcurl. This method adds an\n\
existing and valid Curl object to the CurlMulti object.\n\
\n\
*Changed in version 7.43.0.2:* add_handle now ensures that the Curl object\n\
is not garbage collected while it is being used by a CurlMulti object.\n\
Previously application had to maintain an outstanding reference to the Curl\n\
object to keep it from being garbage collected.\n\
\n\
.. _curl_multi_add_handle:\n\
    https://curl.haxx.se/libcurl/c/curl_multi_add_handle.html";

PYCURL_INTERNAL const char multi_assign_doc[] = "assign(sock_fd, object) -> None\n\
\n\
Creates an association in the multi handle between the given socket and\n\
a private object in the application.\n\
Corresponds to `curl_multi_assign`_ in libcurl.\n\
The multi handle keeps a strong reference to the assigned object.\n\
\n\
``assign()`` may be called from inside the ``M_SOCKETFUNCTION`` callback;\n\
this is the typical place to attach per-socket state. The new value takes\n\
effect for *future* callbacks for that socket -- the ``socketp`` argument\n\
already passed to the in-flight callback is not mutated.\n\
\n\
If ``object`` is ``None``, clears any association for the socket.\n\
For convenience, :py:meth:`pycurl.CurlMulti.unassign` is equivalent to\n\
``multi.assign(sock_fd, None)``.\n\
\n\
.. _curl_multi_assign: https://curl.haxx.se/libcurl/c/curl_multi_assign.html";

PYCURL_INTERNAL const char multi_close_doc[] = "close() -> None\n\
\n\
Corresponds to `curl_multi_cleanup`_ in libcurl. This method is\n\
automatically called by pycurl when a ``CurlMulti`` object no longer has\n\
any references to it, but can also be called explicitly.\n\
\n\
It removes all easy handles from the multi handle before closing the\n\
multi handle.\n\
\n\
If the ``CurlMulti`` was constructed with ``close_handles=True``, the\n\
removed easy handles are also closed after removal. Otherwise, they\n\
remain open.\n\
\n\
``close()`` may not be called while ``perform()`` or ``socket_action()``\n\
is on the stack (for example, from inside ``M_SOCKETFUNCTION`` or\n\
``M_TIMERFUNCTION``); doing so raises ``pycurl.error``.\n\
\n\
.. _curl_multi_cleanup:\n\
    https://curl.haxx.se/libcurl/c/curl_multi_cleanup.html";

PYCURL_INTERNAL const char multi_closed_doc[] = "closed() -> bool\n\
\n\
Return ``True`` if the ``CurlMulti`` object was already closed, ``False`` otherwise.";

PYCURL_INTERNAL const char multi_contains_doc[] = "__contains__(Curl object) -> bool\n\
\n\
Implements the ``in`` operator for CurlMulti objects. This method returns\n\
``True`` if the given Curl object is currently added to the CurlMulti\n\
object, and ``False`` otherwise.\n\
\n\
Raises ``TypeError`` if the argument is not a Curl object.";

PYCURL_INTERNAL const char multi_fdset_doc[] = "fdset() -> tuple of lists with active file descriptors, readable, writeable, exceptions\n\
\n\
Returns a tuple of three lists that can be passed to the select.select() method.\n\
\n\
Corresponds to `curl_multi_fdset`_ in libcurl. This method extracts the\n\
file descriptor information from a CurlMulti object. The returned lists can\n\
be used with the ``select`` module to poll for events.\n\
\n\
Example usage::\n\
\n\
    import pycurl\n\
    c = pycurl.Curl()\n\
    c.setopt(pycurl.URL, \"https://curl.haxx.se\")\n\
    m = pycurl.CurlMulti()\n\
    m.add_handle(c)\n\
    _, num_handles = m.perform()\n\
    while num_handles:\n\
        apply(select.select, m.fdset() + (1,))\n\
        _, num_handles = m.perform()\n\
.. _curl_multi_fdset:\n\
    https://curl.haxx.se/libcurl/c/curl_multi_fdset.html";

PYCURL_INTERNAL const char multi_info_read_doc[] = "info_read([max_objects]) -> tuple(number of queued messages, a list of successful objects, a list of failed objects)\n\
\n\
Corresponds to the `curl_multi_info_read`_ function in libcurl.\n\
\n\
This method extracts at most *max* messages from the multi stack and returns\n\
them in two lists. The first list contains the handles which completed\n\
successfully and the second list contains a tuple *(curl object, curl error\n\
number, curl error message)* for each failed curl object. The curl error\n\
message is returned as a Python string which is decoded from the curl error\n\
string using the `surrogateescape`_ error handler. The number of\n\
queued messages after this method has been called is also returned.\n\
\n\
.. _curl_multi_info_read:\n\
    https://curl.haxx.se/libcurl/c/curl_multi_info_read.html\n\
\n\
.. _surrogateescape:\n\
    https://www.python.org/dev/peps/pep-0383/";

PYCURL_INTERNAL const char multi_perform_doc[] = "perform() -> tuple of status and the number of active Curl objects\n\
\n\
Corresponds to `curl_multi_perform`_ in libcurl.\n\
\n\
This method raises an exception if ``curl_multi_perform`` returns a value other than\n\
``CURLM_OK``.\n\
\n\
.. _curl_multi_perform:\n\
    https://curl.haxx.se/libcurl/c/curl_multi_perform.html";

PYCURL_INTERNAL const char multi_remove_handle_doc[] = "remove_handle(Curl object) -> None\n\
\n\
Corresponds to `curl_multi_remove_handle`_ in libcurl. This method\n\
removes an existing and valid Curl object from the CurlMulti object.\n\
\n\
.. _curl_multi_remove_handle:\n\
    https://curl.haxx.se/libcurl/c/curl_multi_remove_handle.html";

PYCURL_INTERNAL const char multi_select_doc[] = "select([timeout]) -> number of ready file descriptors or 0 on timeout\n\
\n\
Returns result from doing a select() on the curl multi file descriptor\n\
with the given timeout.\n\
\n\
This is a convenience function which simplifies the combined use of\n\
``fdset()`` and the ``select`` module.\n\
\n\
Example usage::\n\
\n\
    import pycurl\n\
    c = pycurl.Curl()\n\
    c.setopt(pycurl.URL, \"https://curl.haxx.se\")\n\
    m = pycurl.CurlMulti()\n\
    m.add_handle(c)\n\
    _, num_handles = m.perform()\n\
    while num_handles:\n\
        ret = m.select(1.0)\n\
        if ret == 0:  continue\n\
        _, num_handles = m.perform()";

PYCURL_INTERNAL const char multi_setopt_doc[] = "setopt(option, value) -> None\n\
\n\
Set curl multi option. Corresponds to `curl_multi_setopt`_ in libcurl.\n\
\n\
*option* specifies which option to set. PycURL defines constants\n\
corresponding to ``CURLMOPT_*`` constants in libcurl, except that\n\
the ``CURLMOPT_`` prefix is replaced with ``M_`` prefix.\n\
For example, ``CURLMOPT_PIPELINING`` is\n\
exposed in PycURL as ``pycurl.M_PIPELINING``. For convenience, ``CURLMOPT_*``\n\
constants are also exposed on CurlMulti objects::\n\
\n\
    import pycurl\n\
    m = pycurl.CurlMulti()\n\
    m.setopt(pycurl.M_PIPELINING, 1)\n\
    # Same as:\n\
    m.setopt(m.M_PIPELINING, 1)\n\
\n\
*value* specifies the value to set the option to. Different options accept\n\
values of different types:\n\
\n\
- Options specified by `curl_multi_setopt`_ as accepting ``1`` or an\n\
  integer value accept Python integers and booleans::\n\
\n\
    m.setopt(pycurl.M_PIPELINING, True)\n\
    m.setopt(pycurl.M_PIPELINING, 1)\n\
\n\
- ``*FUNCTION`` options accept a function. Supported callbacks are\n\
  ``CURLMOPT_SOCKETFUNCTION`` and ``CURLMOPT_TIMERFUNCTION``; see the\n\
  ``SOCKETFUNCTION`` and ``TIMERFUNCTION`` sections of the\n\
  :ref:`callbacks <callbacks>` page. ``CURLMOPT_SOCKETDATA`` and\n\
  ``CURLMOPT_TIMERDATA`` are reserved by PycURL (set internally to the\n\
  ``CurlMulti`` instance) and cannot be set from Python.\n\
\n\
Raises TypeError when the option value is not of a type accepted by the\n\
respective option, and pycurl.error exception when libcurl rejects the\n\
option or its value.\n\
\n\
.. _curl_multi_setopt: https://curl.haxx.se/libcurl/c/curl_multi_setopt.html";

PYCURL_INTERNAL const char multi_socket_action_doc[] = "socket_action(sock_fd, ev_bitmask) -> (result, num_running_handles)\n\
\n\
Returns result from doing a socket_action() on the curl multi file descriptor\n\
with the given timeout.\n\
Corresponds to `curl_multi_socket_action`_ in libcurl.\n\
\n\
PycURL exposes the relevant constants as ``pycurl.CSELECT_IN``,\n\
``CSELECT_OUT``, ``CSELECT_ERR`` (for *ev_bitmask*) and\n\
``pycurl.SOCKET_TIMEOUT`` (for *sock_fd*); refer to the\n\
`curl_multi_socket_action`_ docs for their meaning.\n\
\n\
The return value is a two-element tuple. The first element is the return\n\
value of the underlying ``curl_multi_socket_action`` function, and it is\n\
always zero (``CURLE_OK``) because any other return value would cause\n\
``socket_action`` to raise an exception. The second element is the number of\n\
running easy handles within this multi handle. When the number of running\n\
handles reaches zero, all transfers have completed. Note that if the number\n\
of running handles has decreased by one compared to the previous invocation,\n\
this is not mean the handle corresponding to the ``sock_fd`` provided as\n\
the argument to this function was the completed handle.\n\
\n\
.. _curl_multi_socket_action: https://curl.haxx.se/libcurl/c/curl_multi_socket_action.html";

PYCURL_INTERNAL const char multi_socket_all_doc[] = "socket_all() -> tuple\n\
\n\
Returns result from doing a socket_all() on the curl multi file descriptor\n\
with the given timeout.";

PYCURL_INTERNAL const char multi_timeout_doc[] = "timeout() -> int\n\
\n\
Returns how long to wait for action before proceeding, in milliseconds, or\n\
``-1`` if libcurl has no timeout currently set.\n\
Corresponds to `curl_multi_timeout`_ in libcurl.\n\
\n\
.. _curl_multi_timeout: https://curl.haxx.se/libcurl/c/curl_multi_timeout.html";

PYCURL_INTERNAL const char multi_unassign_doc[] = "unassign(sock_fd) -> None\n\
\n\
Clears the association in the multi handle for the given socket,\n\
releasing the previously assigned object.\n\
\n\
``multi.unassign(sock_fd)`` is equivalent to\n\
:py:meth:`multi.assign(sock_fd, None) <pycurl.CurlMulti.assign>`.\n\
Like ``assign()``, it may be called from inside the ``M_SOCKETFUNCTION``.";

PYCURL_INTERNAL const char pycurl_global_cleanup_doc[] = "global_cleanup() -> None\n\
\n\
Cleanup curl environment.\n\
\n\
Corresponds to `curl_global_cleanup`_ in libcurl.\n\
\n\
.. _curl_global_cleanup: https://curl.haxx.se/libcurl/c/curl_global_cleanup.html";

PYCURL_INTERNAL const char pycurl_global_init_doc[] = "global_init(option) -> None\n\
\n\
Initialize curl environment.\n\
\n\
*option* is one of the constants pycurl.GLOBAL_SSL, pycurl.GLOBAL_WIN32,\n\
pycurl.GLOBAL_ALL, pycurl.GLOBAL_NOTHING, pycurl.GLOBAL_DEFAULT.\n\
\n\
Corresponds to `curl_global_init`_ in libcurl.\n\
\n\
.. _curl_global_init: https://curl.haxx.se/libcurl/c/curl_global_init.html";

PYCURL_INTERNAL const char pycurl_module_doc[] = "This module implements an interface to the cURL library.\n\
\n\
Types:\n\
\n\
Curl() -> New object.  Create a new curl object.\n\
CurlMulti() -> New object.  Create a new curl multi object.\n\
CurlShare() -> New object.  Create a new curl share object.\n\
\n\
Functions:\n\
\n\
global_init(option) -> None.  Initialize curl environment.\n\
global_cleanup() -> None.  Cleanup curl environment.\n\
version_info() -> tuple.  Return version information.";

PYCURL_INTERNAL const char pycurl_version_info_doc[] = "version_info() -> tuple\n\
\n\
Returns a 12-tuple with the version info.\n\
\n\
Corresponds to `curl_version_info`_ in libcurl. Returns a tuple of\n\
information which is similar to the ``curl_version_info_data`` struct\n\
returned by ``curl_version_info()`` in libcurl.\n\
\n\
Example usage::\n\
\n\
    >>> import pycurl\n\
    >>> pycurl.version_info()\n\
    (3, '7.33.0', 467200, 'amd64-portbld-freebsd9.1', 33436, 'OpenSSL/0.9.8x',\n\
    0, '1.2.7', ('dict', 'file', 'ftp', 'ftps', 'gopher', 'http', 'https',\n\
    'imap', 'imaps', 'pop3', 'pop3s', 'rtsp', 'smtp', 'smtps', 'telnet',\n\
    'tftp'), None, 0, None)\n\
\n\
.. _curl_version_info: https://curl.haxx.se/libcurl/c/curl_version_info.html";

PYCURL_INTERNAL const char share_doc[] = "CurlShare(detach_on_close=True) -> New CurlShare object\n\
\n\
Creates a new :ref:`curlshareobject` which corresponds to a\n\
``CURLSH`` handle in libcurl. CurlShare objects is what you pass as an\n\
argument to the SHARE option on :ref:`Curl objects <curlobject>`.\n\
\n\
The ``CurlShare`` object can be used as a context manager. Exiting the\n\
context calls ``close()``.\n\
\n\
When a ``CurlShare`` is closed, its behavior depends on the value of\n\
``detach_on_close``.\n\
\n\
Example::\n\
\n\
    with pycurl.CurlShare(detach_on_close=True) as s:\n\
        curl.setopt(pycurl.SHARE, s)\n\
        # perform operations\n\
    # the CurlShare is closed and the Curl object has been detached\n\
\n\
:param bool detach_on_close:\n\
    Controls how associated :ref:`Curl objects <curlobject>` are handled\n\
    when the ``CurlShare`` is closed.\n\
\n\
    If ``True`` (default), all live ``Curl`` objects associated with the\n\
    share are automatically detached when ``close()`` is called or when\n\
    exiting the context manager. Detaching clears the ``SHARE`` option on\n\
    each ``Curl`` object, but does **not** close them. The caller remains\n\
    responsible for managing the lifetime of the ``Curl`` objects.\n\
\n\
    If ``False``, calling ``close()`` (or exiting the context manager)\n\
    while there are still ``Curl`` objects associated with the share\n\
    raises an exception. In this mode, the caller must explicitly remove\n\
    or close all associated ``Curl`` objects before closing the\n\
    ``CurlShare``.\n\
\n\
.. warning::\n\
\n\
   Detaching ``Curl`` objects from a ``CurlShare`` is **not thread-safe**\n\
   with respect to those ``Curl`` objects.\n\
\n\
   The caller is responsible for ensuring proper synchronization when\n\
   using ``CurlShare`` and ``Curl`` objects across multiple threads.";

PYCURL_INTERNAL const char share_close_doc[] = "close() -> None\n\
----------------\n\
\n\
Close shared handle.\n\
\n\
Corresponds to `curl_share_cleanup`_ in libcurl. This method is\n\
automatically called by pycurl when a ``CurlShare`` object no longer has\n\
any references to it, but can also be called explicitly.\n\
\n\
The behavior of ``close()`` depends on the ``detach_on_close`` setting\n\
of the ``CurlShare``:\n\
\n\
- If ``detach_on_close`` is ``True`` (default), all associated\n\
  :ref:`Curl objects <curlobject>` are first detached from the share\n\
  before the share handle is closed. Detaching clears the ``SHARE``\n\
  option on each ``Curl`` object but does not close them.\n\
\n\
- If ``detach_on_close`` is ``False``, calling ``close()`` while there\n\
  are still associated ``Curl`` objects raises ``pycurl.error`` and the\n\
  share handle is not closed.\n\
\n\
.. warning::\n\
\n\
   Automatic detachment performed when ``detach_on_close`` is ``True``\n\
   is **not thread-safe** with respect to the associated ``Curl``\n\
   objects. The caller must ensure that no other thread is operating on\n\
   those ``Curl`` objects while ``close()`` is executing.\n\
\n\
.. _curl_share_cleanup:\n\
    https://curl.haxx.se/libcurl/c/curl_share_cleanup.html";

PYCURL_INTERNAL const char share_closed_doc[] = "closed() -> bool\n\
\n\
Return ``True`` if the ``CurlShare`` object was already closed, ``False`` otherwise.";

PYCURL_INTERNAL const char share_setopt_doc[] = "setopt(option, value) -> None\n\
\n\
Set curl share option.\n\
\n\
Corresponds to `curl_share_setopt`_ in libcurl, where *option* is\n\
specified with the ``CURLSHOPT_*`` constants in libcurl, except that the\n\
``CURLSHOPT_`` prefix has been changed to ``SH_``. Currently, *value* must be\n\
one of: ``LOCK_DATA_COOKIE``, ``LOCK_DATA_DNS``, ``LOCK_DATA_SSL_SESSION`` or\n\
``LOCK_DATA_CONNECT``.\n\
\n\
Example usage::\n\
\n\
    import pycurl\n\
    curl = pycurl.Curl()\n\
    s = pycurl.CurlShare()\n\
    s.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_COOKIE)\n\
    s.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_DNS)\n\
    curl.setopt(pycurl.URL, 'https://curl.haxx.se')\n\
    curl.setopt(pycurl.SHARE, s)\n\
    curl.perform()\n\
    curl.close()\n\
\n\
Raises pycurl.error exception upon failure.\n\
\n\
.. _curl_share_setopt:\n\
    https://curl.haxx.se/libcurl/c/curl_share_setopt.html";

