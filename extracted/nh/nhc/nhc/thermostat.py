from .action import NHCBaseAction

class NHCThermostat(NHCBaseAction):
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self._measured = data["measured"] / 10
        self._setpoint = data["setpoint"] / 10
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]

    @property
    def id(self):
        return f"thermostat-{self._id}"
    
    @property
    def action_id(self):
        return self._id
    
    @property
    def measured(self):
        return self._measured

    @property
    def setpoint(self):
        return self._setpoint
    
    @property
    def mode(self):
        return self._state
    
    @property
    def overrule(self):
        return self._overrule
    
    @property
    def overruletime(self):
        return self._overruletime
    
    @property
    def ecosave(self):
        return self._ecosave
    
    async def set_mode(self, mode):
        await self._controller.execute_thermostat_mode(self._id, mode, self._overruletime, self._overrule)

    async def set_temperature(self, setpoint):
        await self._controller.execute_thermostat_set_temperature(self._id, setpoint * 10)
    
    def update_state(self, data):
        self._state = data["mode"]
        self._setpoint = data["setpoint"] / 10
        self._measured = data["measured"] / 10
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]

