import sys
from kimaris import kimaris
from timeit import default_timer
endpoint = "http://localhost:5000"
if len(sys.argv) > 1:
    endpoint = sys.argv[1]

trials = 50
scores = {}
k = kimaris(endpoint)
for target in k.targeting_points:
    temp_score = 0
    fails = 0
    for trial in range(trials):
        start = default_timer()
        good = k.attack_captcha(target)
        time_taken = default_timer() - start
        if not good:
            fails += 1
        temp_score += time_taken
    scores[target] = (temp_score/trials, (trials-fails)/trials)
    print(f"finished {target} with {trials} trials and average score {scores[target]}\n")
for k in scores.keys():
    print(k,":", scores[k])