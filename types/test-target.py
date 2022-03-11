from hashlib import sha256
from secrets import token_hex
from threading import Thread

def kill(input, options = []):
    key = input.challenge.split(",")[1]
    while True:
        guess = token_hex(2)
        if sha256(guess.encode("ascii")).hexdigest() == key:
            return (guess, input)