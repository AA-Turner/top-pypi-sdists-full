from kirin.decl.base import BaseModifier

from ._create_fn import create_fn
from ._set_new_attribute import set_new_attribute


class EmitRepr(BaseModifier):

    def emit_repr(self):
        if "repr" not in self.params or not self.params["repr"]:
            return

        body = [f'ret = "{self.cls.__name__}("']
        for idx, field in enumerate(self.fields):
            if idx > 0:
                body.append('ret += ", "')
            body.append(f'ret += f"{field.name}={{{self._self_name}.{field.name}}}"')
        body.append('ret += ")"')
        body.append("return ret")

        set_new_attribute(
            self.cls,
            "__repr__",
            create_fn(
                "__repr__",
                args=[self._self_name],
                body=body,
                globals=self.globals,
                return_type=str,
            ),
        )
