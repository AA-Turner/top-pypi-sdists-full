import urllib.request
import re
import logging

from bs4 import BeautifulSoup

SP_URL_REGEX = re.compile('https://open\.spotify\.com/(?P<type>[^/]*)/(?P<id>[^?]*)')
SP_ID_REGEX = re.compile('spotify:(?P<type>[^:]*):(?P<id>[^ ]*)')
SP_IFRAME_REGEX = re.compile('<iframe src="https://open\.spotify\.com/embed/(?P<type>[^/]*)/(?P<id>[^"]*)" .*</iframe>')
SP_URI_REGEX = re.compile('spotify://(?P<type>[^/]*)/(?P<id>[^?]*)')
SP_ANDROID_URI_REGEX = re.compile('android-app://com\.spotify\.music/spotify/(?P<type>[^/]*)/(?P<id>[^?]*)')
SP_REGEX = (SP_URL_REGEX, SP_ID_REGEX, SP_IFRAME_REGEX, SP_URI_REGEX, SP_ANDROID_URI_REGEX)


def pairwise(iterable):
    """i -> (i0, i1), (i2, i3), (i4, i5), ..."""
    a = iter(iterable)
    return zip(a, a)


class SpotifyGeneric:
    def __init__(self, share_string_or_url=None, init=True):
        if share_string_or_url:
            self.url = self.convert_to_url(share_string_or_url)

        if init == True:
            self.init()

    def init(self):
        if self.url:
            self.soup = self.get_webpage(self.url)
            self.metatags = self.soup.findAll("meta")
        else:
            self.soup = False
            self.metatags = False


    @staticmethod
    def convert_to_url(share_string):
        for regex in SP_REGEX:
            match = regex.match(share_string)
            if match:
                url = "https://open.spotify.com/" + match.group("type") + "/" + match.group("id")
                logging.info(f"found {match.group('type')}url: {url}")
                return url

        print("no spotify url found in: \n '''" + share_string + "'''")
        return False

    @staticmethod
    def filter_property(propertys):
        if propertys == str:
            propertys = [propertys]

        def inner(tag):
            return "property" in tag.attrs and tag.attrs["property"] in propertys

        return inner

    def get_metatag_content_of(self, propertys):
        tags = list(filter(self.filter_property(propertys), self.metatags))
        content = []
        for tag in tags:
            content.append(tag.attrs["content"])

        if len(content) == 1:
            return content[0]
        else:
            return content

    @staticmethod
    def get_webpage(url):
        """
        :param url: url of the webpage
        :return: soup of the content form url, if it failes -> False
        """

        try:
            resp = urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            logging.error("got error urllib.error.HTTPError with " + url)
            return False
        except urllib.error.URLError:
            logging.error("got error urllib.error.URLError with " + url)
            return False

        if resp.code != 200:
            logging.error("got httperror 200 with " + url)
            return False
        else:
            return BeautifulSoup(resp.read(), "html.parser")


class Playlist(SpotifyGeneric):
    def __init__(self, share_string_or_url, init=True):
        self.url = self.convert_to_url(share_string_or_url)

        if init == True:
            self.init()

    def init(self):
        super(Playlist, self).init()

        self.title = self.get_metatag_content_of("twitter:title")
        self.image_url = self.get_metatag_content_of("twitter:image")
        self.creator_url = self.get_metatag_content_of("music:creator")

        self.tracks = self.get_tracks()

    def __repr__(self):
        return f"Playlist({self.url})"

    def __str__(self):
        return self.title

    def get_tracks(self):
        tracks = []
        for track_url, track_counter in pairwise(self.get_metatag_content_of(["music:song:track", "music:song"])):
            tracks.append(Track(track_url))

            if track_counter == 50:
                print("there are 50 or more tracks")
                print("this libary can only parse the first 50 tracks of spotify")

        return tracks


class Track(SpotifyGeneric):
    def __init__(self, share_string_or_url, init=True):
        self.url = self.convert_to_url(share_string_or_url)

        if init == True:
            self.init()

    def init(self):
        super(Track, self).init()

        # track stuff
        self.title = self.get_metatag_content_of("twitter:title")
        self.releasedate = self.get_metatag_content_of("music:release_date")
        self.duration = int(self.get_metatag_content_of("music:duration"))

        # artist stuff
        self.artist = self.get_metatag_content_of("twitter:audio:artist_name")
        self.artist_url = self.get_metatag_content_of("music:musician")

        # album stuff
        self.album_url = self.get_metatag_content_of("music:album")
        self.album_number = int(self.get_metatag_content_of("music:album:track")[1])

        # misc
        self.image_url = self.get_metatag_content_of("og:image")
        self.audio_preview_url = self.get_metatag_content_of("music:preview_url:secure_url")


    def __repr__(self):
        return f"Track({self.url})"

    def __str__(self):
        return " - ".join((self.artist, self.title))
