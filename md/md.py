from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np


def get_atoms(text, fontsize):
    myfont = ImageFont.truetype("fonts/ipaexg.ttf", fontsize)
    img = Image.new('1', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=myfont)

    w, h = img.size
    rx = []
    ry = []
    for x in range(w):
        for y in range(h):
            v = img.getpixel((x, y))
            if v is 0:
                rx.append(float(x))
                ry.append(h - float(y))
    nx = np.array(rx)
    ny = np.array(ry)
    nx -= np.min(nx)
    ny -= np.min(ny)
    return nx, ny


def get_bonds(rx, ry):
    n = len(rx)
    bonds = []
    for i in range(n-1):
        for j in range(i + 1, n):
            r2 = (rx[i] - rx[j]) ** 2 + (ry[i] - ry[j]) ** 2
            if r2 < 3.1:
                bonds.append((i, j, r2))
    return bonds


def calculate(vx, vy, rx, ry, bonds):
    dt = 0.01
    G = 0.2
    K = 1000.0

    rx += vx * dt
    ry += vy * dt
    vy -= G * dt

    for i, j, l in bonds:
        dx = rx[j] - rx[i]
        dy = ry[j] - ry[i]
        r2 = dx ** 2 + dy ** 2
        f = K * (r2 - l)
        vx[i] += f*dx*dt
        vy[i] += f*dy*dt
        vx[j] -= f*dx*dt
        vy[j] -= f*dy*dt

    for i, y in enumerate(ry):
        if y < 0.0:
            vy[i] -= 10.0 * y * dt


def save_img(rx, ry, w, h, i):
    img = Image.new('RGB', (w*2, h*2), 'white')
    draw = ImageDraw.Draw(img)
    rx2 = rx * 2
    ry2 = ry * 2
    for x, y in zip(rx2, ry2):
        draw.ellipse((x, y, x + 2, y + 2), fill=(255, 0, 0))
    img = ImageOps.flip(img)
    filename = "img%03d.png" % i
    img.save(filename)
    print(filename)


def simulate(rx, ry, bonds):
    vx = np.zeros_like(rx)
    vy = np.zeros_like(rx)
    w = np.max(rx).astype(np.int)
    h = np.max(ry).astype(np.int)
    imgs = []
    for i in range(2000):
        if i % 100 is 0:
            save_img(rx, ry, w, h, i//100)
        calculate(vx, vy, rx, ry, bonds)
    return imgs


def save_positions(rx, ry):
    with open("positions.dat", "w") as f:
        for x, y in zip(rx, ry):
            f.write("%f %f\n" % (x, y))


def save_bonds(rx, ry, bonds):
    with open("bonds.dat", "w") as f:
        for i, j, _ in bonds:
            dx = rx[j]-rx[i]
            dy = ry[j]-ry[i]
            f.write("%f %f %f %f\n" % (rx[i], ry[i], dx, dy))


def main():
    rx, ry = get_atoms("スパコン", 32)
    bonds = get_bonds(rx, ry)
    save_positions(rx, ry)
    save_bonds(rx, ry, bonds)
    #simulate(rx, ry, bonds)


main()
