from backend.conversations import GlobalMemoryManager

manager = GlobalMemoryManager("test-uid")
manager.add_contact("messages@sageworksai.com", "Test Bridge", "")
print("Added contact successfully")
