# print('Executing expLogbook.py')
# from getComment4File import *
import requests
import urllib.parse
import os
import builtins
import re
from elog.logbook_exceptions import *
import elog
from datetime import datetime
from time import localtime

# disable warnings about ssl verification
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class myLogbook(elog.Logbook):
        
    def getMessage4File(self, filename):
        ids = super().search({'file':filename})
        if len(ids) > 0:
            message, _ , _ = super().read(ids[0])
            return message
        else:
            print("File {} in eLog not found!".format(filename))
            return None

    def getShortMessage4File(self,filename):
        stuff = self.getMessage4File(filename)
        import html2text
        h = html2text.HTML2Text()
        # Ignore converting links from HTML
        h.ignore_links = True
        if stuff: return h.handle(stuff)
        return


##########################################################################################################
# ogf settings:
try:
    from libhreels.eLogCredentials import dummy, unsafe    # Defines User credentials
    logbook = myLogbook('https://labor-ep3.physik.uni-halle.de/HREELS/', user=dummy, password=unsafe)
    print('eLog available!')
    available = True
except:
    available = False

