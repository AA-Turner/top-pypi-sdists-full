"""No-op reporter."""


class NullReporter:
    async def begin_test(self, name): pass
    async def pass_test(self): pass
    async def fail_test(self, error): pass
    async def begin_step(self, description, instruction_id=None): pass
    async def end_step(self, description, ok, error=None, instruction_id=None): pass
    async def warn_step(self, description, error): pass
    async def send_element_bounds(self, bbox, instruction_id=None): pass
    # async def attach_screenshot(self, data): pass
