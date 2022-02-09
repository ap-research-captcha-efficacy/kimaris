def kill(input):
    challenge = input.challenge.split(",")[1]
    print(challenge)
    print(input.challenge, input.token, input.appx_gen_time)
    return ("swej", input)