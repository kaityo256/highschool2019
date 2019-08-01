from PIL import Image, ImageDraw, ImageFont


def get_atoms(text):
    myfont = ImageFont.truetype("fonts/ipaexg.ttf", 24)
    img = Image.new('1', (100, 100), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=myfont)

    w, h = img.size

    for x in range(w):
        for y in range(h):
            v = img.getpixel((x, y))
            if v is 0:
                print('{} {}'.format(x, y))


get_atoms("日本語")
