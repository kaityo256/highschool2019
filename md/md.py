from PIL import Image, ImageDraw, ImageFont


def get_atoms(text):
    myfont = ImageFont.truetype("fonts/ipaexg.ttf", 24)
    img = Image.new('1', (100, 100), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=myfont)

    w, h = img.size
    atoms = []
    for x in range(w):
        for y in range(h):
            v = img.getpixel((x, y))
            if v is 0:
                atoms.append([float(x), float(y)])
    return atoms


def get_bonds(atoms):
    n = len(atoms)
    bonds = []
    for i in range(n-1):
        (xi, yi) = atoms[i]
        for j in range(i + 1, n):
            (xj, yj) = atoms[j]
            r2 = (xi - xj) ** 2 + (yi - yj) ** 2
            if r2 < 3.1:
                bonds.append((i, j, r2))
    return bonds


def main():
    atoms = get_atoms("日本語")
    bonds = get_bonds(atoms)
    for i, j, _ in bonds:
        (xi, yi) = atoms[i]
        (xj, yj) = atoms[j]
        print(xi, yi, (xj-xi), (yj-yi))
    # for x, y in atoms:
    #    print('{} {}'.format(x, y))


main()
