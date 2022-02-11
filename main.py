import sys
from kimaris import kimaris
from timeit import default_timer
endpoint = "http://localhost:5000"
if len(sys.argv) > 1:
    endpoint = sys.argv[1]
k = kimaris(endpoint)
for target in k.targeting_points:
    start = default_timer()
    k.attack_captcha(target)
    end = default_timer()
    print(f"finished with {target} in {end-start}")