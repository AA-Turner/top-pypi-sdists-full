from DIRAC.MonitoringSystem.Client.MonitoringReporter import MonitoringReporter
from DIRAC.DataManagementSystem.Agent.RequestOperations.DMSRequestOperationsBase import (
    DMSRequestOperationsBase,
)


class CTADMSRequestOperationsBase(DMSRequestOperationsBase):
    def __init__(self, operation=None, csPath=None):
        super().__init__(operation, csPath)
        self.rmsMonitoringReporter = None

    def _initMonitoring(self):
        # The flag  'rmsMonitoring' is set by the RequestTask and is False by default.
        # Here we use 'createRMSRecord' to create the ES record which is defined inside OperationHandlerBase.
        if self.rmsMonitoring:
            self.rmsMonitoringReporter = MonitoringReporter(
                monitoringType="RMSMonitoring"
            )

    def _recordMonitoring(self, status, count):
        if self.rmsMonitoring:
            if not isinstance(status, list):
                status = [status]
            for s in status:
                self.rmsMonitoringReporter.addRecord(self.createRMSRecord(s, count))

    def _commitMonitoring(self):
        if self.rmsMonitoring:
            self.rmsMonitoringReporter.commit()
