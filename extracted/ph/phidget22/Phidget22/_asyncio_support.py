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

import asyncio
from Phidget22.PhidgetException import PhidgetException


# Used to bridge the old-style async calls to the new async/await syntax. Not intended for public use.
async def wrap_async_call(async_func, *args):
    loop = asyncio.get_event_loop()
    future = asyncio.Future(loop=loop)

    def internal_callback(ch, res, details, *extra_args):
        # We check the error code first
        if res != 0:
            loop.call_soon_threadsafe(future.set_exception, PhidgetException(res))
        else:
            # If there are extra args return them.
            # If only one extra arg exists, return it directly; otherwise return a tuple.
            if len(extra_args) == 1:
                loop.call_soon_threadsafe(future.set_result, extra_args[0])
            elif len(extra_args) > 1:
                loop.call_soon_threadsafe(future.set_result, extra_args)
            else:
                loop.call_soon_threadsafe(future.set_result, None)

    # Call the library function with the handler
    async_func(*args, asyncHandler=internal_callback)

    # Await the result. The exception will be raised here if res != 0
    return await future
