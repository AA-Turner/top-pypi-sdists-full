from .imports import *
from .src import *

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def makeAbstractVideoManager(output_dir='downloads'):
    return AbstractVideoManager(output_dir)

def get_itags(video_url):
    player = extract_player_response(video_url)
    return get_any_value(player, 'itag')

def get_itag(video_url, itag=None):
    itags = get_itags(video_url)
    if itag and itag in itags:
        return itag
    return itags[0]

def getDirectUrlDict(video_url, itag=None, output_dir='downloads', manager=None):
    if manager is None:
        manager = makeAbstractVideoManager(output_dir)
    itag = get_itag(video_url, itag=itag)
    return manager.resolve_direct_url(video_url=video_url, itag=itag)

def getDirectUrl(video_url, itag=None, manager=None):
    result = getDirectUrlDict(video_url=video_url, itag=itag, manager=manager)
    return result["direct_url"]

def getMetaData(video_url, itag=None, manager=None):
    result = getDirectUrlDict(video_url=video_url, itag=itag, manager=manager)
    return result["metadata"]

def getTitle(video_url, itag=None, manager=None):
    result = getMetaData(video_url=video_url, itag=itag, manager=manager)
    return result.get("title", "video").replace("/", "_")

def getVideoFilename(video_url, itag=None, manager=None):
    return getTitle(video_url=video_url, itag=itag, manager=manager)
    
def getVideoBasename(video_url, itag=None,filename=None,ext=None, manager=None):
    filename = filename or getVideoFilename(video_url, itag=itag, manager=manager)
    ext= ext or '.mp4'
    ext = eatAll(ext,'.')
    return f"{filename}.{ext}"
def check_dir_for_basename(basename,directory):
    dirlist = os.listdir(output_dir)
    for i,item in range(len(dirlist)):
        if item == basename:
            return True
def getFilePath(video_url,  itag=None, output_dir=None,filename=None,ext=None, manager=None):
    basename = getVideoBasename(video_url, itag=itag,filename=filename,ext=ext, manager=manager)
    output_dir = output_dir or get_default_videos_dir()
    file_path = os.path.join(output_dir,basename)
    if os.path.isfile(file_path):
        dirlist = os.listdir(output_dir)
        file_part = get_file_parts(file_path)
        dirname = file_part.get('dirname')
        filename = file_part.get('filename')
        ext = file_part.get('ext')
        basename = file_part.get('basename')
        for i,item in range(len(dirlist)):
            if not check_dir_for_basename(basename,dirname):
                file_path = os.path.join(dirname,basename)
                break
            basename = f"{filename}_{i+1}{ext}"
    return file_path
def abstractVideoDownload(video_url, itag=None, output_dir=None,filename=None,ext=None, manager=None):
    output_dir = output_dir or get_default_videos_dir()
    
    if manager is None:
        manager = makeAbstractVideoManager(output_dir)
    getVideoFilename(video_url=video_url, itag=itag, manager=manager)
    direct_url = getDirectUrl(video_url=video_url, itag=itag, manager=manager)
    file_path = getFilePath(video_url=video_url, itag=itag,output_dir=output_dir, filename=filename,ext=ext,manager=manager)
    return manager.download(url=direct_url, filename=file_path)
