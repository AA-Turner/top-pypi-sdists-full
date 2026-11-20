#include <ur_rtde/rtde_receive_interface.h>
#include <thread>
#include <chrono>
#include <csignal>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <iostream>

using namespace ur_rtde;
using namespace std::chrono;

// Interrupt flag
bool running = true;
void raiseFlag(int param)
{
  running = false;
}

int main(int argc, char* argv[])
{
  try {
    std::string robot_ip = "localhost";
    double frequency = 500.0;
    std::string output = "robot_data.csv";
    bool show_help = false;

    // --------------------------------
    // Parse command line arguments
    // --------------------------------
    for (int i = 1; i < argc; ++i) {
      const std::string arg(argv[i]);
      if (arg == "--help" || arg == "-h") {
        show_help = true;
        continue;
      }

      const std::size_t equals = arg.find('=');
      const std::string name = arg.substr(0, equals);
      std::string value;

      if (equals != std::string::npos) {
        value = arg.substr(equals + 1);
      } else {
        if (i + 1 >= argc) {
          throw std::runtime_error("Missing value for option: " + name);
        }
        value = argv[++i];
      }

      if (name == "--robot_ip") {
        robot_ip = value;
      } else if (name == "--frequency") {
        std::size_t parsed = 0;
        frequency = std::stod(value, &parsed);
        if (parsed != value.size()) {
          throw std::invalid_argument("Invalid frequency: " + value);
        }
      } else if (name == "--output") {
        output = value;
      } else {
        throw std::runtime_error("Unknown option: " + name);
      }
    }

    if (show_help) {
      std::cout << "Allowed options:\n"
                << "  --help, -h          Record robot data to a (.csv) file\n"
                << "  --robot_ip <value>  IP address of the robot (default: localhost)\n"
                << "  --frequency <value> Recording frequency (default: 500Hz)\n"
                << "  --output <value>    Output CSV file (default: robot_data.csv)\n";
      return 0;
    }
    // --------------------------------
    // run script
    // --------------------------------

    std::signal(SIGINT, raiseFlag);
    RTDEReceiveInterface rtde_receive(robot_ip, frequency, {}, true, false);

    rtde_receive.startFileRecording(output);
    std::cout << "Data recording started. press [Ctrl-C] to end recording." << std::endl;
    int i=0;
    while (running)
    {
      steady_clock::time_point t_start = rtde_receive.initPeriod();
      if (i % 10 == 0)
      {
        std::cout << '\r';
        std::cout << std::setfill('0') << std::setw(3) << i << " samples.";
        std::cout << std::flush;
      }
      rtde_receive.waitPeriod(t_start);
      i++;
    }

    // Stop data recording.
    rtde_receive.stopFileRecording();
    std::cout << "\nData recording stopped." << std::endl;
  }
  catch(std::exception& e) {
    std::cerr << "error: " << e.what() << "\n";
    return 1;
  }
  catch(...) {
    std::cerr << "Exception of unknown type!\n";
  }
  return 0;
}
