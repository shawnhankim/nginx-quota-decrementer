import threading
import time

from utils import debug

def thread_function(name):
    debug(f"Thread {name}: starting")
    time.sleep(5)
    debug(f"Thread {name}: finishing")

def quota_decrement():
    debug("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    debug("Main    : before running thread")
    x.start()
    debug("Main    : wait for the thread to finish")
    # x.join()
    debug("Main    : all done")


