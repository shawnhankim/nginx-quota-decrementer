from datetime import datetime
import logging

def debug(msg):
    logging.info(msg)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time + ': ' + msg)
    f = open("/var/log/quota/quota.log", "a")
    f.write(current_time + ': ' + msg + '\n')
    f.close()

