from fabric.runners import Remote
from invoke.terminals import WINDOWS
from invoke.util import has_fileno, isatty


class InteractiveRemote(Remote):
    def read_our_stdin(self, input_):
        try:
            return super().read_our_stdin(input_)
        except SystemError as exc:
            if str(exc) != "buffer overflow" or WINDOWS or not isatty(input_) or not has_fileno(input_):
                raise

        # Invoke uses a short-sized buffer for FIONREAD, which writes a C int.
        # Python 3.14 rejects that overflow and leaves interactive sessions
        # without stdin. Retry with the correct size until Invoke fixes it:
        # https://github.com/pyinvoke/invoke/pull/1077
        import fcntl
        import struct
        import termios

        available = fcntl.ioctl(input_, termios.FIONREAD, struct.pack("i", 0))
        data = input_.read(struct.unpack("i", available)[0])
        return self.decode(data) if isinstance(data, bytes) else data
