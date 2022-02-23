import sys
from kimaris import kimaris
from timeit import default_timer
endpoint = "http://localhost:5000"
if len(sys.argv) > 1:
    endpoint = sys.argv[1]

trials = 3
scores = {}
k = kimaris(endpoint)
for target in k.targeting_points:
    temp_score = 0
    for trial in range(trials):
        start = default_timer()
        k.attack_captcha(target)
        time_taken = default_timer() - start
        temp_score += time_taken
    scores[target] = temp_score/3
    print(f"finished {target} with {trials} trials and average score {scores[target]}")
print(scores)