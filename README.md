## personal test project of keras deep-learning

python + keras + deep-learning 勉強用のプロジェクトです。

## セットアップ手順

pyenvを(ユーザー上に)インストールする
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
source ~/.bash_profile 
```

pythonを(pyenv上に)インストールする
```bash
pyenv install 3.6.6
```

pythonのバージョン指定を(プロジェクトディレクトリ上で)行う
```bash
pyenv local 3.6.6
python --version
pip --version
```

pipが古くて後続のコマンドが失敗するので、upgradeする
```bash
pip install --upgrade pip
pip --version
```

pipenvを(pyenv上のpython 3.6.6上に)インストールする
```bash
pip install pipenv
```

プロジェクト環境を(プロジェクトディレクトリ上に作る)
```bash
pipenv install keras tensorflow
```
↑pipenv installは
Locking [packages] dependencies...のあと、
何も表示されずに止まるが、
ダウンロード待ちなので、
待てば終わる。

## ハマったところ

全体的にpythonの環境構築は、
rubyやnodeを比較してハマりやすかった。

### brew経由でインストールしたらハマった

brewでインストールしたらなんかおかしくなったので、
brewでインストールしたpython関連のもの(pyenv, virtualenv)を全てけして、
github checkout方式でインストールした。

※ 原因はbrewではなかったかもしれないが、原因の候補が増えたので、ハマり脱出の効率が落ちた

### pip installではなく、pipenv install

pip installではなく、
pipenv installを使うらしい
間違えてpip installを使うと、
グローバルにインストールされる。

### Your Pipfile requires python_version 3.6.6, but you are using 3.7.0

一度も3.7.0とか指定していないのに、
いきなり3.7.0とか出てきた。
pipenv run python --version
でも3.7.0がかえってくる。

確かに、
pipenv run python --versionを実行すると3.7.0だが、
Pipfile内は3.6.6指定になっている。

3.7.0の由来
(cd ~/ && python3 --version)
を実行すると3.7.0がかえっててくる
システムのpythonのバージョンということか。
以下の情報によると、pipenvは.python-versionを見ていないらしい。
https://github.com/pypa/pipenv/issues/729#issuecomment-332539758

3.6.6の由来
多分、pipenv installをやったタイミングで、
そのときのpyenvのpythonバージョンが、
Pipfileに書き込まれるんだと思う。

解決策
pipenvにpyenvのpythonバージョンを認識させないとやりづらい。

まず、pipenvが使うpythonがどこにあるかを調べる。
pipenv run which python
で以下が返ってくる
~/.local/share/virtualenvs/dl_test-hzhqb1fI/bin/python

これを作るタイミングで何かすれば、
切り替えられるかもしれない。
多分、最初にpipenvを使うときだから、pipenv install。

試しに以下をやってみた。
出力から推測するとvirtualenvを作り直して、
パッケージを再インストールしているみたい。
pipenv --python 3.6.6 install

pipenv run python --version
を実行したら3.6.6が返ってきた。

推測
pipenvが3.6.6というバージョン番号だけから、
python 3.6.6を発見できるということは、
pyenvを知ってはいる。が、.python-versionを見ていない。
バージョン指定付きのpipenv installを実行したタイミングで、
pipenvに3.6.6で問い合わせて、pythonを特定し、
そのpythonでvirtualenvを作るんだと思う。

疑問
後続のpipenv installで毎回pythonバージョン指定する必要はあるのか？
以下を実行してみたが、必要なかった。
pipenv install
pipenv run python --version

結論、原因をまとめると
pipenvのpythonバージョン認識方法に一貫性がない
(Pipfileにかかれるものと、virtualenv構築に使うものの、認識方法が違う)

### 3.7.0だとtensorflowが動かない

あまり詳しく調べていないので、誤認かもしれないが、
tensorflow内部のコードで、syntax errorになって動作しなかった。

### pypiとpypyは違う

Pipfileの中のnameがpypiになっていて、
pypyと勘違いしたが、
違うものらしい。

https://pypi.org/
https://pypy.org/

## Rubyとの対応
pyenv -> rbenv
pip install [x] -> gem install [x]
pipenv install [x] -> add [x] to Gemfile and bundle install
pipenv run [x] -> bundle exec [x]
pipenv shell -> あるのか知らない

## パフォーマンス

mnist_mlp.pyを実行すると以下が表示される。
Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA

AVXが使えていれば問題ないと思うので、
AVXが使われているか調べる。

こちらの情報によると使われているらしい。
https://qiita.com/KEINOS/items/4c66eeda4347f8c13abb

CPU使用率を見たところ、
並列化はされているらしい。

## 実行

https://github.com/keras-team/keras/blob/master/examples/mnist_mlp.py
のサンプル実行

```bash
wget https://raw.githubusercontent.com/keras-team/keras/master/examples/mnist_mlp.py
pipenv run python mnist_mlp.py
```

その他のサンプル実行
```bash
pipenv run python test1.py
```

## LICENSE

The license of all contents in this repository is CC0.
