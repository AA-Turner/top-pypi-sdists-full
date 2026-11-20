#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>
#include <chrono>
#include <cmath>
#include <csignal>
#include <iostream>
#include <thread>
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
  RTDEControlInterface  rtde_control("192.168.56.101");
  RTDEReceiveInterface  rtde_receive("192.168.56.101");
  std::signal(SIGINT, signal_handler);

  // Task parameters
  std::vector<double> task_frame       = {0, 0, 0, 0, 0, 0};
  std::vector<int>    compliance_vector = {1, 1, 1, 0, 0, 0};
  std::vector<double> init_q           = {-pi/2, -pi/2, -pi/2, -pi/2, pi/2, 0.0};
  std::vector<double> v_max            = {0.5, 0.5, 0.5, 0.2, 0.2, 0.2};

  // Spiral search parameters
  double F_tangential      = 30.0; // N - tangential force keeping the robot orbiting
  double growth_rate_mm_s  = 1.0;  // mm/s - desired outward radial growth rate (easy to tune)
  double z_force           = -5.0; // N - downward force
  double F_radial = F_tangential * (growth_rate_mm_s / 1000.0) / v_max[0];

  // Move to initial joint position
  rtde_control.moveJ(init_q);
  rtde_control.zeroFtSensor();
  std::this_thread::sleep_for(milliseconds(200));

  // Record the starting TCP position — the spiral center
  std::vector<double> start_tcp = rtde_receive.getActualTCPPose();
  double start_x = start_tcp[0];
  double start_y = start_tcp[1];

  try
  {
    while (should_run)
    {
      steady_clock::time_point t_start = rtde_control.initPeriod();

      // Compute force direction based on current position relative to spiral center
      std::vector<double> tcp = rtde_receive.getActualTCPPose();
      double dx = tcp[0] - start_x;
      double dy = tcp[1] - start_y;
      double r  = std::sqrt(dx*dx + dy*dy);

      double cos_phi, sin_phi;
      if (r > 0.001) 
      {
        cos_phi = dx / r;
        sin_phi = dy / r;
      } 
      else 
      {
        cos_phi = 1.0; sin_phi = 0.0;
      }

      double Fx = F_tangential * (-sin_phi) + F_radial * cos_phi;
      double Fy = F_tangential * cos_phi  + F_radial * sin_phi;
      double Fz = z_force;

      rtde_control.forceMode(task_frame, compliance_vector, {Fx, Fy, Fz, 0, 0, 0}, 2, v_max);
      rtde_control.waitPeriod(t_start);
    }
  }
  catch (const std::exception& e)
  {
    std::cerr << e.what() << std::endl;
  }

  std::cout << "Stopped spiral search" << std::endl;
  rtde_control.forceModeStop();
  rtde_control.stopScript();

  return 0;
}

