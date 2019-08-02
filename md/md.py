from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from numba import jit


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
                qy.append(h - float(y))
    nx = np.array(qx)
    ny = np.array(qy)
    nx -= np.min(ny)
    ny -= np.min(ny)
    return nx, ny


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


@jit
def calculate(vx, vy, qx, qy, bonds):
    n = len(vx)
    dt = 0.01
    G = 0.1
    K = 1000.0

    qx += vx * dt
    qy += vy * dt

    for i, j, l in bonds:
        dx = qx[j] - qx[i]
        dy = qy[j] - qy[i]
        r2 = dx ** 2 + dy ** 2
        f = K * (r2 - l)
        vx[i] += f*dx*dt
        vy[i] += f*dy*dt
        vx[j] -= f*dx*dt
        vy[j] -= f*dy*dt

    vy -= G * dt

    for i in range(n):
        if qy[i] < 0.0:
            vy[i] -= 10.0 * qy[i] * dt


@jit
def simulate(qx, qy, bonds):
    vx = np.zeros_like(qx)
    vy = np.zeros_like(qx)
    for i in range(10000):
        if i % 100 is 0:
            save_img(qx, qy, i//100)
        calculate(vx, vy, qx, qy, bonds)


def show_bonds(qx, qy, bonds):
    for i, j, _ in bonds:
        (xi, yi) = qx[i], qy[i]
        (xj, yj) = qx[j], qy[j]
        print(xi, yi, (xj-xi), (yj-yi))


@jit
def save_img(qx, qy, i):
    img = Image.new('RGB', (400, 100), 'white')
    draw = ImageDraw.Draw(img)
    qx2 = qx * 2
    qy2 = qy * 2
    for x, y in zip(qx2, qy2):
        draw.ellipse((x, y, x + 2, y + 2), fill=(255, 0, 0))
    img = ImageOps.flip(img)
    filename = "img%03d.png" % i
    img.save(filename)
    print(filename)


def get_img(qx, qy, w, h):


def main():
    qx, qy = get_atoms("スパコン")
    w = np.max(qx)
    h = np.max(qy)
    #bonds = get_bonds(qx, qy)
    #simulate(qx, qy, bonds)


main()
