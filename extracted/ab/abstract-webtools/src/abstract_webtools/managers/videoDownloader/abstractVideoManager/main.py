from .imports import *
from .src import *
# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
_abstractVideoManager = None
_output_dir = None
def getAbstractVideoManager(output_dir=None):
    if _abstractVideoManager is not None:
        _output_dir = output_dir or 'downloads'
        _abstractVideoManager = AbstractVideoManager(_output_dir)
    return _abstractVideoManager
def get_itags(video_url):
    player = extract_player_response(video_url)
    itags = get_any_value(player,'itag')
    return itags
def get_itag(video_url,itag=None):
    itags = get_itags(video_url)
    if itag and itag in itags:
        pass
    else:
        itag = itags[0]
    return itag

def getDirectUrlDict(video_url,itag=None,output_dir='downloads'):
    
    itag = get_itag(video_url,itag=itag)
    result = getAbstractVideoManager(output_dir).resolve_direct_url(video_url=video_url,itag=itag)
    return result
def getDirectUrl(video_url,itag=None):
    result = getDirectUrlDict(video_url=video_url,itag=itag)
    return result["direct_url"]
def getMetaData(video_url,itag=None):
    result = getDirectUrlDict(video_url=video_url,itag=itag)
    return result["metadata"]
def getTitle(video_url,itag=None):
    result = getMetaData(video_url=video_url,itag=itag)
    return result.get("title", "video").replace("/", "_")  
def getVideoFilename(video_url,itag=None):
    title = getTitle(video_url=video_url,itag=itag)
    return f"{title}.mp4" 
def abstractVideoDownload(video_url,itag=None,output_dir='downloads'):
    direct_url = getDirectUrl(video_url=video_url,itag=itag)
    filename = getVideoFilename(video_url=video_url,itag=itag)
    out = getAbstractVideoManager(output_dir).download(
        url=direct_url,
        filename=filename,
    )
