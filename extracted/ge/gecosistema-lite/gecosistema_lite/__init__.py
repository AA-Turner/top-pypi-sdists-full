# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        __init__.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     05/09/2017
# -------------------------------------------------------------------------------
from .version import *
from .strings import *
from .filesystem import *
from .datatypes import *
from .execution import *
from .compression import *
from .gdal_shape import *
from .gdal_utils import *
from .gdal_numpy import *
from .gdal_wrappers import *
from .databases import *
from .http import *
from .sqlitedb import *
from .spatialdb import *
from .mssqldb import *
from .sqltable import *
from .stime import *
from .number import *
from .taudem import *
from .xml_utils import *
from .excel import *
from .ftp_utils import *
try:
    from .crypto import *
except:
    print("pycrypto is not installed")
from .mail import *
from .audio import *

from .mapserver import *
