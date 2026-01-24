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
# Name:        crypto.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     19/08/2017
# -------------------------------------------------------------------------------

from base64 import b64encode, b64decode
import hashlib
import os
from Crypto.Cipher import AES


def __padr__(text, n, c):
    text = str(text)
    return text + str(c) * (n - len(text))


def encrypt(raw, key=None):
    key = key if key != None else juststem(__file__)
    r = 32 - len(raw) % 32
    raw = __padr__(raw, len(raw) + r, chr(r))
    iv = os.urandom(AES.block_size)
    # iv = "0123456789123456".encode("utf-8")
    # key = hashlib.sha256(key.encode()).digest()
    key = hashlib.md5(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, key=None):
    key = key if key != None else juststem(__file__)
    enc = b64decode(enc)
    iv = enc[:AES.block_size]
    # key = hashlib.sha256(key.encode()).digest()
    key = hashlib.md5(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(enc[AES.block_size:])
    data = data[:-ord(data[-1:])]
    return data.decode('utf-8')

def main():
    print(AES.block_size)
    message = "The answer is xyz."
    key = "123456"
    ctxt = encrypt(message, key)
    print(ctxt)
    print(decrypt(ctxt, key))

if __name__ == "__main__":
    main()
