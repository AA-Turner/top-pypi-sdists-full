import os
import re

files_17888 = [
    "cvc/gateway.py",
    "cvc/core/models.py",
    "cvc/cli.py",
    "cvc/sdk/telemetry.py",
    "cvc/launcher.py"
]

files_54321 = [
    "cvc/auth.py",
    "cvc/cli.py"
]

files_8000 = [
    "cvc/core/models.py",
    "cvc/agent/chat.py"
]

for f in set(files_17888 + files_54321 + files_8000):
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 17888 -> 13421
    content = content.replace("17888", "13421")
    # 54321 -> 13421
    content = content.replace("54321", "13421")
    
    # Custom for 8000 so we don't hit 128000 or [:8000]
    if f == "cvc/core/models.py":
        content = content.replace("proxy_port: int = 8000", "proxy_port: int = 13421")
        content = content.replace('os.getenv("CVC_PORT", "8000")', 'os.getenv("CVC_PORT", "13421")')
    if f == "cvc/agent/chat.py":
        content = content.replace('port: int = 8000', 'port: int = 13421')
        
    with open(f, "w", encoding="utf-8") as file:
        file.write(content)

print("Replaced ports in python files")
