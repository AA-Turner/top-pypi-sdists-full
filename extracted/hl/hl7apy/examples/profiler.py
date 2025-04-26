import numpy as np
import time

from hl7apy import load_message_profile, VALIDATION_LEVEL as VL
from hl7apy.parser import parse_message

MP = load_message_profile("./lab_62_response")

fl = "/home/vitto/Documents/CRS4/Progetti/hl7apy/hl7_messages/PASSED/20003.hl7"
# fl = "./lab_order_message"
with open(fl) as f:
    er7 = f.read().replace("\n", "\r")

print er7.replace("\r", "\n")

times = []
n = 1
for i in xrange(n):
    start = time.time()
    # parsed = parse_message(er7, message_profile=MP, validation_level=VL.TOLERANT, find_groups=True)
    parsed = parse_message(er7, validation_level=VL.TOLERANT, find_groups=True)
    times.append(time.time() - start)

print np.mean(times)
