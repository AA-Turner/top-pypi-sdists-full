# -*- coding: utf8 -*-
import sys

class ConstModule(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError("can't change const.%s" % name)
        self.__dict__[name] = value

sys.modules[__name__] = ConstModule()
