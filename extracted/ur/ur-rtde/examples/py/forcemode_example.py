from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
import numpy as np
import time

rtde_c = RTDEControl("192.168.56.101")
rtde_r = RTDEReceive("192.168.56.101")

# Task parameters
dt = 1.0 / 500 # 500Hz control loop
task_frame = [0, 0, 0, 0, 0, 0]
compliance_vector = [1, 1, 1, 0, 0, 0]
init_q = [-np.pi/2, -np.pi/2, -np.pi/2, -np.pi/2, np.pi/2, 0.0]

# Spiral search parameters
F_tangential     = 30.0  # N - tangential force that keeps the robot orbiting
growth_rate_mm_s = 1.0   # mm/s - desired outward radial growth rate (easy to tune)
z_force          = -5.0  # N - downward force
v_max = [0.5, 0.5, 0.5, 0.2, 0.2, 0.2]

# Derive F_radial from the desired growth rate
F_radial = F_tangential * (growth_rate_mm_s / 1000.0) / v_max[0]

# Move to initial joint position with a regular moveJ
rtde_c.moveJ(init_q)

rtde_c.zeroFtSensor() # zero ft sensor
time.sleep(0.2)

# Record the starting TCP position (the spiral center)
start_tcp = rtde_r.getActualTCPPose()
start_x, start_y = start_tcp[0], start_tcp[1]

try:
    while True:
        t_start = rtde_c.initPeriod()

        # Compute force direction based on current position relative to spiral center
        actual_tcp = rtde_r.getActualTCPPose()
        dx = actual_tcp[0] - start_x
        dy = actual_tcp[1] - start_y
        r  = np.sqrt(dx**2 + dy**2)

        if r > 0.001:
            cos_phi = dx / r
            sin_phi = dy / r
        else:
            cos_phi, sin_phi = 1.0, 0.0

        Fx = F_tangential * (-sin_phi) + F_radial * cos_phi
        Fy = F_tangential *   cos_phi  + F_radial * sin_phi
        Fz = z_force

        rtde_c.forceMode(task_frame, compliance_vector, [Fx, Fy, Fz, 0, 0, 0], 2, v_max)
        rtde_c.waitPeriod(t_start)

except KeyboardInterrupt:
    print("Stopped spiral search")
    rtde_c.forceModeStop()
    rtde_c.stopScript()

