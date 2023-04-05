import json
import requests
import threading
import time

from utils import debug

NGINX_PLUS_HOST_PORT = 'http://host.docker.internal:2000'
NGINX_PLUS_KEY_VAL_URI = '/api/7/http/keyvals/'

def quota_decrement_thread(name, env):
    debug(f"Thread {name}: starting")
    zone_id = env['HTTP_X_QUOTA_ID'] if 'HTTP_X_QUOTA_ID' in env else ''
    zone_name = env['HTTP_X_QUOTA_ZONE'] if 'HTTP_X_QUOTA_ZONE' in env else ''

    try:
        # TODO: Mutex 
        url = f"{NGINX_PLUS_HOST_PORT}{NGINX_PLUS_KEY_VAL_URI}{zone_name}"
        res = requests.get(url, params={'key': zone_id})
        if res.status_code != 200:
            debug(f"  GET quotas response : {res.status_code}")
            return

        data = res.json()
        quotas = data[zone_id] if zone_id in data else ''
        if not quotas:
            debug(f"quota not found for {zone_id}")
            return
        quotas = quotas.split(',')
        quota_remaining = int(quotas[1]) - 1
        quotas[1] = f"{quota_remaining}"
        quotas = ",".join(quotas)
        head = {'Content-Type': 'application/json'}
        res = requests.patch(
            url, data=json.dumps({zone_id: quotas}), headers=head
        )
        if res.status_code != 204:
            debug(f"  PATCH quotas response : {res.status_code}")
            return
        debug(f"quota zone updated (quota_remaining: {quota_remaining})")
    except:
        debug('error when connecting to NGINX Plus')

    time.sleep(5)
    debug(f"Thread {name}: finishing")

def quota_decrement(env):
    debug("Main    : before creating thread")

    x = threading.Thread(target=quota_decrement_thread, args=(1, env))
    debug("Main    : before running thread")
    x.start()
    debug("Main    : wait for the thread to finish")
    # x.join()
    debug("Main    : all done")


