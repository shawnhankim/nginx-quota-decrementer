import logging
import threading
import time
from datetime import datetime


def debug(msg):
    logging.info(msg)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time + ': ' + msg)
    f = open("/var/log/quota/quota.log", "a")
    f.write(current_time + ': ' + msg + '\n')
    f.close()


def thread_function(name):
    debug(f"Thread {name}: starting")
    time.sleep(5)
    debug(f"Thread {name}: finishing")


def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    debug("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    debug("Main    : before running thread")
    x.start()
    debug("Main    : wait for the thread to finish")
    # x.join()
    debug("Main    : all done")

    return (b"Hello, NGINX Quota Decrementer on Unit!\n")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
