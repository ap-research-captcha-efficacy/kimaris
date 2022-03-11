from PIL import Image, ImageFilter
from io import BytesIO
from base64 import b64encode, b64decode
import pytesseract


def kill(input, options = []):
    challenge = input.challenge.split("base64,")[1]
    challenge = b64decode(challenge.encode("ascii"))
    data = BytesIO(challenge)
    img = Image.open(data).convert("L")

    if "removelines" in options:
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.convert("L")
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixel = img.getpixel((i, j))
                if pixel < 90:
                    img.putpixel((i,j), 0)
                else:
                    img.putpixel((i,j), 255)

    # img.show()
    solution = pytesseract.image_to_string(img)[0:6]
    if "limitchars" in options:
        solution = solution.lower()
        reps = {
            "o": "0",
            "¢": "c",
            "s": "5",
            "t": "f",
        }
        for rep in reps.keys():
            solution = solution.replace(rep, reps[rep])
    # img.show()
    return (solution, input)