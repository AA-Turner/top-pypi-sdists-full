from ..imports import *
def bool_or_default(obj,default=True):
    if obj == None:
        obj =  default
    return obj
def get_video_url(url=None, video_url=None):
    video_url = url or video_url
    if video_url:
        video_url = get_corrected_url(video_url)
    return video_url
def return_num_str(obj):
    return int(obj) if is_number(obj) else obj
def safe_mp_context():
    """Return a safe multiprocessing context that avoids fork deadlocks."""
    return mproc.get_context("spawn")
logger = get_logFile('videos_console')

def get_abs_videos_directory(directory=None):
    if not directory:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos')
    os.makedirs(directory, exist_ok=True)
    return directory


def export_srt(segments, path):
    with open(path, 'w') as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n{str(seg['start']).replace('.', ',')} --> {str(seg['end']).replace('.', ',')}\n{seg['text']}\n\n")

def get_from_local_host(endpoint, **kwargs):
    return postRequest(f"https://abstractendeavors.com{endpoint}", data=kwargs)

def download_audio(youtube_url, audio_path, output_format="wav"):
    if output_format.startswith("."):
        output_format = output_format[1:]

    if audio_path.endswith(f".{output_format}"):
        audio_path = audio_path[:-(len(output_format)+1)]

    if output_format == "webm":
        # raw download, no conversion
        ydl_opts = {
            "format": "251",  # opus/webm
            "outtmpl": f"{audio_path}.webm",  # force extension
            "overwrites": True,
        }
        final_path = f"{audio_path}.webm"
    else:
        # conversion via ffmpeg
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_path,
            "overwrites": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": output_format,
                "preferredquality": "0",
            }],
        }
        final_path = f"{audio_path}.{output_format}"

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return final_path


def build_ydl_opts(
    outtmpl,
    ydl_opts=None,
    extractor_client=None,
    user_agent=None,
    operating_system=None,
    browser=None,
    version=None,
    randomAll=False,
    randomOperatingSystem=False,
    randomBrowser=False):
    opts = {
        "quiet": True,
        "noprogress": True,
        # write under <download_directory>/<id>/<id>.<ext>
        "outtmpl": outtmpl,                      # see call-site below
        # pick best and merge; final container = mp4
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        # remux to mp4 even when streams are webm/opus
        "postprocessors": [
            {"key": "FFmpegVideoRemuxer", "preferedformat": "mp4"},
        ],
        "retries": 5,
        "fragment_retries": 5,
        "ignoreerrors": False,
        # optional: YouTube client to reduce 403s
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }
    if extractor_client:
        opts.setdefault("extractor_args", {}).setdefault("youtube", {})["player_client"] = [extractor_client]
    if user_agent:
        if user_agent == True:
            user_agent_mgr = UserAgentManager(
                operating_system=operating_system,
                browser=browser,
                version=version,
                user_agent=user_agent,
                randomAll=randomAll,
                randomOperatingSystem=randomOperatingSystem,
                randomBrowser=randomBrowser
                )
            user_agent = user_agent_mgr.get_user_agent()
        opts["http_headers"] = {"User-Agent": user_agent}
    opts.update(ydl_opts or {})
    return opts

