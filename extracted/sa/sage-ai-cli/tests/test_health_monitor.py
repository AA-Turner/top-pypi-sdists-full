import pytest
from utils.SystemHealthMonitor import SystemHealthMonitor

def test_health_monitor_get_status():
    monitor = SystemHealthMonitor()
    status = monitor.get_status()
    assert "cpu_ok" in status
    assert "ram_ok" in status
    assert "disk_ok" in status
    assert isinstance(status["cpu_ok"], bool)
    assert isinstance(status["ram_ok"], bool)
    assert isinstance(status["disk_ok"], bool)
