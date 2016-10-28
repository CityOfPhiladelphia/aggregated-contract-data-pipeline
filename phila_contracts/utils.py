import sys
from contextlib import contextmanager


@contextmanager
def open_or_stream(filename, mode=None):
    """
    Use the specified file, stdin, or stdout as the open file as appropriate.
    This function may be used as a context manager. In the case that the stream
    is a file, the file will be closed on exit. In the case that stdin/stdout
    is the stream, nothing will happen on exit.
    """
    if filename == '-':
        if mode is None or mode.startswith('r'):
            yield sys.stdin
        else:
            yield sys.stdout
    else:
        with open(filename) as opened_file:
            yield opened_file
