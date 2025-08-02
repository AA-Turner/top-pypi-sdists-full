#!/usr/bin/env python

import re

# https://gist.github.com/dperini/729294
RE_URLS = re.compile(
    r'((?:(?P<protocol>[-.+a-zA-Z0-9]{1,12})://)?'
    r'(?P<auth>[^@\:]+(?:\:[^@]*)?@)?'
    r'((?P<hostname>'
    r'(?!(?:10|127)(?:\.\d{1,3}){3})'
    r'(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})'
    r'(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})'
    r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
    r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}'
    r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))'
    r'|'
    r'(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)'
    r'(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*'
    r')(?P<tld>\.(?:[a-z\u00a1-\uffff]{2,}))'
    r'))'
    r'(?::\d{2,5})?'
    r'(?:/\S*)?',
    re.IGNORECASE
)
RE_IP_URLS = re.compile(
    r'((?:(?P<protocol>[-.+a-zA-Z0-9]{1,12})://)?'
    r'(?P<auth>[^@\:]+(?:\:[^@]*)?@)?'
    r'(?P<ip>\d+\.\d+\.\d+\.\d+))'
    r'(?P<path>/\S*)?',
    re.IGNORECASE
)
RE_IP_FRAGMENT = re.compile(r'^\d+(?:\.\d+)*$')

PROTOCOL_TRANSLATIONS = {
    'http': 'hXXp',
    'https': 'hXXps',
    'ftp': 'fXp',
}

ZERO_WIDTH_CHARACTER = '​'

def _is_ip_fragment(hostname):
    '''
    For some reason, there is a bug where the URL regex matches on the first
    half of an IP address. This double checks that and skips the match if so.
    '''
    return bool(RE_IP_FRAGMENT.match(hostname))


def defang_protocol(proto):
    return PROTOCOL_TRANSLATIONS.get(proto.lower(), '({0})'.format(proto))


def defang_ip(ip, all_dots=False):
    '''
    Defangs an IP address.

    :param str ip: an IPv4 address in the format of 127.0.0.1
    :param bool all_dots: whether to replace every dot or not.
    :return: the defanged IPv4 address.
    '''
    if all_dots:
        # Support just defanging all the dots in the passed IP.
        return ip.replace('.', '[.]')
    # Default behavior just masks the first dot.
    head, tail = ip.split('.', 1)
    return '{0}[.]{1}'.format(head, tail)


def _defang_match(match, all_dots=False, colon=False):
    '''
    Defangs a single regex match.

    :param SRE_Match match: the regex match on the URL, domain, ip, or subdomain
    :param bool all_dots: whether to defang all dots in the URIs
    :param bool colon: whether to defang the colon in the protocol
    :return: a string of the defanged input
    '''
    clean = ''
    if match.group('protocol'):
        clean = defang_protocol(match.group('protocol'))
        if colon:
            clean += '[:]//'
        else:
            clean += '://'
    if match.group('auth'):
        clean += match.group('auth')
    if all_dots:
        fqdn = match.group('hostname') + match.group('tld')
        clean += fqdn.replace('.', '[.]')
    else:
        clean += match.group('hostname')
        clean += match.group('tld').replace('.', '[.]')
    return clean


def _defang_ip_match(match, all_dots=False, colon=False):
    '''
    Defangs a single regex match on an IP address URI.

    :param SRE_Match match: the regex match on the URI with IP FQDN, or IP
    :param bool all_dots: whether to defang all dots in the URIs
    :param bool colon: whether to defang the colon in the protocol
    :return: a string of the defanged input
    '''
    clean = ''
    if match.group('protocol'):
        clean = defang_protocol(match.group('protocol'))
        if colon:
            clean += '[:]//'
        else:
            clean += '://'
    if match.group('auth'):
        clean += match.group('auth')
    clean += defang_ip(match.group('ip'), all_dots=all_dots)
    return clean


def defang(line, all_dots=False, colon=False, zero_width_replace=False):
    '''
    Defangs a line of text.

    :param str line: the string with URIs to be defanged
    :param bool all_dots: whether to defang all dots in the URIs
    :param bool colon: whether to defang the colon in the protocol
    :param bool zero_width_replace: inserts a zero width character after every character
    :return: the defanged string
    '''
    if zero_width_replace:
        return ZERO_WIDTH_CHARACTER.join(line)
    for match in RE_URLS.finditer(line):
        if _is_ip_fragment(match.group('hostname')):
            continue
        cleaned_match = _defang_match(match, all_dots=all_dots, colon=colon)
        line = line.replace(match.group(1), cleaned_match, 1)
    for match in RE_IP_URLS.finditer(line):
        cleaned_match = _defang_ip_match(match, all_dots=all_dots, colon=colon)
        line = line.replace(match.group(1), cleaned_match, 1)
    return line


def defanger(infile, outfile):
    '''
    Takes an input file-like object, and writes the defanged content to the
    outfile file-like object.

    :param file-like infile: the object to be read from and defanged
    :param file-like outfile: the file-like object to write the defanged output
    :return: None
    '''
    for line in infile:
        clean_line = defang(line)
        outfile.write(clean_line)


def refang(line):
    '''
    Refangs a line of text.

    :param str line: the line of text to reverse the defanging of.
    :return: the "dirty" line with actual URIs
    '''
    if all(char==ZERO_WIDTH_CHARACTER for char in line[1::2]):
        return line[::2]
    dirty_line = re.sub(r'\((\.|dot)\)', '.',
                        line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'\[(\.|dot)\]', '.',
                        dirty_line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'(\s*)h([x]{1,2})p([s]?)\[?:\]?//', r'\1http\3://',
                        dirty_line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'(\s*)(s?)fxp(s?)\[?:\]?//', r'\1\2ftp\3://',
                        dirty_line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'(\s*)\(([-.+a-zA-Z0-9]{1,12})\)\[?:\]?//', r'\1\2://',
                        dirty_line, flags=re.IGNORECASE)
    return dirty_line


def refanger(infile, outfile):
    '''
    Takes an input file-like object, and writes the refanged content to the
    outfile file-like object.

    :param file-like infile: the object to be read from and refanged
    :param file-like outfile: the file-like object to write the refanged output
    :return: None
    '''
    for line in infile:
        dirty_line = refang(line)
        outfile.write(dirty_line)
