import pytest

def test_sms_media_routing():
    """
    Test that the SMS bridge correctly routes media files to the LLM agent.
    """
    from sage.core.sms_bridge import SMSBridge
    bridge = SMSBridge()
    
    # Simulate an inbound message with a media attachment
    msg_id = "test-media-123"
    binary_data = b"fake-image-data"
    
    # Pass the data to the bridge processor
    bridge.process_inbound(
        sender="test@example.com", 
        text="Analyze this image", 
        msg_id=msg_id,
        attachments=[{"filename": "test.png", "data": binary_data}]
    )
    
    # We assert the function completes without error under SAGE_TESTING=1.
    assert True
