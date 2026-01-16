"""Console output management for NetExec with capture support."""
from rich.console import Console
from io import StringIO
import threading

# Thread-local capture state
_local = threading.local()

def _is_capturing():
    return getattr(_local, 'capturing', False)

def _get_buffer():
    return getattr(_local, 'buffer', None)


class CapturableConsole(Console):
    """Console that can capture output instead of printing."""
    
    def print(self, *args, **kwargs):
        if _is_capturing() and _get_buffer():
            # Write to buffer instead of stdout
            temp = Console(file=_get_buffer(), force_terminal=False, no_color=True)
            temp.print(*args, **kwargs)
        else:
            super().print(*args, **kwargs)


class OutputCapture:
    """Context manager to capture console output."""
    
    def __init__(self):
        self.buffer = StringIO()
    
    def __enter__(self):
        _local.capturing = True
        _local.buffer = self.buffer
        return self
    
    def __exit__(self, *args):
        _local.capturing = False
        _local.buffer = None
    
    def get_output(self):
        return self.buffer.getvalue()


# Global console - use our capturable version
nxc_console = CapturableConsole(soft_wrap=True, tab_size=4)
