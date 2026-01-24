/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#ifndef _COMMAND_H_
#define _COMMAND_H_

#include "common_header.h"

class PyCmd : public Tango::Command {
  public:
    PyCmd(std::string &command_name,
          Tango::CmdArgType in,
          Tango::CmdArgType out,
          std::string &in_desc,
          std::string &out_desc,
          Tango::DispLevel level) :
        Tango::Command(command_name, in, out, in_desc, out_desc, level),
        py_allowed_defined(false) { }

    PyCmd(const char *command_name, Tango::CmdArgType in, Tango::CmdArgType out) :
        Tango::Command(command_name, in, out),
        py_allowed_defined(false) { }

    PyCmd(const char *command_name,
          Tango::CmdArgType in,
          Tango::CmdArgType out,
          const char *in_desc,
          const char *out_desc,
          Tango::DispLevel level) :
        Tango::Command(command_name, in, out, in_desc, out_desc, level),
        py_allowed_defined(false) { }

    ~PyCmd() override = default;

    CORBA::Any *execute(Tango::DeviceImpl *dev, const CORBA::Any &any) override;
    bool is_allowed(Tango::DeviceImpl *dev, const CORBA::Any &any) override;

    void set_allowed(const std::string &f_name) {
        py_allowed_defined = true;
        py_allowed_name = f_name;
    }

  private:
    bool py_allowed_defined;
    std::string py_allowed_name;
};

#endif
