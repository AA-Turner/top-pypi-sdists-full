#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2026 Mathieu Pasquet
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging
from getpass import getpass
from argparse import ArgumentParser
import sys

import datetime
import asyncio
import slixmpp
from slixmpp import JID

log = logging.getLogger(__name__)


async def get_stdin_reader():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


def parse_stdin(_in: bytes) -> list[tuple[str, list[int]]]:
    """
    Parse a string from stdin. Overcomplicated for what the script currently
    does.
    Spits out a list of (command, list of messages to act on).
    """
    stdin_str = _in.decode('utf-8')
    split_cmds = stdin_str.split(';')
    parsed_cmds = []
    for cmd in split_cmds:
        cmd = cmd.strip()
        split_cmd = cmd.split()
        if not split_cmd:
            continue
        cmd_verb = split_cmd.pop(0).lower()
        if cmd_verb not in ('d', 'q'):
            print(f"unknown command: {cmd}")
            continue
        if cmd_verb == 'q':
            break
        params = []
        for num in split_cmd:
            if '-' in num:
                num_split = num.split('-')
                if len(num_split) != 2:
                    print(f'Bad range: {num}')
                    continue
                try:
                    num1 = int(num_split[0])
                    num2 = int(num_split[1])
                    if num1 >= num2 or num1 < 0:
                        print(f'Bad range: {num}')
                        continue
                    params.extend(list(range(num1, num2+1)))
                except ValueError:
                    print(f'Bad range: {num}')
            else:
                try:
                    num_int = int(num)
                    if num_int < 0:
                        print(f'Bad number: {num}')
                    params.append(num_int)
                except ValueError:
                    print(f'Bad number: {num}')
        if not params:
            print(f'Bad command: {cmd}')
            continue
        parsed_cmds.append((cmd_verb, params))

    return parsed_cmds


class RoomCleanup(slixmpp.ClientXMPP):

    """
    A basic client fetching mam archive messages
    """

    def __init__(self, jid, password, remote_jid, start, max_messages):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.remote_jid = JID(remote_jid)
        self.start_date = start
        self.messages = dict()
        self.max_messages = max_messages

        self.add_event_handler("session_start", self.start)

    async def start(self, *args):
        """
        Fetch mam results for the specified JID.
        Use RSM to paginate the results.
        """
        results = self.plugin['xep_0313'].retrieve(
            jid=self.remote_jid, iterator=True,
            rsm={'max': min(50, self.max_messages)},
            reverse=True, start=self.start_date,
        )
        number = 1
        body_msgs = 0
        stop = False
        msgs = []
        async for rsm in results:
            tmp_msgs = []
            for msg in rsm['mam']['results']:
                if msg['mam_result']['forwarded']['stanza']['body']:
                    body_msgs += 1
                    tmp_msgs.append(msg)
                if body_msgs >= self.max_messages:
                    stop = True
                    break
            msgs.extend(tmp_msgs[::-1])
            if stop:
                break
        for msg in msgs[::-1]:
            forwarded = msg['mam_result']['forwarded']
            timestamp = forwarded['delay']['stamp']
            message = forwarded['stanza']
            self.messages[number] = msg['mam_result']['id']
            header = f'{number: <6} [{timestamp}] {message["from"].resource}: '
            if not message['body']:
                continue
            if '\n' in message['body']:
                pad = ' ' * len(header)
                split = message['body'].split('\n')
                first = header + split.pop(0)
                lines = [first] + [pad + line for line in split]
            else:
                lines = [
                    f'{number: <6} [{timestamp}] '
                    f'{message["from"].resource}: {message["body"]}'
                ]
            for line in lines:
                print(line)
            number += 1
        print(
            'Enter a command ("d" for delete or "q" for quit) '
            'followed by message numbers or ranges:\n'
            'example: d 1-5 17 53'
        )
        reader = await get_stdin_reader()
        commands = parse_stdin(await reader.read(1024))
        for command, params in commands:
            match command:
                case "d":
                    await self.delete_messages(params)
                case "q":
                    break

        await self.disconnect()

    async def delete_messages(self, numbers: list[int]) -> None:
        """Actually delete the messages with the IDs kept in cache"""
        success = 0
        for number in numbers:
            if number not in self.messages:
                print(f'Unknown message number: {number}')
                continue
            msg_id = self.messages[number]
            try:
                await self.plugin['xep_0425'].moderate(
                    self.remote_jid,
                    msg_id,
                    reason='moderated',
                )
                success += 1
            except Exception as exc:
                print(f'Failed to moderate message: {exc}')
        print(f'{success} message(s) successfully deleted.')


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(
        description=(
            "Script to clean up the room using message moderation. \n"
            "Messages will be listed with a prepended number, and can be then "
            "moderated by using the 'd' command, either individually or "
            "with a range.\n"
        ),
        epilog=(
            "You must have moderating powers in the room "
            "for the script to work."
        ),
    )
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const",
                        dest="loglevel",
                        const=logging.ERROR,
                        default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    # Other options
    parser.add_argument("-r", "--remote-jid", dest="remote_jid",
                        help="Remote JID")
    today = datetime.datetime.now().strftime('%Y-%m-%dT00:00:00Z')
    parser.add_argument("--start", help="Start date", default=today)
    parser.add_argument("-m", "--messages", help="Number of messages to fetch",
                        type=int, default=50)

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")
    if args.remote_jid is None:
        args.remote_jid = input("Remote JID: ")
    if args.start is None:
        args.start = input("Start time: ")

    xmpp = RoomCleanup(args.jid, args.password, args.remote_jid,
                       args.start, args.messages)
    xmpp.register_plugin('xep_0313')
    xmpp.register_plugin('xep_0425')

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    asyncio.get_event_loop().run_until_complete(xmpp.disconnected)
