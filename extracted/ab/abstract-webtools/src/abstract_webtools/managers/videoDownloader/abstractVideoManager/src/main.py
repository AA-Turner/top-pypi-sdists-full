


class YouTubeResolveError(Exception):
    pass




# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    VIDEO_URL = "https://www.youtube.com/shorts/6vP02wYh4Ds"
    player = extract_player_response(VIDEO_URL)
    for itag in get_any_value(player,'itag'):
    
        downloader = AbstractYouTubeDownloader()

        print("[*] Resolving direct URL...")
        result = downloader.resolve_direc
