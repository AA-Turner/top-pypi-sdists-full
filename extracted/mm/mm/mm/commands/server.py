import mm.util as util
import mm.server.lib.server_threaded as server
from mm.exceptions import *
from mm.basecommand import Command

class StartServerCommand(Command):
    aliases=["server"]
    def execute(self):
        server.run()
