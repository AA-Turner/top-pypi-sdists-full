# Copyright (c) 2025 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found over USB that supports the Config API,
and configures the minimum PIN length and enables PIN complexity policy.
This requires that a PIN is already set.
"""

import logging
import sys
from getpass import getpass

from fido2.ctap2 import Ctap2
from fido2.ctap2.config import Config
from fido2.ctap2.pin import ClientPin
from fido2.hid import CtapHidDevice

logging.basicConfig(level=5, stream=sys.stderr)

# Locate a device
for dev in CtapHidDevice.list_devices():
    try:
        ctap = Ctap2(dev)
        if Config.is_supported(ctap.info):
            break
    except Exception:  # noqa: S112
        continue
else:
    print("No Authenticator supporting Config found")
    sys.exit(1)

if not ctap.info.options.get("clientPin"):
    print("PIN not set for the device!")
    sys.exit(1)

# Authenticate with PIN
print("Configuring minimum PIN length and PIN complexity policy.")
pin = getpass("Please enter PIN: ")
client_pin = ClientPin(ctap)
pin_token = client_pin.get_pin_token(pin, ClientPin.PERMISSION.AUTHENTICATOR_CFG)

# Create Config instance
config = Config(ctap, client_pin.protocol, pin_token)

# Set minimum PIN length to 6 and enable PIN complexity policy
min_pin_length = 6
print(f"Setting minimum PIN length to {min_pin_length}...")
print("Enabling PIN complexity policy...")

config.set_min_pin_length(
    # min_pin_length=min_pin_length,
    pin_complexity_policy=True,
)

print("Configuration updated successfully!")
print(f"- Minimum PIN length: {min_pin_length}")
print("- PIN complexity policy: enabled")
