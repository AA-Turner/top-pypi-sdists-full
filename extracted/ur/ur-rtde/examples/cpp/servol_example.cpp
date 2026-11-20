#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>
#include <chrono>
#include <cmath>
#include <csignal>
#include <iostream>
#include <vector>

constexpr double pi = 3.14159265358979323846;

using namespace ur_rtde;
using namespace std::chrono;

static bool should_run = true;

void signal_handler(int /*signum*/)
{
  should_run = false;
}

int main(int argc, char* argv[])
{
  RTDEControlInterface rtde_control("192.168.56.101");
  RTDEReceiveInterface rtde_receive("192.168.56.101");
  std::signal(SIGINT, signal_handler);

  // Parameters
  double dt            = 1.0 / 500; // 2ms - 500 Hz control loop
  double lookahead_time = 0.1;
  double gain          = 800;
  double velocity      = 0.5;
  double acceleration  = 0.5;

  double radius    = 0.05; // circle radius in meters
  double frequency = 0.5;  // Hz - one full circle per 2 seconds

  // Move to a starting pose using moveL
  std::vector<double> start_pose = rtde_receive.getActualTCPPose();
  std::vector<double> init_pose  = start_pose;
  init_pose[0] += radius; // start at the rightmost point of the circle
  rtde_control.moveL(init_pose, velocity, acceleration);

  auto motion_start_time = steady_clock::now();

  try
  {
    while (should_run)
    {
      steady_clock::time_point t_start = rtde_control.initPeriod();
      double elapsed = duration<double>(steady_clock::now() - motion_start_time).count();
      double angle = 2.0 * pi * frequency * elapsed;

      // Circular trajectory in the XY plane of the base frame
      std::vector<double> target = start_pose;
      target[0] = start_pose[0] + radius * std::cos(angle);
      target[1] = start_pose[1] + radius * std::sin(angle);

      rtde_control.servoL(target, velocity, acceleration, dt, lookahead_time, gain);
      rtde_control.waitPeriod(t_start);
    }
  }
  catch (const std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << std::endl;
  }

  std::cout << "Interrupted. Stopping..." << std::endl;
  rtde_control.servoStop();
  rtde_control.stopScript();

  return 0;
}
