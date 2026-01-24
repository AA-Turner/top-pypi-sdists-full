import sys
from threading import Event, Thread
from time import sleep

from fido2.ctap2 import Ctap2
from fido2.pcsc import CtapPcscDevice

dev = next(CtapPcscDevice.list_devices(), None)
if not dev:
    print("No CCID CTAP device found")
    sys.exit(1)

print("Device found:", dev)

event = Event()


def foo():
    print("START TIMING...")
    sleep(2)
    print("CANCEL!")
    event.set()


# Thread(target=foo).start()

ctap2 = Ctap2(dev)
ctap2.reset(event=event, on_keepalive=lambda status: print("Keepalive status:", status))


print("All done!")
