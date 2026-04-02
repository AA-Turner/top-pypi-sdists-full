import fancy_subprocess
from typing import Unpack

def grab_output(cmd: list[str], **kwargs: Unpack[fancy_subprocess.RunParams]) -> str:
    # Raises ValueError if there are unknown parameters in kwargs or if a keyword argument's type is incorrect
    fancy_subprocess.check_run_params(**kwargs)

    # Make a copy of keyword arguments to be edited
    forwarded_args = kwargs.copy()
    # Make sure nothing's printed, raise ValueError if caller tries to specify "output_quiet" or "message_quiet"
    fancy_subprocess.force_run_params(forwarded_args, message_quiet=True, output_quiet=True)
    # Handle encoding/decoding errors by replacing them with placeholder character by default, but allow callers to still customize behaviour
    fancy_subprocess.change_default_run_params(forwarded_args, errors='replace')

    # Run command, raise fancy_subprocess.RunError on failure
    result = fancy_subprocess.run(cmd, **forwarded_args)

    # Return combined stdout and stderr
    return result.output

comspec = grab_output(['cmd', '/c', 'echo', '%COMSPEC%'])
print(f'COMSPEC={comspec}')

files = grab_output(['cmd', '/c', 'dirr', '/b', '/o:n'], retry=2) # "dir" intentionally misspelled as "dirr"
print('Files in current directory:')
print(files)
