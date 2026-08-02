from python_agent.build_scanner.entities.v3.code_element_with_hash import (
    CodeElementWIthHash,
)


class MethodMetaData(object):
    def __init__(self, type, is_anonymous):
        self.type = type
        self.anonymous = is_anonymous


class MethodData(CodeElementWIthHash):
    def __init__(
        self,
        unique_id,
        display_name,
        position,
        end_position,
        meta,
        hash,
        sig_hash,
        lines,
    ):
        super(MethodData, self).__init__(hash)
        self.uniqueId = unique_id
        self.displayName = display_name
        self.position = position
        self.endPosition = end_position
        self.meta = meta
        self.sigHash = sig_hash
        self.lines = sorted(set(lines))
        if len(self.lines) > 1:
            del self.lines[0]
        self.linesCount = len(self.lines)
