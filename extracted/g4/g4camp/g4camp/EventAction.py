from geant4_pybind import *

class EventAction(G4UserEventAction):

  def __init__(self, app):
    super().__init__()
    self.app = app
    self.data_buffer = app.data_buffer

  def BeginOfEventAction(self, evt):
    self.app.ph_counter = 0
    self.data_buffer.clear()