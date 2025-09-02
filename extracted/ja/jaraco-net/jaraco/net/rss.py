"""
Routines for handling RSS feeds
"""

import itertools
import subprocess
import os
import re
import operator
import datetime
import sys
import mimetypes
import logging
import argparse

import feedparser
import jaraco.logging
from pathvalidate import sanitize_filename
from dateutil import parser as date_parser

from jaraco.net.http import get_url

log = logging.getLogger(__name__)


def parse_filter(filter_string):
    filter_pattern = re.compile('(?:(before|after) )?([0-9-]+)$', re.I)
    match = filter_pattern.match(filter_string)
    sign, date_string = match.groups()
    op = dict(before=operator.le, after=operator.ge).get(sign, operator.eq)
    spec_date = date_parser.parse(date_string)
    return lambda entry: op(datetime.datetime(*entry.updated_parsed[:6]), spec_date)


class CombinedFilter(list):
    """
    A list of callables that can be applied to a filter call.
    """

    def __call__(self, subject):
        return all(filter(subject) for filter in self)


def _parse_args(parser=None):
    parser = parser or argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument(
        '-f',
        '--date-filter',
        help="add a date filter such as 'before 2006'",
        default=CombinedFilter(),
        action="append",
        type=parse_filter,
    )
    jaraco.logging.add_arguments(parser)
    args = parser.parse_args()
    jaraco.logging.setup(args)
    return args


def download_enclosures():
    args = _parse_args()
    d = feedparser.parse(args.url)
    for entry in filter(args.date_filter, d['entries']):
        enclosure = entry.enclosures.pop()
        assert not entry.enclosures, "Only support one enclosure per item"

        title = entry.title
        ext = mimetypes.guess_extension(enclosure.type) or '.mp3'
        filename = title + ext
        log.info('Getting %s', filename)
        sanitized = sanitize_filename(filename, replacement_text='_')
        try:
            get_url(enclosure.url, sanitized, replace_newer=True)
        except KeyboardInterrupt:
            if os.path.exists(sanitized):
                os.remove(sanitized)
            log.info('Quitting')
            break


def launch_feed_enclosure():
    """
    RSS Feed Launcher
    """
    parser = argparse.ArgumentParser(usage=launch_feed_enclosure.__doc__)
    parser.add_argument('-i', '--index', help="launch feed found at specified index")
    args = _parse_args(parser)
    load_feed_enclosure(args.url, args.date_filter, args.index)


def load_feed_enclosure(url, filter_=None, index=None):
    d = feedparser.parse(url)
    print('loaded', d['feed']['title'])
    filtered_entries = filter(filter_, d['entries'])

    if index is None:
        for i, entry in enumerate(filtered_entries):
            fmt = '{0:4d} {1}'
            print(fmt.format(i, entry.title))
        try:
            index = int(input('Which one? '))
        except ValueError:
            print("Nothing selected")
            sys.exit(0)

    player_search = (
        r'C:\Program Files\Windows Media Player\wmplayer.exe',
        r'C:\Program Files (x86)\Windows Media Player\wmplayer.exe',
    )
    player = next(itertools.ifilter(os.path.exists, player_search))

    command = [player, filtered_entries[index].enclosures[0].href]
    print('running', subprocess.list2cmdline(command))
    subprocess.Popen(command)


def launch_feed_as_playlist():
    options, args = _parse_args()
    assert not args, "Positional arguments not allowed"
    get_feed_as_playlist(options.url, filter_=options.date_filter)


def get_feed_as_playlist(url, outfile=sys.stdout, filter_=None):
    d = feedparser.parse(url)
    filtered_entries = filter(filter_, d['entries'])
    # RSS feeds are normally retrieved in reverse cronological order
    filtered_entries.reverse()
    for e in filtered_entries:
        outfile.write(e.enclosures[0].href)
        outfile.write('\n')


if __name__ == '__main__':
    launch_feed_enclosure()
