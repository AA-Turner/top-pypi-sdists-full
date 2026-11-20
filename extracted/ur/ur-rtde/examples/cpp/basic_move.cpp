#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>
#include <cmath>
#include <iostream>
#include <vector>

constexpr double pi = 3.14159265358979323846;

using namespace ur_rtde;

int main(int argc, char* argv[])
{
  RTDEControlInterface rtde_control("192.168.56.101");
  RTDEReceiveInterface rtde_receive("192.168.56.101");

  // Move to a safe home position using moveJ (joint space)
  // Arguments: joint positions [rad], speed [rad/s], acceleration [rad/s^2]
  std::vector<double> home_q = {-pi/2, -pi/2, -pi/2, -pi/2, pi/2, 0.0};
  rtde_control.moveJ(home_q, 0.5, 0.5);

  // Read the TCP pose after arriving at home so moveL targets are always valid
  // Pose: [x, y, z, rx, ry, rz] in meters and axis-angle [rad]
  std::vector<double> tcp_pose = rtde_receive.getActualTCPPose();
  std::cout << "TCP pose at home: "
            << tcp_pose[0] << ", " << tcp_pose[1] << ", " << tcp_pose[2] << std::endl;

  // Move 15 cm down in Z using moveL (Cartesian linear move)
  // Arguments: pose, speed [m/s], acceleration [m/s^2]
  std::vector<double> pose_down = tcp_pose;
  pose_down[2] -= 0.15;
  rtde_control.moveL(pose_down, 0.25, 0.5);

  // Move 10 cm in X
  std::vector<double> pose_side = pose_down;
  pose_side[0] += 0.10;
  rtde_control.moveL(pose_side, 0.25, 0.5);

  // Return to home TCP pose
  rtde_control.moveL(tcp_pose, 0.25, 0.5);

  // Return to home joint configuration
  rtde_control.moveJ(home_q, 0.5, 0.5);

  rtde_control.stopScript();

  return 0;
}
