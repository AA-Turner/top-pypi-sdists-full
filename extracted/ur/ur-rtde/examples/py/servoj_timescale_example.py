import sys
import time
import numpy as np
from dashboard_client import DashboardClient
from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive

# Initial joint position of a URSim.
SIM_INITIAL_Q = [-1.6007, -1.7271, -2.203, -0.808, 1.5951, -0.031]

ROBOT_MODE_POWER_OFF = 3
ROBOT_MODE_POWER_ON = 4
ROBOT_MODE_IDLE = 5
ROBOT_MODE_RUNNING = 7

def wait_for_robot_mode(rtde_r, ready, timeout_s):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if ready(rtde_r.getRobotMode()):
            return True
        time.sleep(0.2)
    return ready(rtde_r.getRobotMode())

def ensure_robot_running(robot_ip, rtde_r):
    if rtde_r.getRobotMode() == ROBOT_MODE_RUNNING:
        return
    dashboard = DashboardClient(robot_ip)
    dashboard.connect()
    try:
        if rtde_r.getRobotMode() <= ROBOT_MODE_POWER_OFF:
            print("Powering on...")
            dashboard.powerOn()
            if not wait_for_robot_mode(rtde_r, lambda mode: mode in (ROBOT_MODE_POWER_ON, ROBOT_MODE_IDLE, ROBOT_MODE_RUNNING), 60):
                sys.exit("Robot did not power on (robot mode %d)." % rtde_r.getRobotMode())
        if rtde_r.getRobotMode() != ROBOT_MODE_RUNNING:
            print("Releasing brakes...")
            dashboard.brakeRelease()
            if not wait_for_robot_mode(rtde_r, lambda mode: mode == ROBOT_MODE_RUNNING, 30):
                sys.exit("Brakes were not released (robot mode %d)." % rtde_r.getRobotMode())
    finally:
        dashboard.disconnect()

robot_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
rtde_r = RTDEReceive(robot_ip)
ensure_robot_running(robot_ip, rtde_r)

# Skip ur_rtde's remote-control check so this can run against a simulator that is not in remote control.
flags = RTDEControl.FLAG_UPLOAD_SCRIPT | RTDEControl.FLAG_DISABLE_REMOTE_CONTROL_CHECK
try:
    rtde_c = RTDEControl(robot_ip, -1.0, flags)
except Exception as e:
    sys.exit("%s\nThe control script did not start. Power on the robot and release the brakes, then run the example again." % e)

# One sample per control step at full scale. Each cycle is a fast out-and-back.
# The cursor advances by getSpeedScalingCombined(), which is
# speed_scaling * target_speed_fraction.
# servoJ leaves fixed_steptime off, so the controller also scales the 2 ms step.
dt = 1.0 / 500  # 2 ms
lookahead_time = 0.03
gain = 800
cycle_time = 0.5
cycles = 12
duration = cycle_time * cycles
amplitude = np.array([0.80, -0.70, 0.70, 1.00, -1.00, 1.20])

print("Moving to the simulator initial joint position.")
if not rtde_c.moveJ(SIM_INITIAL_Q, 1.05, 1.4):
    rtde_c.stopScript()
    sys.exit("moveJ to the simulator initial position failed.")

q0 = np.array(SIM_INITIAL_Q, dtype=float)
samples_per_cycle = int(round(cycle_time / dt))
n = samples_per_cycle * cycles + 1
s = np.arange(n) / float(samples_per_cycle)
blend = 0.5 * (1.0 - np.cos(2.0 * np.pi * s))
path = q0 + blend[:, None] * amplitude
last = float(n - 1)

print("Playing %d fast out-and-back cycles (%.1f s at full scale) from the simulator initial position." % (cycles, duration))
print("Move the speed slider to slow or pause the path. Ctrl+C stops.")

cursor = 0.0
last_printed_scale = -1.0
step = 0

try:
    while True:
        if cursor > last:
            cursor = last
        t_start = rtde_c.initPeriod()
        scale = rtde_r.getSpeedScalingCombined()
        scale = min(1.0, max(0.0, scale))

        i0 = int(np.floor(cursor))
        if i0 >= n - 1:
            joint_q = path[-1]
        else:
            frac = cursor - i0
            joint_q = path[i0] + frac * (path[i0 + 1] - path[i0])
        rtde_c.servoJ(joint_q.tolist(), 0.0, 0.0, dt, lookahead_time, gain)
        rtde_c.waitPeriod(t_start)

        if step % 250 == 0 or abs(scale - last_printed_scale) > 0.02:
            print("cursor %.1f / %.1f  scale %.3f" % (cursor, last, scale))
            last_printed_scale = scale

        if cursor >= last:
            break
        cursor += scale
        step += 1
except KeyboardInterrupt:
    print("KeyboardInterrupt received.")
finally:
    print("Stopping robot movement...")
    rtde_c.servoStop()
    rtde_c.stopScript()
