from .action import NHCEnergyAction

class NHCEnergy(NHCEnergyAction):
    @property
    def id(self):
        return f"energy-{self._id}"
    
    @property
    def action_id(self):
        return self._id