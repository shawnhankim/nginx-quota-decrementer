import threading
import time

from utils import debug

def decrement_thread(name, env):
    debug(f"Thread {name}: starting")
    quota_id = env['HTTP_X_QUOTA_ID'] if 'HTTP_X_QUOTA_ID' in env else ''
    zone_name = env['HTTP_X_QUOTA_ZONE'] if 'HTTP_X_QUOTA_ZONE' in env else ''
    debug(f"  - quota ID   : {quota_id}")
    debug(f"  - quota Zone : {zone_name}")
    time.sleep(5)
    debug(f"Thread {name}: finishing")

def quota_decrement(env):
    debug("Main    : before creating thread")

    x = threading.Thread(target=decrement_thread, args=(1, env))
    debug("Main    : before running thread")
    x.start()
    debug("Main    : wait for the thread to finish")
    # x.join()
    debug("Main    : all done")


