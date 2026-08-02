# -*- config:utf-8 -*-

from tldparse.__version__ import __version__
import os


# @see https://publicsuffix.org/list/public_suffix_list.dat
# for the list of public suffixes
class TLDParseObject:
    def __init__(self):
        self.suffixes = None

    def load(self, filepath=None):
        if not filepath:
            filepath = os.path.join(os.path.dirname(__file__), 'public_suffix_list.dat')

        self._load(filepath)

    def __call__(self, domain, private=True):
        if not self.suffixes:
            self.load()

        if not isinstance(domain, str):
            domain = domain.decode('utf-8')

        result = [None, None, None]
        if private:
            result = self._lookup(b'private', domain)

        if result[0] is None:
            result = self._lookup(b'public', domain)

        return result

    def _lookup(self, category, domain):
        parts = [x.encode('idna') for x in domain.split('.')]
        parts.reverse()

        if parts[0] not in self.suffixes[category]:
            return None, None, None

        tld = []
        current = self.suffixes[category]
        iterator = iter(parts)

        for part in iterator:
            if part not in current:
                if b'*' in current:
                    tld.append(part)
                    try:
                        part = next(iterator)
                    except StopIteration:
                        part = b''
                        break
                elif category == b'private':
                    # Special treatment - In this case we expect a full compatibility
                    # Since current is not empty, it means there are subdomains expected, so we continue
                    if len(current) > 0:
                        return None, None, None

                break

            if part is not None:
                tld.append(part)
                current = current[part]

        tld.reverse()
        part = part.decode('idna')

        return self._post_process(b'.'.join(tld).decode('idna'), part, domain)

    def add(self, tld, category=b'private'):
        if isinstance(tld, str):
            tld = tld.encode('utf-8')

        if isinstance(category, str):
            category = category.encode('utf-8')

        if tld.find(b'.') > -1:
            current = self.suffixes[category]
            parts = tld.split(b'.')
            parts.reverse()
            for part in parts:
                part = part.decode('utf-8').encode('idna')
                if part not in current:
                    current[part] = {}

                current = current[part]
        else:
            self.suffixes[category][tld.decode('utf-8').encode('idna')] = {}

    def remove(self, domain, category=b'private'):
        if isinstance(category, str):
            category = category.encode('utf-8')

        parts = [x.encode('idna') for x in domain.split('.')]
        parts.reverse()

        while self._remove_parts(parts, category):
            parts.pop()

    def _remove_parts(self, parts, category):
        current = self.suffixes[category]
        if len(parts) > 1:
            for i in range(0, len(parts) - 1):
                part = parts[i]
                if part not in current:
                    return False

                current = current[part]

        last_part = parts[len(parts) - 1]

        if len(current[last_part]) > 0:
            return False

        del current[last_part]
        return True

    def _load(self, filepath):
        content = None
        with open(filepath, 'rb') as f:
            content = f.read()

        self.suffixes = {
            b'public': {},
            b'private': {}
        }

        # Now we process
        list_name = b'public'
        for line in content.split(b'\n'):
            line = line.strip()
            if line == b'':
                continue

            if line == b'// ===BEGIN PRIVATE DOMAINS===':
                list_name = b'private'

            if line.startswith(b'//'):
                continue

            self.add(line, list_name)

    def _post_process(self, tld, domain, original):
        if tld == '':
            tld = None

        if domain == '':
            domain = None

        subdomain = None

        if domain:
            subdomain = original.replace('{0}.{1}'.format(domain, tld), '')
            if subdomain == '':
                subdomain = None
            elif subdomain.endswith('.'):
                subdomain = subdomain[0:-1]

        return tld, domain, subdomain


TLDParse = TLDParseObject()


class DomainResult:
    def __init__(self, domain, parser=None, private=True):
        if not parser:
            parser = TLDParse
        self.parser = parser

        self._tld = None
        self._domain = None
        self._subdomain = None

        self._parse(domain, private)

    def _parse(self, domain, private):
        if not domain:
            return None

        # Removing :// parts
        if domain.find('://') > -1:
            domain = domain[domain.find('://') + 3:]

        if domain.find('/') > -1:
            domain = domain[0:domain.find('/')]

        if domain.find(':') > -1:
            domain = domain[0:domain.find(':')]

        self._tld, self._domain, self._subdomain = self.parser(domain, private)

    def __repr__(self):
        return '{0}.{1}.{2}'.format(self._subdomain, self._domain, self._tld)

    @property
    def fqdn(self):
        """
        Returns the fully qualified domain name
        For instance: google.com
        In case the _domain is None, like "co.uk", then the fqdn will be null too
        """
        if not self._domain:
            return None
        return '{0}.{1}'.format(self._domain, self._tld)

    @property
    def suffix(self):
        """
        Returns the suffix of the domain
        For instance: com
        """
        return self._tld

    @property
    def domain(self):
        """
        Returns the domain name without suffix and subdomain
        For instance: google
        """
        return self._domain

    @property
    def subdomain(self):
        """
        Returns any subdomain - if present.
        For instance: www
        """
        return self._subdomain
