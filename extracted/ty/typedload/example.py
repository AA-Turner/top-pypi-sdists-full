#!/usr/bin/python3

# typedload
# Copyright (C) 2020-2024 Salvo "LtWorf" Tomaselli
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>


# This is a practical example on how to use the typedload library.
# It is a somewhat simple use case so most capabilities are not
# shown here.

# Json data is downloaded from the internet and then loaded into
# Python data structures (dictionaries, lists, strings, and so on).

#This example queries github API

import argparse
from datetime import datetime
from uuid import UUID
import json
from typing import *
import urllib.request

import typedload


class CommandLine(NamedTuple):
    full: bool
    project: Optional[str]
    username: Optional[str]

    def get_url(self) -> str:
        if self.username is None and self.project is None:
            username = 'ltworf'
            project = 'relational'
        elif self.username and self.project:
            username = self.username
            project = self.project
        else:
            raise ValueError('Username and project need to be set together')
        return f'https://codeberg.org/api/v1/repos/{username}/{project}/releases'


class User(NamedTuple):
    id: int
    login: str
    email: str
    created: datetime
    username: str


class Asset(NamedTuple):
    id: int
    name: str
    size: int
    download_count: int
    created_at: datetime
    uuid: UUID
    browser_download_url: str


class Release(NamedTuple):
    id: int
    tag_name: str
    name: str
    url: str
    html_url: str
    tarball_url: str
    zipball_url: str
    draft: bool
    prerelease: bool
    created_at: datetime
    published_at: datetime
    author: User
    assets: List[Asset]


def get_data(args: CommandLine) -> Any:
    """
    Use the github API to get releases information
    """
    req = urllib.request.Request(args.get_url())
    with urllib.request.urlopen(req) as f:
        return json.load(f)


def print_report(data: List[Release], args: CommandLine):
    for i in data:
        if i.draft or i.prerelease:
            continue
        print('Release:', i.name, end=' ')

        if args.full:
            print('Created by:', i.author.login, 'on:', i.created_at)
        else:
            print()

        for asset in i.assets:
            if asset.download_count or args.full:
                print('\t%d\t%s' % (asset.download_count, asset.name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='The username to query')
    parser.add_argument('-p', '--project', help='The project to query')
    parser.add_argument('-f', '--full', help='Print the full report', action='store_true')

    # We load the args into a NamedTuple, so it is no longer an obscure dynamic object but it is typed
    args = typedload.load(parser.parse_args(), CommandLine)
    data = get_data(args)

    # Github returns dates like this "2016-08-23T18:26:00Z", which are not supported by typedload
    # So we make a custom handler for them.
    loader = typedload.dataloader.Loader()

    # We know what the API returns so we can load the json into typed data
    typed_data = loader.load(data, List[Release])
    print_report(typed_data, args)


if __name__ == '__main__':
    main()
