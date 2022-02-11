from hashlib import sha256
from secrets import token_hex
from threading import Thread

def kill(input):
    key = input.challenge.split(",")[1]
    while True:
        guess = token_hex(3)
        if sha256(guess.encode("ascii")).hexdigest() == key:
            print("found >> ", guess)
            return (guess, input)