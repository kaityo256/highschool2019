from PIL import Image, ImageDraw, ImageFont


def get_atoms(text):
    myfont = ImageFont.truetype("fonts/ipaexg.ttf", 48)
    img = Image.new('1', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=myfont)

    w, h = img.size
    qx = []
    qy = []
    for x in range(w):
        for y in range(h):
            v = img.getpixel((x, y))
            if v is 0:
                qx.append(float(x))
                qy.append(h-float(y))
    return qx, qy


def get_bonds(qx, qy):
    n = len(qx)
    bonds = []
    for i in range(n-1):
        (xi, yi) = qx[i], qy[i]
        for j in range(i + 1, n):
            (xj, yj) = qx[j], qy[j]
            r2 = (xi - xj) ** 2 + (yi - yj) ** 2
            if r2 < 3.1:
                bonds.append((i, j, r2))
    return bonds


def show_bonds(qx, qy, bonds):
    for i, j, _ in bonds:
        (xi, yi) = qx[i], qy[i]
        (xj, yj) = qx[j], qy[j]
        print(xi, yi, (xj-xi), (yj-yi))


def main():
    qx, qy = get_atoms("スパコン")
    bonds = get_bonds(qx, qy)
    show_bonds(qx, qy, bonds)
   # for x, y in atoms:
    #    print('{} {}'.format(x, y))


main()
