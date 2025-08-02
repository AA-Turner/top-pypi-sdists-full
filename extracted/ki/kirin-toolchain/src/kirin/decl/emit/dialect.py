from kirin.decl.base import BaseModifier


class EmitDialect(BaseModifier):

    def emit_dialect(self):
        setattr(self.cls, "dialect", self.dialect)
        return
