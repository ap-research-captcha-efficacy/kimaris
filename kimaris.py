import requests, json, sys, os
from datetime import datetime
class captcha_context():
    def __init__(self, challenge, token, appx_gen_time):
        self.challenge = challenge
        self.token = token
        self.appx_gen_time = appx_gen_time
    def is_approximately_expired(self):
        return ((datetime.now().timestamp() - self.appx_gen_time) > 119)

class kimaris():
    def __init__(self, target):
        self.endpoint = target
        self.targeting_points = json.loads(self.__wrap_critical_get(self.endpoint+"/captchas").text)["captchas"]
        self.suite = {}
        self.__load_types()
    def attack_captcha(self, name):
        if not(name in self.targeting_points):
            print("target not on endpoint\nbailing...")
            return
        oname = name
        name = name.split("?modifiers=")[0]
        if not(name in self.suite):
            print("no module found for target")
            return
        try:
            print(oname)
            ans = getattr(self.suite[name], "kill")(self.get_captcha_response(oname))
            # print(ans[0])
            if self.test_solution(ans[0], ans[1].token):
                print(f"successfully killed {name} with {ans[0]}")
                return True
            else:
                print(f"/solution check failed for {name}, likely a solving error")
        except Exception as e:
            print(e)
            print("error calling killer")
        return False
    def test_solution(self, sol, token):
        return (self.__wrap_critical_get(self.endpoint+"/solution", params={"proposal": sol, "token": token}).status_code == 200)
    def get_captcha_response(self, name, mods = []):
        if not(name.split("?modifiers=")[0] in self.targeting_points):
            print("target not on endpoint\nbailing...")
            return
        res = json.loads(self.__wrap_critical_get(self.endpoint+"/captcha/"+name).text)
        return captcha_context(res["challenge"], res["token"], datetime.now().timestamp())
    def __load_types(self):
        sys.path.append("./types")
        types = [name.split(".py")[0] for name in os.listdir("./types") if name.endswith(".py")]
        for type in types:
            try:
                module = __import__(type)
            except: 
                print(f"error loading type {type}")
                continue
            if not(hasattr(module, "kill")):
                print(f"type {type} is invalid: crucial attribute missing!")
                continue
            else:
                self.suite[module.__name__] = module
                print(f"loaded type {module.__name__}")
    def __wrap_critical_get(self, url, **kwargs):
        try:
            return requests.get(url, **kwargs)
        except:
            print("presumably fatal error in GET request, check your endpoint")
            sys.exit(-1)