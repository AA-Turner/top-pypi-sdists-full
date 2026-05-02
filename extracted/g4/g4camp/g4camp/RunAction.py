from geant4_pybind import *

class RunAction(G4UserRunAction):

  def __init__(self, isMaster):
    super().__init__()
#    G4RunManager.GetRunManager().SetPrintProgress(1000)
    self.isMaster = isMaster
    self.printTiming = False
    if self.isMaster: 
      self.timer = G4Timer()

  def BeginOfRunAction(self, aRun):
    # inform the runManager to save random number seed
    G4RunManager.GetRunManager().SetRandomNumberStore(False)
    if self.isMaster:
      self.timer.Start()

  def SetPrintTiming(self, print_timing):
    self.printTiming = print_timing

  def EndOfRunAction(self, aRun):
    if self.isMaster:
      self.timer.Stop()
      if self.printTiming:
        import datetime
        dt_real = datetime.timedelta(seconds = self.timer.GetRealElapsed())
        dt_user = datetime.timedelta(seconds = self.timer.GetUserElapsed())
        dt_syst = datetime.timedelta(seconds = self.timer.GetSystemElapsed())
        print(f" Number of events: {aRun.GetNumberOfEvent()}")
        print(f" Real time:    {dt_real}")
        print(f" User time:    {dt_user}")
        print(f" System time:  {dt_syst}")
