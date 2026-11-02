from sys import getrefcount
from _rl_accel import unicode2T1

utext = 'This is the end of the world'

class Font:
    def __init__(self,name):
        self.fontName = name
        self.substitutionFonts = []
        self.encName = 'utf8'

font = Font('Helvetica')

defns = 'utext font font.encName font.fontName font.substitutionFonts'.split()
rc0 = [getrefcount(eval(x,globals())) for x in defns]
print(rc0)
unicode2T1(utext,[font]+font.substitutionFonts)
rc1 = [getrefcount(eval(x,globals())) for x in defns]
print(rc1)
if rc1!=rc0:
    print('!!!!! reference counts changed !!!!!')
