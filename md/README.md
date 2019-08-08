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
    myfont = ImageFont.truetype("ipaexg.ttf", fontsize)
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

なお、事前にIPAフォント`ipaexg.ttf`をカレントディレクトリに置いておく必要がある。

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
def get_img(rx, ry, w, h):
    img = np.zeros((h,w))
    for x,y in zip(rx,ry):
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

分子動力学法(Molecular Dynamics method, MD)は、原子や分子といった「つぶつぶ」にかかる力を計算し、ニュートンの運動方程式に従って時間発展させる手法である。タンパク質の折りたたみのシミュレーションといったミクロなものから、生物の細胞膜の運動、血流中の赤血球の動きの解析といったミリオーダーの世界、さらには銀河系の衝突などの巨大なスケールまで、様々な研究に用いられている。世の中はすべて原子でできているのだから、十分な数の原子を用意することができればなんでも再現できるはずである。しかし、化学反応を再現するには量子力学が必要だったり、計算機の能力の限界によりあまり多数の原子を扱えないため、「なんでも」は再現できるわけではない。とにかくたくさん「つぶつぶ」があればあるほど再現できる世界が広がるのは想像できるであろう。どんな計算をするかにもよるが、普通のパソコンで計算できるのはせいぜい100万原子くらいまでであろう。100万というと多いように思えるが、三次元なら100x100x100、つまり一辺に100個しか原子がない。原子間距離は0.1ナノメートル程度であるから、たった10ナノの世界しか表現できない。もっと大きな計算がしたいが、どうすればよいだろう？

普通のパソコンでは100万個しか扱えないが、それは「一台の」パソコンをつかった場合だ。2台あったら200万個、10台あったら1000万個扱えるんじゃないだろうか？こうして、「パソコンをたくさん並べてつないで、大きなコンピュータとして使おう」という発想が生まれる。このようなコンピュータを**スーパーコンピュータ**、略してスパコンと呼ぶ。スパコンを使って、できるだけ大きな計算をして、新しい発見を目指す、それが渡辺の研究である。例えば今年退役する「京」コンピュータは、8万個のパソコン(スパコンではパソコンにあたるものをノードと呼ぶ)をつないで作られた巨大なスパコンだ。渡辺はこの「京」を使って3000億原子までの計算を行った。たくさんのパソコンをつないなものを実行するためには「並列計算」と呼ばれる技術が必要になる。複数のパソコンが通信で情報をやりとりして、一つの大きな計算実行するのが並列計算である。並列計算をするためには、通信部分も自分でプログラムしなければならない。スパコンとは何か、どうやって使うかについて「一週間でなれる！スパコンプログラマ」という記事を書いたので、もしスパコンに興味を持ったら参照してみて欲しい。

「一週間でなれる！スパコンプログラマ」
[https://kaityo256.github.io/sevendayshpc/](https://kaityo256.github.io/sevendayshpc/)
