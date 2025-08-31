import time
from collections.abc import Callable

from constants import *


# TODO: decorator check function processing speed
def show_latency(func: Callable):
    def wapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        
        debug("%s took %ims" % (func.__qualname__, (t1 - t0) * 1000))
        
        return result
    return wapper

import sys


def is_debug_mode() -> bool:
    return len(sys.argv) > 1 and sys.argv[1] == '--debug'

def debug(*args):
    if is_debug_mode():
        print(f"[{FG_AQUA + 'd' + RESET}]", *args)

def clamp(nmin: int, n: int, nmax: int) -> int:
    return max(nmin, min(n, nmax))