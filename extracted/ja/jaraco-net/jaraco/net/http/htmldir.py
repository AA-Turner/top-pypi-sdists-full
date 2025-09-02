# from http://tools.cherrypy.org/wiki/staticdirindex
import os
import os.path
import datetime
import cherrypy


def htmldir(section="", dir="", path="", hdr=True, **kwargs):
    fh = ''
    url = (
        "http://"
        + cherrypy.request.headers.get('Host', '')
        + cherrypy.request.path_info
    )

    # preamble
    if hdr:
        fh += (
            """<html>
<head>
<title>Directory listing for: %s</title>
<meta name="Author" content="Glenn Linderman">
<style type="text/css">@import url("/style.css");</style>
</head>
<body>
"""
            % url
        )

    path = path.rstrip(r"\/")
    fh += '<h3>Directory listing for: <a href="' + url + '">' + url + '</a></h3><hr>\n'
    for dpath, ddirs, dfiles in os.walk(path):
        for dn in sorted(ddirs):
            fdn = os.path.join(dpath, dn)
            dmtime = os.path.getmtime(fdn)
            dtim = datetime.datetime.fromtimestamp(dmtime).isoformat('-')
            fh += """<a href="{}" title="mod: {}">{}/</a><br>
""".format(
                dn + '/',
                dtim,
                dn,
            )

        del ddirs[:]  # limit to one level

        for fil in sorted(dfiles):
            fn = os.path.join(dpath, fil)
            siz = os.path.getsize(fn)
            fmtime = os.path.getmtime(fn)
            ftim = datetime.datetime.fromtimestamp(fmtime).isoformat('-')
            fh += """<a href="{}" title="mod: {}  size: {}">{}</a><br>
""".format(
                fil,
                ftim,
                str(siz),
                fil,
            )

    # postamble
    if hdr:
        fh += """
</html>
"""

    return fh
