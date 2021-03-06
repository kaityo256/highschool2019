# テーマ1：拡散方程式

## 目的

拡散方程式を数値的に解き、熱がどのように伝わるかを調べる。

## プログラム

### 最初のセル

まず、これから使うライブラリをインポートする。以下を入力してから「Run」ボタンを押すか、「Shift+Enter」を押してみよ。

```py
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from matplotlib import animation, rc
```

正しく入力されていれば、左の「In [ ]:」という表示が、「In [1]:」という表示に変わるはずである。エラーが出たらどこか入力ミスをしているはずなのでチェックすること。

### 2番目のセル

次のセルでは、ラプラシアンを計算する関数を入力しよう。ラプラシアンとは高次元の二階微分演算子である。といっても、差分化していれば上下左右と現在地での値の差を返すだけである。

```py
@jit
def laplacian(ix, iy, s):
    ts = 0.0
    ts += s[ix-1, iy]
    ts += s[ix+1, iy]
    ts += s[ix, iy-1]
    ts += s[ix, iy+1]
    ts -= 4.0*s[ix, iy]
    return ts
```

ここで、最初に`@jit`と入力するのと、最初の関数定義`def laplacian(ix, iy, s):`の最後のコロンを忘れないこと、さらに、関数の中身(ブロック)の各行では、空白を4つ入力する。これを「インデント」と呼ぶ。Pythonはインデントによりブロックを表現する言語である。

こちらも実行し、エラーが出たら入力ミスを修正し、また実行し、という作業を繰り返すこと。`@jit`はプログラムを高速化するための「おまじない」である。

### 3番目のセル

3番目のセルは、一回呼び出すたびに、温度の値が1ステップ進む関数`calc`を実装する。一つ前のステップの温度分布を`u`、そこから計算される次のステップの温度分布を`u2`としている。やはり、コロンとインデントを忘れないこと。特に、インデントされたブロックの中に、さらにインデントがあったり(インデントのネスト)、その後にインデントの深さが減るところがあることに注意。

```py
@jit
def calc(u, u2):
    (L, _) = u.shape
    dt = 0.2
    Q = 1.0
    for ix in range(1, L-1):
        for iy in range(1, L-1):
            u2[ix, iy] = u[ix,iy] + laplacian(ix, iy, u)*dt
    h = L//2
    u2[h-6:h+6, h-6:h+6] += Q*dt
```

### 4番目のセル

4番目のセルは、1ステップ時間をすすめる関数`calc`を何度も呼んで、時間発展を記述する関数`simulation`を実装する。

```py
@jit
def simulation():
    L = 32
    u = np.zeros((L, L))
    u2 = np.zeros((L, L))
    r = []
    for i in range(1000):
        if i % 2 == 0:
            calc(u, u2)
        else:
            calc(u2, u)
        if i%10 == 0:
            r.append(u.copy())
    return r
```

ここでは1000ステップ計算しているが、10ステップごとに「写真」を撮っている。`r`は写真の配列であり、100枚写真が撮られている。

### 5番目のセル

実際に計算できるかどうか確認してみよう。計算結果は100枚の写真(`imgs`)に収められているが、その最後、すなわち100枚目の写真を確認する。Pythonの配列のインデックスは0から数えるため、100枚目は`imgs[99]`に入っている。

```py
imgs = simulation()
fig = plt.figure()
im = plt.imshow(imgs[-1], cmap="inferno",vmin = 0, vmax = 30)
```

上記を実行して、なにか模様が出てくれば計算成功である。

### 6番目のセル

せっかく100枚の写真を撮影したので、それをパラパラ漫画のようにアニメーションさせて見よう。以下のプログラムを入力して実行せよ。

```py
def update(i):
  im.set_array(imgs[i])
  return im,

ani = animation.FuncAnimation(fig, update, interval=50)
rc('animation', html='jshtml')
ani
```

しばらくするとコントロールパネルが表示されるので「▶」をクリックせよ。ここまで正しく入力できていれば、アニメーションが表示されるはずである。

## 解説

数値計算とは、解析的に解くことが難しい方程式をなんらかの方法で近似して数値的に近似解を求める手法である。特に、この世界は微分方程式で記述されている(らしい)ため、この世界の振る舞いを調べるには微分方程式を解かなければならない。しかし、微分方程式は一般には解析的に解くことができないため、計算機で数値的に近似解を求めることが行われている。これを数値シミュレーションと呼ぶ。日常で一番お世話になっているのは天気予報であろう。日本各地に設置されたセンサーから情報を収集し、それを入力として微分方程式(ナビエ・ストークス方程式など、複数の方程式を連立した式)を気象庁のスーパーコンピュータでシミュレーションし、その結果を気象予報士が解析した結果を天気予報として発表しているのである。

今回、一番最初のテーマに選んだのは「拡散方程式」と呼ばれる微分方程式で、その名の通り「なにかが広がっていく」様子を記述する方程式である。これを「熱の伝わり方を表す式である」と解釈すると、「熱伝導方程式」と呼ばれる。鉄の棒のどこかを火で炙ると、まずはそこだけ熱くなるが、やがて熱い部分が広がっていき、そのうち持ち手も熱くなるだろう。そして、火をとめてしばらく放って置くと、棒は冷めて全体が同じ温度になるだろう。つまり、熱している時も、冷えているときも、鉄の棒は「全体で同じ温度になろう」としている。この振る舞いを記述するのが拡散方程式である。

さて、拡散方程式の性質を決めているのは、ラプラシアンと呼ばれる演算子であり、その中身は二階の微分演算子である。これが、「自分の値が周りの平均よりも大きいと負に、小さいと正」になることは既に説明した。従って、ラプラシアンは「出る杭を打つ」「凹んでる杭はひっぱり上げる」ような働きを持っている。この式で記述された世界は、「まわりと違う」ことを許さず、どんどんまわりを「平均化」しようとする。時間がたつと、他の場所と同じ値に、つまり「のっぺり」した世界に落ち着いていく。ラプラシアンは世の中を安定に導く。

このように、式や演算子にはそれぞれ意味がある。意味を組み合わせれば、自分で新しい意味を持つ微分方程式を作ることができる。このようにして世界を記述、理解していこう、という学問が物理である。しかし、そうしてできた微分方程式は手で解析的に解けないことがほとんどなんので、数値的に解いて調べましょう、という学問が計算物理である。
