from imports import *
video_url = "https://www.youtube.com/watch?v=0XFudmaObLI&list=RD0XFudmaObLI&start_radio=1"
input( get_default_videos_dir())
player_responses = abstractVideoDownload(video_url,output_dir=None,filename=None,ext=None,)
input(player_responses)
##player_response = iter_streaming_urls(player_responses)
##
##for raw in [url for url in player_response if 'itag' in url]:
##    url = json.loads(f'"{raw}"')
##    print(url)
##    session = requests.Session()
##    session.headers.update({
##        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
##        "Referer": "https://www.youtube.com/",
##        "Origin": "https://www.youtube.com",
##        "Accept": "*/*",
##        "Accept-Encoding": "identity",
##        "Connection": "keep-alive",
##    })
##    with session.get(url, stream=True, timeout=30) as r:
##        r.raise_for_status()
##        with open("video.mp4", "wb") as f:
##            for chunk in r.iter_content(1024 * 1024):
##                if chunk:
##                    f.write(chunk)
