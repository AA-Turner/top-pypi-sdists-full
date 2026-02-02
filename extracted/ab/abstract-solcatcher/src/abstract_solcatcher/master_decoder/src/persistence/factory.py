from .file_sink import FileDecodeSink
from .db_sink import DatabaseDecodeSink
from .multi_sink import MultiSink
from .file_sink import return_all_datas
import logging

log = logging.getLogger(__name__)

def get_decode_sink():
    sinks = [FileDecodeSink()]

    try:
        from ..db.repositories.decoded import DecodedRepository
        repo = DecodedRepository()
        sinks.append(DatabaseDecodeSink(repo))
    except Exception:
        log.warning("DB unavailable, using file-only decode sink")

    return MultiSink(sinks)
