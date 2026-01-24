from ..imports import *

def get_text(
    *args,
    text=None,
    url=None,
    file_path=None,
    audio_path=None,
    video_url=None,
    video_path=None,
    video_id=None,
    data_url=None,
    **kwargs
):
    # 1. Explicit text
    if text:
        if video_id:
            db_upsert(video_id, {"text": text})
        return text

    # 2. Audio/video → whisper
    if audio_path or video_url or video_path:
        text = get_whisper_text(
            *args,
            audio_path=audio_path,
            video_url=video_url,
            video_path=video_path,
            **kwargs
        )
        if video_id and text:
            db_upsert(video_id, {"whisper": {"text": text}})
        return text

    # 3. URL / file ingestion
    if url or file_path:
        filename = None
        if file_path:
            basename = os.path.basename(file_path)
            filename, ext = os.path.splitext(basename)
        else:
            domain = urlManager(url).domain
            logger.info(domain)
            filename, ext = os.path.splitext(domain)
            basename = f"{filename}.json"

        save_file = os.path.join(DEFAULT_DOCUMENTS_ROOT, basename)
        text = get_soup_text(url) or read_file_as_text(file_path)

        # Mirror in registry as cache
        info = get_infoRegistry().add_file(
            file_path=file_path or save_file,
            url=url,
            video_id=video_id,
            data_url=data_url
        )
        safe_dump_to_file(data={filename: text}, file_path=save_file)

        # DB as single source of truth
        if video_id and text:
            db_upsert(video_id, {"info": info, "text": text})

        if text and info.get("text_path"):
            write_to_file(info["text_path"], text)
        return text

    # 4. Last chance → DB only
    if video_id:
        rec = db_get(video_id)
        if rec and rec.info:
            return rec.info.get("text")

    return None
