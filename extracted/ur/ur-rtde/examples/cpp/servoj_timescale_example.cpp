#include <ur_rtde/dashboard_client.h>
#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>
#include <chrono>
#include <cmath>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <vector>

constexpr double pi = 3.14159265358979323846;

using namespace ur_rtde;
using namespace std::chrono;

// Initial joint position of a URSim.
const std::vector<double> SIM_INITIAL_Q = {-1.6007, -1.7271, -2.203, -0.808, 1.5951, -0.031};

constexpr int32_t ROBOT_MODE_POWER_OFF = 3;
constexpr int32_t ROBOT_MODE_POWER_ON = 4;
constexpr int32_t ROBOT_MODE_IDLE = 5;
constexpr int32_t ROBOT_MODE_RUNNING = 7;

static bool should_run = true;

bool waitForRobotMode(RTDEReceiveInterface& receive, bool (*ready)(int32_t), int timeout_ms)
{
  const auto start = steady_clock::now();
  while (duration_cast<milliseconds>(steady_clock::now() - start).count() < timeout_ms)
  {
    if (ready(receive.getRobotMode()))
      return true;
    std::this_thread::sleep_for(milliseconds(200));
  }
  return ready(receive.getRobotMode());
}

bool poweredForBrakeRelease(int32_t mode)
{
  return mode == ROBOT_MODE_POWER_ON || mode == ROBOT_MODE_IDLE || mode == ROBOT_MODE_RUNNING;
}

bool isRunning(int32_t mode)
{
  return mode == ROBOT_MODE_RUNNING;
}

// Sends dashboard "power on" and "brake release" when needed, then waits until the arm is running.
bool ensureRobotRunning(const std::string& robot_ip, RTDEReceiveInterface& receive)
{
  if (isRunning(receive.getRobotMode()))
    return true;

  DashboardClient dashboard(robot_ip);
  dashboard.connect();

  if (receive.getRobotMode() <= ROBOT_MODE_POWER_OFF)
  {
    std::cout << "Powering on..." << std::endl;
    dashboard.powerOn();
    if (!waitForRobotMode(receive, poweredForBrakeRelease, 60000))
    {
      std::cerr << "Robot did not power on (robot mode " << receive.getRobotMode() << ").\n";
      return false;
    }
  }

  if (!isRunning(receive.getRobotMode()))
  {
    std::cout << "Releasing brakes..." << std::endl;
    dashboard.brakeRelease();
    if (!waitForRobotMode(receive, isRunning, 30000))
    {
      std::cerr << "Brakes were not released (robot mode " << receive.getRobotMode() << ").\n";
      return false;
    }
  }
  return true;
}

void signal_handler(int /*signum*/)
{
  should_run = false;
}

// One sample per control step at full scale. Each cycle is a fast out-and-back
// that starts and ends on q0. Peak joint speed is amplitude * pi / cycle_time.
std::vector<std::vector<double>> makePath(const std::vector<double>& q0, double dt, double cycle_time, int cycles)
{
  const int samples_per_cycle = static_cast<int>(std::llround(cycle_time / dt));
  const int n = samples_per_cycle * cycles + 1;
  const std::vector<double> amplitude = {0.80, -0.70, 0.70, 1.00, -1.00, 1.20};
  std::vector<std::vector<double>> path;
  path.reserve(static_cast<size_t>(n));
  for (int i = 0; i < n; ++i)
  {
    const double s = static_cast<double>(i) / static_cast<double>(samples_per_cycle);
    const double blend = 0.5 * (1.0 - std::cos(2.0 * pi * s));
    std::vector<double> q = q0;
    for (int j = 0; j < 6; ++j)
      q[j] += amplitude[j] * blend;
    path.push_back(q);
  }
  return path;
}

std::vector<double> qAt(const std::vector<std::vector<double>>& path, double cursor)
{
  const double last = static_cast<double>(path.size() - 1);
  if (cursor <= 0.0)
    return path.front();
  if (cursor >= last)
    return path.back();
  const auto i0 = static_cast<size_t>(std::floor(cursor));
  const double frac = cursor - static_cast<double>(i0);
  const std::vector<double>& a = path[i0];
  const std::vector<double>& b = path[i0 + 1];
  std::vector<double> q(6);
  for (size_t j = 0; j < 6; ++j)
    q[j] = a[j] + frac * (b[j] - a[j]);
  return q;
}

int main(int argc, char* argv[])
{
  const std::string robot_ip = (argc > 1) ? argv[1] : "127.0.0.1";
  RTDEReceiveInterface rtde_receive(robot_ip);
  try
  {
    if (!ensureRobotRunning(robot_ip, rtde_receive))
      return 1;
  }
  catch (const std::exception& e)
  {
    std::cerr << e.what() << std::endl;
    return 1;
  }

  // Skip ur_rtde's remote-control check so this can run against a simulator that is not in remote control.
  const uint16_t flags = RTDEControlInterface::FLAG_UPLOAD_SCRIPT | RTDEControlInterface::FLAG_DISABLE_REMOTE_CONTROL_CHECK;
  std::signal(SIGINT, signal_handler);

  std::unique_ptr<RTDEControlInterface> rtde_control;
  try
  {
    rtde_control.reset(new RTDEControlInterface(robot_ip, -1.0, flags));
  }
  catch (const std::exception& e)
  {
    std::cerr << e.what() << "\n"
              << "The control script did not start. Power on the robot and release the brakes, then run the example again.\n";
    return 1;
  }

  const double dt = 1.0 / 500;  // 2 ms
  const double lookahead_time = 0.03;
  const double gain = 800;
  const double cycle_time = 0.5;
  const int cycles = 12;
  const double duration = cycle_time * cycles;

  std::cout << "Moving to the simulator initial joint position." << std::endl;
  if (!rtde_control->moveJ(SIM_INITIAL_Q, 1.05, 1.4))
  {
    std::cerr << "moveJ to the simulator initial position failed." << std::endl;
    rtde_control->stopScript();
    return 1;
  }

  const std::vector<std::vector<double>> path = makePath(SIM_INITIAL_Q, dt, cycle_time, cycles);
  const double last = static_cast<double>(path.size() - 1);

  std::cout << "Playing " << cycles << " fast out-and-back cycles (" << duration
            << " s at full scale) from the simulator initial position.\n"
            << "Move the speed slider to slow or pause the path. Ctrl+C stops.\n"
            << "servoJ leaves fixed_steptime off, so the controller also scales the 2 ms step.\n";

  double cursor = 0.0;
  double last_printed_scale = -1.0;
  int step = 0;

  try
  {
    while (should_run)
    {
      if (cursor > last)
        cursor = last;

      steady_clock::time_point t_start = rtde_control->initPeriod();
      double scale = rtde_receive.getSpeedScalingCombined();
      if (scale < 0.0)
        scale = 0.0;
      else if (scale > 1.0)
        scale = 1.0;

      rtde_control->servoJ(qAt(path, cursor), 0.0, 0.0, dt, lookahead_time, gain);
      rtde_control->waitPeriod(t_start);

      if (step % 250 == 0 || std::abs(scale - last_printed_scale) > 0.02)
      {
        std::cout << "cursor " << cursor << " / " << last << "  scale " << scale << std::endl;
        last_printed_scale = scale;
      }

      if (cursor >= last)
        break;
      cursor += scale;
      ++step;
    }
  }
  catch (const std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << std::endl;
  }

  std::cout << "Stopping robot movement..." << std::endl;
  rtde_control->servoStop();
  rtde_control->stopScript();

  return 0;
}
