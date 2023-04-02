import logging

from quota_decrement import quota_decrement

def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    quota_decrement()
    return (b"Hello, NGINX Quota Decrementer on Unit!\n")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
