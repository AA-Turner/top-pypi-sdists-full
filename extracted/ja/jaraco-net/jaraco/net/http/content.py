import cherrypy

form = """
<form method="post" enctype="multipart/form-data">
    <input type="file" name="file"/>
    <input type="submit" />
</form>
"""


class ContentTypeReporter:
    @cherrypy.expose
    def index(self, file=None):
        if not file:
            return form
        return f"Content type is {file.content_type}"

    @classmethod
    def run(cls):
        config = {'global': {'server.socket_port': 8080, 'server.socket_host': '::0'}}
        cherrypy.quickstart(cls(), config=config)
