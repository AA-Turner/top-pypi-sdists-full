from .functions import (os,
                        logger,
                        whisper,
                        AudioSegment,
                        sr,
                        detect_nonsilent,
                        format_timestamp,
                        safe_dump_to_file,
                        List,
                        shutil,
                        np,
                        Optional,
                        _format_srt_timestamp)

SAMPLE_RATE = whisper.audio.SAMPLE_RATE  # 16000 Hz

def get_audio_duration(file_path):
    audio = AudioSegment.from_wav(file_path)
    duration_seconds = len(audio) / 1000
    duration_formatted = format_timestamp(len(audio))
    return duration_seconds,duration_formatted
def transcribe_audio_file_clean(
    audio_path: str,
    json_data: str = None,
    min_silence_len: int = 500,
    silence_thresh_delta: int = 16
    ):
    """
    Load `audio_path`, detect all non-silent ranges, transcribe each,
    and (optionally) dump to JSON at `output_json`.
    """
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)

    # 1) Calibrate once on the first second
    calib = audio[:1000]
    calib_path = os.path.join(os.path.dirname(audio_path), "_calib.wav")
    calib.export(calib_path, format="wav")
    with sr.AudioFile(calib_path) as src:
        recognizer.adjust_for_ambient_noise(src, duration=1)
    os.remove(calib_path)

    # 2) Compute dynamic silence threshold, then find real speech segments
    silence_thresh = audio.dBFS - silence_thresh_delta
    nonsilent = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    
    json_data["audio_text"] = []
    for idx, (start_ms, end_ms) in enumerate(nonsilent):
        logger.info(f"Transcribing segment {idx}: {start_ms}-{end_ms} ms")
        chunk = audio[start_ms:end_ms]

        chunk_path = f"_chunk_{idx}.wav"
        chunk.export(chunk_path, format="wav")

        with sr.AudioFile(chunk_path) as src:
            audio_data = recognizer.record(src)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = ""

        json_data["audio_text"].append({
            "start_time": format_timestamp(start_ms),
            "end_time": format_timestamp(end_ms),
            "text": text
        })
        os.remove(chunk_path)

    # 3) Optionally write out the JSON

        full_text = [ entry["text"] 
                for entry in json_data.get("audio_text", []) 
                if entry.get("text") ]
        full_text = " ".join(full_text).strip()
        json_data["full_text"] = full_text
        safe_dump_to_file(json_data, json_data['info_path'])
    
    return json_data

def chunk_fixed(
    audio_array: np.ndarray,
    sr: int = SAMPLE_RATE,
    chunk_length_s: int = 30,
    overlap_s: int = 5
) -> List[np.ndarray]:
    """
    Split a numpy audio array into fixed-size chunks with overlap.
    """
    chunk_len = chunk_length_s * sr
    overlap  = overlap_s  * sr
    step     = chunk_len - overlap
    total    = audio_array.shape[0]
    chunks: List[np.ndarray] = []
    for start in range(0, total, step):
        end = min(start + chunk_len, total)
        chunks.append(audio_array[start:end])
        if end == total:
            break
    return chunks

def chunk_on_silence(
    audio_path: str,
    min_silence_len: int = 700,
    silence_thresh: Optional[int] = None,
    keep_silence: int = 300
) -> List[AudioSegment]:
    """
    Load the file and split on silent parts.
    Returns a list of pydub AudioSegment chunks.
    """
    audio = AudioSegment.from_file(audio_path)
    # dynamically set threshold ~16 dB below average loudness
    silence_thresh = silence_thresh or int(audio.dBFS) - 16
    return split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )

def transcribe_in_chunks(
    audio_path: str,
    model_size: str      = "medium",
    language: Optional[str] = None,
    use_silence: bool    = True,
    info_data = None,
    # parameters for fixed chunking:
    chunk_length_s: int  = 30,
    overlap_s: int       = 5,
    # parameters for silence chunking:
    min_silence_len: int = 700,
    keep_silence: int    = 300
) -> str:
    """
    Transcribe by splitting the audio into chunks and stitching results.
    """
    info_data =info_data or {}
    model = whisper.load_model(model_size)
    output_dir = info_data.get('info_dir') or info_data.get('info_directory') or info_data.get('output_directory') or info_data.get('directory') or os.getcwd()
    audio_dir = os.path.join(output_dir,'audio')
    os.makedirs(audio_dir,exist_ok=True)
    full_text = []
    if use_silence:
        segments = chunk_on_silence(
            audio_path,
            min_silence_len=min_silence_len,
            keep_silence=keep_silence
        )
        audio_paths  = []
        for i, seg in enumerate(segments):
            audio_path = os.path.join(audio_dir,f"chunk_{i}.wav")
            audio_paths.append(audio_path)
            seg.export(audio_path, format="wav")
            res = model.transcribe(audio_path, language=language)
            full_text.append(res["text"].strip())
            if audio_path and os.path.isfile(audio_path):
                os.remove(audio_path)
        shutil.rmtree(audio_dir)
        for audio_path in audio_paths:
            if audio_path and os.path.isfile(audio_path):
                os.remove(audio_path)
        
    else:
        audio = whisper.load_audio(audio_path)  # returns np.ndarray
        # no need to pad/trim if chunking manually
        chunks = chunk_fixed(
            audio, SAMPLE_RATE,
            chunk_length_s=chunk_length_s,
            overlap_s=overlap_s
        )
        for chunk in chunks:
            res = model.transcribe(chunk, language=language)
            full_text.append(res["text"].strip())
    result = {"text":" ".join(full_text).strip()}
    info_data["whisper_result"] = result
    return info_data
def transcribe_with_whisper_local(
    audio_path: str,
    model_size: str = "tiny",           # one of "tiny", "base", "small", "medium", "large"
    language: str = "english",
    use_silence=True,
    info_data=None):
    info_data =info_data or {}
    audio_path = audio_path or os.getcwd()
    if audio_path and os.path.isdir(audio_path):
        audio_path = os.path.join(audio_path,'audio.wav')
    info_data =info_data or {}
    # parameters for fixed chunki)
    """
    Returns the full transcript as a string.
    """
    model = whisper.load_model(model_size)           # loads to GPU if available
    # options: you can pass `task="translate"` for translating to English
 
    result = model.transcribe(audio_path, language=language)
    return result

def export_srt_whisper(whisper_json: dict, output_path: str):
    """
    Write an .srt file from Whisper's verbose_json format.
    `whisper_json["segments"]` should be a list of {start,end,text,...}.
    """
    logger.info(f"export_srt_whisper: {output_path}")
    segments = whisper_json.get("segments", [])
    output_path= output_path or os.getcwd()
    if output_path and os.path.isdir(output_path):
        output_path = os.path.join(output_path,'captions.srt')
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, start=1):
            start_ts = _format_srt_timestamp(seg["start"])
            end_ts   = _format_srt_timestamp(seg["end"])
            text     = seg["text"].strip()
            f.write(f"{idx}\n")
            f.write(f"{start_ts} --> {end_ts}\n")
            f.write(f"{text}\n\n")
            
def export_srt(audio_text, output_path):
    logger.info(f"export_srt: {output_path}")
    with open(output_path, 'w') as f:
        for i, entry in enumerate(audio_text, 1):
            start = entry['start_time'].replace('.', ',')
            end = entry['end_time'].replace('.', ',')
            f.write(f"{i}\n{start} --> {end}\n{entry['text']}\n\n")
    result = model.transcribe(audio_path, language=language)
    info_data["whisper_result"] = result
    return info_data
