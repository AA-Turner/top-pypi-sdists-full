#include <ur_rtde/rtde_control_interface.h>
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
  std::signal(SIGINT, signal_handler);

  // Parameters
  double dt = 1.0 / 500; // 2ms
  double lookahead_time = 0.1;
  double gain = 800;
  const std::vector<double> joint_q_start = {-pi / 2, -pi / 2, -pi / 2, -pi / 2, pi / 2, 0.0};

  // Move to initial joint position with a regular moveJ
  rtde_control.moveJ(joint_q_start);

  // Continuous small sinusoidal motion on all 6 joints
  const std::vector<double> amplitudes   = {0.03, 0.03, 0.03, 0.02, 0.02, 0.02}; // rad
  const std::vector<double> frequencies  = {0.5,  0.6,  0.7,  0.8,  0.9,  1.0};  // Hz
  const std::vector<double> phases       = {0.0,  pi / 6.0, pi / 3.0,
                                            pi / 2.0, 2.0 * pi / 3.0, 5.0 * pi / 6.0};

  auto motion_start_time = steady_clock::now();
  std::vector<double> joint_q(6);

  try
  {
    while (should_run)
    {
      steady_clock::time_point t_start = rtde_control.initPeriod();
      double elapsed = duration<double>(steady_clock::now() - motion_start_time).count();

      for (int i = 0; i < 6; i++)
        joint_q[i] = joint_q_start[i] + amplitudes[i] * std::sin(2.0 * pi * frequencies[i] * elapsed + phases[i]);

      rtde_control.servoJ(joint_q, 0.0, 0.0, dt, lookahead_time, gain);
      rtde_control.waitPeriod(t_start);
    }
  }
  catch (const std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << std::endl;
  }

  std::cout << "Stopping robot movement..." << std::endl;
  rtde_control.servoStop();
  rtde_control.stopScript();

  return 0;
}
