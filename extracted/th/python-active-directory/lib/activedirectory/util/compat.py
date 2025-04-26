#
# This file is part of Python-AD. Python-AD is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# Python-AD is copyright (c) 2007-2009 by the Python-AD authors. See the
# file "AUTHORS" for a complete overview.

import ldap
import ldap.dn

from distutils import version

# ldap.str2dn has been removed in python-ldap >= 2.3.6. We now need to use
# the version in ldap.dn.
try:
    str2dn = ldap.dn.str2dn
except AttributeError:
    str2dn = ldap.str2dn

def disable_reverse_dns():
    # Possibly add in a Kerberos minimum version check as well...
    return hasattr(ldap, 'OPT_X_SASL_NOCANON')

if version.StrictVersion('2.4.0') <= version.StrictVersion(ldap.__version__):
    LDAP_CONTROL_PAGED_RESULTS = ldap.CONTROL_PAGEDRESULTS
else:
    LDAP_CONTROL_PAGED_RESULTS = ldap.LDAP_CONTROL_PAGE_OID


class SimplePagedResultsControl(ldap.controls.SimplePagedResultsControl):
    """
        Python LDAP 2.4 and later breaks the API. This is an abstraction class
        so that we can handle either.
        http://planet.ergo-project.org/blog/jmeeuwen/2011/04/11/python-ldap-module-24-changes
    """

    def __init__(self, page_size=0, cookie=''):
        if version.StrictVersion('2.4.0') <= version.StrictVersion(ldap.__version__):
            ldap.controls.SimplePagedResultsControl.__init__(
                    self,
                    size=page_size,
                    cookie=cookie
                )
        else:
            ldap.controls.SimplePagedResultsControl.__init__(
                    self,
                    LDAP_CONTROL_PAGED_RESULTS,
                    critical,
                    (page_size, '')
                )

    def cookie(self):
        if version.StrictVersion('2.4.0') <= version.StrictVersion(ldap.__version__):
            return self.cookie
        else:
            return self.controlValue[1]

    def size(self):
        if version.StrictVersion('2.4.0') <= version.StrictVersion(ldap.__version__):
            return self.size
        else:
            return self.controlValue[0]
