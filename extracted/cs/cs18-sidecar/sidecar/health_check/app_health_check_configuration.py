from typing import Dict


class HealthCheckConfiguration:
    #  ===  Reminder to the structure of healthcheck in the app yaml ===
    #
    #       healthcheck:
    #           timeout: 30
    #           script: test.sh             -> The script that we want to run as our healthcheck
    #           wait_for_ports: 70,100      -> If we don't have a script file then we can just use this
    #                                          (to test specific ports or just write 'ALL' to test all the ports)
    #
    # ===================================================================
    def __init__(self, script_name: str, target_ports: [], timeout_sec: int):
        # (target_ports is actually the 'wait_for_ports' from the section of 'healthcheck' in the app yaml)
        self.target_ports = target_ports
        self.timeout_sec = timeout_sec
        self.script_name = script_name


class AppHealthCheckConfiguration:
    _app_health_checks: Dict[str, HealthCheckConfiguration] = {}

    def add_app_healthcheck_info(self, app_name: str, script_name: str, target_ports: [], timeout_sec: int):
        self._app_health_checks[app_name] = HealthCheckConfiguration(script_name, target_ports, timeout_sec)
        return self

    def get_configuration(self, app_name: str)->HealthCheckConfiguration:
        if app_name not in self._app_health_checks:
            raise Exception("No health-check configuration was found for app '{}'".format(app_name))
        return self._app_health_checks[app_name]
