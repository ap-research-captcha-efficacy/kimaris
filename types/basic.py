from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode
import pytesseract


def kill(input, options = []):
    challenge = input.challenge.split("base64,")[1]
    challenge = b64decode(challenge.encode("ascii"))
    data = BytesIO(challenge)
    img = Image.open(data).convert("L")
    solution = pytesseract.image_to_string(img)[0:6]
    if "limitchars" in options:
        solution = solution.lower()
    # img.show()
    return (solution, input)