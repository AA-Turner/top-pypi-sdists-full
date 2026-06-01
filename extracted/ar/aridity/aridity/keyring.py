from .model import Scalar
from base64 import b64decode
from subprocess import CalledProcessError, check_output
from tempfile import NamedTemporaryFile

class Password(str):

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        pass

class DecryptionFailedException(Exception): pass

def gpg(scope, resolvable):
    'Use gpg to decrypt the given base64-encoded blob.'
    with NamedTemporaryFile() as f:
        f.write(b64decode(resolvable.resolve(scope).textvalue))
        f.flush()
        try:
            return Scalar(Password(check_output(['gpg', '-d', f.name]).decode('ascii')))
        except CalledProcessError:
            raise DecryptionFailedException
