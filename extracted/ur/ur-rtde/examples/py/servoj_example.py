import time
import numpy as np
from rtde_control import RTDEControlInterface as RTDEControl

rtde_c = RTDEControl("127.0.0.1")

# Parameters
dt = 1.0/500  # 2ms
lookahead_time = 0.1
gain = 800
joint_q = [-np.pi/2, -np.pi/2, -np.pi/2, -np.pi/2, np.pi/2, 0.0]

# Move to initial joint position with a regular moveJ
rtde_c.moveJ(joint_q)

# Continuous small sinusoidal motion on all 6 joints.
joint_q_start = np.array(joint_q, dtype=float)
amplitudes = np.array([0.03, 0.03, 0.03, 0.02, 0.02, 0.02], dtype=float)  # rad
frequencies = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0], dtype=float)  # Hz
phases = np.array([0.0, np.pi / 6.0, np.pi / 3.0, np.pi / 2.0, 2.0 * np.pi / 3.0, 5.0 * np.pi / 6.0], dtype=float)
motion_start_time = time.time()

try:
	while True:
		t_start = rtde_c.initPeriod()
		elapsed = time.time() - motion_start_time
		sine_argument = 2.0 * np.pi * frequencies * elapsed + phases
		joint_q = (joint_q_start + amplitudes * np.sin(sine_argument)).tolist()
		rtde_c.servoJ(joint_q, 0.0, 0.0, dt, lookahead_time, gain)
		rtde_c.waitPeriod(t_start)
except KeyboardInterrupt:
	print("KeyboardInterrupt received. Stopping robot movement...")
finally:
	rtde_c.servoStop()
	rtde_c.stopScript()
