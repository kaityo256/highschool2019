# テーマ4：分子動力学法

## 目的

プログラムで構造を作り、分子動力学法により時間発展させる。

## プログラム

新たなノートブックを開き、「md」という名前をつけて保存しよう。

### 最初のセル

最初のセルではライブラリをインポートする。

```py
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
```

### 二番目のセル

次に、文字列を受け取って、それを原子の座標に変換するコードを書く。

```py
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
```

### 三番目のセル

原子の座標を受け取り、近い原子同士をバネでつなぐ。

```py
def get_bonds(rx, ry):
    n = len(rx)
    bonds = []
    for i in range(n-1):
        for j in range(i + 1, n):
            r2 = (rx[i] - rx[j]) ** 2 + (ry[i] - ry[j]) ** 2
            if r2 < 3.1:
                bonds.append((i, j, r2))
    return bonds
```

### 四番目のセル

1ステップだけ計算する。原子間に働く力を計算し、速度と位置を更新する。

```py
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
```

### 5番目のセル

後の「写真」のために、原子の位置から画像を作る関数を作っておく。

```py
def get_img(qx, qy, w, h):
    img = np.zeros((h,w))
    for x,y in zip(qx,qy):
        x = int(x)
        y = int(y)
        if x in range(w) and y in range(h):
            img[h-y-1][x] = 1.0
    return img
```

### 6番目のセル

シミュレーションを行う。速度を初期化してから`calculate`を何度も呼び出すことで時間発展をさせる。あとでアニメーションを作るため、100ステップに一度「写真」を撮っておく。

```py
def simulate(rx, ry, bonds):
    vx = np.zeros_like(rx)
    vy = np.zeros_like(rx)
    w = np.max(rx).astype(np.int)
    h = np.max(ry).astype(np.int)
    imgs = []
    for i in range(2000):
        if i % 100 is 0:
            img = get_img(rx, ry, w, h)
            imgs.append(img.copy())
            plt.imshow(img)
            plt.show()
        calculate(vx, vy, rx, ry, bonds)
    return imgs
```

### 7番目

ではいよいよシミュレーションしてみよう。例えば32ピクセルのサイズで「スパコン」という文字列の形をした構造を作って、下に落としてみる。

```py
rx, ry = get_atoms("スパコン",32)
bonds = get_bonds(rx, ry)
imgs = simulate(rx, ry, bonds)
```

実行すると、次々に「写真」が表示されるであろう。

### 8番目

アニメーションの準備をする。デフォルトの色では味気ないので、カラーマップを`plasma`に変えてみよう。

```py
fig = plt.figure()
im = plt.imshow(imgs[0],cmap="plasma")
```

実行すると、青字に黄色で文字が表示されたはずである。

### 9番目のセル

撮った写真をまとめてアニメーションを作ろう。

```py
def update(i):
    im.set_array(imgs[i])

ani = animation.FuncAnimation(fig, update,frames=len(imgs))
rc('animation', html='jshtml')
ani
```

実行するとコントロールパネルが出るはずなので、再生ボタンを押すことでアニメーションが表示される。

ここまで成功したら、7番目のセルの文字列をいろいろ変えて実行してみよう。例えば自分の名前などはどうなるだろう？ひらがなやカタカナの方が面白いので試してみよう。

## 解説

