class NHCActionEvent:
    @property
    def value1(self) -> int:
        return self._value1
    
    @property
    def id(self) -> int:
        return self._id
    
    def __init__(self, event):
        self._id = event["id"]
        self._value1 = event["value1"]

class NHCEnergyEvent():
    @property
    def channel(self) -> int:
        return self._channel
    
    @property
    def v(self) -> int:
        return self._v
    
    def __init__(self, event):
        self._channel = event["channel"]
        self._v = event["v"]

class NHCThermostatEvent(): 
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def mode(self) -> int:
        return self._mode
    
    @property
    def setpoint(self) -> int:
        return self._setpoint
    
    @property
    def measured(self) -> int:
        return self._measured
    
    @property
    def overrule(self) -> int:
        return self._overrule
    
    @property
    def overruletime(self) -> str:
        return self._overruletime
    
    @property
    def ecosave(self) -> int:
        return self._ecosave
    
    def __init__(self, event):
        self._id = event["id"]
        self._mode = event["mode"]
        self._setpoint = event["setpoint"]
        self._measured = event["measured"]
        self._overrule = event["overrule"]
        self._overruletime = event["overruletime"]
        self._ecosave = event["ecosave"]