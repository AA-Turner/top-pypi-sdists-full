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
# Name:        mail.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     12/03/2013
# -------------------------------------------------------------------------------
import smtplib, json
from smtplib import SMTP_SSL as SMTP
try:
    #Python2
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
except:
    pass
try:
    # Python3
    from email.mime.MIMEMultipart import MIMEMultipart
    from email.mime.MIMEText import MIMEText
except:
    pass
from .strings import *
from .filesystem import *


# -------------------------------------------------------------------------------
#   mailto
# -------------------------------------------------------------------------------
def system_mail(dest, Body="", Subject=None, fileconf="mail.conf"):
    if isstring(dest):
        receivers = dest.split(",")
    if not Subject:
        Subject = Body[:16] + "[...]"

    if fileconf and file(fileconf):
        conf = {}
        text = filetostr(fileconf)
        conf = json.loads(text)
        server = conf["server"] if "server" in conf else ""
        username = conf["username"] if "username" in conf else ""
        password = conf["password"] if "password" in conf else ""
        port = int(conf["port"]) if "port" in conf else 465

        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = ",".join(receivers)
        msg['Subject'] = Subject
        msg.attach(MIMEText(Body))

        try:
            # mailServer = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer = SMTP(server, port)
            mailServer.login(username, password)
            mailServer.sendmail(username, receivers, msg.as_string())
            mailServer.close()
        except smtplib.SMTPException as ex:
            print(ex)


# -------------------------------------------------------------------------------
#   main
# -------------------------------------------------------------------------------
def main():
    system_mail("valerio.luzzi@gecosistema.it", "This is a test smtplib message.")


if __name__ == '__main__':
    main()
