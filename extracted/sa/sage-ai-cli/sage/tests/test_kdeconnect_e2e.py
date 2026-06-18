import socket
import pytest
from sage.core import kdeconnect_listener
from sage.core import kdeconnect_e2e_check

def test_kdeconnect_e2e_takeover(monkeypatch):
    """E2E protocol check for the KDE Connect inbound listener using a dynamically allocated port to prevent collisions."""
    # Find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        free_port = s.getsockname()[1]
        
    # Monkeypatch the port constants to avoid conflict on 1716
    monkeypatch.setattr(kdeconnect_listener, "KDC_PORT", free_port)
    monkeypatch.setattr(kdeconnect_e2e_check, "KDC_PORT", free_port)
    
    # Mock trusted certs loading to return False to skip mutual TLS check on dev/test machines
    monkeypatch.setattr(kdeconnect_listener, "_load_trusted_certs_into_context", lambda ctx: False)
    
    # Execute the protocol takeover verification loop
    success = kdeconnect_e2e_check.run()
    assert success is True, "KDE Connect protocol e2e check failed"
