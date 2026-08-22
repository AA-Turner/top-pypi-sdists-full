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
import ctypes
from Phidget22._phidget_support import PhidgetSupport


class AsyncSupport:
    __callbacks = {}  # type: ignore
    # Cache for different function signatures to prevent GC of the function objects
    __native_callback_cache = {}  # type: ignore

    @staticmethod
    def add(entry, phid, adapter=None):
        t = (entry, phid, adapter)
        AsyncSupport.__callbacks[id(t)] = t
        return id(t)

    @staticmethod
    def __getAndRemove(id):
        entry = AsyncSupport.__callbacks.get(id)
        if entry:
            del AsyncSupport.__callbacks[id]
        return entry

    @staticmethod
    def __async_callback(handle, ctx, res, *args):
        if ctx is None:
            return

        # Look up the original Python callback and the Phidget object
        entry = AsyncSupport.__getAndRemove(ctx)
        if entry is None:
            return

        callback, phid, adapter = entry

        details = ""
        _code = ctypes.c_int(res)
        _desc = ctypes.c_char_p()
        result = PhidgetSupport.getDll().Phidget_getErrorDescription(_code, ctypes.byref(_desc))
        if result == 0 and _desc.value is not None:
            details = _desc.value.decode("utf-8")

        # If an adapter exists, transform the raw *args into Python objects
        if adapter:
            processed_args = adapter(*args)
            callback(phid, res, details, *processed_args)
        else:
            callback(phid, res, details, *args)

    @staticmethod
    def getCallback(*extra_arg_types):
        # Standard signature prefix: (handle, ctx, res)
        argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
        argtypes.extend(extra_arg_types)

        signature_key = tuple(argtypes)

        if signature_key not in AsyncSupport.__native_callback_cache:
            if sys.platform == "win32":
                functype = ctypes.WINFUNCTYPE(None, *argtypes)
            else:
                functype = ctypes.CFUNCTYPE(None, *argtypes)

            AsyncSupport.__native_callback_cache[signature_key] = functype(
                AsyncSupport.__async_callback
            )

        return AsyncSupport.__native_callback_cache[signature_key]
