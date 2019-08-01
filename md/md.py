from PIL import Image, ImageDraw, ImageFont
import numpy as np


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
    return np.array(qx), np.array(qy)


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


def calculate(vx, vy, qx, qy):
    n = len(vx)
    dt = 0.01
    G = 1.0
    qx += vx * dt
    qy += vy * dt
    vy -= G * dt
    for i in range(n):
        if qy[i] < 0.0:
            vy[i] -= 10.0*qy[i] * dt


def simulate(qx, qy, bonds):
    vx = np.zeros_like(qx)
    vy = np.zeros_like(qx)
    ymin = np.min(qy)
    qy -= ymin
    for _ in range(500):
        calculate(vx, vy, qx, qy)


def show_bonds(qx, qy, bonds):
    for i, j, _ in bonds:
        (xi, yi) = qx[i], qy[i]
        (xj, yj) = qx[j], qy[j]
        print(xi, yi, (xj-xi), (yj-yi))


def main():
    qx, qy = get_atoms("スパコン")
    bonds = get_bonds(qx, qy)
    simulate(qx, qy, bonds)
    show_bonds(qx, qy, bonds)
   # for x, y in atoms:
    #    print('{} {}'.format(x, y))


main()
