from contextlib import contextmanager
import argparse

@contextmanager
def argparse_full_errors():
    original = argparse.ArgumentParser.error
    def error_with_traceback(self, message):
        raise ValueError(f"argparse error: {message}\nprog: {self.prog}")
    argparse.ArgumentParser.error = error_with_traceback
    try:
        yield
    finally:
        argparse.ArgumentParser.error = original
