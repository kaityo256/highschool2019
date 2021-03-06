# 夏休み研究体験2019

## 概要

これは2019年8月に慶應義塾大学理工学部で行われた、「高校生のための夏休み研究体験」の資料です。物理情報工学科渡辺研究室では「コンピュータシミュレーションをしてみよう」と題して、Pythonを使った数値シミュレーションを行いました。

* GitHubリポジトリ: [https://github.com/kaityo256/highschool2019](https://github.com/kaityo256/highschool2019)
* ウェブ版: [https://kaityo256.github.io/highschool2019/](https://kaityo256.github.io/highschool2019/)

## 説明スライド

最初に、コンピュータシミュレーションの概要について説明をしました。そのスライドは以下にアップロードしてあります。

[コンピュータシミュレーションをしてみよう](https://speakerdeck.com/kaityo256/simulation-for-high-school-students)

## 実習

説明の後、テキストを配って、プログラムを入力、実行してもらいました。実WindowsマシンにAnacondaを入れ、Jupyter Notebook上で実行する形式です。

テーマは以下の通りです。

* テーマ1：[拡散方程式](diffusion/README.md)
  * 微分方程式を差分化して解いてみます。簡単な方程式の一つである拡散方程式(熱伝導方程式)をシミュレーションし、熱の伝わり方を観察します。
* テーマ2：[反応拡散方程式](gray-scott/README.md)
  * 拡散に反応過程を追加してみます。周期的に振動する化学反応系と拡散が組み合わさることで、チューリング・パターンと呼ばれる不思議な模様が生まれます。
* テーマ3：[ロジスティック・マップ](logistic/README.md)
  * ロジスティック・マップは生物の個体数の時間発展を表現する式です。非常に簡単な式であるにもかかわらず、その振る舞いは非常に複雑です。このように、簡単な式から予測困難な挙動が生まれる「カオス」を体験します。
* テーマ4：[分子動力学法](md/README.md)
  * 物体に力を加えると速度が変化します。それを記述するのがニュートンの運動方程式で、それを数値的に解く手法が分子動力学法です。バネとビーズで構造物を作り、そこに重力をかけるとどうなるか調べてみましょう。
* テーマ5: [ニュートン法とフラクタル](newton/README.md)
  * 方程式の解を求めるのに有効なニュートン法ですが、解が複素数の場合は不思議なことが起こります。ニュートン法が生み出すフラクタル図形を見てみましょう。

## 体験を終えて

本当はテーマ4までしか用意してませんでしたが、想像以上に進度が早かったので急遽テーマ5を用意しました。内容はわからなくても、どれくらい組めばどのくらいのことが可能になるのかを実感してもらおうと、事前に用意したプログラムを「写経」してもらいました。入力ミスによりエラーが出たとき、そこから原因を探るのに苦労していたようです。初学者は写経から入るのがよい、と思っていましたが、やはり「組んでいるプログラムがどういうものかわからなかった」という感想が多かったため、もう少しプログラムの内容について説明した方がよかったかもしれません。

## ライセンス

Copyright (C) 2019 Hiroshi Watanabe

この文章と絵(pptxファイルを含む)はクリエイティブ・コモンズ 4.0 表示 (CC-BY 4.0)で提供します。

This article and pictures are licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

本リポジトリに含まれるプログラムは、[MITライセンス](https://opensource.org/licenses/MIT)で提供します。

The source codes in this repository are licensed under [the MIT License](https://opensource.org/licenses/MIT).
