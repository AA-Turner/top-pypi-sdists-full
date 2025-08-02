from kirin.decl.base import BaseModifier
from kirin.decl.camel2snake import camel2snake

from ._set_new_attribute import set_new_attribute


class EmitName(BaseModifier):

    def emit_name(self):
        set_new_attribute(self.cls, "name", camel2snake(self.cls.__name__))
