import pytest

def test_sms_binary_storage():
    """
    Test the binary storage component of the SMS bridge (for images/attachments).
    """
    from sage.core.sms_bridge import SMSBridge
    bridge = SMSBridge()
    
    # Write a dummy image to simulate an attachment
    binary_data = b"fake-image-data-89234"
    file_path = bridge.store_attachment("test-attachment.png", binary_data)
    
    assert file_path is not None
    
    # Verify we can read it back
    with open(file_path, "rb") as f:
        read_data = f.read()
        
    assert read_data == binary_data
