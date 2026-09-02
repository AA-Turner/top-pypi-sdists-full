# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2018 Luzzi Valerio 
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
# Name:        audio.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     25/07/2018
# -------------------------------------------------------------------------------
from .filesystem import *

try:
    import winsound
except:
    pass


def beep():
    """
    beep
    """
    freq, duration = 2500, 500
    if isWindows():
        winsound.Beep(freq, duration)


if __name__ == "__main__":
    main()
