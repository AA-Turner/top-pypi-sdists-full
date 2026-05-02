"""
    Static assignments for universally used colors and variables

"""
import os
from spotlib.statics import local_config
from libtools import Colors

c = Colors()

try:

    from libtools.oscodes_unix import exit_codes
    os_type = 'Linux'
    user_home = os.getenv('HOME')
    splitchar = '/'                                     # character for splitting paths (linux)

    # special colors - linux
    acct = c.BOLD + c.BRIGHT_GREEN
    text = c.BRIGHT_PURPLE
    TITLE = c.WHITE + c.BOLD

except Exception:
    from libtools.oscodes_win import exit_codes          # non-specific os-safe codes
    os_type = 'Windows'
    username = os.getenv('username')
    splitchar = '\\'                                    # character for splitting paths (windows)
    user_home = 'Users' + splitchar + username
    # special colors - windows
    acct = c.CYAN
    text = c.LT2GRAY
    TITLE = c.WHITE + c.BOLD


# universal colors
bd = c.BOLD
bcy = c.BRIGHT_CYAN
bbc = bd + c.BRIGHT_CYAN
bdcy = c.CYAN + c.BOLD       
bl = c.BLUE
bbl = c.BRIGHT_BLUE
bbbl = bd + c.BRIGHT_BLUE
btext = text + c.BOLD
bwt = c.BRIGHT_WHITE
bdwt = c.BOLD + c.BRIGHT_WHITE
gn = c.BRIGHT_GREEN
frame = gn + bd
fs = c.GOLD3
highlight = bd + c.BRIGHT_BLUE
rd = c.RED + c.BOLD
title = c.BRIGHT_WHITE + c.BOLD
ub = c.UNBOLD
yl = c.YELLOW + c.BOLD
rst = c.RESET

# globals
config_dir = local_config['CONFIG']['CONFIG_PATH']      # path to localhost configuration directory
