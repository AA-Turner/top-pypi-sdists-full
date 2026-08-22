# Copyright (c) 2015-2026 Phidgets Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os


class PhidgetSupport:
    __dll = None

    @staticmethod
    def getDll():
        if PhidgetSupport.__dll is None:
            libs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".libs")
            if sys.platform == "win32":
                from ctypes import windll

                if os.path.exists(os.path.join(libs_path, "phidget22.dll")):
                    PhidgetSupport.__dll = windll.LoadLibrary(
                        os.path.join(libs_path, "phidget22.dll")
                    )
                else:
                    PhidgetSupport.__dll = windll.LoadLibrary("phidget22.dll")
            elif sys.platform == "darwin":
                from ctypes import cdll

                if os.path.exists(os.path.join(libs_path, "libphidget22.dylib")):
                    PhidgetSupport.__dll = cdll.LoadLibrary(
                        os.path.join(libs_path, "libphidget22.dylib")
                    )
                else:
                    PhidgetSupport.__dll = cdll.LoadLibrary("libphidget22.dylib")
            else:
                from ctypes import cdll

                if os.path.exists(os.path.join(libs_path, "libphidget22.so")):
                    PhidgetSupport.__dll = cdll.LoadLibrary(
                        os.path.join(libs_path, "libphidget22.so")
                    )
                else:
                    PhidgetSupport.__dll = cdll.LoadLibrary("libphidget22.so.0")
        return PhidgetSupport.__dll
