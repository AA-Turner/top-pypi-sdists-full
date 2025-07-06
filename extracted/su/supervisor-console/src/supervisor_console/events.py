from supervisor.events import Event
from sys import stderr, stdout
from typing import Dict, BinaryIO
from datetime import datetime

__log_format: str = "{processname} | {timestamp:%Y-%m-%d %H:%M:%S} | {line}"
__CHANNEL_MAP: Dict[str, BinaryIO] = dict(stdout=stdout, stderr=stderr)


def event_handler(event: Event, response: str) -> None:
    try:
        if not isinstance (response, bytes):
            if not isinstance(response, str):
                print ("Expected str or bytes, got {}: {}".format(response.__class__, response), file=stderr)
                response = str(response) 
            response = response.encode('utf-8')
        lines = response.splitlines(False)
        header_line = lines[0]
        lines = lines[1:] 
        headers = dict([x.split(b':') for x in header_line.split()])
        processname, channel_name = headers[b'processname'], headers[b'channel']
        channel = __CHANNEL_MAP[channel_name] \
            if channel_name in __CHANNEL_MAP.keys() else stdout

        timestamp: datetime = datetime.utcnow()
        text = '\n'.join(__log_format.format(
            processname=processname.decode("utf-8"),
            timestamp=timestamp,
            line=line.decode("utf-8")) for line in lines)

        print(text, file=channel)
    except:
        import traceback
        traceback.print_exc()
