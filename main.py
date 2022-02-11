import sys
from kimaris import kimaris
endpoint = "http://localhost:5000"
if len(sys.argv) > 1:
    endpoint = sys.argv[1]
k = kimaris(endpoint)
k.attack_captcha("test-target")