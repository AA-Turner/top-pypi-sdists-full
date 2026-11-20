import math
import time
import numpy as np
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive

rtde_c = RTDEControl("192.168.56.101")
rtde_r = RTDEReceive("192.168.56.101")

# Parameters
dt = 1.0 / 500       # 2ms - 500 Hz control loop
lookahead_time = 0.1
gain = 800
velocity = 0.5
acceleration = 0.5

radius = 0.05        # circle radius in meters
frequency = 0.5      # Hz - one full circle per 2 seconds

# Move to a starting pose using moveL
start_pose = rtde_r.getActualTCPPose()
init_pose = start_pose[:]
init_pose[0] += radius  # start at the rightmost point of the circle
rtde_c.moveL(init_pose, velocity, acceleration)

motion_start_time = time.time()

try:
    while True:
        t_start = rtde_c.initPeriod()
        elapsed = time.time() - motion_start_time
        angle = 2.0 * math.pi * frequency * elapsed

        # Circular trajectory in the XY plane of the base frame
        target = start_pose[:]
        target[0] = start_pose[0] + radius * math.cos(angle)
        target[1] = start_pose[1] + radius * math.sin(angle)

        rtde_c.servoL(target, velocity, acceleration, dt, lookahead_time, gain)
        rtde_c.waitPeriod(t_start)
except KeyboardInterrupt:
    print("Interrupted. Stopping...")
finally:
    rtde_c.servoStop()
    rtde_c.stopScript()
