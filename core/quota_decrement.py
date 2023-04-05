import json
import requests
import time
from threading import (
    Lock,
    Thread
)
from utils import debug


NGINX_PLUS_HOST_PORT = 'http://host.docker.internal:2000'
NGINX_PLUS_KEY_VAL_URI = '/api/7/http/keyvals/'

mtx = {}

def quota_decrement_thread(lock, zone_id, zone_name):
    debug(f"Thread {zone_name}: starting")
    try:
        url = f"{NGINX_PLUS_HOST_PORT}{NGINX_PLUS_KEY_VAL_URI}{zone_name}"
        with lock: # TODO: mutex timeout
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
            debug(f"quota zone updated (quota_remaining: {quota_remaining})")
            time.sleep(2)
    except:
        debug('error when connecting to NGINX Plus')

    debug(f"Thread {zone_name}: finishing")


def quota_decrement(env):
    zone_id = env['HTTP_X_QUOTA_ID'] if 'HTTP_X_QUOTA_ID' in env else ''
    zone_name = env['HTTP_X_QUOTA_ZONE'] if 'HTTP_X_QUOTA_ZONE' in env else ''
    
    debug(f"Main: start creating thread {zone_name}")
    if zone_name not in mtx:
        mtx[zone_name] = Lock()
    Thread(
        target=quota_decrement_thread, 
        args=(mtx[zone_name], zone_id, zone_name)
    ).start()

    debug(f"Main: thread request done for {zone_name}")
