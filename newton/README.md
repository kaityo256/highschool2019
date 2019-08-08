# テーマ5：ニュートン法とフラクタル

## 目的

複素数におけるニュートン法を実装し、フラクタル図形を見てみる。

## プログラム

$x^3 = 1$の解をニュートン法で探すコードを書いてみよう。

### 最初のセル

最初のセルでライブラリのインポートをしよう。

```py
from PIL import Image, ImageDraw
import IPython
```

### 2つ目のセル

ニュートン法を10回繰り返した結果を返す関数を実装する。

```py
def newton(x):
  for _ in range(10):
    x = x - (x**3-1)/(3*x**2)
  return x
```

`return x`のインデントに注意。`x = x - (x**3-1)/(3*x**2)`ではなく、`for`と同じ高さにしなければならない。

### 3つ目のセル

こちらは、複素数空間の様々な点を初期点として、最終的に三つの解のうちどこに収束したかを色分けするプログラムである。実数解を赤、複素数解のうち、虚部が正のものを緑、負のものを青としている。

```py
def plot(draw, s):
    hs = s/2
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    for x in range(s):
        for y in range(s):
            z = complex(x-hs, y-hs)/s*4 + 0.01
            z = newton(z)
            if z.real > 0.0:
                c = red
            else:
                if z.imag > 0:
                    c = green
                else:
                    c = blue
            draw.rectangle([x, y, x+1, y+1], fill=c)
```

#### 4つ目のセル

実際にプログラムを実行し、「収束地図」を作ってみよう。きれいに三分割されるだろうか？

```py
size = 512
im = Image.new("RGB", (size, size))
draw = ImageDraw.Draw(im)
plot(draw, size)
im.save("test.png")
IPython.display.Image("test.png")
```

## ニュートン法

ある方程式を解きたいが、その解が厳密にはわからないとする。その場合でも数値計算で必要な精度で解を求めることができる。そのような場合によく用いられるのがニュートン法である。

いま、

$$
f(x) = 0
$$

という方程式を解きたいとする。もし、真の解を$x$として、それに近い値$\tilde{x} = x+\epsilon$があったとする。$f(x)$を$\tilde{x}$の周りでテイラー展開すると、

$$
f(\tilde{x} - \varepsilon) = f(\tilde{x}) - \varepsilon f'(\tilde{x}) + O(\varepsilon^2)
$$

$\varepsilon$の二次の項を無視した状態で、$f(\tilde{x} - \varepsilon)$が0となるように$\varepsilon$の値を選ぶと、

$$
\varepsilon = \frac{f(\tilde{x})}{f'(\tilde{x})}
$$

$\tilde{x} = x + \varepsilon$であったから、$\varepsilon$を引けば、より真の値に近づくはずである。以上から、

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

という数値列を得る。この数列が収束するということは$x_{n+1} = x_n$なので、$f(x_n)=0$が満たされなければならず、それはすなわち$x_n$が解に収束したことを示す。これを確認してみよう。

いま、$x^3 = 1$の解を知りたいとする。この時、$f(x) = 0$の形に書きたいので、$f(x) = x^3 - 1$である。$f'(x) = 3 x^2$であるから、対応するニュートン法のアルゴリズムは、

$$
x_{n+1} = x_n - \frac{x^3 -1}{3 x^2}
$$

である。
