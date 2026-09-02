import sys
import logging
from contextlib import contextmanager

def _patch_logging_handlers():
    """Temporarily protect logging StreamHandler to avoid BrokenPipeError"""
    # Protect root logger handlers
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.StreamHandler):
            _make_handler_safe(handler)
    
    # Protect all registered logger handlers
    for logger_name in logging.Logger.manager.loggerDict:
        logger_obj = logging.getLogger(logger_name)
        if hasattr(logger_obj, 'handlers'):
            for handler in logger_obj.handlers[:]:
                if isinstance(handler, logging.StreamHandler):
                    _make_handler_safe(handler)


def _make_handler_safe(handler):
    """Add error protection to a single handler"""
    if hasattr(handler, '_novita_patched'):
        # Already patched, avoid duplicate patching
        return
    
    original_emit = handler.emit
    
    def safe_emit(record):
        try:
            original_emit(record)
        except (BrokenPipeError, OSError, ValueError, IOError):
            # Silently ignore stream errors
            pass
        except Exception:
            # Other exceptions still need to be handled, but cannot interrupt the program
            pass
    
    def silent_handle_error(record):
        """Silently handle errors without printing to stderr"""
        # Completely suppress error output to avoid "--- Logging error ---" messages
        pass
    
    handler.emit = safe_emit
    handler.handleError = silent_handle_error  # Override handleError to suppress error messages
    handler._novita_patched = True  # Mark as patched


@contextmanager
def safe_stdout_context(logger_instance=None):
    """
    Complete standard stream safety context manager
    
    Protects all operations that may trigger BrokenPipeError:
    - print() and sys.stdout.write()
    - sys.stderr.write() and exception output
    - logging StreamHandler
    - Third-party library output
    
    Args:
        logger_instance: Optional logger for recording intercepted stdout/stderr output
    """
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_stdin = sys.stdin
    original_raise_exceptions = logging.raiseExceptions
    
    class SafeWriter:
        """Completely safe writer"""
        def __init__(self, original, logger=None, level='info'):
            self.original = original
            self.logger = logger
            self.level = level
            self.encoding = getattr(original, 'encoding', 'utf-8')
            self.errors = getattr(original, 'errors', 'replace')
        
        def write(self, message):
            try:
                # Try to write to original stream
                if hasattr(self.original, 'write') and not self._is_closed():
                    self.original.write(message)
                    return
            except (BrokenPipeError, OSError, ValueError, IOError):
                # Stream unavailable, log to logger
                if self.logger and message and message.strip():
                    log_msg = f"[{'STDERR' if self.level == 'error' else 'STDOUT'}] {message.rstrip()}"
                    if self.level == 'error':
                        self.logger.debug(log_msg)
                    else:
                        self.logger.debug(log_msg)
            except Exception:
                # Silently ignore other errors
                pass
        
        def _is_closed(self):
            """Check if stream is closed"""
            try:
                return self.original.closed if hasattr(self.original, 'closed') else False
            except:
                return True
        
        def flush(self):
            try:
                if hasattr(self.original, 'flush') and not self._is_closed():
                    self.original.flush()
            except (BrokenPipeError, OSError, ValueError, IOError):
                pass
            except Exception:
                pass
        
        def isatty(self):
            try:
                return self.original.isatty() if hasattr(self.original, 'isatty') else False
            except:
                return False
        
        def fileno(self):
            try:
                return self.original.fileno() if hasattr(self.original, 'fileno') else -1
            except:
                return -1
        
        def __getattr__(self, name):
            """Proxy other attributes to original stream"""
            try:
                return getattr(self.original, name)
            except:
                return lambda *args, **kwargs: None
    
    class SafeReader:
        """Safe reader (for stdin)"""
        def __init__(self, original):
            self.original = original
        
        def read(self, *args, **kwargs):
            try:
                if hasattr(self.original, 'read'):
                    return self.original.read(*args, **kwargs)
            except Exception:
                return ""
        
        def readline(self, *args, **kwargs):
            try:
                if hasattr(self.original, 'readline'):
                    return self.original.readline(*args, **kwargs)
            except Exception:
                return ""
        
        def __getattr__(self, name):
            try:
                return getattr(self.original, name)
            except:
                return lambda *args, **kwargs: None
    
    try:
        # Disable logging error messages to stderr
        logging.raiseExceptions = False
        
        # Replace standard streams
        sys.stdout = SafeWriter(original_stdout, logger_instance, 'info')
        sys.stderr = SafeWriter(original_stderr, logger_instance, 'error')
        sys.stdin = SafeReader(original_stdin)
        
        # Protect logging handlers (does not need logger_instance)
        _patch_logging_handlers()
        
        yield
        
    finally:
        # Restore original streams
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        sys.stdin = original_stdin
        
        # Restore logging error handling
        logging.raiseExceptions = original_raise_exceptions