from PIL import Image, ImageFilter
from io import BytesIO
from base64 import b64encode, b64decode
import pytesseract
from external.amadeus.amadeus import amadeus

a = amadeus("", (12,19), 32, load_from_file=True, epochs=15)

def kill(input, options = []):
    challenge = input.challenge.split("base64,")[1]
    challenge = b64decode(challenge.encode("ascii"))
    data = BytesIO(challenge)
    img = Image.open(data).convert("L")

    solution = ""

    if "removelines" in options:
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.convert("L")
        x = None
        y = None
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixel = img.getpixel((i, j))
                if pixel == 0:
                    if i == 0:
                        y = j
                    elif j == 0:
                        x = i
                if pixel < 90:
                    img.putpixel((i,j), 0)
                else:
                    img.putpixel((i,j), 255)
        if "deeper" in options:
            tw, th = (12,19)
            keysize = 6
            single = tw/keysize
            for char_idx in range(keysize):
                loc = x+(char_idx*(tw))
                char_img = img.crop((loc, y, loc+tw, y+th))
                # char_img.show()
                solution += a.test_accuracy_on_image_pil(char_img)
            

    # img.show()
    if not "deeper" in options:
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